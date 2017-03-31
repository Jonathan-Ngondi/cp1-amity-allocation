import random
from amity import Amity
from rooms import Rooms , Office

class Person(Amity):


    def __init__(self):
        Amity.__init__(self)
        self.all_people={}
        self.allocations_people=[]
        self.office = Office()
        self.all_rooms = self.office.all_rooms

    def add_person(self, person_name, person_type, accomodation='N'):
        self.all_people.update({person_name:person_type})
        allocation = random.choice(self.all_rooms.keys())
        self.allocations_people.append({person_name: allocation})
        return person_name + " has been allocated to " + allocation + "."
        

    def reallocate_person(self, person_name, room_name):
        """This function re-allocates a person a room in Amity."""
        self.allocations_people.append({person_name:room_name})
        return self.allocations_people
        
    def load_file(self, file_name):
        # """This function loads people's names into Amity and adds them accordingly."""
        # with open(file_name,"r") as 
        # names 
        pass



class Staff(Person):

    def __init__(self):
        pass

class Fellow(Person):

    def __init__(self):
        pass
