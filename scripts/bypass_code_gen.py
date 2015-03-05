import csv
import mock
import json

import duo_client

DEBUG = True

INTEGRATION_KEY = ''
SECRET_KEY = ''
HOST = ''

BYPASS_CODES = [
    "407176182",
    "016931781",
    "338390347",
    "537828175",
    "006165274",
    "438680449",
    "877647224",
    "196167433",
    "719424708",
    "727559878"
  ]

USER = r'''
{
    "response": [{
    "user_id": "DU3RP9I2WOC59VZX672N",
    "username": "jsmith",
    "realname": "Joe Smith",
    "email": "jsmith@example.com",
    "status": "active",
    "groups": [{
      "desc": "People with hardware tokens",
      "name": "token_users"
    }],
    "last_login": 1343921403,
    "notes": "",
    "phones": [{
      "phone_id": "DPFZRS9FB0D46QFTM899",
      "number": "+15555550100",
      "extension": "",
      "name": "",
      "postdelay": null,
      "predelay": null,
      "type": "Mobile",
      "capabilities": [
        "sms",
        "phone",
        "push"
      ],
      "platform": "Apple iOS",
      "activated": false,
      "sms_passcodes_sent": false
    }],
    "tokens": [{
      "serial": "0",
      "token_id": "DHIZ34ALBA2445ND4AI2",
      "type": "d1"
    }]
  }]
}
'''

def get_fresh_codes(user, admin_api):
    user_id = user['user_id']
    bypass_codes = admin_api.get_user_bypass_codes(user_id)

    return bypass_codes

def generate_codes(users, admin_api, exclude=None):
    code_dict = {}

    for user in users:
        code_dict[user['username']] = get_fresh_codes(user, admin_api)

    return code_dict

def write_codes(code_dict, file):
    with open(file, 'w') as csvfile:
        fieldnames = ['username']
        for i in range (1,11):
            fieldnames.append('code %s' % i)

        writer = csv.writer(csvfile)
        for key, value in code_dict.iteritems():
            writer.writerow([key] + value)

def initiate_api():
    if not DEBUG:
        admin_api = duo_client.Admin(ikey=INTEGRATION_KEY, skey=SECRET_KEY, host=HOST)

    else:
        admin_api = mock.MagicMock()
        admin_api.get_user_bypass_codes.return_value = BYPASS_CODES
        admin_api.get_users.return_value = json.loads(USER)['response']

    return admin_api

def main():
    admin_api = initiate_api()
    users = admin_api.get_users()
    code_dict = generate_codes(users, admin_api)
    write_codes(code_dict, 'api_output.txt')


if __name__ == '__main__':
    main()




