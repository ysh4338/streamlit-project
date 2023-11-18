# PostgreSQL Install
sudo dnf update
sudo dnf install postgresql15 
sudo dnf install postgresql15-server

# user switching
# postgres 유저 내 생성되는 Data Directory 접근은 가능하지만 다른 유저에서는 생성하지 못한다.
su - postgres

# initialize database
initdb
pg_ctl -D /var/lib/pgsql/data -l logfile start

# Database 설정
# psql 이용 접속 후 나머지 작업은 initial_settings_db.sql 파일 실행
psql
