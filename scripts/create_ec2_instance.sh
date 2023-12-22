#!/bin/bash

# VPC / SUBNETS INFORMATION
VPC_NAME="lab-edu-vpc-ap-01"
PRI_SUB_NAME_01="lab-edu-sub-pri-01"
PRI_SUB_NAME_02="lab-edu-sub-pri-02"
NETWORK_EC2_NAME_01="lab-edu-ec2-network-ap-01"
NETWORK_EC2_NAME_02="lab-edu-ec2-network-ap-02"

VPC_ID=$(aws ec2 describe-vpcs --filters "Name=tag:Name,Values=$VPC_NAME" --query "Vpcs[].VpcId" --output text)
SUBNET_ID_PRIVATE_01=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" "Name=tag:Name,Values=$PRI_SUB_NAME_01" --query "Subnets[].SubnetId" --output text)
SUBNET_ID_PRIVATE_02=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" "Name=tag:Name,Values=$PRI_SUB_NAME_02" --query "Subnets[].SubnetId" --output text)

# INSTANCE INFORMATION
AMI_ID="ami-0ff1cd0b5d98708d1"
INSTANCE_TYPE="t3.micro"

# CREATE KEY-PAIR
KEY_NAME="lab-edu-pem-network"
mkdir ec2_pem
cd ec2_pem
aws ec2 create-key-pair --key-name $KEY_NAME --query 'KeyMaterial' --output text > $KEY_NAME.pem
chmod 400 $KEY_NAME.pem

# CREATE SECURITY-GROUP
SG_NAME="lab-edu-sg-network"
SG_ID=$(aws ec2 create-security-group --group-name $SG_NAME --description "My security group" --vpc-id $VPC_ID --output text)
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 22 --cidr 10.0.0.0/8 > /dev/null

# CREATE INSTANCES
NETWORK_EC2_IP_01=$(aws ec2 run-instances --image-id $AMI_ID --count 1 --instance-type $INSTANCE_TYPE --key-name $KEY_NAME --security-group-ids $SG_ID --subnet-id $SUBNET_ID_PRIVATE_01 --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$NETWORK_EC2_NAME_01}]" --query "Instances[0].PrivateIpAddress" --output text)
NETWORK_EC2_IP_02=$(aws ec2 run-instances --image-id $AMI_ID --count 1 --instance-type $INSTANCE_TYPE --key-name $KEY_NAME --security-group-ids $SG_ID --subnet-id $SUBNET_ID_PRIVATE_02 --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$NETWORK_EC2_NAME_02}]" --query "Instances[0].PrivateIpAddress" --output text)

echo "$NETWORK_EC2_IP_01 | $NETWORK_EC2_NAME_01" >> ec2_information.txt
echo "$NETWORK_EC2_IP_02 | $NETWORK_EC2_NAME_02" >> ec2_information.txt



