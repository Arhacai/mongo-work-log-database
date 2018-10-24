import utils
import mongo


class TaskSearch:

    @classmethod
    def search_by_name(cls):
        employee = mongo.Employee(utils.get_search_name())
        entries = employee.get_tasks()
        return [mongo.Task(entry['_id']) for entry in entries]

    @classmethod
    def search_by_date(cls):
        """Search by Date of Task"""
        date = utils.get_search_date()
        entries = mongo.db.tasks.find({'date': date})
        return [mongo.Task(entry['_id']) for entry in entries]

    @classmethod
    def search_by_range(cls):
        """Search by Range of Dates"""
        start_date, end_date = utils.get_date_range()
        entries = mongo.db.tasks.find(
            {'date': {'$lt': end_date, '$gte': start_date}}
        )
        return [mongo.Task(entry['_id']) for entry in entries]

    @classmethod
    def search_by_time(cls):
        """Search by Time Spent"""
        time = utils.get_time()
        entries = mongo.db.tasks.find({'time': time})
        return [mongo.Task(entry['_id']) for entry in entries]

    @classmethod
    def search_by_term(cls):
        """Search by Search Term"""
        term = utils.get_term()
        entries = mongo.db.tasks.find(
            {
                '$or': [
                    {'title': {'$regex': term}},
                    {'notes': {'$regex': term}}
                ]
            }
        )
        return [mongo.Task(entry['_id']) for entry in entries]