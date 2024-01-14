# Telegram OAuth

## Configuration

```dotenv
CONN_URI=sqlite+aiosqlite:///data/db.sqlite3 # 数据库 uri
DEBUG=True # 调试模式
PROJECT_URL=http://127.0.0.1 # 项目可访问的地址
PROJECT_LOGIN_SUCCESS_URL=http://google.com # 登录成功后跳转的地址
PROJECT_PORT=80 # 项目运行的端口
JWT_PRIVATE_KEY='data/private_key' # jwt 私钥
JWT_PUBLIC_KEY='data/public_key' # jwt 公钥
BOT_TOKEN=xxx # 机器人 token
BOT_USERNAME=xxxxBot # 机器人用户名
BOT_API_ID=111 # api id
BOT_API_HASH=aaa # api hash
BOT_MANAGER_IDS=[111,222] # 管理员 id
```

## OIDC Endpoints

Auth URL : `/oauth2/authorize`

Token URL : `/oauth2/token`

Cert URL : `/oauth2/keys`

## OIDC Client

```sql
INSERT INTO "client" ("grant_types", "response_types", "redirect_uris", "id", "client_id", "client_secret", "scope") VALUES ('authorization_code', 'code', 'https://127.0.0.1/access/callback', 'UUID', '123456', '123456', 'openid profile email');
```
