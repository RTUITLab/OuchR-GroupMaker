from datetime import datetime
import re


class Member:
    id = 0
    first_name = ''
    last_name = ''
    age = 0

    country = ''
    city = ''

    university = ''
    graduation = ''
    faculty = ''

    company = ''
    position = ''

    it_metrics = {}
    it_score = 0

    def __init__(self, raw_member):
        self.id = raw_member['id']
        self.first_name = raw_member['first_name']
        self.last_name = raw_member['last_name']

        if 'country' in raw_member:
            self.country = raw_member['country']['title']

        if 'city' in raw_member:
            self.city = raw_member['city']['title']

        if 'university_name' in raw_member:
            self.university = raw_member['university_name']
            self.graduation = raw_member['graduation']
            self.faculty = raw_member['faculty_name']

        if 'career' in raw_member:
            career_list = list(raw_member['career'])
            if len(career_list) != 0:
                if isinstance(career_list, list):
                    career_list = list(career_list)
                if 'company' in career_list[-1]:
                    self.company = career_list[-1]['company']
                if 'position' in career_list[-1]:
                    self.position = career_list[-1]['position']
                if 'group_id' in career_list[-1]:
                    self.company = career_list[-1]['group_id']

        if 'bdate' in raw_member and len(raw_member['bdate']) > 6:
            bdate = datetime.strptime(raw_member['bdate'], '%d.%m.%Y')
            cur_date = datetime.today()
            self.age = cur_date - bdate

        self.calc_it_score()

    def get_param(self, param_name):
        if param_name == 'city':
            return self.city
        if param_name == 'university':
            return self.university
        if param_name == 'company':
            return self.company
        if param_name == 'position':
            return self.position

    def is_it_faculty(self):
        it_fac_patterns = [r'инженер',  # под вопросом
                           r'цифр',
                           r'информ',
                           r'безопас',
                           r'кибер',
                           r'автомат',
                           r'прог',
                           r'комп']
        for pattern in it_fac_patterns:
            if re.search(pattern, self.faculty, re.IGNORECASE):
                return True
        return False

    def calc_it_score(self):

        if self.is_it_faculty():
            self.it_metrics['faculty'] = 1