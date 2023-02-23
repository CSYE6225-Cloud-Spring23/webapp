

## CSYE 6225 - Spring'23


# Network Structures and Cloud Computing 

# Tools used
_________________________________________________________

Backend Language: Python
Framework Used: Flask
DB: MySQL





# Assignment 4 

## Packer and AMI


<ul><li>Install Packer</li></ul>


<ul><li>Create a Packer template file: hcl file</li></ul>
<ul><li>Define the builder</li></ul>
<ul><li>Build the image</li></ul>
packer init ami.pkr.hcl 
packer build ami.pkr.hcl 
packer validate ami.pkr.hcl
packer build -var-file=variables.pkrvars.hcl ami.pkr.hcl
<ul><li>Build the image</li></ul>
<ul><li>Test the image</li></ul>


## Systemd in Python
A webapp service file is a Systemd unit file that defines a service for a web application running on a Linux system. This file specifies how the service should be 
started, stopped, and managed by the Systemd service manager.
<ul><li>[Unit]</li></ul>
This section specifies that the service should start after the network is available. This ensures that the network is up and running before the web 
application is started.
<ul><li>[Service]</li></ul>
This section defines how the service should be run. It specifies that the service is a simple service, meaning that it runs in the foreground and 
does not fork any child processes. It also specifies the user that the service should run as (ec2-user), the working directory for the service (/home/ec2-user/webapp/), and the command to start the web application (/home/ec2-user/webapp/env/bin/python3 /home/ec2-user/webapp/main.py).
<ul><li>Restart=always</li></ul>
This line specifies that the service should be restarted automatically if it fails. This ensures that the web application is always running and available.
<ul><li>[Install]</li></ul>
This section specifies that the service should be enabled and started automatically when the system boots up, and that it should be installed as a multi-user
target service.

##Basic Steps for setting EC2 instance 
1.  Connect to the EC2 instance: Use SSH to connect to the EC2 instance. You can do this using the steps I outlined in my previous response.
1.  Install dependencies: Once you've connected to the EC2 instance, install any necessary dependencies for your API. 
1. Copy your API code to the EC2 instance: Use the SCP command to copy your API code from your local machine to the EC2 instance. For example, the command scp -i keyfile.pem api.js ec2-user@public-IP-address:/home/ec2-user/api/ would copy a file called "api.js" to a directory called "api" in the home directory of the "ec2-user" account on the EC2 instance.
1. Start the API: Once your code is on the EC2 instance, start the API by running the appropriate command. The specific command you use will depend on the language and framework that you're using to build your API. For example, if you're using Node.js and Express, you might use the command node api.js to start the server.
1. Configure security: Be sure to configure the security settings for your API to restrict access as necessary. This may involve creating security groups, setting up network access control lists (ACLs), or configuring other security features as required.

## Terraform Steps
1. terraform init
1. terraform plan -var-file=terraform.tfvars
1. terraform apply --auto-approve
1. terraform destroy --auto-approve
1. terraform fmt -recursive

## DeployPacker.yaml GitHub Actions workflow file written in YAML format that automates the process of building and deploying an Amazon Machine Image (AMI) using Packer.
1. Check out the repository using the actions/checkout action.
1. Zip the repository files into a webapp.zip archive using the git archive command.
1. Upload the webapp.zip artifact using the actions/upload-artifact action.
1. Initialize Packer using the packer init command.
1. Configure AWS credentials using the aws-actions/configure-aws-credentials action.
1. Build the AMI using Packer and the packer build command, using the ami.pkr.hcl Packer template file and the variables.pkrvars.hcl variable file.
1. Clean up the dist directory using the rm command.

## Testrum.yaml
1. Check out the repository using the actions/checkout action.
1.Set up the Python environment using the actions/setup-python action, which installs the specified version of Python.
1. Install the dependencies for the application using the pip install command and the requirements.txt file.
1. Run the unit tests using the python -m pytest command, which runs the pytest test runner and discovers and executes tests in the application.


## Validate.yaml
1. Check out the repository using the actions/checkout action.
1. Validate the ami.pkr.hcl Packer template file using the packer validate command with the -syntax-only flag, which checks the syntax of the Packer configuration without building the image.

##TO INSTALL MYSQL ON EC2

* To install the requirements of MySQL on your EC2 instance, you can follow these steps:
* Connect to your EC2 instance using SSH: Use the SSH command to connect to your EC2 instance. You can use the same command you used earlier, replacing the "public-IP-address" with the public IP address of your instance.
* Update the package list: Use the command sudo yum update to update the package list on your EC2 instance.
* Install the MySQL server: Use the command sudo yum install mysql-server to install the MySQL server on your EC2 instance.
* Start the MySQL service: Use the command sudo service mysqld start to start the MySQL service.
* Secure your MySQL installation: Use the command sudo mysql_secure_installation to secure your MySQL installation by setting a root password and removing some insecure defaults. This step is optional but highly recommended for security purposes.
__________________________________________________________

# Build Instructions



Clone this repository

$ git clone git@github.com:CSYE6225-Cloud-Spring23/webapp.git


Navigate to webapp directory

$ cd webapp 




__________________________________________________________


# Deploy Instructions


Create Enviornment File



DATABASE_URL=mysql://root:root@localhost/CSYE_CLOUD2
APP_HOST=localhost
APP_PORT=5000

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

Request Body: Type JSON file

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

Endpoint   : /v1/user/{userId}


Update User's account information



----------------------------------------------------


Endpoint   /v1/product

Creates a user account

Method: POST



-----------------------------------------------------------


Endpoint   /v1/product/{productId}

Method: PUT


Update Product


---------------------------------------------------------------------

Endpoint    /v1/product/{productId}


Method: PUT


Update Patch

-----------------------------------------------------


Endpoint  /v1/product/{productId}


Method: PUT


Update Patch


----------------------------------------------------------------------