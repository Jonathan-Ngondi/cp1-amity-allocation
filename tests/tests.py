"""Unittests for Amity """
import unittest
from models.amity import Amity
from models.person import Person, Staff, Fellow
from models.rooms import Room, Office, LivingSpace
from nose.plugins.attrib import attr



@attr('Methods')
class AmityMethodBaseTestCases(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()
        self.model_ls = self.amity.create_room('ls',['Hurlingham'])
        self.model_office = self.amity.create_room('Office',['Texas'])


    def test_create_office_room(self):
        """Test to check if the create_room function creates an office in amity."""
        new_room = self.amity.create_room("O", ["Mozambique"])
        offices = self.amity.offices
        self.assertEqual(len(offices), 2)

    def test_create_ls_room(self):
        """Test to check whether the create_room function creates a living space in amity."""
        new_room = self.amity.create_room("ls", ["Malawi"])
        lss = self.amity.livingspaces
        self.assertEqual(len(lss), 2)

    def test_create_room_against_duplicates(self):
        newer_room = self.amity.create_room('ls', ['Hurlingham'])
        newest_room = self.amity.create_room('O', ['Texas'])
        print(newest_room)
        self.assertEqual(newer_room, "\x1b[31mWhat you doin' bana? That room has already been created.")
        self.assertEqual(newest_room, "\x1b[31mWhat you doin' bana? That room has already been created.")

    def test_create_room_bad_room_type(self):
        """"This tests asserts that input other than Office, O, LS, or LIVINGSPACE returns a message."""
        new_room = self.amity.create_room("Jimbo",["Manhattan"])
        self.assertEqual(new_room, "\x1b[31mAin't no such type of room as what you typed.")

    def test_create_room_name_is_alpha(self):
        """This tests that the name of the room is alphabetical input."""
        new_room = self.amity.create_room("Office","J3322%&*!)")
        self.assertEqual(new_room, "\x1b[31mThe room name needs to be made up of L-E-T-T-E-R-S.")

    def test_office_max_capacity_office(self):
        """Test to check if the max_capacity of the office class is 6."""
        self.cotonou = Office('Cotonou')
        self.assertEqual(self.cotonou.max_capacity, 6, "Should ensure that the max capacity of the office is 6")

    def test_living_space_max_capacity_ls(self):
        """Test to check if the max_capacity of the office class is 4."""
        self.barbados = LivingSpace('Barbados')
        self.assertEqual(self.barbados.max_capacity, 4, "Should ensure that the max capacity of the living space is 4")

    def test_check_if_offices_amity_works_empty_list(self):
        """Test to check whether the helper function returns a true value for an empty choice list"""
        self.amity.offices[0].num_of_persons = 6
        message = self.amity.check_if_offices_amity_full()
        self.assertEqual(message, True)

    def test_check_if_offices_ls_works_empty_list(self):
        """Test to check whether the helper function returns a true value for an empty choice list"""
        self.amity.choice_l_list = []
        message = self.amity.check_if_ls_amity_full()
        self.assertEqual(message, True)

    def test_check_if_ls_works(self):
        """"Test to check whether returns True for a full living space."""
        self.amity.livingspaces[0].num_of_persons = 4
        message = self.amity.check_if_ls_amity_full()
        self.assertEqual(message, True)


    def test_add_person_adds_allocates_fellows(self):
        """Tests to check whether amity adds and allocates a fellow."""
        fellow = self.amity.add_person("James Muratha", "Fellow","Y")
        self.assertEqual(len(self.amity.employees), 1)
        self.assertEqual(fellow, "\x1b[32mJAMES MURATHA has been allocated to TEXAS and s/he can stay in HURLINGHAM.")

    def test_add_person_adds_allocates_staff(self):
        """Tests to check whether amity adds and allocates a staff member."""
        staff = self.amity.add_person("Joshua Mwaniki", "Staff")
        self.assertEqual(len(self.amity.employees), 1)
        self.assertEqual(staff, "\x1b[32mJOSHUA MWANIKI has been allocated to TEXAS.")

    def test_add_person_for_bad_name_input(self):
        staff = self.amity.add_person("n00B5a!B0T", "Staff")
        self.assertEqual(staff, "\x1b[31mPeople's names need to be spelt with L-E-T-T-E-R-S!")

    def test_add_staff_no_room_created(self):
       self.amity2 =Amity()
       person = self.amity2.add_person("James Mwaniki", "Staff")
       self.assertIn("JAMES MWANIKI has been added but there are no rooms created in Amity,", person)
    
    def test_add_fellow_no_room_created(self):
        self.amity.offices = []
        message = self.amity.add_person("Josh Brown", "Fellow","Y")
        self.assertEqual(message, "\x1b[34mJOSH BROWN has been added but there are no rooms created in Amity, create a room and reallocate the new member.")


    def test_add_person_when_offices_full(self):
        self.amity.offices[0].num_of_persons = 6
        message = self.amity.add_person("Brian Sumba", "Fellow", "N")
        self.assertEqual(message, "\x1b[34mAll office spaces are full BRIAN SUMBA cannot be allocated at this time.")

    def test_add_person_when_ls_full(self):
        """"The """
        self.amity.livingspaces[0].num_of_persons = 4
        message = self.amity.add_person("Marvin Otieno", "Fellow", "Y")
        self.assertEqual(message, \
        "\x1b[35mMARVIN OTIENO has been allocated to TEXAS but they are awaiting a livingspace.")

    def test_reallocate_person(self):
        """Tests to check whether Amity will allocate a person a room."""
        self.amity.add_person("Bob Marley","Staff")
        self.amity.create_room("Office",["Kingston"])
        message = self.amity.reallocate_person(self.amity.staff[0].employee_id, "Kingston")
        self.assertEqual(message, "\x1b[32mBOB MARLEY has been reallocated to Kingston.")

    def test_reallocate_person_bad_id(self):
        self.amity.add_person("Bob Marley","Staff")
        self.amity.create_room("Office",["Kingston"])
        message = self.amity.reallocate_person(122, "Kingston")
        self.assertEqual(message, "\x1b[31mYo that id doesn't exist in Amity, check them digits.")

    def test_reallocate_person_right_allocation(self):
        self.amity.add_person("Bob Marley","Staff")
        message = self.amity.reallocate_person(self.amity.staff[0].employee_id, "Hurlingham")
        self.assertEqual(message,"\x1b[31mYou cannot accomodate a staff member in a livingspace.")

    def test_reallocate_person_fellow_not_removed(self):
        """This test confirms whether reallocate_person will keep person with livingspace
            accomodated when allocating an office. 
        """
        self.amity.add_person("Kabbaka Pyramid", "Fellow", "Y")
        self.amity.create_room("Office",["Kingston"])
        message = self.amity.reallocate_person(self.amity.fellows[0].employee_id, "Kingston")
        self.assertEqual(self.amity.livingspaces[0].current_occupants, ['KABBAKA PYRAMID'])

    def test_reallocate_person_fellow_removed(self):

        """This test confirms whether reallocate_person will remove a fellow from livingspace
            allocated when allocating a new livingspace. 
        """
        self.amity.add_person("Kabbaka Pyramid", "Fellow", "Y")
        self.amity.create_room("LS",["Kingston"])
        message = self.amity.reallocate_person(self.amity.fellows[0].employee_id, "Kingston")
        self.assertEqual(self.amity.livingspaces[0].current_occupants, [])

    def test_search_room_works(self):
        message = self.amity.search_rooms('Texas')
        self.assertEqual(message, self.amity.offices[0])

    def test_search_room_for_wrong_input(self):
        message = self.amity.search_rooms('Nebraska')
        assert isinstance(message, Office)

    def test_print_allocations(self):
        """Test asserts that test prints allocations to console."""
        self.amity.add_person("James Brown", "Staff")
        message = self.amity.print_allocated()
        self.assertEquals(message, "\x1b[32mAll rooms printed successfully.")

    def test_print_unallocated(self):
        """Test asserts that test prints unallocated people to console."""
        self.amity.add_person("James Brown", "Staff")
        message = self.amity.print_unallocated()
        self.assertEquals(message, None)

    def test_print_room(self):
        """Tests whether room is printed to console."""
        self.amity.add_person("James Brown", "Staff")
        message = self.amity.print_room('Texas')
        self.assertEquals(message, '\x1b[32mJAMES BROWN')

    def test_print_room_bad_input(self):
        """"Tests whether bad room input returns an error message."""
        self.amity.add_person("James Brown", "Staff")
        message = self.amity.print_room('Tahiti')
        self.assertEquals(message, "\x1b[31mHow do I print things that don't exist? Try again.")

    def test_loads_people(self):
        """Tests to check whether persons can be added via a txt file."""
        self.amity.create_room("Office", ["France"])
        self.amity.create_room("LS", ["Nairobi"])
        self.amity.load_people('people')
        self.assertEquals(self.amity.fellows[0].name, "EBRAHIM JANOOSH")
        self.assertIn("DIDACHUS ODHIAMBO", self.amity.allocations)

    def test_loads_people_non_existent_file(self):
        """Tests whether loads people returns error message for non-existent file."""
        message = self.amity.load_people('peop3')
        self.assertEqual(message, "\x1b[31mThis file doesn't exist chief!")


    def test_check_if_offices_full_works(self):

        message = self.amity.check_if_offices_amity_full()
        assert isinstance(message, Office)

    def test_if_offices_full_work_if_true(self):
        self.amity.offices[0].num_of_persons = 6
        message = self.amity.check_if_offices_amity_full()
        self.assertEqual(message, True)


    def test_save_state(self):
        """Tests whether the database saves data from Amity"""
        message = self.amity.save_state(None)
        self.assertEqual(message, "\x1b[32mData has been successfully saved to amity!")

    def test_load_state(self):
        self.amity.save_state(None)
        self.amity.load_state()
        message = self.amity.offices[0].name
        self.assertEqual(message, 'TEXAS')

    def test_load_state_adds_livingspaces(self):
        self.amity.create_room("LS",["Earth"])
        self.amity.save_state(None)
        self.amity.load_state()
        message = self.amity.livingspaces[1].name
        self.assertEqual(message, "EARTH")
    def test_load_state_loads_successfully(self):
        message = self.amity.load_state(None)
        self.assertEqual(message, "\x1b[32mData has been loaded in Amity successfully.")



    def test_system_tear_down(self):
        """"Tests"""
        self.amity.system_tear_down()
        self.assertEqual(self.amity.employees, [])

if __name__ == '__main__':
    unittest.main()
