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


    @attr('create_room')
    def test_create_office_room(self):
        """Test to check if the create_room function creates an office in amity."""
        new_room = self.amity.create_room("o","Mozambique")
        self.assertEqual(new_room, "An office space named Mozambique has been created.")
    
    def test_create_ls_room(self):
        """Test to check whether the create_room function creates a living space in amity."""
        new_room = self.amity.create_room("ls","Malawi")
        self.assertEqual(new_room, "A living space named Malawi has been created.")

    def test_office_max_capacity_office(self):
        """Test to check if the max_capacity of the office class is 6."""
        self.cotonou = Office('Cotonou')
        self.assertEqual(self.cotonou.max_capacity, 6, "Should ensure that the max capacity of the office is 6")

    def test_living_space_max_capacity_ls(self):
        """Test to check if the max_capacity of the office class is 4."""
        self.barbados = LivingSpace('Barbados')
        self.assertEqual(self.barbados.max_capacity, 4, "Should ensure that the max capacity of the living space is 4")

    @attr('add_person')
    def test_add_person_working(self):
        """Tests to check whether a person was added in Amity."""
        self.amity.add_person("James Muratha", "Fellow","Y")
        self.assertEqual(len(self.amity.employees), 1)
    @attr('allocate_person')
    def test_add_person_allocates_a_person(self):
        """Tests whether a person gets allocated a room in Amity"""
        self.amity.create_room('Office','Krypton')
        self.amity.add_person("James Muratha", "Fellow")
        self.assertIn("James Muratha", self.amity.allocations)

    @attr('reallocate_person')
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
