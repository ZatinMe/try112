from __future__ import print_function
from future.standard_library import install_aliases

install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import google.oauth2.credentials
import google_auth_oauthlib.flow 


# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res + "returned file")
    r = make_response(res)
    print("res test 1")
    print (r)
    r.headers['Content-Type'] = 'application/json'
    print("res test 2")
    print (r)
    return r


def processRequest(req):
    if req.get("result").get("action") == "action_1":
        
        SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
        CLIENT_SECRET ='client_secret.json'
        
        store = file.Storage('storage.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRET, scope=[SCOPES])
            authorization_url, state = flow.authorization_url(access_type='offline',include_granted_scopes='true')
   
            creds = tools.run_flow(flow,store)
        GMAIL = build('gmail', 'v2', http=creds.authorize(Http()))

        threads = GMAIL.users().threads().list(userId='me').execute().get('threads',[])
        i = 0
        sub = ""
        for thread in threads:
            if i>5:
                break
            i+=1

            tdata = GMAIL.users().threads().get(userId='me', id=thread['id']).execute()
            nmsgs = len(tdata['messages'])

            if nmsgs > 0:
                msg = tdata['messages'][0]['snippet']
                subject = msg
                if subject:
                    print ('%s (%d msgs)' % (subject, nmsgs))
                    sub = str(i) + sub + subject + "/n"   
        speech = sub
        print("response:")
        print(speech)
        
        return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
