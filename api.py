from flask import Flask
from flask import render_template


from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

import sys
import json
import os
import time
import readline


def call(api, endpoint):
    response = api.get('https://api.intra.42.fr/v2/' + endpoint)
    raw_json = response.content
    parsed_json = json.loads(raw_json)
    #dumped_json = json.dumps(parsed_json, indent=4, sort_keys=True)
    return parsed_json

def init_api():
    client_id = os.environ['API42_ID']
    client_secret = os.environ['API42_SECRET']
    client = BackendApplicationClient(client_id=client_id)
    api = OAuth2Session(client=client)
    token = api.fetch_token(token_url='https://api.intra.42.fr/oauth/token', client_id=client_id, client_secret=client_secret)

    return(api)

app = Flask(__name__)
@app.route('/')
def index():
    parsed_json = call(api, sys.argv[1])

    pool_month = parsed_json['pool_month']
    pool_year = parsed_json['pool_year']
    pool_date = pool_month + ", " + pool_year

    return render_template("index.html", email = parsed_json['email'], name = parsed_json['first_name'], last_name=parsed_json['last_name'], image_src=parsed_json['image_url'],
    id = parsed_json['id'], location = parsed_json['location'], pool = pool_date, profile = parsed_json['url'])

@app.route('/projects.html')
def projects():
    parsed_json = call(api, sys.argv[1])
    projects = parsed_json['projects_users']

    return render_template('projects.html', image_src=parsed_json['image_url'], project_data = projects)

if __name__ == "__main__":
    try:
        api = init_api()
        app.run()
    except KeyboardInterrupt:
        sys.exit()
