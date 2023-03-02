import datetime
import os
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import create_engine, select, text
from Schemas import User,Product,Image
import re
import boto3

import mysql.connector
from mysql.connector import Error
import security
import datetime
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)



BUCKET_NAME = os.getenv("S3_Bucket_Name")

conn = engine.connect()
create_database_query = text("CREATE DATABASE IF NOT EXISTS webapp")
conn.execute(create_database_query)

engine = create_engine(DATABASE_URL+"/webapp")



def get_user(user_id):  
    response_json = {}

    session = Session(engine)

    stmt = select(User).where(User.id.in_([user_id]))
    try:
        for user in session.scalars(stmt):
            response_json["id"] = user.id
            response_json["first_name"] = user.first_name
            response_json["last_name"] = user.last_name
            response_json["username"] = user.username
            response_json["account_created"] = user.account_created
            response_json["account_updated"] = user.account_updated
    except NoResultFound:
        return {}

    return response_json




def fetch_id(model):                                    ##Total number of id count +1 
    session = Session(engine)
    _id = session.query(model.id).count() + 1
    session.close()
    return _id




def user_create(first_name, last_name, password, user_name):
    
    resp_json = {}
    
    resp_json['fisrt_name'] = first_name
    resp_json['last_name']  = last_name
    resp_json['user_name']  = user_name
    encrypted_password = security.get_bcrypt_password(password)
    account_created = datetime.datetime.isoformat(datetime.datetime.now())
    account_updated = datetime.datetime.isoformat(datetime.datetime.now())
    access_token = security.get_encoded_token(user_name+":"+password)

    _id = fetch_id(User)
    try:
        user = User(id=_id, first_name=first_name, last_name=last_name, password=encrypted_password,
                    username=user_name, account_created=account_created, account_updated=account_updated)

        session = Session(engine)

        session.add(user)
        session.commit()
        session.close()
    except IntegrityError:
        return "Exists"
    except Exception as e:
        print (e)
        return "Error"                                          ## Why Just Id
    resp_json["id"] = _id
    resp_json['account_created'] = account_created
    resp_json['account_updated'] = account_updated
    
    return resp_json



def fetch_user(user_id):
    resp_json = {}

    session = Session(engine)

    stmt = select(User).where(User.id.in_([user_id]))
    try:
        for user in session.scalars(stmt):
            resp_json["id"] = user.id
            resp_json["first_name"] = user.first_name
            resp_json["last_name"] = user.last_name
            resp_json["username"] = user.username
            resp_json["accorunt_created"] = user.account_created
            resp_json["account_updated"] = user.account_updated
    except NoResultFound:
        return {}

    return resp_json


def modify_user(user_id, first_name, last_name, password):
    flag = False

    session = Session(engine)

    query = select(User).where(User.id == user_id)

    user = session.scalars(query).one()

    if first_name:
        flag = True
        user.first_name = first_name

    if last_name:
        flag = True
        user.last_name = last_name

    if password:
        flag = True
        encrypted_password = security.get_bcrypt_password(password)
        user.password = encrypted_password
        

    if flag:
        account_updated = datetime.datetime.isoformat(datetime.datetime.now())
        user.account_updated = account_updated

    session.commit()
    session.close()


def user_validation(token):
    token = token.replace("Basic ", "")

    user_name, password = security.get_decoded_token(token)


    session = Session(engine)
    query = select(User).where(User.username == user_name)
    try:
        user = session.scalars(query).one()
        session.close()

        stored_password = user.password

        if security.password_check(password, stored_password):
            return user.id
        else:
            return ""
    except NoResultFound:
        return ""
    



def get_product(product_id):
    session = Session(engine)
    query = select(Product).where(Product.id == product_id)
    try:
        product = session.scalars(query).one()
    except NoResultFound:
        return {}
    pro_json = {}

    pro_json['id'] = product.id
    pro_json['name'] = product.name
    pro_json['description'] = product.description
    pro_json['sku'] = product.sku
    pro_json['manufacturer'] = product.manufacturer
    pro_json['quantity'] = product.quantity
    pro_json['date_added'] = product.date_added
    pro_json['date_updated'] = product.date_last_updated
    pro_json['owner_user_id'] = product.owner_user_id

    session.close()

    return pro_json



def owner_check(user_id, product_id):
    session = Session(engine)

    query = select(Product).where(Product.id == product_id)

    product = session.scalars(query).one()

    session.close()
    if product.owner_user_id == user_id:
        return True
    return False


