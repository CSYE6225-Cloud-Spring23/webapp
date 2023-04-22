

import DbConfig
import security
import validator
import sqlalchemy
import os
from dotenv import load_dotenv
import json
from sqlalchemy import create_engine, text
import datetime
from flask import (Flask, Response, request)
from TableSchemas import ProductSchema,UserSchema
import Schemas
from werkzeug.utils import secure_filename
import logging
from functools import wraps
import statsd





statsd_config = statsd.StatsClient('localhost', 8125) 






app = Flask(__name__)



logging.basicConfig(filename='api_hit.log',
                    level=logging.DEBUG, format= '%(asctime)s %(name)s, %(levelname)s : %(message)s')





load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

UPLOAD_FOLDER = os.path.join(app.instance_path, 'uploads')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

engine = create_engine(DATABASE_URL)

conn = engine.connect()
create_database_query = text("CREATE DATABASE IF NOT EXISTS webapp")
conn.execute(create_database_query)

engine = create_engine(DATABASE_URL+"/webapp")



Schemas.Base.metadata.create_all(engine)



def api_hit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        statsd_config.incr("api_hit",1)
        return decorated_function



def api_hit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        statsd_config.incr("api_hit",1)
        statsd_config.incr(f.__name__, 1)
        return f(*args, **kwargs)
    return decorated_function






@app.route('/')
@api_hit
def MainPage():
    
    return 'Welcome User!'



@app.route('/healthz')
@api_hit
def healthz():
    app.logger.info("Server is Up and Running!")
    return Response(str("Server is Up and Running!"), status=200, mimetype='application/json')


@app.route('/v2/user', methods=['POST'])
@api_hit
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
        app.logger.error("User already exists!")
        return Response(str("User already exists"), status=400, mimetype='application/json')
    elif reponse_json == "Error":
        app.logger.error("Unable to Create the User")
        return Response(str("Unable to Create the User"), status=400, mimetype='application/json')













@app.route("/v1/product/", methods=["POST"])
@api_hit
def create_product():

    create_product_schema = ProductSchema.ProductSchema()

    errors = create_product_schema.validate(request.json)

    if errors:
        return Response(str(errors), status=422, mimetype='application/json')

    token = request.headers.get("Authorization")
    if not token:
        app.logger.error("Bad Request")
        return Response(str("Bad Request"), status=400, mimetype='application/json')

    user_token = DbConfig.user_validation(token)
    if not user_token:
        app.logger.error("Not Authorized")
        return Response(str("Not Authorized"), status=401, mimetype='application/json')
    reponse_json = DbConfig.create_product(request.json, user_token)
    return Response(json.dumps(reponse_json, default=str), status=201, mimetype='application/json')





@app.route('/v1/product/<int:product_id>')
@api_hit
def get_product(product_id):
    product = DbConfig.get_product(product_id)
    if not product:
        app.logger.error("Not Found")
        return Response(str("Not Found"), status=404, mimetype='application/json')
    return Response(json.dumps(product, default=str), status=200, mimetype='application/json')


@app.route("/v1/product/<int:product_id>", methods=["DELETE"])
@api_hit
def delete_product(product_id):
    token = request.headers.get("Authorization")
    if not token:
        app.logger.error("Bad Request")
        return Response(str("Bad Request"), status=400, mimetype='application/json')

    user_token = DbConfig.user_validation(token)

    if not DbConfig.get_product(product_id):
        app.logger.error("Not Found")
        return Response(str("Not Found"), status=404, mimetype='application/json')

    if not DbConfig.owner_check(user_token, product_id):
        app.logger.error("Unauthorized")
        return Response(str("Unauthorized"), status=401, mimetype='application/json')

    flag = DbConfig.del_product(product_id)

    return Response(str("Product has been Deleted"), status=204, mimetype='application/json')


@app.route("/v1/product/<int:product_id>", methods=["PUT", "PATCH"])
@api_hit
def update_product(product_id):
    token = request.headers.get("Authorization")
    if not token:
        app.logger.error("Bad Request")
        return Response(str("Bad Request"), status=400, mimetype='application/json')

    user_token = DbConfig.user_validation(token)

    product = DbConfig.get_product(product_id)
    if not product:
        app.logger.error("Bad Request")
        return Response(str("Bad Request"), status=400, mimetype='application/json')

    if product.get("owner_user_id") != user_token:
        app.logger.error("Not Authorized")
        return Response(str("Not Authorized"), status=401, mimetype='application/json')

    name = request.json.get("name", "")
    description = request.json.get("description", "")
    sku = request.json.get("sku", "")
    manufacturer = request.json.get("manufacturer", "")
    quantity = request.json.get("quantity", "")

    flag = DbConfig.modify_product(
        product_id, name, description, sku, manufacturer, quantity)
    app.logger.info("Product Details  Modified")
    return Response(str("Product Details  Modified"), status=204, mimetype='application/json')




