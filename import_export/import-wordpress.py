import base64
import json
import os.path
import requests

import sys
sys.path.append('../common/src')
import utils

from flask import Flask, has_request_context, request
from flask_restful import Api, Resource, reqparse
from git import Repo

ROOT_PATH = "/var/tms-data"

# TODO: Unit testing, end-to-end testing

def write_post(post):
    title = "wp" + str(post['id'])
    filename = f"{ROOT_PATH}/source_files/en/{title}.json"
    with open(filename, 'w') as outfile:
        d = {}
        d['id'] = post['id']
        d['wptitle'] = post['title']
        d['content'] = post['content']
        d['link'] = post['link']
        d['modified_gmt'] = post['modified_gmt']
        json.dump(d, outfile)

def get_posts():
    import_url = os.environ.get('WP_IMPORT_URL')
    url = f"{import_url}/wp-json/wp/v2/posts"
    user = os.environ.get('WP_IMPORT_USER')
    password = os.environ.get('WP_IMPORT_PASSWORD')
    credentials = user + ':' + password
    token = base64.b64encode(credentials.encode())

    header = {'Authorization': 'Basic ' + token.decode('utf-8'), 'User-Agent': "", }
    response = requests.get(url, headers=header )
    return response.json()

def do_work():
    for post in get_posts():
        write_post(post)
    utils.git_push(utils.PROJECT_ROOT_GIT_PATH, commit_message="Update shared repository: wordpress", enable_push=True)

app = Flask(__name__)
api = Api(app)

class WordpressUpdateListener(Resource):
    def get(self):
        do_work()
        return "Get"

    def post(self):
        do_work()
        return "Post"

api.add_resource(WordpressUpdateListener, "/wp-updates")

if __name__ == "__main__":
    # Warning: When debug mode is unsafe. Attackers can use it to run arbitrary python code.
    app.run(debug=False, host='0.0.0.0')