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
        model_office = self.amity.create_room('Office','Texas')
        model_ls = self.amity.create_room('Ls','Hurlingham')

    def test_create_office_room(self):
        """Test to check if the create_room function creates an office in amity."""
        new_room = self.amity.create_room("o","Mozambique")
        self.assertEqual(new_room, "An office space named Mozambique has been created.")
    
    def test_create_ls_room(self):
        """Test to check whether the create_room function creates a living space in amity."""
        new_room = self.amity.create_room("ls","Malawi")
        self.assertEqual(new_room, "A living space named Malawi has been created.")

    def test_create_room_against_duplicates(self):
        self.amity.create_room('ls','Nanyuki')
        newer_room = self.amity.create_room('ls','Nanyuki')
        self.amity.create_room('O','NewYork')
        newest_room = self.amity.create_room('O','NewYork')
        self.assertEqual(newer_room, "What you doin' bana? That room has already been created.")
        self.assertEqual(newest_room, "What you doin' bana? That room has already been created.")

    def test_create_room_bad_room_type(self):
        """"This tests asserts that input other than Office, O, LS, or LIVINGSPACE returns a message."""
        new_room = self.amity.create_room("Jimbo","Manhattan")
        self.assertEqual(new_room, "Ain't no such type of room as what you typed.")
    
    def test_create_room_name_is_alpha(self):
        """This tests that the name of the room is alphabetical input."""
        new_room = self.amity.create_room("Office","J3322%&*!)")
        self.assertEqual(new_room, "The room name needs to be made up of L-E-T-T-E-R-S.")

    def test_office_max_capacity_office(self):
        """Test to check if the max_capacity of the office class is 6."""
        self.cotonou = Office('Cotonou')
        self.assertEqual(self.cotonou.max_capacity, 6, "Should ensure that the max capacity of the office is 6")

    def test_living_space_max_capacity_ls(self):
        """Test to check if the max_capacity of the office class is 4."""
        self.barbados = LivingSpace('Barbados')
        self.assertEqual(self.barbados.max_capacity, 4, "Should ensure that the max capacity of the living space is 4")

    
    def test_add_person_adds_allocates_fellows(self):
        """Tests to check whether amity adds and allocates a fellow."""
        fellow = self.amity.add_person("James Muratha", "Fellow","Y")
        self.assertEqual(len(self.amity.employees), 1)
        self.assertEqual(fellow, "James Muratha has been allocated to Texas and s/he can stay in Hurlingham.")
    
    def test_add_person_adds_allocates_staff(self):
        """Tests to check whether amity adds and allocates a staff member."""
        staff = self.amity.add_person("Joshua Mwaniki", "Staff")
        self.assertEqual(len(self.amity.employees), 1)
        self.assertEqual(staff, "Joshua Mwaniki has been allocated to Texas.")

    def test_add_person_for_bad_name_input(self):
        staff = self.amity.add_person("n00B5a!B0T", "Staff")
        self.assertEqual(staff, "People's names need to be spelt with L-E-T-T-E-R-S!")

    def test_add_person_no_room_created(self):
       self.amity2 =Amity()
       person = self.amity2.add_person("James Mwaniki", "Staff")
       self.assertIn("James Mwaniki has been added but there are no rooms created in Amity,", person)
   
    def test_reallocate_person(self):
        """Tests to check whether Amity will allocate a person a room."""
        pass

    def test_check_the_availabilty(self):
        """Test to check whether a room is available or not."""
        pass
    @attr('loads_file')
    def test_loads_file_adds_people(self):
        """Tests to check whether persons can be added via a txt file."""
        self.amity.create_room("Office","France")
        self.amity.create_room("LS","Nairobi")
        self.amity.load_people('people')
        self.assertEquals(self.amity.fellows[0].name, "DIDACHUS ODHIAMBO")
        self.assertIn("DIDACHUS ODHIAMBO", self.amity.allocations)

    def test_print_allocated(self):
        """Tests whether the function to print_all_rooms prints all the rooms saved to Amity."""
        pass
    def test_save_state(self):
        """Tests whether the database saves data from Amity"""
        #Use mock here to simulate db
        pass
    
    def test_print_available_rooms(self):
        """Tests whether Amity prints all the available rooms"""
        pass

if __name__ == '__main__':
    unittest.main()
