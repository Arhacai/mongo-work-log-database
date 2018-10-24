import pymongo
from pymongo import MongoClient

import utils

client = MongoClient()
db = client.worklog
db.employees.create_index([('name', pymongo.ASCENDING)], unique=True)
db.tasks.create_index([('title', pymongo.TEXT), ('notes', pymongo.TEXT)])


class Employee:

    def __init__(self, name):
        name = name.lower()
        self.employee = db.employees.find_one({'name': name})
        if not self.employee:
            result = db.employees.insert_one({'name': name})
            self.employee = db.employees.find_one({'_id': result.inserted_id})

    def get_id(self):
        return self.employee.get('_id', None)

    def get_name(self):
        return self.employee.get('name', '').title()

    @classmethod
    def get_employees(cls):
        return db.employees.find()

    def get_tasks(self):
        return db.tasks.find({'employee_id': self.get_id()})

    def edit(self):
        name = utils.get_name(self.get_name())
        db.employees.update(self.employee, {'name': name})
        self.employee = db.employees.find_one({'name': name})


class Task:

    def __init__(self, task_id):
        try:
            self.task = db.tasks.find_one({'_id': task_id})
            if not self.task:
                raise IndexError
        except IndexError:
            print("Sorry, there is no tasks with that id")
        else:
            self.employee = self.get_employee()

    def get_employee_id(self):
        return self.task.get('employee_id', None)

    def get_employee(self):
        employee = db.employees.find_one({'_id': self.get_employee_id()})
        return Employee(employee['name'])

    @classmethod
    def create(cls, **kwargs):
        task_id = db.tasks.insert_one(kwargs).inserted_id
        return Task(task_id)

    def show(self):
        utils.clear_screen()
        print(self.employee.get_name())
        print("=" * len(self.employee.employee['name']))
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
