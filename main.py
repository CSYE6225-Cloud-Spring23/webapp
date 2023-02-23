import json
from flask import (Flask, Response, request)
from dotenv import load_dotenv
import os
import TableSchemas
from TableSchemas import UserSchema, ProductSchema
from sqlalchemy import create_engine, text
import Schemas
import DbConfig

app = Flask(__name__)

load_dotenv()

DB_URL = os.environ.get("DB_URL")


engine = create_engine(DB_URL)
conn = engine.connect()
create_database_query = text("CREATE DATABASE IF NOT EXISTS webapp")
conn.execute(create_database_query)

engine = create_engine(DB_URL+"/webapp")

Schemas.Base.metadata.create_all(engine)


@app.route('/')
def hello_world():
    """
    Home endpoint
    """
    return 'Welcome User!'


@app.route('/healthz')
def healthz():
    """
    Check Server status
    """
    return Response(str("Server is up and Running"), status=200, mimetype='application/json')


@app.route('/v1/user', methods=['POST'])
def create_user():
    """
    Endpoint to create user
    """
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    password = request.json.get('password')
    user_name = request.json.get('user_name')

    create_user_schema = UserSchema.CreateUserInputSchema()

    errors = create_user_schema.validate(request.json)

    if errors:  
        return Response(str(errors), status=422, mimetype='application/json')

    resp_json = DbConfig.create_user(
        first_name, last_name, password, user_name)
    print(resp_json)
    if isinstance(resp_json, dict):
        return Response(json.dumps(resp_json), status=201, mimetype='application/json')
    
    elif resp_json == "Exists":
        return Response(str("User already exists"), status=400, mimetype='application/json')
    
    elif resp_json == "Error":
        return Response(str("DB error"), status=400, mimetype='application/json')


@app.route('/v1/user/<int:user_id>', methods=['GET', 'PUT'])
def fetch_user(user_id):
    """
    Method GET:
        Endpoint to fetch User
    Method PUT:
        Endpoint to update user
    """
    token = request.headers.get("Authorization")
    if not token:
        return Response(str("Bad Request"), status=400, mimetype='application/json')
    user_token = DbConfig.validate_user(token)

    if not user_token:
        return Response(str("Unauthorized"), status=401, mimetype='application/json')

    if user_token != user_id:
        return Response(str("Forbidden"), status=403, mimetype='application/json')

    if request.method == 'GET':
        result = DbConfig.fetch_user(user_id)

        print(result)
        return Response(json.dumps(result, default=str), status=200, mimetype='application/json')

    if request.method == 'PUT':
        if request.json.keys() - set(["first_name", "last_name", "password"]):
            return Response(str("Bad Request"), status=400, mimetype='application/json')

        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        password = request.json.get('password')

        DbConfig.update_user(user_id, first_name, last_name, password)

        return Response(str("Done"), status=204, mimetype='application/json')


@app.route('/v1/product/<int:product_id>')
def fetch_product(product_id):
    product = DbConfig.fetch_product(product_id)
    if not product:
        return Response(str("Not Found"), status=404, mimetype='application/json')
    return Response(json.dumps(product, default=str), status=200, mimetype='application/json')


@app.route("/v1/product/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    token = request.headers.get("Authorization")
    if not token:
        return Response(str("Bad Request"), status=400, mimetype='application/json')

    user_token = DbConfig.validate_user(token)

    if not user_token:
        return Response(str("Unauthorized"), status=401, mimetype='application/json')

    if not DbConfig.fetch_product(product_id):
        return Response(str("Not Found"), status=404, mimetype='application/json')

    if not DbConfig.check_product_owner(user_token, product_id):
        return Response(str("Forbidden"), status=403, mimetype='application/json')

    flag = DbConfig.delete_product(product_id)

    return Response(str(""), status=204, mimetype='application/json')


@app.route("/v1/product/<int:product_id>", methods=["PUT", "PATCH"])
def update_product(product_id):
    token = request.headers.get("Authorization")
    if not token:
        return Response(str("Bad Request"), status=400, mimetype='application/json')

    user_token = DbConfig.validate_user(token)

    if not user_token:
        return Response(str("Unauthorized"), status=401, mimetype='application/json')

    product = DbConfig.fetch_product(product_id)
    if not product:
        return Response(str("Bad Request"), status=400, mimetype='application/json')

    if product.get("owner_user_id") != user_token:
        return Response(str("Forbidden"), status=403, mimetype='application/json')

    create_product_schema = ProductSchema.ProductSchema()
    if request.method == "PUT":
        errors = create_product_schema.validate(request.json)
    elif request.method == "PATCH":
        errors = create_product_schema.validate(request.json, partial=True)

    if errors:
        return Response(str(errors), status=422, mimetype='application/json')


    name = request.json.get("name", "")
    description = request.json.get("description", "")
    sku = request.json.get("sku", "")
    manufacturer = request.json.get("manufacturer", "")
    quantity = request.json.get("quantity", "")

    flag = DbConfig.update_product(
        product_id, name, description, sku, manufacturer, quantity)
    print (flag)
    if flag == True:
        return Response(str(""), status=204, mimetype='application/json')
    else:
        return Response(str(""), status=400, mimetype='application/json')


@app.route("/v1/product/", methods=["POST"])
def create_product():

    create_product_schema = ProductSchema.ProductSchema()

    errors = create_product_schema.validate(request.json)

    if errors:
        return Response(str(errors), status=422, mimetype='application/json')

    token = request.headers.get("Authorization")
    if not token:
        return Response(str("Bad Request"), status=400, mimetype='application/json')

    user_token = DbConfig.validate_user(token)
    if not user_token:
        return Response(str("Not Authorized"), status=401, mimetype='application/json')
    
    resp_json = DbConfig.create_product(request.json, user_token)
    if isinstance(resp_json, dict):
        return Response(json.dumps(resp_json, default=str), status=201, mimetype='application/json')
    else:
        return Response(json.dumps(resp_json, default=str), status=400, mimetype='application/json')

if __name__ == '__main__':
    PORT = os.getenv("APP_PORT")
    HOST = os.getenv("APP_HOST")
    print(HOST, PORT)
    app.run(port=PORT, host=HOST, debug=False)
