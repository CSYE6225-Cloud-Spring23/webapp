# Updating OS
sudo yum update -y
sudo yum upgrade -y

sudo yum install amazon-cloudwatch-agent -y


##Install Cloud Watch Agent

sudo yum install amazon-cloudwatch-agent -y



# Install mySQL
sudo amazon-linux-extras install epel -y



sudo yum install mysql -y

sudo yum install -y mysql-devel

sudo yum install default-libmysqlclient-dev -y

sudo yum install gcc -y

sudo yum install python3-devel -y


unzip webapp.zip

sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
    -a fetch-config \
    -m ec2 \
    -c file:/home/ec2-user/cloud_watch.json \
    -s


pip3 install -r requirements.txt

sudo cp /home/ec2-user/webapp.service /etc/systemd/system/webapp.service

sudo systemctl daemon-reload

sudo systemctl start webapp

sudo systemctl enable webapp




