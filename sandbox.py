from Requests import Requests
import main


def execute():
    Requests.load_token()
    members_info = Requests.get_member_info_proto()
    r_members = main.convert_to_member_class(members_info)
    city_stats = main.make_top(r_members, 'city')
    edu_stats = main.make_top(r_members, 'university')
    it_count = main.calculate_it_specs(r_members)
    this_year_count = main.calculate_grads(r_members, 'this')
    next_year_count = main.calculate_grads(r_members, 'next')
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
