import os
import itertools
from random import randint, choice
from models.rooms import *
from models.person import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models.db import *

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
        self.rooms = []
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
        
        if ''.join(room_name).isalpha()==False:
            return "The room name needs to be made up of L-E-T-T-E-R-S."

        for object in self.rooms:
            if object.name == room_name:
                return "What you doin' bana? That room has already been created."

        if room_type.upper() == "OFFICE" or room_type.upper() == "O":
            self.room_type = "O"
            self.office = Office(room_name)
            self.offices.append(self.office)
            self.rooms.extend(self.offices)
            return "An office space named %s has been created." % room_name

        elif room_type.upper() == "LIVINGSPACE" or room_type.upper() == "LS" or room_type.upper() == "L":
            self.room_type = "L"
            self.livingspace = LivingSpace(room_name)
            self.livingspaces.append(self.livingspace)
            self.rooms.extend(self.livingspaces)
            return "A living space named %s has been created." % room_name

        else:
            return "Ain't no such type of room as what you typed."

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
        if ''.join(name.split()).isalpha()==False:
            return  "People's names need to be spelt with L-E-T-T-E-R-S!"
        employee_id = randint(1000, 9999)

        if role.upper() == "STAFF":
            if self.offices == []:
                new_staff = Staff(employee_id, name)
                self.staff.append(new_staff)
                self.employees.append(new_staff)

              
                return "%s has been added but there are no rooms created in Amity, create a room and reallocate the new member." % (name)
                
            else:

                wants_accomodation = "N"
                new_staff = Staff(employee_id, name)
                self.allocations[name] = self.randomly_allocate_office()
                office_allocation = self.allocations[name]
                office_index = self.offices.index(office_allocation)
                self.offices[office_index].num_of_persons += 1
                self.offices[office_index].current_occupants.append(name)
                new_staff.is_allocated = True
                self.staff.append(new_staff)
                self.employees.append(new_staff)


                return "%s has been allocated to %s." % (name, office_allocation.name)

        if role.upper() == "FELLOW":
            if self.offices == []:

                new_fellow = Fellow(employee_id, name)
                self.fellows.append(new_fellow)
                self.employees.append(new_fellow)

                return "%s has been added but there are no rooms created in Amity,\n create a room and reallocate the new member." % (name)
            else:

                if wants_accomodation == "N" or wants_accomodation == None:

                    new_fellow = Fellow(employee_id, name)
                    self.fellows.append(new_fellow)
                    self.employees.append(new_fellow)
                    all_full_office = Amity.check_if_offices_amity_full(self)
                    if all_full_office is True:
                        return "All office spaces are full, Amity member cannot be added at this time."

                    else:
                        self.allocations[name] = self.randomly_allocate_office()
                        office_allocation = self.allocations[name]
                        office_index = self.offices.index(office_allocation)
                        self.offices[office_index].num_of_persons += 1
                        self.offices[office_index].current_occupants.append(name)
                        new_fellow.is_allocated = True

                        return "%s has been allocated to %s." % (name, office_allocation.name)

                elif wants_accomodation == "Y":

                    new_fellow = Fellow(employee_id, name)
                    self.fellows.append(new_fellow)
                    self.employees.append(new_fellow)
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

                        return "%s has been allocated to %s." % (name, office_allocation.name)

                    elif all_full_office is True:
                        self.allocations[name] = self.randomly_allocate_ls()
                        ls_allocation = self.allocations[name]
                        ls_index = self.livingspaces.index(ls_allocation)
                        self.livingspaces[ls_index].num_of_persons += 1
                        self.livingspaces[ls_index].current_occupants.append(name)

                        return "%s has been allocated to %s." % (name, ls_allocation.name)

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
                        new_fellow.is_allocated = True

                        return "%s has been allocated to %s and s/he can stay in %s." % (name, office_allocation.name, ls_allocation.name)

    def load_people(self, file_name):
        dir_path = os.path.dirname(__file__)
        file_path = os.path.join(dir_path, file_name + '.txt')
        with open(file_path, "r") as input_file:
            for line in input_file:
                string = line.split()
                name = string[0] + " " + string[1]
                role = string[2]
                if len(string) < 4:
                    print(self.add_person(name, role))
                else:
                    wants_accomodation = string[3]
                    print(self.add_person(name, role, wants_accomodation))

    def print_allocations(self):

        for k, v in self.allocations.items():
            if isinstance(v, list):
                print("%s : %s , %s" % (k, v[0].name, v[1].name))
            else:
                print("%s : %s" % (k, v.name))

    def reallocate_person(self, name, room_name):
        if isinstance(self.search_rooms(room_name), str):
            return "That room does not exist."
        else:
            self.remove_person_from_room(name)
            room = self.search_rooms(room_name)
            self.allocations[name] = room
            room.current_occupants.append(name)
            room.num_of_persons += 1

    def search_rooms(self, room_name):
        self.rooms = self.offices + self.livingspaces

        for room in self.rooms:
            try:
                if room.name == room_name:
                    return room
            except:
                return "Room not found."

    def remove_person_from_room(self, name):
        
        for office in self.offices:
            if name in office.current_occupants:
               
                office.current_occupants.remove(name)
                office.num_of_persons -= 1
            else:
                continue
                

        for ls in self.livingspaces:
            if name in ls.current_occupants:
                ls.current_occupants.remove(name)
                ls.num_of_persons -= 1

    def print_allocated(self):
        rooms = self.offices + self.livingspaces
        for space in rooms:
            print(space.name.upper())
            print("-"*35)
            print("")
            print((space.current_occupants))

    def print_unallocated(self):
        for member in self.employees:
            if member.name not in self.allocations:
                print(member.name)
    
    def save_state(self, filename='amity'):
          self.rooms = self.offices + self.livingspaces
          create_db()
          Session = sessionmaker()
          engine = create_engine('sqlite:///'+filename+'.db')
          Session.configure(bind=engine)
          session = Session()
          for person in self.employees:
              id_number = person.employee_id
              name = person.name
              allocation_status = person.is_allocated
              person_details = Person(id_number, name, allocation_status)
              person_list = session.query(Person).all()
              person_check = [item.id_number for item in person_list]
              if (id_number) in person_check:
                  session.query(Person).filter(Person.id == id_number).update\
                  ({'allocation_status': allocation_status})
              else:
                  session.add(person_details)

          for room in self.rooms:
              room_name = room.name
              max_capacity = room.max_capacity
              current_occupants = ', '.join(room.current_occupants)
              room_details = Room(room_name, current_occupants, max_capacity)
              room_list = session.query(Room).all()
              room_check = [item.room_name for item in room_list]
              if (room_name) in room_check:
                  session.query(Room).filter(Room.room_name == room_name).update\
                  ({'current_occupants': current_occupants})
              else:
                  session.add(room_details)

          session.commit()
          return "Data has been successfully saved to %s!" % filename

    def load_state(self, filename):
        import pdb;pdb.set_trace()
        create_db()
        Session = sessionmaker()
        self.engine = create_engine('sqlite:///'+filename+'.db')
        Session.configure(bind=self.engine)
        session = Session()
        
        person_data = session.query(Person).all()
        room_data = session.query(Room).all()
        

        for record in person_data:
             pass

    #     if filename.endswith('.db'):
    #         pass
    #     else:
    #         filename = 'amity.db'

    #     self.database = SqlDatabase(filename)
    #     for office in self.offices:
    #         office_data = Room(
    #                 room_name = office.name,
    #                 max_capacity = office.max_capacity,
    #                 occupants = office.current_occupants
    #         )
    #         self.database.session.add(office_data)
    #     self.database.close()
        # for person in self.employees:
           
        #     if isinstance(person, Fellow):
        #         self.role = "Fellow"
        #     else:
        #         self.role = "Staff"
        #     import pdb; pdb.set_trace()
        #     db_record = People(
        #          name = person.name,
                 
        #          id = (person.employee_id, ForeignKey),
        #          is_allocated = person.is_allocated,
        #          role = self.role
        #                 )
        #     self.Sqldatabase.session.add(db_record)
     
    

    def load_state(self):
        pass