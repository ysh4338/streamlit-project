import boto3
import time
import psutil
from widget.side_bar import start_process
import requests
import pandas as pd
import streamlit as st


class Homepage:
    def __init__(self):
        self.homepage()

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

    def get_instance_name_tag(ec2_client, instance_id):
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                # 태그 목록 내에서 'Name' 키를 가진 태그를 찾습니다.
                name_tag = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), None)
                if name_tag:
                    return name_tag  # 'Name' 태그 값 반환
        return None

    def server_monitoring():
        # 상태 표시할 빈 컨테이너 생성
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        cpu_slot = col1.empty()
        memory_slot = col2.empty()
        disk_usage_slot = col3.empty()
        uptime_slot = col4.empty()
        load_avg_slot_1 = col5.empty()
        load_avg_slot_5 = col6.empty()
        load_avg_slot_15 = col7.empty()

        # CPU 및 메모리 정보를 실시간으로 업데이트
        while True:
            # 메트릭 정보 수집
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk_usage = psutil.disk_usage('/')
            load_average = psutil.getloadavg()
            uptime_seconds = time.time() - psutil.boot_time()

            # 컬럼에 메트릭 정보 표시
            cpu_slot.metric(label="CPU Usage", value=cpu_percent)
            memory_slot.metric(label="Memory Usage", value=memory.percent)
            disk_usage_slot.metric(label="Disk Usage", value=disk_usage.percent)

            uptime_info = f"{uptime_seconds / 60:,.0f} M"
            uptime_slot.metric(label="Uptime", value=uptime_info)

            load_avg_slot_1.metric(label="Load Avg(1)", value=f"{load_average[0]:.2f}")
            load_avg_slot_5.metric(label="Load Avg(5)", value=f"{load_average[1]:.2f}")
            load_avg_slot_15.metric(label="Load Avg(15)", value=f"{load_average[2]:.2f}")

            # 1초간 쉬었다가 계속 진행 (데이터 새로고침 간격)
            time.sleep(1)

    def homepage(self):
        st.title("AWS EC2 Information")
        placeholder = st.empty()
        st.header('EC2 Instance Information Table', divider = "gray")

        with st.sidebar:
            st.sidebar.header('System Control Panner')
            timeout = st.sidebar.number_input('Enter timeout and click button for the stress test:', value=300)
            if st.sidebar.button("Start Stress Test", use_container_width=True):
                start_process(timeout)

        # EC2 Version
        token = Homepage.get_token()
        ec2_client = boto3.client('ec2')
        instance_id = Homepage.get_instance_metadata(token, "instance-id")
        name_tag = Homepage.get_instance_name_tag(ec2_client, instance_id)
        metadata_info = {
            "Name": name_tag,
            "Instance ID": Homepage.get_instance_metadata(token, "instance-id"),
            "Instance Type": Homepage.get_instance_metadata(token, "instance-type"),
            "Region": Homepage.get_instance_metadata(token, "placement/region"),
            "Private IP": Homepage.get_instance_metadata(token, "local-ipv4"),
            "Public IP": Homepage.get_instance_metadata(token, "public-ipv4"),
            "Availability Zone": Homepage.get_instance_metadata(token, "placement/availability-zone"),
        }

        # 데이터프레임 생성
        df = pd.DataFrame(list(metadata_info.items()), columns=['Metadata', 'Value'])
        st.table(df)

        #Monitoring Information
        with placeholder.container():
            Homepage.server_monitoring()