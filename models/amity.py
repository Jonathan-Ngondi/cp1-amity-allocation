import os
import itertools
from colorama import *
from random import randint, choice
from models.rooms import *
from models.person import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import db
from models.db import *

class Amity(object):
    """
        Amity class is the main engine for room allocation in the Amity program.

        The main functionality of the program sits in this class;
        create_room -- creates a room in amity.
        add_person -- adds a person to amity and allocates them to a room.
        reallocate_person -- reallocates a person to amity.
        print_allocated -- prints the allocated people within the program.
        print_unallocated -- prints the unallocated people within the program.
        load_people -- loads people from a txt file into amity.
        save_state -- saves the state of amity to a db.

     """

    def __init__(self):
        self.offices = []
        self.choice_o_list = []
        self.livingspaces = []
        self.choice_l_list = []
        self.rooms = []

        self.staff = []
        self.fellows = []
        self.employees = []
        self.allocations = {}
        self.db_names = []

    def create_room(self, room_type, room_name):
        """
            Create one of 2 types of rooms in Amity, a Living Space or an Office.

            Arguments:
                room_type -- a str describing the type of room, 'OFFICE' or 'LIVING SPACE'
                room_name -- a tuple describing the name of the room
        """
        self.rooms = self.offices + self.livingspaces



        for item in room_name:
            item = item.upper()
            for object in self.rooms:
                if object.name == item:
                    return Fore.RED + "What you doin' bana? That room has already been created."

            if ''.join(room_name).isalpha() is False:
                return Fore.RED +"The room name needs to be made up of L-E-T-T-E-R-S."

            else:
                if room_type.upper() == "OFFICE" or room_type.upper() == "O":

                    office = Office(item.upper())
                    self.offices.append(office)
                    self.choice_o_list.append(office)
                    self.rooms.extend(self.offices)
                    print(Fore.GREEN + "An office space named %s has been created." % item)

                elif room_type.upper() == "LIVINGSPACE" or room_type.upper() == "LS"\
                                                                    or room_type.upper() == "L":
                    livingspace = LivingSpace(item)
                    self.livingspaces.append(livingspace)
                    self.choice_l_list.append(livingspace)
                    self.rooms.extend(self.livingspaces)
                    print(Fore.GREEN + "A living space named %s has been created." % item)

                else:
                    return Fore.RED + "Ain't no such type of room as what you typed."




    def check_if_offices_amity_full(self):
        """
            Helper function that checks to see if the offices in amity are full.
        """
        if self.choice_o_list == []:
            return True
        else:
            allocation_choice = choice(self.choice_o_list)
            # try:
            for office in self.choice_o_list:

                if office.name == allocation_choice.name.upper():
                    if office.num_of_persons  < 6:
                        return office

                    elif office.num_of_persons == 6:
                        self.choice_o_list.remove(office)
                        return self.check_if_offices_amity_full()
            # except IndexError:
            #     return True


    def check_if_ls_amity_full(self):
        """
            Helper function that checks to see if the living spaces in amity are full.
        """

        if self.choice_l_list == []:
            return True
        else:
            allocation_choice = choice(self.choice_l_list)

            for lspace in self.choice_l_list:

                if lspace.name == allocation_choice.name.upper():
                    if lspace.num_of_persons  < 4:
                        return lspace

                    elif lspace.num_of_persons == 4:
                        self.choice_l_list.remove(lspace)
                        return self.check_if_ls_amity_full()


    def add_person(self, name, role, wants_accomodation=None):
        """
            Adds a person to Amity and allocates them randomly to an office space or if required
            a living space.

            Arguments:
                name -- this is the person's name
                role -- this argument specifies whether they are a Fellow or Staff member
                wants_accomodation -- an optional argument that signifies whether a fellow wants
                                     accomodation or not.
        """

        name = name.upper()
        for person in self.employees:
            if name == person.name:
                prompt = input\
