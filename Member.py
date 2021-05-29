import json
from datetime import datetime
import re
from dateutil.relativedelta import relativedelta


class Member:
    id = 0
    firstName = ''
    lastName = ''
    age = 0
    sex = ''

    city = ''

    university = ''
    graduation = 0
    faculty = ''
    gradYear = ''  # far/this/next

    employed = False

    isITSpec = False
    iTMetrics = {}
    iTScore = 0

    def __init__(self, raw_member):
        self.city = ''
        self.university = ''
        self.graduation = 0
        self.faculty = ''
        self.gradYear = ''  # far/this/next
        self.employed = False
        self.isITSpec = False
        self.iTMetrics = {}
        self.iTScore = 0

        self.id = raw_member['id']
        self.firstName = raw_member['first_name']
        self.lastName = raw_member['last_name']
        self.sex = raw_member['sex']
        if 'bdate' in raw_member and len(raw_member['bdate']) > 6:
            bdate = datetime.strptime(raw_member['bdate'], '%d.%m.%Y')
            cur_date = datetime.today()
            self.age = relativedelta(cur_date, bdate).years

        if 'city' in raw_member:
            self.city = raw_member['city']['title']

        if 'university_name' in raw_member:
            if 'university_name' != '':
                self.university = raw_member['university_name']
            if 'graduation' != 0:
                self.graduation = raw_member['graduation']
            if 'faculty' != '':
                self.faculty = raw_member['faculty_name']

        if 'career' in raw_member:
            career_list = list(raw_member['career'])
            if len(career_list) != 0:
                if isinstance(career_list, list):
                    career_list = list(career_list)
                if 'until' not in career_list[-1]:
                    self.employed = True

        self.set_grad_year()
        self.calc_it_score()

    def set_grad_year(self):
        cur_date = datetime.today()
        if self.graduation == 0:
            return

        if cur_date.month < 6 and self.graduation == cur_date.year:
            self.gradYear = 'this'
            return

        if self.graduation == cur_date.year+1:
            self.gradYear = 'next'
            return

        self.gradYear = 'far'

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
        self.iTMetrics['faculty'] = 0

        if self.is_it_faculty():
            self.iTMetrics['faculty'] = 10
            self.iTScore += 10

    def encode(self):
        return self.__dict__
