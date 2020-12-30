# Copyright © 2020 Nikita Gusev.
# All rights reserved.
# Contacts: <sheihe24gn@gmail.com>

from datetime import date
import codecs
import calendar


class Teacher(object):
    loop = True
    ''' Create instance of a teacher for salary calculations
    vage: cost per lesson for a given teacher
    days: list of days when lessons were conducted
    salary: cost for lessons for a given teacher
    extra_work: additional work cost
    total: total cost including salary and 
    '''
    def __init__(self, name: str, vage: int):
        self.name = name
        self.vage = vage
        self.days = []
        self.salary = 0
        self.extra_work = 0
        self.total = 0
        print()
        print(f'Преподаватель {self.name}, ставка {self.vage}\n')

    def __repr__(self):
        print(f'Преподаватель {self.name}, ставка {self.vage}\n')

    def options(self):
        ''' Main teacher function, gives options for salary calculation'''
        while self.loop:
            print('МЕНЮ >>>\n')
            print('1. Добавить дни занятий\n2. Добавить занятость\n3. Удалить дни занятий\n'
                  '4. Отобразить дни занятий\n5. Посчитать ЗП\n6. Закончить')
            option = int(input())
            if option == 1:
                self.add_days()
            elif option == 2:
                self.add_work()
            elif option == 3:
                self.remove_days()
            elif option == 4:
                self.show_days()
            elif option == 5:
                self.count_salary()
            elif option == 6:
                self.report()
                self.loop = False
            else:
                print('Неверная опция!\n')

    def add_days(self):
        ''' Takes str of days as input and adds it into internal arr.
        Logs calendar in console'''
        today = date.today()
        year = today.year
        month = today.month
        print()
        print(calendar.month(year, month))
        while True:
            dates = input('Введите дни занятий в одну строку через пробел: ').strip().split(' ')
            if self.check_dates(dates):
                break
        self.days += dates
        days = ' '.join(self.days)
        print()
        print(f'Преподавателю {self.name} добавлены дни занятий: {days}\n')

    @staticmethod
    def check_dates(arr):
        ''' Checks if all dates in a given array are numbers and < 32'''
        try:
            if all([int(i) < 32 for i in arr]):
                return True
            else:
                print('Необходимо указать корректные даты\n')
        except ValueError:
            print('Необходимо указать корректные числовые значения\n')

    def show_days(self):
        ''' Shows lesson days'''
        days = ' '.join(self.days)
        print()
        print(f'Дни занятий: {days}\n')

    def count_salary(self):
        ''' Counts total salary for the teacher'''
        if not self.salary:
            salary = self.vage * len(self.days)
            self.salary += salary
        self.total = self.salary + self.extra_work
        print()
        print(f'ЗП: {self.total}\n')

    def add_work(self):
        ''' Adds optional work and its cost to total salary'''
        print('Дополнительная занятость >>>\n ')
        work = input('Название занятости: ')
        # Check for correct input data type: number
        while True:
            vage = input('Оплата: ')
            if check_int(vage):
                break
        # Check for correct input data type: number
        while True:
            count = input('Количество: ')
            if check_int(count):
                break

        self.extra_work += int(vage) * int(count)
        print()
        print(f'Преподавателю {self.name} добавлена занятость {work}\n')

    def remove_days(self):
        ''' Removes days from list of days'''
        print('Удаление занятий >>>\n')
        rem_days = input('Введите через пробел дни, которые нужно удалить: ').strip().split(' ')
        for rem_day in rem_days:
            for day in self.days:
                if rem_day == day:
                    self.days.remove(day)
        # Showing remnant days from list of days
        self.show_days()

    def report(self):
        ''' Automatically logs info to file '''
        with codecs.open('log.txt', 'a', 'utf-8') as log:
            data = f'Дата: {str(date.today())}\n' \
                   f'Учитель {self.name}, ставка {self.vage}\n' \
                   f'Дни занятий: {self.days}\n' \
                   f'ЗП: {self.total}\n\n'
            log.write(data)
            print()
            print('Отчёт добавлен в log.txt\n')


def main():
    print()
    print('Программа для расчёта заработной платы, версия 1.0\n'
          'Разработано Sheihesinusslon для WakeUpSpb\n\n')
    number_of_teachers = input('Количество преподавателей: ')
    # Check for valid input data type for param: number_of_teachers
    while number_of_teachers not in '0123456789':
        print('Необходимо указать число\n')
        number_of_teachers = input('Количество преподавателей: ')
    # Create teacher instances for all teachers one by one
    for i in range(int(number_of_teachers)):
        create_teacher()


def create_teacher():
    ''' Creates Teacher instances, asks for args from user'''
    name = input('Имя преподавателя: ')
    # Check for valid input data type for param: vage
    while True:
        vage = input('Ставка: ')
        if check_int(vage):
            break

    # Create an instance with a given args and start loop
    t = Teacher(name, int(vage))
    t.options()


def check_int(inp):
    ''' Checks in a given input param a number'''
    try:
        inp = int(inp)
        return True
    except ValueError:
        print('Необходимо ввести число')


if __name__ == '__main__':
    main()