(Fore.BLUE + "%s is already a member of Amity do you want to add someone with the same name?" % name +"\n"+\
"Y for Yes" + "\n" + "N for No"+"\n")
                if prompt.upper() == "N":
                    return Fore.YELLOW + "Cool, I got you."+"\n"
                elif prompt.upper() == "Y":
                    pass
                else:
                    return Fore.MAGENTA + "What does that mean?"
        if ''.join(name.split()).isalpha() is False:
            return  Fore.RED + "People's names need to be spelt with L-E-T-T-E-R-S!"

        employee_id = randint(10000, 99999)
        if wants_accomodation is None:
            wants_accomodation = "N"


        if role.upper() == "STAFF":

            if self.offices == []:
                new_staff = Staff(employee_id, name)
                self.staff.append(new_staff)
                self.employees.append(new_staff)
                new_staff.is_allocated = False


                return Fore.GREEN +\
     "%s has been added but there are no rooms created in Amity, create a room and reallocate the new member." % (name)

            else:

                wants_accomodation = "N"
                new_staff = Staff(employee_id, name)
                office_object = self.check_if_offices_amity_full()
                if office_object is True:
                    self.staff.append(new_staff)
                    self.employees.append(new_staff)
                    new_staff.is_allocated = False
                    
                    return Fore.BLUE + "All offices are full %s can't be allocated now." % (name)

                else:

                    self.allocations[name] = office_object
                    office_allocation = office_object
                    office_index = self.offices.index(office_allocation)
                    self.offices[office_index].num_of_persons += 1
                    self.offices[office_index].current_occupants.append(name)
                    new_staff.is_allocated = True
                    self.staff.append(new_staff)
                    self.employees.append(new_staff)


                return Fore.GREEN + "%s has been allocated to %s." % (name, office_allocation.name)

        #Case for creating and allocating a new fellow
        if role.upper() == "FELLOW":
            if self.rooms == []:

                new_fellow = Fellow(employee_id, name)
                self.fellows.append(new_fellow)
                self.employees.append(new_fellow)
                new_fellow.is_allocated = False

                return Fore.GREEN + \
        "%s has been added but there are no rooms created in Amity, create a room and reallocate the new member." % (name)
            else:
                #Conditions for when Fellow does not want accomodation
                if wants_accomodation.upper() == "N":
                    #Condition for no offices created in Amity
                    if self.offices == []:
                        new_fellow = Fellow(employee_id, name)
                        self.fellows.append(new_fellow)
                        self.employees.append(new_fellow)
                        new_fellow.is_allocated = False

                        return Fore.BLUE + "%s has been added but there are no offices created in Amity, create an office and reallocate them" % (name)

                    #Normal operating conditions
                    new_fellow = Fellow(employee_id, name)
                    self.fellows.append(new_fellow)
                    self.employees.append(new_fellow)
                    office_object = self.check_if_offices_amity_full()

                    #Condition if all offices are full
                    if office_object is True:
                        new_fellow.is_allocated = False
                        return Fore.BLUE + \
                        "All office spaces are full %s cannot be allocated at this time." % name

                    #Continue normal operating conditions
                    else:
                        self.allocations[name] = office_object
                        office_allocation = office_object
                        office_index = self.offices.index(office_allocation)
                        self.offices[office_index].num_of_persons += 1
                        self.offices[office_index].current_occupants.append(name)
                        new_fellow.is_allocated = True

                        return Fore.YELLOW + \
                         "%s has been allocated to %s." % (name, office_allocation.name)
                #Case for Fellow who want's accomodation
                elif wants_accomodation.upper() == "Y":

                    new_fellow = Fellow(employee_id, name)
                    self.fellows.append(new_fellow)
                    self.employees.append(new_fellow)
                    office_object = self.check_if_offices_amity_full()
                    ls_object = self.check_if_ls_amity_full()

                    if office_object is True and ls_object is True:
                        new_fellow.is_allocated = False
                        return Fore.BLUE \
            + "All spaces are full, %s cannot be allocated or accomodated at this time." % (name)

                    elif ls_object is True and office_object is not True:

                        self.allocations[name] = [office_object]
                        office_allocation = self.allocations[name][0]
                        office_index = self.offices.index(office_allocation)
                        self.offices[office_index].num_of_persons += 1
                        self.offices[office_index].current_occupants.append(name)
                        new_fellow.is_allocated = None

                        return Fore.MAGENTA\
                + "%s has been allocated to %s but they are awaiting a livingspace."\
                 % (name, office_allocation.name)

                    elif office_object is True and ls_object is not True:

                        self.allocations[name] = [ls_object]
                        ls_allocation = self.allocations[name][0]
                        ls_index = self.livingspaces.index(ls_allocation)
                        self.livingspaces[ls_index].num_of_persons += 1
                        self.livingspaces[ls_index].current_occupants.append(name)
                        new_fellow.is_allocated = None

                        return Fore.GREEN +\
                        "%s can live in %s but they are awaiting an office." \
                        % (name, ls_allocation.name)

                    else:

                        self.allocations[name] = [office_object, ls_object]
                        office_allocation = self.allocations[name][0]
                        office_index = self.offices.index(office_allocation)
                        self.offices[office_index].num_of_persons += 1
                        self.offices[office_index].current_occupants.append(name)
                        ls_allocation = self.allocations[name][1]
                        ls_index = self.livingspaces.index(ls_allocation)
                        self.livingspaces[ls_index].num_of_persons += 1
                        self.livingspaces[ls_index].current_occupants.append(name)
                        new_fellow.is_allocated = True

                        return Fore.GREEN +\
                        "%s has been allocated to %s and s/he can stay in %s." \
                        % (name, office_allocation.name, ls_allocation.name)

    def load_people(self, file_name):
        """Load_people loads people into Amity from a .txt file"""
        try:
            if file_name == None:
                file_name = 'people'

            dir_path = os.path.dirname(__file__)
            file_path = os.path.join(dir_path+"/textfiles/" + file_name + '.txt')
            with open(file_path, "r") as input_file:
                for line in input_file:
                    string = line.split()
                    name = string[0] + " " + string[1]
                    role = string[2]

                    for person in self.employees:
                        if name == person.name:
                            prompt = input\
