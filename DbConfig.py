import os
import re
import mysql.connector
from mysql.connector import Error
import security
import datetime
from dotenv import load_dotenv

load_dotenv()

def create_connection():  ##Function for  Creating DB Connection using mysql connector
    host_name = os.getenv("DB_HOSTNAME")
    user_name = os.getenv("DB_UNAME")
    user_password = os.getenv("DB_PWD")
    connection = None
    
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database="csye_cloud"
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):   ##Function for Executing Query
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):  ##Function for read Query
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def get_id():
    connection = create_connection()
    
    count_query = "Select count(*) from users_table;"
    res = execute_read_query(connection, count_query)

    if res:
        return res[0][0]+1
    
    return 1


def create_user(first_name, last_name, password, user_name):
    resp_json = {}
    resp_json['fisrt_name'] = first_name
    resp_json['last_name'] = last_name
    resp_json['user_name'] = user_name
   
    encrypted_password = security.get_bcrypt_password(password)
    account_created = datetime.datetime.isoformat(datetime.datetime.now())
    account_updated = datetime.datetime.isoformat(datetime.datetime.now())
    access_token = security.get_encoded_token(user_name+":"+password)
    connection = create_connection()
    _id = get_id()
    create_users = """INSERT INTO `users_table` (`id`, `first_name`, `last_name`, `password`, `username`, `account_created`, `account_updated`, `access_token`) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}');""".format(
        _id, first_name, last_name, encrypted_password, user_name, account_created, account_updated, access_token)

    print(create_users)
    execute_query(connection, create_users)

    resp_json['account_created'] = account_created
    resp_json['account_updated'] = account_updated

    return resp_json


def fetch_user(user_id):
    resp_json = {}

    connection = create_connection()


    fetch_query = "Select * from users_table where id={0};".format(user_id)

    results = execute_read_query(connection, fetch_query)

    result = ()
    if not results:
        return None

    field_list = {
        0: 'id',
        1: 'first_name',
        2: 'last_name',
        3: 'user_name',
        5: 'account_created',
        6: 'account_updated',
    }
    for k, v in field_list.items():
        resp_json[v] = results[0][k]

    return resp_json


def update_user(user_id, first_name, last_name, password):    #Function To Update User

    connection = create_connection()
    flag = False
    update_query = "update users_table set "
    
    if first_name:
        flag = True
        update_query = update_query + "first_name='{0}', ".format(first_name)
    
    if last_name:
        flag = True
        update_query = update_query + "last_name='{0}', ".format(last_name)
    
    if password:
        flag = True
        encrypted_password = security.get_bcrypt_password(password)
        update_query = update_query  + "password='{0}', ".format(encrypted_password)
    
    if flag:
        account_updated = datetime.datetime.isoformat(datetime.datetime.now())
        update_query = update_query + "account_updated='{0}'".format(account_updated)

    if update_query.endswith(", "):
        update_query = update_query[:-2]
    update_query = update_query + " where id={0};".format(user_id)

    print (update_query)
    execute_query(connection, update_query)


def validate_user(token):
    token = token.replace("Basic ","")
    connection = create_connection()
    fetch_query = "Select * from users_table where access_token='{0}';".format(token)
    print (fetch_query)
    results = execute_read_query(connection, fetch_query)
    if not results:
        return None
    
    else:
        return str(results[0][0])