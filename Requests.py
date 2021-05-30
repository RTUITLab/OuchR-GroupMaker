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
    def get_members(params, total):
        result = []
        params['count'] = 1000
        loaded = 0
        while loaded < total:
            response = r.get('https://api.vk.com/method/groups.getMembers', params=params).json()
            # Uncomment for more then 1000 users
            # total = response['response']['count']
            response = response['response']['items']
            result.append(response)
            loaded += 1000
            params['offset'] = loaded
        return result

    @staticmethod
    def load_token():
        qtoken_file = open("tkn_q", 'r')
        token_file = open("tkn", 'r')
        Requests.qtoken = qtoken_file.read()
        Requests.token = token_file.read()

    @staticmethod
    def get_members_proto():
        raw_script = Requests.load_script('getMembersScript')
        param_script = raw_script.format(access_token=Requests.qtoken,
                                         group_id=Requests.group_id)

        params = {
            'v': '5.131',
            'access_token': Requests.token,
            'code': param_script
            }
        result = r.get('https://api.vk.com/method/execute', params=params).json()['response']
        return result

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
        print(0)
