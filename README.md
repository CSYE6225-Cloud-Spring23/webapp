Network Structures and Cloud Computing 

Tools used
_________________________________________________________

Backend Language: Python
Framework Used: Flask
DB: MySQL


__________________________________________________________

Build Instructions



Clone this repository

$ git clone git@github.com:CSYE6225-Cloud-Spring23/webapp.git


Navigate to webapp directory

$ cd webapp 




__________________________________________________________


Deploy Instructions


Create Enviornment File



DATABASE_HOSTNAME=localhost
DATABASE_UNAME=root
DATABASE_PWD=root
DATABASE= webapp


To start Application Run Below Command



python.exe .\app.py



Test api endpoint using Postman or other Browser.

___________________________________________________________________

To Execute Test Cases


python.exe -m pytest .\app_test.py
