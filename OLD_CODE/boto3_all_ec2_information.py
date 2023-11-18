import streamlit as st
import boto3


ec2 = boto3.resource('ec2')
instances = ec2.instances.all()

instances_info = []
for instance in instances:
    instance_name = 'Unknown'
    for tag in instance.tags:
        if 'Key' in tag and tag['Key'] == 'Name':
            instance_name = tag.get('Value', 'Unknown')  # 태그에 'Value'가 없는 경우를 위한 기본값
            break

    instance_info = {
        'Name': instance_name,
        'AvailabilityZone': instance.placement['AvailabilityZone'],
        'Type': instance.instance_type,
        'State': instance.state['Name'],
        'Private IP': instance.private_ip_address,
        'Public IP': instance.public_ip_address or 'N/A',  # Public IP가 없는 경우 'N/A'로 표시
        'ID': instance.id
    }
    instances_info.append(instance_info)

st.table(instances_info)