# import streamlit as st

# # 페이지 설정
# st.set_page_config(page_title="로그인", page_icon="🔑")

# # 로그인 함수
# def validate(username, password):
#     # 여기에서 실제 인증 로직을 구현합니다.
#     # 예를 들어, 사용자 이름과 비밀번호가 모두 'admin'이면 로그인 성공으로 간주합니다.
#     return username == "admin" and password == "admin"

# # 로그인 UI
# def login_ui():
#     st.title("로그인 페이지")

#     with st.form("login_form", clear_on_submit=False):
#         username = st.text_input("사용자 이름")
#         password = st.text_input("비밀번호", type="password")
#         submit_button = st.form_submit_button("로그인")

#         if submit_button:
#             if validate(username, password):
#                 st.success("로그인 성공!")
#                 # 로그인 성공 시 표시할 내용
#                 st.write("환영합니다!")
#             else:
#                 st.error("잘못된 사용자 이름 또는 비밀번호입니다.")

# # 메인 함수
# def main():
#     login_ui()

# if __name__ == "__main__":
#     main()
import streamlit as st
from streamlit_login_auth_ui.widgets import __login__


def login():
    __login__obj = __login__(
        auth_token = "courier_auth_token", 
        company_name = "Shims",
        width = 200, height = 250, 
        logout_button_name = 'Logout', 
        hide_menu_bool = True, 
        hide_footer_bool = False,)
        # lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')
    return __login__obj


LOGIN = login()
LOGGED_IN = LOGIN.build_login_ui()

if LOGGED_IN == True:
    st.markdown("Your Streamlit Application Begins here!")