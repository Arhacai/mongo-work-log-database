import pymongo
from pymongo import MongoClient

import utils

client = MongoClient()
db = client.worklog
db.tasks.create_index([
    ('employee', pymongo.ASCENDING),
    ('title', pymongo.TEXT),
    ('notes', pymongo.TEXT)
])


class Task:

    def __init__(self, task_id):
        try:
            self.task = db.tasks.find_one({'_id': task_id})
            if not self.task:
                raise IndexError
        except IndexError:
            print("Sorry, there is no tasks with that id")

    @classmethod
    def all(cls):
        return [Task(entry['_id']) for entry in db.tasks.find()]

    @classmethod
    def employees(cls):
        return list(set([task.task['employee'] for task in Task.all()]))

    @classmethod
    def create(cls, **kwargs):
        task_id = db.tasks.insert_one(kwargs).inserted_id
        return Task(task_id)

    def show(self):
        utils.clear_screen()
        print(self.task['employee'].capitalize())
        print("=" * len(self.task['employee']))
        print("Date: {}".format(self.task['date'].strftime('%d/%m/%Y')))
        print("Task: {}".format(self.task['title']))
        print("Time spent: {} minutes".format(self.task['time']))
        if self.task.get('notes', False):
            print("Notes: {}".format(self.task['notes']))
        print()

    def edit(self):
        self.show()
        print("EDIT entry (Leave fields blank for no changes)")
        title = utils.get_title(self.task.get('title', ''))
        date = utils.get_date(self.task.get('date', ''))
        time = utils.get_time(self.task.get('time', ''))
        notes = utils.get_notes(self.task.get('notes', ''))

        db.tasks.update(
            self.task, {
                '$set': {
                    'title': title,
                    'date': date,
                    'time': time,
                    'notes': notes
                }
            }
        )
        self.task = db.tasks.find_one({'_id': self.task['_id']})
