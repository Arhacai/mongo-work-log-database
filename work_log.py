import datetime

import models
import utils
from menu import MainMenu


class WorkLog:
    """WorkLog is a terminal application for logging what work someone did on a
    certain day. It holds a list of tasks, let the user to add, edit or delete
    any of them aswell several ways to search through the tasks. It stores this
    info on a database.
    """

    @classmethod
    def add_task(cls):
        """Add new entry"""
        employee = models.Employee(utils.get_name())
        new_task = {
            "employee_id": employee.get_id(),
            "title": utils.get_title(),
            "date": datetime.datetime.now(),
            "time": utils.get_time(),
            "notes": utils.get_notes()
        }
        task = models.Task.create(**new_task)
        task.show()
        input("The entry has been added. Press enter to return to the menu")

    @classmethod
    def edit_task(self, index, tasks):
        """Edit entry"""
        tasks[index].edit()
        return index

    @classmethod
    def delete_task(self, index, tasks):
        """Delete a task for the user selected."""
        answer = input("Do you really want to delete this task? [y/N]: ")
        if answer.lower() == 'y':
            models.db.tasks.delete_one({'_id': tasks[index].task['_id']})
            tasks.remove(tasks[index])
            if index > 1:
                return index - 1
            return 0
        return index


if __name__ == '__main__':
    MainMenu().run()