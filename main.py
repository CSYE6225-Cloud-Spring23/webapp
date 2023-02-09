

import DbConfig
import security
import validator
import sqlalchemy
import os
from dotenv import load_dotenv
import json
from sqlalchemy import create_engine
import datetime
from flask import (Flask, Response, request)
from TableSchemas import ProductSchema,UserSchema
import Schemas





app = Flask(__name__)


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)




Schemas.Base.metadata.create_all(engine)





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

    create_user_schema = UserSchema.CreateUserInputSchema()

    errors = create_user_schema.validate(request.json)

    if errors:
        return Response(str(errors), status=422, mimetype='application/json')

    reponse_json = DbConfig.user_create(first_name, last_name, password, user_name)
    print(reponse_json)
    if isinstance(reponse_json, dict):
        return Response(json.dumps(reponse_json), status=201, mimetype='application/json')
    elif reponse_json == "Exists":
        return Response(str("User already exists"), status=400, mimetype='application/json')
    elif reponse_json == "Error":
        return Response(str("Unable to Create the User"), status=400, mimetype='application/json')






@app.route('/v1/user/<int:user_id>', methods=['GET', 'PUT'])
def fetch_user(user_id):
    
    token = request.headers.get("Authorization")
    if not token:
        return Response(str("Bad Request"), status=400, mimetype='application/json')
    user_token = DbConfig.user_validation(token)
    if user_token != user_id:
        return Response(str("Unauthorized"), status=401, mimetype='application/json')

    if request.method == 'GET':
        result = DbConfig.get_user(user_id)

        print(result)
        return Response(json.dumps(result, default=str), status=200, mimetype='application/json')

    if request.method == 'PUT':
        if request.json.keys() - set(["first_name", "last_name", "password"]):
            return Response(str("Bad Request"), status=400, mimetype='application/json')

        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        password = request.json.get('password')

        DbConfig.modify_user(user_id, first_name, last_name, password)

        return Response(str("Updated The User"), status=204, mimetype='application/json')




@app.route("/v1/product/", methods=["POST"])
def create_product():

    create_product_schema = ProductSchema.ProductSchema()

    errors = create_product_schema.validate(request.json)

    if errors:
        return Response(str(errors), status=422, mimetype='application/json')

    token = request.headers.get("Authorization")
    if not token:
        return Response(str("Bad Request"), status=400, mimetype='application/json')

    user_token = DbConfig.user_validation(token)
    if not user_token:
        return Response(str("Not Authorized"), status=401, mimetype='application/json')
    reponse_json = DbConfig.create_product(request.json, user_token)
    return Response(json.dumps(reponse_json, default=str), status=201, mimetype='application/json')





@app.route('/v1/product/<int:product_id>')
def get_product(product_id):
    product = DbConfig.get_product(product_id)
    if not product:
        return Response(str("Not Found"), status=404, mimetype='application/json')
    return Response(json.dumps(product, default=str), status=200, mimetype='application/json')


@app.route("/v1/product/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    token = request.headers.get("Authorization")
    if not token:
        return Response(str("Bad Request"), status=400, mimetype='application/json')

    user_token = DbConfig.user_validation(token)

    if not DbConfig.get_product(product_id):
        return Response(str("Not Found"), status=404, mimetype='application/json')

    if not DbConfig.owner_check(user_token, product_id):
        return Response(str("Unauthorized"), status=401, mimetype='application/json')

    flag = DbConfig.del_product(product_id)

    return Response(str("Product has been Deleted"), status=204, mimetype='application/json')











if __name__ == '__main__':
    port = int(5000)
    app.run(port=port, host='0.0.0.0', debug=True)
    # app.run()







