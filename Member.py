class Member:
    id = 0
    first_name = ''
    last_name = ''
    age = 0
    country = ''
    city = ''
    university = ''
    graduation = ''

    def __init__(self, raw_member):
        self.id = raw_member['id']
        self.first_name = raw_member['first_name']
        self.last_name = raw_member['last_name']
        self.country = raw_member['country']['title']
        self.city = raw_member['city']['title']
        self.university = raw_member['university']['title']

        date_str = raw_member['bdate']