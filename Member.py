from datetime import datetime
import re
from dateutil.relativedelta import relativedelta


class Member:
    id = 0
    first_name = ''
    last_name = ''
    age = 0
    sex = ''

    city = ''

    university = ''
    graduation = 0
    faculty = ''
    grad_year = ''  # far/this/next

    employed = False

    is_it_spec = False
    it_metrics = {}
    it_score = 0

    def __init__(self, raw_member):

        self.id = raw_member['id']
        self.first_name = raw_member['first_name']
        self.last_name = raw_member['last_name']
        self.sex = raw_member['sex']
        if 'bdate' in raw_member and len(raw_member['bdate']) > 6:
            bdate = datetime.strptime(raw_member['bdate'], '%d.%m.%Y')
            cur_date = datetime.today()
            self.age = relativedelta(cur_date, bdate).years

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
                if 'until' not in career_list[-1]:
                    self.employed = True

        self.calc_it_score()

    def get_param(self, param_name):
        if param_name == 'city':
            return self.city
        if param_name == 'university':
            return self.university

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