import datetime
import os

from work_log import db


def clear_screen():
    """Clear the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_name(initial=None):
    """Gets the name of the employee from user"""
    if not initial:
        clear_screen()
    while True:
        name = input("Employee's Name: ").lower().strip()
        if name != '':
            return name
        if initial:
            return initial
        print("Sorry, you must provide a name.\n")


def get_title(initial=None):
    """
    Gets a valid title from user. If no title provided, it returns
    the initial title or None.
    """
    if not initial:
        clear_screen()
    while True:
        title = input("Title of the task: ").strip()
        if title != '':
            return title
        if initial:
            return initial
        print("Sorrry, you must provide a task title")


def get_date(initial=None):
    """
    Gets a valid date from user. If no date provided, it returns
    the initial date or None.
    """
    if not initial:
        clear_screen()
    while True:
        print("Enter a date for the task")
        date = input("Please use DD/MM/YYYY: ")
        if date == '' and initial:
            return initial
        try:
            date = datetime.datetime.strptime(date, '%d/%m/%Y')
        except ValueError:
            print("Sorry, you must enter a valid date.\n")
        else:
            return date


def get_search_name():
    """Gets the name of the employee from user"""
    clear_screen()
    name_list = list(set([task['employee'] for task in db.tasks.find()]))
    print("List of employees:")
    print("==================")
    for name in name_list:
        print("- {}".format(name.capitalize()))
    while True:
        name = input("\nEmployee's Name: ").lower().strip()
        if name != '' and name in name_list:
            return name
        print("Sorry, you must enter a valid name.\n")


def get_search_date():
    """
    Gets a valid date from user. If no date provided, it returns
    the initial date or None.
    """
    clear_screen()
    date_list = [task['date'].strftime('%d/%m/%Y') for task in db.tasks.find()]
    print("Dates with tasks:")
    print("=================")
    for date in date_list:
        print("- {}".format(date))
    while True:
        print("Enter a date to view its entries")
        date = input("Please use DD/MM/YYYY: ")
        if date in date_list:
            date = datetime.datetime.strptime(date, '%d/%m/%Y')
            return date
        print("Sorry, you must enter a valid date.\n")


def get_date_range():
    """
    Gets a valid date from user. If no date provided, it returns
    the initial date or None.
    """
    clear_screen()
    while True:
        print("Enter the start date")
        start_date = input("Please use DD/MM/YYYY: ")
        try:
            start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
        except ValueError:
            print("Sorry, you must enter a valid date.\n")
        else:
            break

    while True:
        print("Enter the end date")
        end_date = input("Please use DD/MM/YYYY: ")
        try:
            end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')
        except ValueError:
            print("Sorry, you must enter a valid date.\n")
        else:
            return start_date, end_date


def get_time(initial=None):
    """
    Gets a valid time spent from user. If no time provided, it returns
    the initial time spent or None.
    """
    if not initial:
        clear_screen()
    while True:
        time = input("Time spent (rounded minutes): ")
        if time == '' and initial:
            return initial
        try:
            time = round(int(time))
            if time <= 0:
                raise ValueError
        except ValueError:
            print("Sorry, you must enter a valid numeric time")
        else:
            return time


def get_notes(initial=None):
    """
    Gets notes from user. If no notes provided, it returns the initial
    notes or None.
    """
    if initial is None:
        clear_screen()
    notes = input("Notes (Optional, you can leave this empty): ").strip()
    if notes:
        return notes
    if not initial:
        return ''
    answer = input("Do you want to keep actual notes? y/N ").lower()
    if answer == 'y':
        return initial
    return ''


def get_term():
    """Asks the user to provide a search term in tasks/notes and returns it"""
    clear_screen()
    term = input("Enter a string to search in task name or notes: ").strip()
    return term
