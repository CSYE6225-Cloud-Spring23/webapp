# Updating OS
sudo yum update -y
sudo yum upgrade -y


# Install mySQL
sudo amazon-linux-extras install epel -y

sudo yum install https://dev.mysql.com/get/mysql80-community-release-el7-5.noarch.rpm -y

sudo yum install mysql-community-server -y

sudo systemctl start mysqld

sudo yum install -y mysql-devel

sudo yum install default-libmysqlclient-dev -y

sudo yum install gcc -y

sudo yum install python3-devel -y

# get Temporary root Password
root_temp_pass=$(sudo grep 'A temporary password' /var/log/mysqld.log |tail -1 |awk '{split($0,a,": "); print a[2]}')

echo "root_temp_pass:"$root_temp_pass

# mysql_secure_installation.sql
cat > mysql_secure_installation.sql << EOF
# Make sure that NOBODY can access the server without a password
ALTER USER 'root'@'localhost' IDENTIFIED BY 'Welcome!22';
# Kill the anonymous users
DELETE FROM mysql.user WHERE User='';
# disallow remote login for root
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
# Kill off the demo database
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';
# Make our changes take effect
FLUSH PRIVILEGES;
EOF

mysql -uroot -p"$root_temp_pass" --connect-expired-password <mysql_secure_installation.sql

unzip webapp.zip

cd webapp

pip3 install -r requirements.txt

sudo cp /home/ec2-user/webapp/webapp.service /etc/systemd/system/webapp.service

sudo systemctl daemon-reload

sudo systemctl start webapp

sudo systemctl enable webapp

# Install requirements.txt
