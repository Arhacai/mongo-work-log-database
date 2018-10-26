import utils
from search import TaskSearch
from work_log import db, WorkLog


class Menu:

    options = []

    def print_title(self):
        """Main Menu header"""
        raise NotImplementedError()

    def print_options(self):
        """Prints the list of menu options"""
        for option in self.options:
            print(option)

    def print_menu(self):
        """Prints the whole menu on screen: Title and Options"""
        utils.clear_screen()
        self.print_title()
        self.print_options()

    def get_option(self):
        """
        Gets the user's choice. If its not in the list of keys from the
        option list, it displays an error and repeat again until a valid one
        is provided
        """
        while True:
            choice = input("> ")
            for option in self.options:
                if choice == option[0]:
                    return choice
            print("Sorry, you must choose a valid option")

    def run(self):
        """
        Display all info on screen, gets the user's choice and execute the
        option chosen. It keeps looping until quit option is selected.
        """
        raise NotImplementedError()


class MainMenu(Menu):

    def __init__(self):
        self.options = [
            'a) Add new entry',
            'b) Search in existing entries',
            'c) Quit program'
        ]

    def print_title(self):
        print("WORK LOG")
        print("What would you like to do?")

    def run(self):
        while True:
            self.print_menu()
            option = self.get_option()
            if option == 'a':
                WorkLog.add_task()
            if option == 'b':
                SearchMenu().run()
            if option == 'c':
                break


class SearchMenu(Menu, TaskSearch):

    def __init__(self):
        self.options = [
            'a) Employee Name',
            'b) Date of Task',
            'c) Range of Dates',
            'd) Time Spent',
            'e) Search Term',
            'f) Return to menu'
        ]

    def print_title(self):
        print("Do you want to search by:")

    def run(self):
        while True:
            self.print_menu()
            option = self.get_option()
            if option == 'a':
                tasks = self.search_by_name()
                TaskMenu(0, tasks).run()
            if option == 'b':
                tasks = self.search_by_date()
                TaskMenu(0, tasks).run()
            if option == 'c':
                tasks = self.search_by_range()
                TaskMenu(0, tasks).run()
            if option == 'd':
                tasks = self.search_by_time()
                TaskMenu(0, tasks).run()
            if option == 'e':
                tasks = self.search_by_term()
                TaskMenu(0, tasks).run()
            if option == 'f':
                break


class TaskMenu(Menu):

    options = [
        ('p', '[P]revious'),
        ('n', '[N]ext'),
        ('e', '[E]dit'),
        ('d', '[D]elete'),
        ('r', '[R]eturn'),
    ]

    def __init__(self, index=0, tasks=None):
        self.index, self.tasks, self.options = self.initialize(index, tasks)

    def initialize(self, index=0, tasks=None):
        """
        Initializes the menu with a proper options. By default, index is 0
        so the first task in the list is shown. If no tasks provided, this
        menu gets all tasks from the log and shows them. It also creates five
        menu options to show and operate with. Menu options are different
        depending on the index of the task shown, so options are changed
        on __init__ in each case.
        """
        if tasks is None:
            tasks = [entry for entry in db.tasks.find()]
        options = self.get_options(index, len(self.tasks))
        return index, tasks, options

    def get_options(self, index, length):
        """
        Return a list of available options to show in the menu depending
        on the index of the task and the length of tasks.
        """
        if length == 0:
            return [self.options[-1]]
        if index == 0:
            if length == 1:
                return self.options[2:]
            return self.options[1:]
        if index == length - 1:
            return [self.options[0]] + self.options[2:]
        if index >= length:
            raise IndexError("list index out of range")
        return self.options

    def print_title(self):
        if self.tasks:
            WorkLog.show_task(self.tasks[self.index])
            print("Result {} of {}\n".format(self.index + 1, len(self.tasks)))
        else:
            print("There are no tasks to show.\n")

    def print_options(self):
        print(', '.join([option[1] for option in self.options]))

    def run(self):
        while True:
            self.print_menu()
            option = self.get_option()
            if option == 'p':
                self.index -= 1
            if option == 'n':
                self.index += 1
            if option == 'e':
                edited = WorkLog.edit_task(self.tasks[self.index])
                self.tasks[self.index].update(edited)
            if option == 'd':
                if WorkLog.delete_task(self.tasks[self.index]):
                    self.tasks.remove(self.tasks[self.index])
                    if self.index > 1:
                        self.index -= 1
                    else:
                        self.index = 0
            if option == 'r':
                break
            self.initialize(self.index, self.tasks)
