

import DbConfig
import security
import validator


import os
import json
import datetime
from flask import (Flask, Response, request, abort)





app = Flask(__name__)


@app.route('/')
def MainPage():
    
    return 'Welcome User!'



@app.route('/healthz')
def healthz():
    
    return Response(str("Server is Up and Running!"), status=200, mimetype='application/json')


@app.route('/v1/user', methods=['POST'])
def create_user():
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    password = request.json.get('password')
    user_name = request.json.get('user_name')

    create_user_schema = validator.CreateUserInputSchema()

    errors = create_user_schema.validate(request.json)

    if errors:
        return Response(str(errors), status=422, mimetype='application/json')

    # access_token = authenticator.create_access_token(user_name, password)

    resp_json = DbConfig.create_user(
        first_name, last_name, password, user_name)
    print(resp_json)
    return Response(json.dumps(resp_json), status=201, mimetype='application/json')




if __name__ == '__main__':
    port = int(5000)
    app.run(port=port, host='0.0.0.0', debug=True)
    # app.run()