("%s is already a member of Amity do you want to add someone with the same name?" % name +"\n"+\
"Y for Yes" + "\n" + "N for No"+"\n" + "Z for No to all"+"\n")
                            if prompt.upper() == "N":
                                print("Cool, I got you."+"\n")
                                break
                            elif prompt.upper() == "Z":
                                return "Sawa boss, I will not add these people!"
                            else:
                                pass

                    else:
                        if len(string) < 4:
                            print(self.add_person(name, role))
                        else:
                            wants_accomodation = string[3]
                            print(self.add_person(name, role, wants_accomodation))

        except IOError:

            return Fore.RED + "This file doesn't exist chief!"

    def print_ids(self, fname='None', lname='None'):

        if fname is None and lname is None:
            for person in self.employees:
                print(Fore.GREEN + str(person.employee_id) + " " + person.name)
        else:
            person_name = fname +" "+ lname
            for person in self.employees:

                if person.name == person_name.upper():
                    print(Fore.GREEN + str(person.employee_id) + " " + person.name)
                else:
                    continue

    def reallocate_person(self, id, room_name):
        """This function reallocates a person in Amity to a new room using a unique id."""

        employees = self.staff + self.fellows

        for person in employees:

            if int(person.employee_id) == id:
                found_person = person
                if self.search_rooms(room_name).name == 'Example':

                    return Fore.RED + "Quit playing fam, type in real rooms."
                else:
                    room = self.search_rooms(room_name)

                    if found_person.name in room.current_occupants:
                        return Fore.RED + \
                        "Whatchu doin'? %s is already in %s fam!" % (found_person.name, room_name)

                    else:
                        if room.num_of_persons == room.max_capacity:
                            return Fore.RED + \
                        "%s cannot be reallocated to %s because that room is full." % (found_person.name, room.name)
                        elif isinstance(found_person, Fellow) and isinstance(room, Office):
                            self.remove_person_from_room(found_person.name, 'o')
                            room.current_occupants.append(found_person.name)
                            room.num_of_persons += 1
                            self.allocations[found_person.name] = room
                            return Fore.GREEN + \
                            "%s has been reallocated to %s." % (found_person.name, room_name)
                        elif isinstance(found_person, Fellow) and isinstance(room, LivingSpace):
                            self.remove_person_from_room(found_person.name, 'ls')
                            room.current_occupants.append(found_person.name)
                            room.num_of_persons += 1
                            self.allocations[found_person.name] = room
                            return Fore.GREEN +\
                             "%s can live in %s." % (found_person.name, room_name)

                        elif isinstance(found_person, Staff) and isinstance(room, LivingSpace):
                            return Fore.RED + \
                            "You cannot accomodate a staff member in a livingspace."

                        else:
                            self.remove_person_from_room(found_person.name)
                            room.current_occupants.append(found_person.name)
                            room.num_of_persons += 1
                            self.allocations[found_person.name] = room
                            return Fore.GREEN+\
                            "%s has been reallocated to %s." % (found_person.name, room_name)

        return Fore.RED + "Yo that id doesn't exist in Amity, check them digits."


    def search_rooms(self, room_name):
        self.rooms = self.offices + self.livingspaces

        for room in self.rooms:
            
            if room.name == room_name.upper():
                return room
            else:
                continue
        return Office('Example')

    def remove_person_from_room(self, name, room_type=None):
        """Removes person from a room they've been allocated."""
        if room_type == 'O' or room_type == 'o' or None:
            for room in self.offices:
                if name in room.current_occupants:
                    room.current_occupants.remove(name)
                    room.num_of_persons -= 1
                else:
                    continue
        else:
            for ls in self.livingspaces:
                if name in ls.current_occupants:
                    ls.current_occupants.remove(name)
                    ls.num_of_persons -= 1

    def print_allocated(self, filename=None):
        self.rooms = self.livingspaces + self.offices
        if self.allocations == {}:
            return "There have been no allocations made yet."
        if filename is None:
            for space in self.rooms:
                print(Fore.GREEN + space.name.upper())
                print(Fore.GREEN + "-"*35)
                print("")
                print(Fore.GREEN + ", ".join(space.current_occupants)+'\n')
            return Fore.GREEN + "All rooms printed successfully."
        else:
            Amity_path = os.path.dirname(__file__)
            filename += '.txt'
            filename =os.path.join(Amity_path+'/textfiles/', filename)
            with open(filename, 'w') as a_file:

                for space in self.rooms:
                    a_file.write(space.name+'\n')
                    a_file.write("-"*35+'\n')
                    a_file.write(", ".join(space.current_occupants)+'\n')
                    a_file.write("\n")

                return Fore.GREEN + "All rooms have been printed successfully."

    def print_unallocated(self, filename=None):

        if filename is None:
            print(Fore.GREEN + "THE POOR UNALLOCATED SOULS")
            print(Fore.GREEN + "-"*35)
            for member in self.employees:
                if member.name not in self.allocations:
                    print(Fore.GREEN + member.name +"  "+ member.employee_id)
        else:
            Amity_path = os.path.dirname(__file__)
            filename += '.txt'
            filename = os.path.join(Amity_path+'/textfiles', filename)
            with open(filename, 'w') as a_file:
                a_file.write("THE POOR UNALLOCATED SOULS"+'\n')
                a_file.write("-"*35+'\n')
                for member in self.employees:
                    if member.name not in self.allocations:
                        a_file.write(member.name +"  "+ str(member.employee_id) + '\n')


    def print_room(self, room_name):
        self.rooms = self.livingspaces + self.offices
        if room_name is None:
            for room in self.rooms:
                print(Fore.GREEN + room.name.upper())
                print(Fore.GREEN + "-"*35)
                print(Fore.GREEN + ", ".join(room.current_occupants))
            return Fore.GREEN + "Here's all your rooms, aint they pretty :-)!"
        else:

            for room in self.rooms:
                if room.name == room_name.upper():
                    print(Fore.GREEN + room.name.upper())
                    print(Fore.GREEN + "-"*35)
                    return Fore.GREEN + ", ".join(room.current_occupants)
                else:
                    continue
        return Fore.RED + "How do I print things that don't exist? Try again."

    def save_state(self, filename):
        """Saves the state of Amity into a db."""
        if filename ==None:
            filename = 'amity'
        self.rooms = self.offices + self.livingspaces
        db.create_db(filename)
        Session = sessionmaker()
        engine = create_engine('sqlite:///'+filename+'.db')
        Session.configure(bind=engine)
        session = Session()
        for person in self.employees:
            if isinstance(person, Fellow):
                person_type = 'Fellow'
            else:
                person_type = 'Staff'

            id_number = person.employee_id
            name = person.name
            allocation_status = person.is_allocated
            person_details = Person(id_number, name, allocation_status, person_type)
            person_list = session.query(Person).all()
            person_check = [item.id_number for item in person_list]
            if id_number in person_check:
                session.query(Person).filter(Person.id_number == id_number).update\
                ({'allocation_status': allocation_status})
            else:
                session.add(person_details)

        for room in self.rooms:
            if isinstance(room, Office):
                room_type = 'Office'
            else:
                room_type = 'Livingspace'
            room_name = room.name
            max_capacity = room.max_capacity
            current_occupants = ','.join(room.current_occupants)
            num_of_occupants = room.num_of_persons
            room_details = Rooms(room_name, room_type, current_occupants,\
                                num_of_occupants, max_capacity)
            room_list = session.query(Rooms).all()
            room_check = [item.room_name for item in room_list]
            if room_name in room_check:
                session.query(Rooms).filter(Rooms.room_name == room_name).update\
                ({'current_occupants': current_occupants})
            else:
                session.add(room_details)

        session.commit()
        return Fore.GREEN + "Data has been successfully saved to %s!" % filename

    def load_state(self, filename=None):
        """Loads data from db into Amity."""
        self.system_tear_down()
        if filename is None:
            filename = 'amity'


        db.create_db(filename)
        Session = sessionmaker()
        engine = create_engine('sqlite:///'+filename+'.db')
        Session.configure(bind=engine)
        session = Session()

        # Loading person data from a database.
        person_data = session.query(Person).all()
        for obj in person_data:
            if obj.person_type == 'Fellow':
                person_object = Fellow(int(obj.id_number), obj.name)
                person_object.is_allocated = obj.allocation_status
                self.fellows.append(person_object)
            else:
                person_object = Staff(int(obj.id_number), obj.name)
                person_object.is_allocated = obj.allocation_status
                self.staff.append(person_object)
        self.employees = self.staff + self.fellows
        #Loading room data from a database.
        room_data = session.query(Rooms).all()
        for obj in room_data:
            if obj.room_type == 'Office':
                room_object = Office(obj.room_name)
                room_object.max_capacity = obj.max_capacity
                room_object.current_occupants = (obj.current_occupants).split(',')
                for person_name in room_object.current_occupants:
                    self.allocations[person_name] = [room_object]
                self.offices.append(room_object)
            else:
                room_object = LivingSpace(obj.room_name)
                room_object.max_capacity = obj.max_capacity
                room_object.current_occupants = (obj.current_occupants).split(',')
                for person_name in room_object.current_occupants:
                    self.allocations[person_name] = [room_object]
                self.livingspaces.append(room_object)
        self.rooms = self.offices + self.livingspaces
        return Fore.GREEN + "Data has been loaded in Amity successfully."

    def system_tear_down(self):
        """This is a function to reset Amity to its original state."""
        self.offices = []
        self.livingspaces = []
        self.rooms = []
        self.staff = []
        self.fellows = []
        self.employees = []
        self.allocations = {}
        self.db_names = []
