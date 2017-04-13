"""Import Amity class from Amity file"""


class Room(object):

    """
    This class is a superclass of offices and living spaces, it is a subclass of Amity

    """
    def __init__(self, name):
        self.name = name
        self.num_of_persons = 0
        self.current_occupants = []
        self.is_full = False
        self.max_capacity = 0

    def check_room_is_full(self):
        """
            Blahblahblah
        """

        if self.num_of_persons == self.max_capacity:
            self.is_full = True
            return self.is_full


class Office(Room):

    """This class creates an instance of an office in amity, it's a subclass of Rooms"""

    def __init__(self, name):
        super(Office, self).__init__(name)
        self.max_capacity = 6



    def __str__(self):
        return self.name

class LivingSpace(Room):
    """This class creates an instance of an living space in amity, it's a subclass of Rooms"""

    def __init__(self, name):
        super(LivingSpace, self).__init__(name)
        self.max_capacity = 4

