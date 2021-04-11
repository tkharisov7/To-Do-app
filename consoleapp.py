from task import Task
from datetime import date
from os import system, name
from time import sleep
import re
import emoji


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


class ConsoleApp:
    undone_tasks_ = dict()
    done_tasks_ = dict()

    class Colors:
        OK = '\033[92m'  # GREEN
        WARNING = '\033[93m'  # YELLOW
        FAIL = '\033[91m'  # RED
        RESET = '\033[0m'  # RESET COLOR

    def __init__(self):
        self.undone_tasks_ = dict()
        self.done_tasks_ = dict()

    def __add_task(self):
        print("Write the task title.")
        new_task = Task()
        new_task.title_ = str(input())
        clear()
        while True:
            print("Write the task date in format <year>-<month>-<day>. (Example: '2002-3-26')")
            date_str = str(input())
            try:
                year, month, day = map(int, date_str.split('-'))
                new_task.date_ = date(year, month, day)
                # print(new_task.date_)
                clear()
                break
            except:
                print(self.Colors.FAIL + "Wrong format!!!" + self.Colors.RESET)
                sleep(1)
                clear()
                continue
        while True:
            print("Is it a frog?",
                  emoji.emojize(':frog:'), "(https://todoist.com/productivity-methods/eat-the-frog)")
            print("Yes/No?")
            is_frog = str(input())
            clear()
            if is_frog == "Y" or is_frog == "y" or re.search('yes', is_frog, re.IGNORECASE):
                new_task.is_frog_ = True
                break
            if is_frog == "N" or is_frog == "n" or re.search('no', is_frog, re.IGNORECASE):
                new_task.is_frog = False
                break
            print(self.Colors.FAIL + "Wrong format!!!" + self.Colors.RESET)
            sleep(1)
            clear()
        if not (new_task.date_ in self.undone_tasks_):
            self.undone_tasks_[new_task.date_] = []
        self.undone_tasks_[new_task.date_].append(new_task)

    def __current(self):
        current_index = 0
        while True:
            today = date.today()
            frogs = []
            usual = []
            print("Today is", today)
            if not (today in self.undone_tasks_):
                print(self.Colors.OK + "Hooray! No tasks for today! You can chill and enjoy your life."
                      + self.Colors.RESET)
                sleep(3)
                clear()
                break
            for i in range(current_index, len(self.undone_tasks_[today])):
                x = self.undone_tasks_[today][i]
                if x.is_frog_:
                    frogs.append(x)
                else:
                    usual.append(x)
            for i in range(0, current_index):
                x = self.undone_tasks_[today][i]
                if x.is_frog_:
                    frogs.append(x)
                else:
                    usual.append(x)
            undone_amount = len(frogs) + len(usual)
            all_amount = undone_amount + (len(self.done_tasks_[today]) if (today in self.done_tasks_) else 0)
            if undone_amount == 0:
                print(self.Colors.OK + "Congratulations! You have done all tasks for today!" + self.Colors.RESET)
                sleep(3)
                clear()
                break
            else:
                print(f'You have completed {all_amount - undone_amount} from {all_amount} tasks today. Good work!')
            if len(frogs) > 0:
                current_task = frogs[len(frogs) - 1]
            else:
                current_task = usual[len(usual) - 1]
            print("Current task:", self.Colors.OK + current_task.title_ + self.Colors.RESET)
            print("Is frog?", emoji.emojize(':frog:'), end="")
            if current_task.is_frog_:
                print(self.Colors.OK + " Yes" + self.Colors.RESET)
            else:
                print(self.Colors.FAIL + " No" + self.Colors.RESET)
            print("Type DONE if task is done.")
            print("Type SKIP if you want to skip the task.")
            print("Type RETURN if you want to return to the main menu.")
            x = str(input())
            if x.lower() != "done" and x.lower() != "skip" and x.lower != "return":
                print(self.Colors.FAIL + "Incorrect input! Please, try again." + self.Colors.RESET)
                sleep(1)
                clear()
                continue
            if x.lower() == "done":
                if not (today in self.done_tasks_):
                    self.done_tasks_[today] = []
                self.done_tasks_[today].append(current_task)
                self.undone_tasks_[today].remove(current_task)
                if not self.undone_tasks_[today]:
                    del self.undone_tasks_[today]
                clear()
                continue
            if x.lower() == "skip":
                if current_task.is_frog_:
                    print(self.Colors.FAIL + "You can't skip the frog!" + self.Colors.RESET)
                    sleep(1)
                    clear()
                    continue
                current_index += 1
                current_index %= len(self.undone_tasks_[today])
                clear()
                continue
            if x.lower() == "return":
                clear()
                break

    def __manage(self):
        find_date = date(2020, 1, 1)
        while True:
            print("Write the task date in format <year>-<month>-<day>. (Example: '2002-3-26')")
            date_str = str(input())
            try:
                year, month, day = map(int, date_str.split('-'))
                find_date = date(year, month, day)
                # print(new_task.date_)
                clear()
                break
            except:
                print(self.Colors.FAIL + "Wrong format!!!" + self.Colors.RESET)
                sleep(1)
                clear()
                continue
        if not (find_date in self.undone_tasks_):
            print(self.Colors.OK + "No tasks at this date" + self.Colors.RESET)
            sleep(1)
            clear()
            return
        current_tasks = self.undone_tasks_[find_date]
        while True:
            clear()
            if len(current_tasks) == 0:
                del self.undone_tasks_[find_date]
                print("No tasks left for today!")
                sleep(1)
                clear()
                return
            print("Tasks for", find_date)
            i = 0
            for task in current_tasks:
                i += 1
                print(str(i) + ")", task.title_, emoji.emojize(':frog:'), end="")
                if task.is_frog_:
                    print(self.Colors.OK + " Yes" + self.Colors.RESET)
                else:
                    print(self.Colors.FAIL + " No" + self.Colors.RESET)
            print("Type 'delete N', where the N is the number of task.")
            print("Type 'return' to return to the main menu.")
            s = str(input())
            if s.lower().find("return") > -1:
                clear()
                return
            try:
                s1, number = s.split(' ')
                number = int(number)
            except:
                print(self.Colors.FAIL + "Wrong format!!!" + self.Colors.RESET)
                sleep(1)
                continue
            if s1.lower() == "delete" and 1 <= number <= len(current_tasks):
                self.undone_tasks_[find_date].pop(number - 1)
                print(self.Colors.OK + "Task was successfully deleted." + self.Colors.RESET)
                sleep(1)
                continue
            print(self.Colors.FAIL + "Wrong format!!!" + self.Colors.RESET)
            sleep(1)

    def run(self):
        print("To-Do-app")
        while True:
            print("Choose what to do:")
            print("Type ADD to add task")
            print("Type CURRENT to open workspace")
            print("Type MANAGE to list all tasks available")
            print("Type EXIT to exit the app")
            x = input()
            clear()
            if x.lower() == "exit":
                break
            if x.lower() != "add" and x.lower() != "current" and x.lower() != "manage" and x.lower() != "exit":
                print(self.Colors.FAIL + "Incorrect input! Please, try again." + self.Colors.RESET)
                sleep(1)
                clear()
                continue
            if x.lower() == "add":
                self.__add_task()
                continue
            if x.lower() == "current":
                self.__current()
            if x.lower() == "manage":
                self.__manage()
