import time
import psutil
import streamlit as st

class Monitoring:
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
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
        disk_usage = psutil.disk_usage('/')
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