@app.route("/v1/product/<int:product_id>/image", methods=["GET"])
@api_hit
def get_all_image(product_id):
    token = request.headers.get("Authorization")
    if not token:
        app.logger.error("Bad Request")
        return Response(str("Bad Request"), status=400, mimetype='application/json')

    user_token = DbConfig.user_validation(token)

    if not user_token:
        return Response(str("Unauthorized"), status=401, mimetype='application/json')

    product = DbConfig.get_product(product_id)
    if not product:     
        return Response(str("Bad Request"), status=400, mimetype='application/json')

    if product.get("owner_user_id") != user_token:
        return Response(str("Forbidden"), status=403, mimetype='application/json')

    resp = DbConfig.get_images(product_id)

    return Response(json.dumps(resp, default=str), status=200, mimetype='application/json')


@app.route("/v1/product/<int:product_id>/image", methods=["POST"])
@api_hit
def upload_image(product_id):
    token = request.headers.get("Authorization")
    if not token:
        return Response(str("Bad Request"), status=400, mimetype='application/json')

    user_token = DbConfig.user_validation(token)

    if not user_token:
        app.logger.error("Unauthorized")
        return Response(str("Unauthorized"), status=401, mimetype='application/json')

    product = DbConfig.get_product(product_id)
    if not product:
        app.logger.error("Bad Request")
        return Response(str("Bad Request"), status=400, mimetype='application/json')

    if product.get("owner_user_id") != user_token:
        app.logger.error("Forbidden")
        return Response(str("Forbidden"), status=403, mimetype='application/json')

    file_obj = request.files["file"]

    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file_obj.filename))

    file_obj.save(file_path)

    resp = DbConfig.insert_image_record(file_path, user_token, product_id)

    return Response(json.dumps(resp, default=str), status=200, mimetype='application/json')



@app.route("/v1/product/<int:product_id>/image/<int:image_id>")
@api_hit
def fetch_image(product_id, image_id):
    token = request.headers.get("Authorization")
    if not token:
        app.logger.error("Bad Request")
        return Response(str("Bad Request"), status=400, mimetype='application/json')

    user_token = DbConfig.user_validation(token)

    if not user_token:
        app.logger.error("Unauthorized")
        return Response(str("Unauthorized"), status=401, mimetype='application/json')

    product = DbConfig.get_product(product_id)
    if not product:
        app.logger.error("Bad Request")
        return Response(str("Bad Request"), status=400, mimetype='application/json')

    if product.get("owner_user_id") != user_token:
        app.logger.error("Forbidden")
        return Response(str("Forbidden"), status=403, mimetype='application/json')

    resp = DbConfig.get_images(product_id, image_id)
    app.logger.info("Image Fetched")
    return Response(json.dumps(resp, default=str), status=200, mimetype='application/json')


@app.route("/v1/product/<int:product_id>/image/<int:image_id>", methods=["DELETE"])
@api_hit
def delete_image(product_id, image_id):
    token = request.headers.get("Authorization")
    if not token:
        app.logger.error("Bad Request")
        return Response(str("Bad Request"), status=400, mimetype='application/json')

    user_token = DbConfig.user_validation(token)

    if not user_token:
        app.logger.error("Unauthorized")
        return Response(str("Unauthorized"), status=401, mimetype='application/json')

    product = DbConfig.get_product(product_id)
    if not product:
        app.logger.error("Bad Request")
        return Response(str("Bad Request"), status=400, mimetype='application/json')

    if not DbConfig.get_images(product_id, image_id):
        app.logger.error("Not Found")
        return Response(str("Not Found"), status=404, mimetype='application/json')

    if product.get("owner_user_id") != user_token:
        app.logger.error("Forbidden")
        return Response(str("Forbidden"), status=403, mimetype='application/json')

    resp = DbConfig.delete_image(product_id, image_id, user_token)
    if resp:
        app.logger.error("Ok")
        return Response(str("OK"), status=204)
    return Response(str("Error"), status=400)









if __name__ == '__main__':
    port = int(5000)
    app.run(port=port, host='0.0.0.0', debug=False)
    # app.run()







