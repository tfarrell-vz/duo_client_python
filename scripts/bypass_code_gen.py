import duo_client

INTEGRATION_KEY = ''
SECRET_KEY = ''
HOST = ''

admin_api = duo_client.Admin(ikey=INTEGRATION_KEY, skey=SECRET_KEY, host=HOST)

users = admin_api.get_users()