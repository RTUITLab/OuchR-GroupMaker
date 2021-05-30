import requests as r
import json
from Member import Member
from Requests import Requests
import datetime as dt


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
        if key != '':
            if key not in cnt_dict:
                cnt_dict[key] = 1
            else:
                cnt_dict[key] += 1
    top_dict = dict(sorted(cnt_dict.items(), key=lambda item: item[1], reverse=True))
    top_list = []
    for td in top_dict:
        new_list = [td, top_dict[td]]
        top_list.append(new_list)

    top_list = top_list[:10]

    return top_list


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


def calc_it_grads(members):
    count = 0
    for m in members:
        if m.gradYear == 'this' and m.isITSpec:
            count += 1
    return count


def calculate_grads(members, year):
    grads_count = 0
    for m in members:
        if m.gradYear == year:
            grads_count += 1
    return grads_count


def calc_membership_score(members):
    pass


def make_age_clusters(members):
    age_clusters = {
        'до 18': 0,
        '18-21': 0,
        '21-24': 0,
        '24-27': 0,
        '27-30': 0,
        '30-40': 0,
        'от 40': 0
    }
    for m in members:
        age = m.age
        if age != 0:
            if age < 18:
                age_clusters['до 18'] += 1
            elif 18 <= age < 21:
                age_clusters['18-21'] += 1
            elif 21 <= age < 24:
                age_clusters['21-24'] += 1
            elif 24 <= age < 27:
                age_clusters['24-27'] += 1
            elif 27 <= age < 30:
                age_clusters['27-30'] += 1
            elif 30 <= age < 40:
                age_clusters['30-40'] += 1
            else:
                age_clusters['от 40'] += 1
    return age_clusters


def execute():
    Requests.load_token()

    members_dict = Requests.get_member_info_proto()
    members = convert_to_member_class(members_dict)

    city_stats = make_top(members, 'city')
    coords = [[55.7522200, 37.6155600],
              [59.9386300, 30.3141300],
              [56.3286700, 44.0020500],
              [56.8519000, 60.6122000],
              [56.4977100, 84.9743700],
              [47.5136100, 42.1513900],
              [55.0415000, 82.9346000],
              [54.9358300, 43.3235200],
              [55.7887400, 49.1221400],
              [55.0968100, 36.6100600]]
    city_list = []
    for i in range(len(city_stats)):
        new_dict = {'city': city_stats[i][0], 'count': city_stats[i][1], 'lat': coords[i][0], 'lng': coords[i][1]}
        city_list.append(new_dict)

    edu_stats = make_top(members, 'university')
    edu_list = []
    for i in range(len(edu_stats)):
        new_dict = {'university': edu_stats[i][0], 'count': edu_stats[i][1]}
        edu_list.append(new_dict)

    it_count = calculate_it_specs(members)
    this_year_count = calculate_grads(members, 'this')
    it_grads_count = calc_it_grads(members)
    age_clusters = make_age_clusters(members)

    data_to_send = {"membersCount": len(members),
                    "itCount": it_count,
                    "thisYearGrads": this_year_count,
                    "itGrads": it_grads_count,
                    "cityTop": city_list,
                    "eduStats": edu_list,
                    "ageClusters": age_clusters
                    }

    return data_to_send


if __name__ == '__main__':
    execute()
