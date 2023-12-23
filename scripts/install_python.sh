#!/bin/bash
# Python 3.11 설치 스크립트

# Python 3.11 패키지 설치
echo "##############################"
echo "Python 3.11 설치를 시작합니다."
echo "##############################"
sudo dnf install python3.11 -y

# Python 3 기본 버전 정보 목록 업데이트 
echo "##############################"
echo "Python Default Version Setting"
echo "update-alternatives 명령 실행."
echo "##############################"
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 2
echo 2 | sudo update-alternatives --config python3
echo

# Python 3.11 버전에 적합한 pip 모듈 설치
echo "################################"
echo "Python 3.11 PIP Module 설치 시작"
echo "################################"
python3 -m ensurepip --default-pip

# Python 명령을 통해 3.11 버전 사용을 위한 심볼링 링크 지정
echo "##############################"
echo "Python3 → Python Symbolic link"
echo "##############################"
echo "sudo ln -fs /usr/bin/python3.11 /usr/bin/python"
sudo ln -fs /usr/bin/python3.11 /usr/bin/python

# 설치가 완료된 Python 버전 확인
echo "#######################"
echo "Python 3.11 설치 완료"
echo "설치된 Python 버전 정보"
echo "#######################"
python --version

# Python 3.9 버전을 사용하는 dnf 명령을 위해 설정 변경
echo "#####################################"
echo "dnf/yum에서 사용하는 Python 버전 지정"
echo "#####################################"
head -1 /usr/bin/dnf
sudo sed -i 's|#!/usr/bin/python3|#!/usr/bin/python3.9|g' /usr/bin/dnf
sudo sed -i 's|#!/usr/bin/python3|#!/usr/bin/python3.9|g' /usr/bin/yum
head -1 /usr/bin/dnf
sudo dnf --version

# Streamlit 설치
echo "##############"
echo "Streamlit 설치"
echo "##############"
python3 -m pip install --upgrade pip
pip install streamlit 
pip install streamlit-option-menu
pip install boto3
pip install psutil

# Stress Tool Install for Auto-Scaling
echo "################"
echo "Stress Tool 설치"
echo "################"
sudo dnf install stress -y

