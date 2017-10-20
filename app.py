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
        
        speech = "this is what is "
        
        print(speech + " \n okay this is it")
        return {
            "speech": speech,
            "displayText": speech,
            "source": "https://github.com/ZatinMe/try112.git"
        }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
