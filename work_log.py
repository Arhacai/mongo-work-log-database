import datetime

import pymongo

import utils

client = pymongo.MongoClient()
db = client.worklog
db.tasks.create_index([
    ('employee', pymongo.ASCENDING),
    ('title', pymongo.TEXT),
    ('notes', pymongo.TEXT)
])


class WorkLog:
    """WorkLog is a terminal application for logging what work someone did on a
    certain day. It holds a list of tasks, let the user to add, edit or delete
    any of them aswell several ways to search through the tasks. It stores this
    info on a mongo database.
    """

    @classmethod
    def add_task(cls):
        """Add new entry"""
        new_task = {
            "employee": utils.get_name(),
            "title": utils.get_title(),
            "date": datetime.datetime.now(),
            "time": utils.get_time(),
            "notes": utils.get_notes()
        }
        db.tasks.insert_one(new_task)
        cls.show_task(new_task)
        input("The entry has been added. Press enter to return to the menu")

    @classmethod
    def edit_task(cls, task):
        """Edit entry"""
        cls.show_task(task)
        print("EDIT entry (Leave fields blank for no changes)")
        title = utils.get_title(task.get('title', ''))
        date = utils.get_date(task.get('date', ''))
        time = utils.get_time(task.get('time', ''))
        notes = utils.get_notes(task.get('notes', ''))
        updated = {'title': title,'date': date, 'time': time, 'notes': notes}
        db.tasks.update(
            task, {
                '$set': updated
            }
        )
        return updated

    @classmethod
    def delete_task(cls, task):
        """Delete a task for the user selected."""
        answer = input("Do you really want to delete this task? [y/N]: ")
        if answer.lower() == 'y':
            db.tasks.delete_one({'_id': task['_id']})
            return True
        return False

    @staticmethod
    def show_task(task):
        utils.clear_screen()
        print(task['employee'].capitalize())
        print("=" * len(task['employee']))
        print("Date: {}".format(task['date'].strftime('%d/%m/%Y')))
        print("Task: {}".format(task['title']))
        print("Time spent: {} minutes".format(task['time']))
        if task.get('notes', False):
            print("Notes: {}".format(task['notes']))
        print()


if __name__ == '__main__':
    from menu import MainMenu
    MainMenu().run()