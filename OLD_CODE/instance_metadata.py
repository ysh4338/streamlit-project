import streamlit as st
import requests
import pandas as pd

def get_token():
    url = "http://169.254.169.254/latest/api/token"
    headers = {"X-aws-ec2-metadata-token-ttl-seconds": "3600"}
    response = requests.put(url, headers=headers)
    return response.text

def get_instance_metadata(token, endpoint):
    url = f"http://169.254.169.254/latest/meta-data/{endpoint}"
    headers = {"X-aws-ec2-metadata-token": token}
    response = requests.get(url, headers=headers)
    return response.text

def main():
    st.title("AWS Instance Metadata")

    token = get_token()

    metadata_info = {
        "Hostname": get_instance_metadata(token, "hostname"),
        "Instance ID": get_instance_metadata(token, "instance-id"),
        "Instance Type": get_instance_metadata(token, "instance-type"),
        "Region": get_instance_metadata(token, "placement/region"),
        "Private IP": get_instance_metadata(token, "local-ipv4"),
        "Public IP": get_instance_metadata(token, "public-ipv4"),
        "Availability Zone": get_instance_metadata(token, "placement/availability-zone"),
    }

    # 데이터프레임 생성
    df = pd.DataFrame(list(metadata_info.items()), columns=['Metadata', 'Value'])

    # 데이터를 테이블로 표시
    st.table(df)

if __name__ == "__main__":
    main()