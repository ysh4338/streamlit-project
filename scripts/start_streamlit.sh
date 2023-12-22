#!/bin/bash
streamlit run /root/main.py --server.port 80 > /dev/null 2> /dev/null < /dev/null &
exit 0