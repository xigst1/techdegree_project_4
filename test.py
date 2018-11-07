"""
TechDegree: Python Web Developer
Project 4: work log with a data base -- unit test
Date: Oct 2018
"""

import unittest

import work_log_with_a_database as log



class TestLog(unittest.TestCase):

	def setUp(self):
		log.initialize()
		self.created_date = '2018-11-03'
		self.employee_name = 'max'
		self.task_name = 'playing'
		self.time_spent = 120.0
		self.note = 'tired'
		self.menu_add_search = log.menu_add_search
		self.menu_search = log.menu_search
		self.add_or_lookup = ['a', 'l', 'q']
		self.lookup_choice = ['1', '2', '3', '4', '5']


	def test_table(self):
		assert log.Task.table_exists()


	def test_createdate(self):
		row = log.Task.get(created_date = self.created_date)
		self.assertEqual(row.created_date, self.created_date)

	def test_employee(self):
		row = log.Task.get(employee_name = self.employee_name)
		self.assertEqual(row.employee_name, self.employee_name)

	def test_task(self):
		row = log.Task.get(task_name = self.task_name)
		self.assertEqual(row.task_name, self.task_name)

	def test_minutes(self):
		row = log.Task.get(time_spent = self.time_spent)
		self.assertEqual(row.time_spent, self.time_spent)

	def test_main_menu(self):
		size = len(self.menu_add_search)
		self.assertEqual(size, 3)


	def test_search_menu(self):
		size = len(self.menu_search)
		self.assertEqual(size, 5)



if __name__ == '__main__':
    unittest.main()

