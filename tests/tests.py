"""Unittests for Amity """
import unittest
from amity import Amity
from person import Person, Staff, Fellow
from rooms import Rooms, Office, LivingSpace
from nose.plugins.attrib import attr




@attr('Classes')
class AmityInheritanceBaseTestCases(unittest.TestCase):
    """Class of tests that checks all inheritance cases for Amity"""

    def test_rooms_is_subclass_amity(self):
        """Tests whether Rooms is a subclass of Amity."""
        new_room = Rooms()
        self.assertIsInstance(new_room, Amity, "Rooms is not a subclass of Amity.")

    def test_person_is_subclass_amity(self):
        """Tests whether Person class is a subclass of Amity."""
        new_person = Person()
        self.assertIsInstance(new_person, Amity, "Person is not a subclass of Amity")

    def test_office_is_subclass_rooms(self):
        """Tests whether Office class is a subclass of Rooms."""
        new_office = Office()
        self.assertIsInstance(new_office, Rooms, "Office is not a subclass of Rooms")

    def test_ls_is_subclass_rooms(self):
        """Tests whether LivingSpace class is a subclass of Rooms."""
        new_ls = LivingSpace()
        self.assertIsInstance(new_ls, Rooms, "LivingSpace is not a subclass of Rooms")

    def test_staff_is_subclass_person(self):
        """Tests whether Staff class is a subclass of Persons."""
        new_staff_member = Staff()
        self.assertIsInstance(new_staff_member, Person, "Staff is not a subclass of Person")

    def test_fellow_is_subclass_person(self):
        """Tests whether Fellow class is a subclass of Persons."""
        new_fellow = Fellow()
        self.assertIsInstance(new_fellow, Person, "Fellow is not a subclass of Person")


@attr('Methods')
class AmityMethodBaseTestCases(unittest.TestCase):

    def setUp(self):
        self.mozambique = Rooms()
        self.ebrahim_j = Person()

    def test_if_room_already_exists(self):
        """Test to check if the room already exists in Amity."""
        print(self.mozambique.create_room("O","Coutonou"))
        self.assertEqual(self.mozambique.create_room("O","Coutonou"), "This room already exists in Amity.", 
        "Should return a message if room exists.")

    def test_create_room(self):
        """Test to check if the create_room function works."""
        print(self.mozambique.create_room("o","Mozambique"))
        self.assertEqual(self.mozambique.create_room("o","Mozambique"), "New office space Mozambique has been successfully created.",
        msg="Should return a message confirming room creation")

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
        print(self.ebrahim_j.add_person("Ebrahim Janoowalla", "FELLOW"))
        self.assertEqual(self.ebrahim_j.add_person("Ebrahim Janoowalla", "FELLOW"), "Ebrahim Janoowalla has been allocated to Cotonou.",
        "Should create a person in Amity.")

    @attr('allocate_person')
    def test_reallocate_person(self):
        """Tests to check whether Amity will allocate a person a room."""
        self.assertEqual(self.ebrahim_j.allocate_person("Ebrahim Janoowalla","Cotonou"), [{"Ebrahim Janoowalla":"Cotonou"}])

    def test_check_the_availabilty(self):
        """Test to check whether a room is available or not."""
        pass
    @attr('loads_file')
    def test_loads_file_adds_people(self):
        """Tests to check whether persons can be added via a txt file."""
        self.txt_file = open("people.txt","r")
        self.first_name = self.txt_file.readline()
        self.txt_file.close()
        self.load_person=self.ebrahim_j.add_person(self.first_name)
        self.assertEquals(self.load_person,"DIDACHUS ODHIAMBO has been allocated to Cotonou.")

    # def test_print_all_rooms(self):
    #     """"""
    #     pass

    # def test_print_available_rooms(self):
    #     """"""
    #     pass

if __name__ == '__main__':
    unittest.main()
