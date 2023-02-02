

## CSYE 6225 - Spring'23


# Network Structures and Cloud Computing 

# Tools used
_________________________________________________________

Backend Language: Python
Framework Used: Flask
DB: MySQL


__________________________________________________________

# Build Instructions



Clone this repository

$ git clone git@github.com:CSYE6225-Cloud-Spring23/webapp.git


Navigate to webapp directory

$ cd webapp 




__________________________________________________________


# Deploy Instructions


Create Enviornment File



DATABASE_HOSTNAME=localhost
DATABASE_UNAME=root
DATABASE_PWD=root
DATABASE= CSYE_CLOUD


To start Application Run Below Command



python.exe .\main.py



Test api endpoint using Postman or other Browser.

___________________________________________________________________

# To Execute Test Cases


python.exe -m pytest .\test_cases.py

____________________________________________________________________

# Brief about the Application



1. Health Check 

Description: Health Endpoint

/healthz

Method: GET

STATUS:  server responds with 200 OK if it is healhty.


____________________________________________________________________
# 2. Create a User Account:  

Description: Creates a User Account

Endpoint: /v1/user

Method: PUT

Request Body: Type JSON

{
    "first_name": "Name(Char)",
    "last_name": " LastName(Char)",
    "password": "Password(Varchar)",
    "user_name": "uname(Varchar)"
}

Responses:

After Successfull Creation returns with Code 201


In case of Error Returns with 401 (Bad Request)

_______________________________________________________________________


# 3. GET User Details:  

Description: Get User Account Details

Endpoint: /v1/user/{userId}

Method: POST

Request Body: NONE

Responses:

After Successfull Creation returns with Code 201 and with Below Format


{
    "id": "(int)",
    "first_name": "(char)",
    "last_name": "(char)",
    "user_name": "(varchar)",
    "account_created": "(TimeStamp)",
    "account_updated": "(TimeStamp)"
}

In case  no  USerId  provided Returns with Status 400 (Bad Request)


For invalid userId  Returns with Status 401


_____________________________________________________________________

# 4. Update User Details:  

Description: Get User Account Details

Endpoint: /v1/user/{userId}

Method: PUT

Request Body: 



{

"first_name": "(Char)",
"last_name": "(Char)",
"password": "(varchar)"


}

Responses:

After Successfull Creation returns with Code 200 after  Details  Being Updated

 
}

In case  no  UserId  provided Returns with Status 400 (Bad Request)


For invalid userId  Returns with Status 401

For Successfull returns with response 200

__

