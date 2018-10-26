import utils
from work_log import db


class TaskSearch:

    @classmethod
    def search_by_name(cls):
        employee = utils.get_search_name()
        entries = db.tasks.find({'employee': employee})
        return [entry for entry in entries]

    @classmethod
    def search_by_date(cls):
        """Search by Date of Task"""
        date = utils.get_search_date()
        entries = db.tasks.find({'date': date})
        return [entry for entry in entries]

    @classmethod
    def search_by_range(cls):
        """Search by Range of Dates"""
        start_date, end_date = utils.get_date_range()
        entries = db.tasks.find(
            {'date': {'$lt': end_date, '$gte': start_date}}
        )
        return [entry for entry in entries]

    @classmethod
    def search_by_time(cls):
        """Search by Time Spent"""
        time = utils.get_time()
        entries = db.tasks.find({'time': time})
        return [entry for entry in entries]

    @classmethod
    def search_by_term(cls):
        """Search by Search Term"""
        term = utils.get_term()
        entries = db.tasks.find(
            {
                '$or': [
                    {'title': {'$regex': term}},
                    {'notes': {'$regex': term}}
                ]
            }
        )
        return [entry for entry in entries]
