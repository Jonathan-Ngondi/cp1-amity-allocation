[![Coverage Status](https://coveralls.io/repos/github/Jonathan-Ngondi/cp1-amity-allocation/badge.svg?branch=master)](https://coveralls.io/github/Jonathan-Ngondi/cp1-amity-allocation?branch=master)


# CP1-Amity-Allocation

This is a python project that allocates staff and fellows to rooms automatically in one of Andela's facilities Amity.
Staff may only be allocated to offices while Fellows can be allocated to offices as well as accomodated in living spaces.

##Installation and Setup
Clone the repo to  a folder of your choosing on your 'terminal'
'''
git clone https://github.com/Jonathan-Ngondi/cp1-amity-allocation.git
'''
Navigate to the project folder
```
cd amity
```
Activate your virtual environment
```
source venv/bin/activate
```
alternatively, if you have a virtualenvwrapper:
```
workon venv
```
Now, install the required packages
```
pip install -r requirements.txt
```
## Launching the application
To launch the application run the following command.
```
python app.py
```
## Commands to run:

* To create a new office or living space(Multiple rooms can be created in line) run ```create_room <room_type> <room_names>...```

* To add a new staff or fellow run```add_person <first_name> <last_name> <role> [<wants_accomodation>]```.
 For fellows who want accomodation specify the optional 'y' parameter

* To view all members in any room run ```print_room <room_name>```

* To view all allocations i.e. every room and their occupants run ```print_allocations [--o=<filename>]``` 
 specifying a filename saves the records in a ```.txt``` file

* To view all unallocated persons run ```print_unallocated [--o=<filename>]``` 
 specifying a filename saves the records in a ```.txt``` file

* ```load_people <filename>``` loads people from an existing ```.txt``` file, leave it blank to load from default ```people.txt```

* ```print_ids [<first_name>] [<last_name>]``` prints the id for a person's name in amity, if left blank prints all the ids in for a people in amity.

* ```reallocate_person <identifier> <new_room_name>``` reallocates a person from their current room to the given room

* ```delete_member <person_id>``` deletes a member from amity as well as from the default amity database.

* ```delete_room <room_name>``` deletes a room from amity as well as from the default amity database.

* ```save_state [<database_name>]``` saves the current state of the application to a database. Specifying the database_name saves the data to named database file

* ```load_state <database_name>``` loads data from an exisitng SQL database


Watch the tutorial here:

https://asciinema.org/a/8xh1vthx9ty5k6shbrw55zjea