def del_product(product_id):
    session = Session(engine)

    query = select(Product).where(Product.id == product_id)

    product = session.scalars(query).one()

    session.delete(product)
    session.commit()
    session.close()




def create_product(product_info, user_id):

    response_json = {}
    _id = fetch_id(Product)
    response_json["id"] = _id

    response_json['name'] = product_info.get("name")
    response_json['description'] = product_info.get("description")
    response_json['sku'] = product_info.get("sku")
    response_json['manufacturer'] = product_info.get("manufacturer")
    response_json['quantity'] = product_info.get("quantity")

    date_created = datetime.datetime.isoformat(datetime.datetime.now())
    date_last_updated = datetime.datetime.isoformat(datetime.datetime.now())

    response_json["date_added"] = date_created
    response_json["date_last_updated"] = date_last_updated
    response_json["owner_user_id"] = user_id
    try:
        user = Product(id=_id, name=response_json["name"], description=response_json["description"],
                       sku=response_json["sku"], manufacturer=response_json.get("manufacturer", ""), quantity=response_json.get("quantity"), date_added=date_created, date_last_updated=date_last_updated, owner_user_id=user_id)

        session = Session(engine)

        session.add(user)
        session.commit()
        session.close()
    except IntegrityError:
        return "User Already Exists"
    except Exception as e:
        print(e)
        return "Error Creating User"

  
    return response_json



def modify_product(product_id, name, description, sku, manufacturer, quantity):
    session = Session(engine)

    query = select(Product).where(Product.id == product_id)
    try:
        product = session.scalars(query).one()
    except NoResultFound:
        return ""
    flag = False
    if name:
        product.name = name
        flag = True

    if description:
        product.description = description
        flag = True

    if sku:
        product.sku = sku
        flag = True

    if manufacturer:
        product.manufacturer = manufacturer
        flag = True

    if quantity:
        product.quantity = quantity
        flag = True

    if flag:
        date_last_updated = datetime.datetime.isoformat(
            datetime.datetime.now())
        product.date_last_updated = date_last_updated

    session.commit()
    session.close()



def get_images(product_id, image_id=None):
    session = Session(engine)
    if image_id:
        stmt = select(Image).where(Image.product_id ==
                                   product_id).where(Image.image_id == image_id)
    else:
        stmt = select(Image).where(Image.product_id == product_id)

    image_list = []

    try:

        images = session.scalars(stmt)
        for i in images:
            image = {}
            image["image_id"] = i.image_id
            image["product_id"] = i.product_id
            image["file_name"] = i.file_name
            image["date_created"] = i.date_created
            image["s3_bucket_path"] = i.s3_bucket_path
            image_list.append(image)
    except NoResultFound:
        return {}

    return image_list





def upload_image(image, user_token):
    s3_client = boto3.client("s3")

    # file_object = open(image)
    image_name = os.path.basename(image)
    key_name = "{0}/{1}".format(user_token, image_name)
    s3_client.upload_file(image, Bucket=BUCKET_NAME, Key=key_name)

    return key_name




def insert_image_record(image, user_id, product_id):
    resp_json = {}

    resp_json['product_id'] = product_id
    image_name = os.path.basename(image)
    resp_json['file_name'] = image_name
    date_created = datetime.datetime.isoformat(datetime.datetime.now())
    resp_json["date_created"] = date_created
    
    image_id = fetch_id(Image)
    resp_json['image_id'] = image_id
    try:
        s3_key = upload_image(image, user_id)
        resp_json["s3_bucket_path"] = s3_key
        image = Image(image_id=image_id, product_id=product_id,
                      file_name=image_name, date_created=date_created, s3_bucket_path=s3_key)

        session = Session(engine)

        session.add(image)
        session.commit()
        session.close()

    except IntegrityError:
        return "Exists"

    except Exception as e:
        print(e)
        return "Error"
    
    return resp_json


def s3_delete_image(image_id, user_token):
    s3_client = boto3.client("s3")
    key_name = "{0}/{1}".format(user_token, image_id)
    response = s3_client.delete_object(Bucket=BUCKET_NAME, Key=key_name)
    if response["ResponseMetadata"]["HTTPStatusCode"] == 204:
        return True
    return False


def delete_image(product_id, image_id, user_token):
    session = Session(engine)

    stmt = select(Image).where(Image.product_id ==
                               product_id).where(Image.image_id == image_id)

    image = session.scalars(stmt).one()

    image_filename = image.file_name
    status = s3_delete_image(image_filename, user_token)
    if status:
        session.delete(image)
        session.commit()
        session.close()
        return True
    return False



















