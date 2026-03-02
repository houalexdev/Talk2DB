from auth import AuthInterface
import flask
import requests
from flask import render_template
import json

class CasdoorAuth(AuthInterface):
    def __init__(self, endpoint: str, client_id: str, client_secret: str):
        self.endpoint = endpoint
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_endpoint = f"{endpoint}/api/login/oauth/access_token"
        self.userinfo_endpoint = f"{endpoint}/api/userinfo"

    def get_user(self, flask_request) -> any:
        return flask_request.cookies.get('user')

    def is_logged_in(self, user: any) -> bool:
        return user is not None

    def override_config_for_user(self, user: any, config: dict) -> dict:
        return config

    def login_form(self) -> str:
        return render_template("login.html")

    def login_handler(self, flask_request) -> str:
        # 重定向到 Casdoor 登录页面
        redirect_url = f"{self.endpoint}/login/oauth/authorize"
        redirect_url += f"?client_id={self.client_id}"
        redirect_url += f"&response_type=code"
        redirect_url += f"&redirect_uri={flask_request.host_url}auth/callback"
        redirect_url += f"&scope=openid profile email"
        redirect_url += f"&state=random_state"
        
        print(f"Redirecting to: {redirect_url}")  # 添加调试日志
        return flask.redirect(redirect_url)

    def callback_handler(self, flask_request) -> str:
        code = flask_request.args.get('code')
        if not code:
            print("No code received in callback")  # 添加调试日志
            return '认证失败：未获取到授权码'

        print(f"Received code: {code}")  # 添加调试日志

        # 获取访问令牌
        token_data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': f"{flask_request.host_url}auth/callback"
        }
        
        print(f"Token request data: {token_data}")  # 添加调试日志
        print(f"Token endpoint: {self.token_endpoint}")  # 添加调试日志
        
        try:
            # 获取访问令牌
            token_response = requests.post(self.token_endpoint, data=token_data)
            print(f"Token response status: {token_response.status_code}")  # 添加调试日志
            print(f"Token response headers: {token_response.headers}")  # 添加调试日志
            print(f"Token response content: {token_response.text}")  # 添加调试日志
            
            token_response.raise_for_status()
            token_info = token_response.json()
            
            if 'access_token' not in token_info:
                print(f"Token response: {token_info}")  # 添加调试日志
                return '认证失败：未获取到访问令牌'
            
            # 获取用户信息
            headers = {'Authorization': f"Bearer {token_info['access_token']}"}
            print(f"Userinfo request headers: {headers}")  # 添加调试日志
            print(f"Userinfo endpoint: {self.userinfo_endpoint}")  # 添加调试日志
            
            userinfo_response = requests.get(self.userinfo_endpoint, headers=headers)
            print(f"Userinfo response status: {userinfo_response.status_code}")  # 添加调试日志
            print(f"Userinfo response content: {userinfo_response.text}")  # 添加调试日志
            
            userinfo_response.raise_for_status()
            user_info = userinfo_response.json()
            
            if 'name' not in user_info:
                print(f"User info response: {user_info}")  # 添加调试日志
                return '认证失败：未获取到用户信息'
            
            # 设置用户 cookie
            response = flask.make_response(flask.redirect('/select_db'))
            response.set_cookie('user', user_info['name'])
            response.status_code = 302
            return response
            
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")  # 添加调试日志
            return f'认证失败：请求错误 - {str(e)}'
        except Exception as e:
            print(f"Unexpected error: {str(e)}")  # 添加调试日志
            return f'认证失败：{str(e)}'

    def logout_handler(self, flask_request) -> str:
        response = flask.make_response('已退出')
        response.delete_cookie('user')
        response.headers['Location'] = '/'
        response.status_code = 302
        return response 