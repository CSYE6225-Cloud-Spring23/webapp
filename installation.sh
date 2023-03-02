# Updating OS
sudo yum update -y
sudo yum upgrade -y


# Install mySQL
sudo amazon-linux-extras install epel -y

sudo yum install https://dev.mysql.com/get/mysql80-community-release-el7-5.noarch.rpm -y

sudo yum install mysql

sudo yum install -y mysql-devel

sudo yum install default-libmysqlclient-dev -y

sudo yum install gcc -y

sudo yum install python3-devel -y


unzip webapp.zip

pip3 install -r requirements.txt

sudo cp /home/ec2-user/webapp.service /etc/systemd/system/webapp.service

sudo systemctl daemon-reload

sudo systemctl start webapp

sudo systemctl enable webapp




