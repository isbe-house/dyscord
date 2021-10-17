# import requests


# def auth_loop():
#     pass

# class auth_junk:
#     OAUTH_AUTH_RUL = 'https://discord.com/api/oauth2/authorize'
#     OAUTH_TOKEN_RUL = 'https://discord.com/api/oauth2/token'
#     OAUTH_REVOKE_RUL = 'https://discord.com/api/oauth2/token/revoke'

#     CLIENT_ID = '889065662641737791'

#     CLIENT_SECRET = 'a74X3B8Qaf3czzfIp54e8YYOlz_QziKu'

#     def __init__(self):
#         pass

#     @classmethod
#     def request_initial_auth(cls):
#         url = 'https://discord.com/api/oauth2/authorize?response_type=code&client_id=889065662641737791&scope=bot'
#         print(url)

#     @classmethod
#     def generate_bearer_token(cls, code):
#         REDIRECT_URI = 'http://localhost/redirect'

#         data = {
#             'client_id': cls.CLIENT_ID,
#             'client_secret': cls.CLIENT_SECRET,
#             'grant_type': 'authorization_code',
#             'code': code,
#             'redirect_uri': REDIRECT_URI
#         }
#         headers = {
#             'Content-Type': 'application/x-www-form-urlencoded'
#         }
#         r = httpx.post('%s/oauth2/token' % cls.BASE_URL, data=data, headers=headers)
#         r.raise_for_status()
#         return r.json()

#     @classmethod
#     def renew_bearer_token(cls):
#         pass
