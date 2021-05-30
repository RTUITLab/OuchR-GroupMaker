import requests as r
import json
from Member import Member
from Requests import Requests
import datetime as dt


def get_members():
    request_params = {'v': 5.131,
                      'group_id': 'rosatomcareer',
                      'sort': 'id_desc',
                      'offset': 1000,
                      'count': 1000,
                      'access_token': 'd9acf98cd9acf98cd9acf98c96d9de6273dd9acd9acf98c874aa57b9b6642522b5a44e4'
                      }

    members_ids = Requests.get_members(request_params, 1000)
    return members_ids


def get_group_name(link):
    request_params = {'v': 5.131,
                      'group_ids': link,
                      'access_token': 'd9acf98cd9acf98cd9acf98c96d9de6273dd9acd9acf98c874aa57b9b6642522b5a44e4'
                      }
    res = r.get('https://api.vk.com/method/groups.getById', params=request_params).json()
    res = res['response'][0]['name']
    return res


def convert_to_member_class(member_base_info):
    new_members = []
    for m in member_base_info['response']:

        if 'is_closed' in m and m['is_closed'] is False \
                and 'bdate' in m and len(m['bdate']) > 6:
            new_member = Member(m)
            new_members.append(new_member)
    return new_members


def make_top(members, param):
    cnt_dict = {}
    for m in members:
        key = m.get_param(param)
        if key not in cnt_dict:
            cnt_dict[key] = 1
        else:
            cnt_dict[key] += 1
    top_dict = dict(sorted(cnt_dict.items(), key=lambda item: item[1], reverse=True))
    top_dict.pop('')
    return top_dict


def get_member_base_info(members_ids):
    ids_json = json.dumps(members_ids)
    extra_fields = 'country,city,bdate,education,career,sex'
    request_params = {'v': 5.131,
                      'user_ids': ids_json,
                      'access_token': 'd9acf98cd9acf98cd9acf98c96d9de6273dd9acd9acf98c874aa57b9b6642522b5a44e4',
                      'fields': extra_fields
                      }
    res = r.get('https://api.vk.com/method/users.get', params=request_params)
    member_base_info = res.json()

    return member_base_info


def get_one_user_info(member_id):
    extra_fields = 'country,city,bdate,education,career,sex'
    request_params = {'v': 5.131,
                      'user_ids': member_id,
                      'access_token': 'd9acf98cd9acf98cd9acf98c96d9de6273dd9acd9acf98c874aa57b9b6642522b5a44e4',
                      'fields': extra_fields
                      }
    res = r.get('https://api.vk.com/method/users.get', params=request_params).json()['response'][0]
    user = Member(res)

    career = ''
    if 'career' in res:
        for c in res['career']:
            if 'company' in c:
                career += c['company'] + ', '
            if 'position' in c:
                career += c['position'] + ', '
            if 'group_id' in c:
                career += get_group_name(c['group_id']) + ', '
    career = career[:-2]
    if user.bdate != '':
        dt.datetime.isoformat(user.bdate)

    data_to_return = {'bdate': user.bdate,
                      'university': user.university,
                      'faculty': user.faculty,
                      'career': career}
    return data_to_return


def calculate_it_specs(members):
    it_count = 0
    s = 0.0
    for m in members:
        s += float(m.iTScore)
    average = s / float(len(members))
    for m in members:
        if float(m.iTScore) >= average:
            it_count += 1
            m.isITSpec = True
    return it_count


def calculate_grads(members, year):
    grads_count = 0
    for m in members:
        if m.gradYear == year:
            grads_count += 1
    return grads_count


def execute():
    r_members = get_members()
    members_bi = get_member_base_info(r_members)
    r_members = convert_to_member_class(members_bi)
    city_stats = make_top(r_members, 'city')
    edu_stats = make_top(r_members, 'university')
    it_count = calculate_it_specs(r_members)
    this_year_count = calculate_grads(r_members, 'this')
    next_year_count = calculate_grads(r_members, 'next')
    data_to_send = {"membersCount": len(r_members),
                    "itCount": it_count,
                    "thisYearGrads": this_year_count,
                    "nextYearGrads": next_year_count,
                    "members": r_members,
                    "cityTop": city_stats,
                    "eduStats": edu_stats
                    }
    return data_to_send


if __name__ == '__main__':
    execute()
