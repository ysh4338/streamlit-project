#!/bin/bash

# Define the metadata base URL and the token endpoint
METADATA_URL="http://169.254.169.254/latest/meta-data/"
TOKEN_ENDPOINT="http://169.254.169.254/latest/api/token"

TOKEN=$(curl -X PUT "$TOKEN_ENDPOINT" -H "X-aws-ec2-metadata-token-ttl-seconds: 3600")

# Retrieve the MAC associated with the primary network interface
MAC=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" "${METADATA_URL}network/interfaces/macs/" | head -1)

# Use the MAC to get the security group IDs
SECURITY_GROUP_IDS=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" "${METADATA_URL}network/interfaces/macs/$MAC/security-group-ids")
aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_IDS --protocol tcp --port 80 --cidr 0.0.0.0/0 > /dev/null
echo "Security Group IDs: $SECURITY_GROUP_IDS"

# Get the IAM Role Name & Attach AmazonEC2FullAccess Policy 
IAM_ROLE_NAME=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" "${METADATA_URL}iam/security-credentials/")
aws iam attach-role-policy --role-name $IAM_ROLE_NAME --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess
echo "IAM Role Name: $IAM_ROLE_NAME"