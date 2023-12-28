#!/bin/bash
touch /etc/rc.d/rc.local
cat <<EOT >> /etc/rc.d/rc.local
#!/bin/bash
streamlit run /root/streamlit-project/main.py --server.port 80
EOT

ln -s /etc/rc.d/rc.local /etc/rc.local
chmod 755 /etc/rc.d/rc.local

echo " " >> /lib/systemd/system/rc-local.service 
echo "[Install]" >> /lib/systemd/system/rc-local.service 
echo "WantedBy=multi-user.target" >> /lib/systemd/system/rc-local.service 

systemctl daemon-reload
systemctl enable rc-local