""" """
from random import randint


class Person(object):
    """


    """
    def __init__(self, name):
        self.name = name


class Staff(Person):
    """


    """

    def __init__(self, employee_id, name):
        super(Staff, self).__init__(name)
        self.employee_id = employee_id
        self.is_allocated = "No"

    def __str__(self):
        return self.name


class Fellow(Person):
    """


    """

    def __init__(self, employee_id, name):
        super(Fellow, self).__init__(name)
        self.employee_id = employee_id
        self.is_allocated = False
    

    def __str__(self):
        return self.name
