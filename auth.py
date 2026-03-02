from abc import ABC, abstractmethod

import flask
from flask import render_template


class AuthInterface(ABC):
    def __init__(self):
        self.auth_type = None
    
    @abstractmethod
    def get_user(self, flask_request) -> any:
        pass

    @abstractmethod
    def is_logged_in(self, user: any) -> bool:
        pass

    @abstractmethod
    def override_config_for_user(self, user: any, config: dict) -> dict:
        pass

    @abstractmethod
    def login_form(self) -> str:
        pass

    @abstractmethod
    def login_handler(self, flask_request) -> str:
        pass

    @abstractmethod
    def callback_handler(self, flask_request) -> str:
        pass

    @abstractmethod
    def logout_handler(self, flask_request) -> str:
        pass

class NoAuth(AuthInterface):
    def get_user(self, flask_request) -> any:
        return {}

    def is_logged_in(self, user: any) -> bool:
        return True

    def override_config_for_user(self, user: any, config: dict) -> dict:
        return config

    def login_form(self) -> str:
        return ''

    def login_handler(self, flask_request) -> str:
        return 'No login required'

    def callback_handler(self, flask_request) -> str:
        return 'No login required'

    def logout_handler(self, flask_request) -> str:
        return 'No login required'


class ConfigFileAuth(AuthInterface):
    def __init__(self, users_config):
        """初始化配置文件认证类
        
        Args:
            users_config: 用户配置列表，格式为[{"user": "用户名", "password": "密码"}]
        """
        self.users_config = users_config or []
        # 将用户配置转换为字典以便快速查找
        self.user_dict = {user["user"]: user["password"] for user in self.users_config}
    
    def get_user(self, flask_request) -> any:
        """从请求中获取用户信息"""
        return flask_request.cookies.get('user')
    
    def is_logged_in(self, user: any) -> bool:
        """检查用户是否已登录"""
        return user is not None
    
    def override_config_for_user(self, user: any, config: dict) -> dict:
        """根据用户覆盖配置"""
        return config
    
    def login_form(self, error_message=None) -> str:
        """返回登录表单HTML，支持显示错误信息"""
        return render_template('login.html', error=error_message, auth_type=self.auth_type)
    
    def login_handler(self, flask_request) -> str:
        """处理登录请求"""
        username = flask_request.form.get('username')
        password = flask_request.form.get('password')
        
        # 验证用户名和密码
        if username in self.user_dict and self.user_dict[username] == password:
            # 登录成功，设置用户cookie并重定向到数据库选择页面
            response = flask.make_response(flask.redirect('/select_db'))
            response.set_cookie('user', username)
            return response
        else:
            # 登录失败，显示错误信息
            return render_template('login.html', error="用户名或密码错误", auth_type=self.auth_type)
    
    def callback_handler(self, flask_request) -> str:
        """处理回调（用户名密码认证不需要回调）"""
        # 直接跳转到登录页面
        return flask.redirect('/')
    
    def logout_handler(self, flask_request) -> str:
        """处理登出请求"""
        response = flask.make_response(flask.redirect('/'))
        response.delete_cookie('user')
        return response
