import time

import requests as r


class Requests:

    group_id = '\'rosatomcareer\''
    qtoken = ''
    token = ''

    @staticmethod
    def load_script(filename):
        script_file = open(filename, "r")
        script = script_file.read()
        script = script.replace('\n', '')
        script = script.replace('\t', '')
        return script

    @staticmethod
    def authorize():
        params = {
            "client_id": 7867111,
            "redirect_uri": 'https://oauth.vk.com/blank.html',
        }
        response = r.get('https://oauth.vk.com/authorize', params=params)

        print(0)

    @staticmethod
    def load_token():
        qtoken_file = open("tkn_q", 'r')
        token_file = open("tkn", 'r')
        Requests.qtoken = qtoken_file.read()
        Requests.token = token_file.read()

    @staticmethod
    def get_member_info_proto():
        raw_script = Requests.load_script('getMembersScript')
        extra_fields = '\'country,city,bdate,education,career,sex\''
        param_script = raw_script.format(access_token=Requests.qtoken,
                                         extra_fields=extra_fields,
                                         group_id=Requests.group_id)
        params = {
            'v': '5.131',
            'access_token': Requests.token,
            'code': param_script
        }
        response = r.get('https://api.vk.com/method/execute', params=params)
        return response.json()

    @staticmethod
    def get_is_member(members, groups):
        raw_script = Requests.load_script('checkMembershipScript')
        total = len(members)
        ids = []
        for i in range(len(members)):
            ids.append(members[i].id)
        loaded = 0
        result = []
        while loaded < total:
            param_script = raw_script.format(access_token=Requests.qtoken,
                                             groups_list=groups,
                                             id_list=ids[loaded:loaded+500])
            loaded += 500
            params = {
                'v': '5.131',
                'access_token': Requests.token,
                'code': param_script
            }
            response = r.get('https://api.vk.com/method/execute', params=params)
            total += 500
            time.sleep(0.5)
            result.append(response)
        return result
