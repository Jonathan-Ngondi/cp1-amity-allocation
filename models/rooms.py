"""Import Amity class from Amity file"""
from amity import Amity

class Rooms(Amity):
    """This class is a superclass of offices and living spaces, it is a subclass of Amity"""

    def __init__(self):
        Amity.__init__(self)
        self.max_capacity = 0
        self.all_rooms = {"Cotonou":"O"}

    def create_room(self, room_type, room_name):
        """This method creates a room in Amity"""
        if room_name in self.all_rooms:
            return "This room already exists in Amity."
        else:
            self.all_rooms.update({room_name:room_type})
            if room_type == 'o' or room_type == 'O':
                return "New office space "+str(room_name)+" has been successfully created."
            elif room_type == 'l' or room_type == 'L':
                return "The living space ${} has been successfully created in Amity.".format(room_name)
            else:
                return "You have entered an invalid room type! Please try again."



class Office(Rooms):
    """This class creates an instance of an office in amity, it's a subclass of Rooms"""

    def __init__(self):
        Rooms.__init__(self)
        self.max_capacity = 6

class LivingSpace(Rooms):
    """This class creates an instance of an living space in amity, it's a subclass of Rooms"""

    def __init__(self):
        Rooms.__init__(self)
        self.max_capacity = 4

