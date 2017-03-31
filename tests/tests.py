"""Unittests for Amity """
import unittest
from models.amity import Amity
from models.person import Person, Staff, Fellow
from models.rooms import Rooms, Office, LivingSpace
from nose.plugins.attrib import attr




@attr('Classes')
class AmityInheritanceBaseTestCases(unittest.TestCase):
    """Class of tests that checks all inheritance cases for Amity"""

    def test_rooms_is_subclass_amity(self):
        """Tests whether Rooms is a subclass of Amity."""
        new_room = Rooms()
        self.assertIsInstance(new_room, Amity, msg="Rooms is not a subclass of Amity.")

    def test_person_is_subclass_amity(self):
        """Tests whether Person class is a subclass of Amity."""
        new_person = Person()
        self.assertIsInstance(new_person, Amity, msg="Person is not a subclass of Amity")

    def test_office_is_subclass_rooms(self):
        """Tests whether Office class is a subclass of Rooms."""
        new_office = Office()
        self.assertIsInstance(new_office, Rooms, msg="Office is not a subclass of Rooms")

    def test_ls_is_subclass_rooms(self):
        """Tests whether LivingSpace class is a subclass of Rooms."""
        new_ls = LivingSpace()
        self.assertIsInstance(new_ls, Rooms, msg="LivingSpace is not a subclass of Rooms")

    def test_staff_is_subclass_person(self):
        """Tests whether Staff class is a subclass of Persons."""
        new_staff_member = Staff()
        self.assertIsInstance(new_staff_member, Person, msg="Staff is not a subclass of Person")

    def test_fellow_is_subclass_person(self):
        """Tests whether Fellow class is a subclass of Persons."""
        new_fellow = Fellow()
        self.assertIsInstance(new_fellow, Person, msg="Fellow is not a subclass of Person")


@attr('Methods')
class AmityMethodBaseTestCases(unittest.TestCase):

    def setUp(self):
        self.new_room = Rooms()
        self.new_person = Person()

    def test_if_room_already_exists(self):
        """Test to check if the room already exists in Amity."""
        print(self.mozambique.create_room("O","Coutonou"))
        self.assertEqual(self.new_room.create_room("O","Coutonou"), "This room already exists in Amity.", 
        msg="Should return a message if room exists.")

    def test_create_room(self):
        """Test to check if the create_room function works."""
        print(self.mozambique.all_rooms)
        self.assertEqual(self.new_room.create_room("o","Mozambique"), "New office space Mozambique has been successfully created.")

    def test_office_max_capacity_office(self):
        """Test to check if the max_capacity of the office class is 6."""
        self.cotonou = Office()
        self.assertEqual(self.cotonou.max_capacity, 6, "Should ensure that the max capacity of the office is 6")

    def test_living_space_max_capacity_ls(self):
        """Test to check if the max_capacity of the office class is 4."""
        self.barbados = LivingSpace()
        self.assertEqual(self.barbados.max_capacity, 4, "Should ensure that the max capacity of the living space is 4")

    @attr('add_person')
    def test_add_person(self):
        """Tests to check whether a person was added in Amity."""
        self.assertEqual(self.new_person.add_person("Ebrahim Janoowalla", "FELLOW"), "Ebrahim Janoowalla has been allocated to Cotonou.")

    @attr('allocate_person')
    def test_reallocate_person(self):
        """Tests to check whether Amity will allocate a person a room."""
        self.assertEqual(self.new_person.reallocate_person("Ebrahim Janoowalla","Cotonou"), [{"Ebrahim Janoowalla":"Cotonou"}])

    def test_check_the_availabilty(self):
        """Test to check whether a room is available or not."""
        pass
    @attr('loads_file')
    def test_loads_file_adds_people(self):
        """Tests to check whether persons can be added via a txt file."""
        self.load_persons = self.new_person.load_file('people.txt')
        self.assertEquals(self.load_persons,"DIDACHUS ODHIAMBO has been allocated to Cotonou.")

    # def test_print_all_rooms(self):
    #     """"""
    #     pass

    # def test_print_available_rooms(self):
    #     """"""
    #     pass

if __name__ == '__main__':
    unittest.main()
