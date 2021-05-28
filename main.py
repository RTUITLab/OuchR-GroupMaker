import requests as r
import json


# Only for 1000 members!
def get_members():

    request_params = {'v': 5.131,
                      'group_id': 'rosatomcareer',
                      'sort': 'id_asc',
                      'offset': 0,
                      'count': 1000,
                      'access_token': 'd9acf98cd9acf98cd9acf98c96d9de6273dd9acd9acf98c874aa57b9b6642522b5a44e4'
                      }

    res = r.get('https://api.vk.com/method/groups.getMembers', params=request_params)
    members_ids = res.json()['response']['items']

    return members_ids


def convert_to_member_class(member_base_info):
    members = []


def get_member_base_info(members_ids):

    ids_json = json.dumps(members_ids)
    extra_fields = 'country,city,bdate,education'
    request_params = {'v': 5.131,
                      'user_ids': ids_json,
                      'access_token': 'd9acf98cd9acf98cd9acf98c96d9de6273dd9acd9acf98c874aa57b9b6642522b5a44e4',
                      'fields': extra_fields
                      }
    res = r.get('https://api.vk.com/method/users.get', params=request_params)
    member_base_info = res.json()



    return member_base_info


if __name__ == '__main__':
    members = get_members()
    get_member_base_info(members)
