import requests as r


class Requests:

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
    def get_members_prototype():
        pass
