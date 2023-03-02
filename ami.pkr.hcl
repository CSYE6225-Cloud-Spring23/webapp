packer {
  required_plugins {
    amazon = {
      version = ">= 0.0.2"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "profile" {
  type    = string
  default = "dev"
}

variable "source_ami" {
  type    = string
  default = "ami-0dfcb1ef8550277af"
}

variable "ssh-user" {
  type    = string
  default = "ec2-user"
}

variable "subnet" {
  type    = string
  default = "subnet-0b35e0574749a573f"
}


variable "ami_user" {

type = list(string)
default = ["783045208422"]
}






variable "ami_region" {
    type = list(string)
    default = ["us-east-1"]
}

source "amazon-ebs" "my-ami" {
  instance_type = "t2.micro"
  source_ami    = var.source_ami
  ssh_username  = var.ssh-user

  subnet_id = var.subnet
  region   = var.aws_region
  ami_name = "csye6225"
  profile = "dev"
  ami_users = var.ami_user
 

  # description = "CSYE 6225 AMI"

  ami_regions = var.ami_region

  aws_polling {
    delay_seconds = 120
    max_attempts  = 10
  }

  launch_block_device_mappings {
    delete_on_termination = true
    device_name           = "/dev/xvda"
    volume_size           = 8
    volume_type           = "gp2"
  }

}

build {
  sources = ["source.amazon-ebs.my-ami"]

  provisioner "file" {
    source      = "./webapp.zip"
    destination = "/home/ec2-user/webapp.zip"
  }

  provisioner "shell" {
    script = "installation.sh"
    # environment_vars = [
    #   "DB_URL=mysql://root:Welcome!22@localhost",
    #   "APP_HOST=0.0.0.0",
    #   "APP_PORT=5000" 
    # ]
  }
}


