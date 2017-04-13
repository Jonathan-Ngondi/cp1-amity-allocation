from random import randint, choice
from models.rooms import *
from models.person import *

class Amity(object):
    """
        Amity class is the main engine for room allocation in the Amity program.
        
        The main functionality of the program sits in this class;
        create_room : creates a room in amity.
        add_person : adds a person to amity and allocates them to a room.
        reallocate_person : reallocates a person to amity.
        print_allocated : prints the allocated people within the program.
        print_unallocated : prints the unallocated people within the program.
        load_people : loads people from a txt file into amity.
        save_state : saves the state of amity to a db.

     """

    def __init__(self):
        self.offices = []
        self.livingspaces = []
        self.rooms = {}
        self.staff = []
        self.fellows = []
        self.employees = []
        self.allocations = {}
    
    def create_room(self, room_type, room_name):
        """
            Create one of 2 types of rooms in Amity, a Living Space or an Office.

            Arguments:
                room_type : a str describing the type of room, 'OFFICE' or 'LIVING SPACE'
                room_name : a tuple describing the name of the room
        """
        
        if str(room_name) in self.rooms:
            return "That room has already been created."

        if room_type.upper() == "OFFICE" or room_type.upper() == "O":
            self.room_type = "O"
            self.office = Office(room_name)
            self.offices.append(self.office)
            return "An office space named %s has been created." % room_name

        elif room_type.upper() == "LIVINGSPACE" or room_type.upper() == "LS" or room_type.upper() == "L":
            self.room_type = "L"
            self.livingspace = LivingSpace(room_name)
            self.livingspaces.append(self.livingspace)
            return "A living space named %s has been created." % room_name

        else:
            return "Invalid room type input."

    @staticmethod
    def randomly_allocate_office():
        """
            Helper function that allocates people randomly to an office in amity.
        
        """
        all_full = Amity.check_if_offices_amity_full(self)
        if all_full is True:
            return "All offices are full, Amity member cannot be added at this time."
        elif all_full is False:
            allocation_choice = choice(self.offices)
            return allocation_choice

    @staticmethod        
    def randomly_allocate_ls():
        """
            Helper function that allocates people randomly to an office in amity.
        
        """

        all_full = Amity.check_if_ls_amity_full(self)
        if all_full is True:
            return "All living spaces are full, Amity member cannot be added at this time."
        elif all_full is False:
            allocation_choice = choice(self.livingspaces)
            return allocation_choice

    @staticmethod        
    def check_if_offices_amity_full():
        """
            Helper function that checks to see if the offices in amity are full.
        
        """
        is_full = False
        count = 0

        while is_full is False:
            for office in self.offices:
                if office.num_of_persons == office.max_capacity:
                    count+=1
            if count != len(self.offices):
                return is_full
                break
            elif count == len(self.offices):
                is_full = True
                return is_full
    
    @staticmethod            
    def check_if_ls_amity_full():
        """
            Helper function that checks to see if the living spaces in amity are full.
        
        """

        is_full = False
        count = 0

        while is_full is False:
            for space in self.livingspaces:
                if space.num_of_persons == space.max_capacity:
                    count += 1
            if count != len(self.livingspaces):
                return is_full
            elif count == len(self.livingspaces):
                is_full = True
            return is_full

    def add_person(self, name, role, wants_accomodation=None):
        """
            Adds a person to Amity and allocates them randomly to an office space or if required
            a living space. 

            Arguments:
                name : this is the person's name
                role : this argument specifies whether they are a Fellow or Staff member
                wants_accomodation : this is an optional argument that signifies whether a fellow wants 
                                     accomodation or not.
        """
        employee_id = randint(1000, 9999)
        if role.upper() == "STAFF":
            wants_accomodation = "N"
            self.new_staff = Staff(employee_id, name)
            self.staff.append(self.new_staff)
            self.employees.append(self.new_staff)
            self.allocations[name] = self.randomly_allocate_office()
            office_allocation = self.allocations[name]
            office_index = self.offices.index(office_allocation)
            self.offices[office_index].num_of_persons += 1
            self.offices[office_index].current_occupants.append(name)

            return  "%s has been allocated to %s." % (name, office_allocation.name)
        if role.upper() == "FELLOW":
            if wants_accomodation == "N" or wants_accomodation == None:
                self.new_staff = Fellow(employee_id, name)
                self.fellows.append(self.new_staff)
                self.employees.append(self.new_staff)
                self.allocations[name] = self.randomly_allocate_office()
                office_allocation = self.allocations[name]
                office_index = self.offices.index(office_allocation)
                self.offices[office_index].num_of_persons += 1
                self.offices[office_index].current_occupants.append(name)
                return  "%s has been allocated to %s." % (name, office_allocation.name)
            elif wants_accomodation == "Y":
                self.new_staff = Fellow(employee_id, name)
                self.fellows.append(self.new_staff)
                self.employees.append(self.new_staff)
                self.allocations[name] = [self.randomly_allocate_office(), self.randomly_allocate_ls()]
                office_allocation = self.allocations[name][0]
                office_index = self.offices.index(office_allocation)
                self.offices[office_index].num_of_persons += 1
                self.offices[office_index].current_occupants.append(name)
                ls_allocation = self.allocations[name][1]
                ls_index = self.livingspaces.index(ls_allocation)
                self.livingspaces[ls_index].num_of_persons +=1
                self.livingspaces[ls_index].current_occupants.append(name)
        
                return "%s has been allocated to %s and he can stay in %s." % (name, office_allocation.name, ls_allocation.name)

    def reallocate_person(self):
        pass