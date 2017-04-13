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


    def randomly_allocate_office(self):
        """
            Helper function that allocates people randomly to an office in amity.

        """
        allocation_choice = choice(self.offices)
        return allocation_choice


    def randomly_allocate_ls(self):
        """
            Helper function that allocates people randomly to an office in amity.
        """
        allocation_choice = choice(self.livingspaces)
        return allocation_choice


    def check_if_offices_amity_full(self):
        """
            Helper function that checks to see if the offices in amity are full.

        """
        is_full = False
        count = 0

        while is_full is False:
            for office in self.offices:
                if office.num_of_persons == office.max_capacity:
                    count += 1
            if count != len(self.offices):
                return is_full

            elif count == len(self.offices):
                is_full = True
                return is_full

    def check_if_ls_amity_full(self):
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
                wants_accomodation : an optional argument that signifies whether a fellow wants
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
                all_full_office = Amity.check_if_offices_amity_full(self)
                if all_full_office is True:
                    return "All office spaces are full, Amity member cannot be added at this time."

                else:
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
                all_full_ls = Amity.check_if_ls_amity_full(self)
                all_full_office = Amity.check_if_offices_amity_full(self)
                
                if all_full_ls is True and all_full_office is True:
                    
                    return "All spaces are full, %s cannot be allocated at this time." % (name)

                elif all_full_ls is True:

                    self.allocations[name] = self.randomly_allocate_office()
                    office_allocation = self.allocations[name]
                    office_index = self.offices.index(office_allocation)
                    self.offices[office_index].num_of_persons += 1
                    self.offices[office_index].current_occupants.append(name)
                    
                    return  "%s has been allocated to %s." % (name, office_allocation.name)
                
                elif all_full_office is True:
                    self.allocations[name] = self.randomly_allocate_ls()
                    ls_allocation = self.allocations[name]
                    ls_index = self.livingspaces.index(ls_allocation)
                    self.livingspaces[ls_index].num_of_persons += 1
                    self.livingspaces[ls_index].current_occupants.append(name)
                    
                    return  "%s has been allocated to %s." % (name, ls_allocation.name)
                
                else:
                    self.allocations[name] = [self.randomly_allocate_office(),
                                            self.randomly_allocate_ls()]
                    office_allocation = self.allocations[name][0]
                    office_index = self.offices.index(office_allocation)
                    self.offices[office_index].num_of_persons += 1
                    self.offices[office_index].current_occupants.append(name)
                    ls_allocation = self.allocations[name][1]
                    ls_index = self.livingspaces.index(ls_allocation)
                    self.livingspaces[ls_index].num_of_persons += 1
                    self.livingspaces[ls_index].current_occupants.append(name)

                    return "%s has been allocated to %s and s/he can stay in %s." % \
                                                (name, office_allocation.name, ls_allocation.name)

    def load_people(self, file_name):
        with open(file_name, "r") as input_file:
            for line in input_file:
                string = line.split()
                name = string[0] + " " + string[1]
                role = string[2]
                if len(string)< 4:
                    print(self.add_person(name, role))  
                else:
                    wants_accomodation = string[3]
                    print(self.add_person(name, role, wants_accomodation))
    
    def print_allocations(self):
        
        for k,v in self.allocations.items():
            if isinstance(v, list):
                print("%s : %s , %s" % (k, v[0].name, v[1].name))
            else:
                print("%s : %s" % (k, v.name))

                     

    def reallocate_person(self):
        pass