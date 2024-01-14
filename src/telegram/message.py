import re

NO_ACCOUNT_MSG = """UID `%s` 还没有注册账号，请联系管理员注册账号。"""
ACCOUNT_MSG = """UID: `%s`\n邮箱: `%s`"""
REG_MSG = """请发送需要使用的邮箱"""
MAIL_REGEX = re.compile(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$")
LOGIN_MSG = """请点击下面的按钮登录："""
LOGIN_BUTTON = """跳转登录"""
