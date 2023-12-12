from flask import jsonify, Blueprint, request, session
# from db_connection import get_db_connection
from db_connection_secrest_manager import get_db_connection

login_session_blueprint = Blueprint('login_sessions', __name__)
    
@login_session_blueprint.route('/login', methods = ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print(username,password)

    # 데이터베이스 연결
    conn = get_db_connection()
    cursor = conn.cursor()

    # 사용자 인증 쿼리
    cursor.execute('SELECT * FROM users WHERE username = %s;', (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    # 사용자 검증
    if user and user[3] == password: 
        session['username'] = user[1]
        session['email'] = user[2]
        return jsonify(success=True)
    else:
        return jsonify(success=False), 401
    
@login_session_blueprint.route('/login', methods = ['GET'])
def check_session():
    # 'session' 쿠키 값을 확인
    print(request)
    print(request.cookies.get('session_id'))
    session_id = request.cookies.get('session_id')
    some_data = session.get(session_id)
    print(some_data)

    # session_id가 있으면 True, 없으면 False 반환
    return jsonify(bool(session_id))