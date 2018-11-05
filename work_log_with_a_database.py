"""
TechDegree: Python Web Developer
Project 4: work log with a data base
Date: Oct 2018
"""

import os
import sys
from peewee import *
from datetime import datetime

db = SqliteDatabase('log.db')

# use a list of tuples to keep menu choices
menu_add_search = [
	('a', 'Add A New Entry'),
	('l', 'Lookup Existing Entries'), 
	('q', 'Exit the Program')
	]

menu_search = [
	('1', 'Employee Name'),
	('2', 'Date'),
	('3', 'Time (minutes) Spent'),
	('4', 'Search Term'),
	('5', 'Exit lookup')
	]

#############################################################
##
##		help functions
##
###################################

class Task(Model):

	created_date = CharField(max_length = 20)  # will be YYYY-mm-dd string format in the database
	employee_name = CharField(max_length = 255)
	task_name = CharField(max_length = 255, unique = True)
	time_spent = FloatField()
	note = TextField()

	class Meta:
		database = db


def initialize():
	"""
	a help functiont to create a table if not existing
	"""
	#db.connect()
	db.create_tables([Task], safe = True)
	db.close()


def check_table():
	"""
	a help function to check if table exists
	"""
	try:
		db.connect()
		Task.select().count() # check if table task is available or not

	except:
		initialize()  # creat the table if it does not exist

	else:
		db.close()


def add_entry(employee, task, minutes, notes, table=Task):
	"""
	A help function to write task assoicated info into a database
	arg: employee, string
	     task, string, the name of a task 
	     minutes, int or decimal, minutes taken to complete a task 
	     notes, string, optional notes for the task
	     table, table name
	return: nothing, just insert data (employee, date, task, minutes, note) into a data base
	"""
	table.create(created_date = datetime.now().strftime('%Y-%m-%d'),
			     employee_name = employee,
			     task_name = task,
			     time_spent = minutes,
			     note = notes
			     )


def print_entries(rows):
	"""
	a help function to print log entry 
	arg: 
	return: does not return anything, just print
	"""
	length, idx = len(rows), 1
	for a_row in rows:
		print('\n{} of {} records'.format(idx, length))
		print('Created Date: {}'.format(a_row.created_date))
		print('Employee Name: {}'.format(a_row.employee_name))
		print('Task Name: {}'.format(a_row.task_name))
		print('Minutes Spent: {}'.format(a_row.time_spent))
		print('Optional Notes: {}'.format(a_row.note))
		idx += 1


def employee_list(table = Task):
	"""
	a help function to obtain all employee name in the table

	"""
	return set([row.employee_name for row in table.select()])


def date_list(table = Task):
	"""
	a help function to obtain all created date in the table
	"""
	return set([row.created_date for row in table.select()])


def select_employee(name, table = Task):
	"""
	a help function to select by employee
	"""
	results = table.select().where(table.employee_name == name)
	clear()

	print_entries(results)


def select_date(a_date, table = Task):
	"""
	a help function to select record by created date
	"""
	results = table.select().where(table.created_date == a_date)
	clear()

	print_entries(results)


def select_minutes(select_minute, table = Task):
	"""
	a help function to select time spend
	"""
	results = table.select().where(table.time_spent == select_minute)
	clear()

	if results:
		print_entries(results)
	else:
		print('No task has been completed by input {} minutes'.format(select_minute))


def select_term(term, table = Task):
	"""
	a help function to select by strings in task name or notes
	"""
	result1 = table.select().where(table.task_name.contains(term))
	result2 = table.select().where(table.note.contains(term))

	results = result1 + result2
	clear()

	if results:
		print_entries(results)
	else:
		print('No task has search term "{}" as provided.'.format(term))


def prompt_menu(menu):
	"""
	a help function to print menu
	arg: menu, a list of items to choose from
	return: nothing, just print onto the scrent
	"""
	for item in menu:
		print('{}) {}'.format(item[0], item[1]))


def clear():
	os.system('cls' if os.name == 'nt' else 'clear')


################################################
##
##	  running code
##
################################


if __name__ == '__main__':

	# check if table task exists
	check_table()

	# main loop
	while True:
		print('\nPlease Select')

		prompt_menu(menu_add_search)
		add_or_lookup = input('Your Choice: ').lower().strip()

		# add new entry
		if add_or_lookup == 'a':
			employee = input('Employee Name: ')
			task = input('Task Name: ')
			minute = float(input('Minutes spent to complete the task: '))
			notes = input('Optional notes: ')

			add_entry(employee, task, minute, notes)
			input('\nPress Enter to continue...')
			clear()

		# lookup 
		elif add_or_lookup == 'l':
			
			while True:
				clear()
				print('\nplease select a lookup method')
				prompt_menu(menu_search)
				lookup_choice = input('Your Choice: ').strip()

				if lookup_choice == '1':
					available_employee = employee_list(table = Task)

					while True:
						print('\nAvailable employee: {}'.format(available_employee))
						employee_choice = input('Employee Name: ')
						if employee_choice in available_employee:
							select_employee(employee_choice)
							break
						else:
							print('\nInvalid input, please re-enter employee\'s name')

				elif lookup_choice == '2':
					available_date = date_list(table = Task)

					while True:
						print('\nAvailable date {}'.format(available_date))
						date_choice = input('Select date in YYYY-MM-DD format: ')
						if date_choice in available_date:
							select_date(date_choice)
							break
						else:
							print('\nInvalid input, please re-enter created date')
							

				elif lookup_choice == '3':
					try:
						minute_choice = float(input('Select minutes to complete a task: '))
						select_minutes(minute_choice, table = Task)
					except ValueError:
						print('\nWrong type of value, has to be integers or decimals. Back to main menueand try again\n')
						continue

				elif lookup_choice == '4':
					term_choice = input('Enter a search term for task name or note lookup: ').lower().strip()
					select_term(term_choice)

				elif lookup_choice == '5':
					print('\nWish you have had a good lookup experience\n')
					break

				else:
					print('\nInvalid input, please select again')

				input('\nPress Enter to continue...')

		# neither add or search for entry, just exit
		elif add_or_lookup == 'q':
			print('\nBye\n')
			break
		
		# if select invalid choice 
		else:
			print('\nInvalid input, please select again')


