"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    create_room  <room_type> <room_name>...
    add_person <first_name> <last_name> <staff_role> [<wants_accommodation>]
    print_ids <first_name> <last_name>
    reallocate_person <person_identifier> <new_room_name>
    load_people [--o=<filename>]
    print_allocations [--o=<filename>]
    print_unallocated [-o=filename]
    print_room <room_name>
    delete_member <id>
    delete_room <room_name>
    save_state [--db=sqlite_database]
    load_state <sqlite_database>

Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.

"""
import cmd
import pyfiglet
from colorama import *
from docopt import docopt, DocoptExit
from models.amity import Amity


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class AmityCommandCentre (cmd.Cmd):
    intro = 'Welcome to my Amity!' \
        + ' (type help for a list of commands.)'
    prompt = Fore.YELLOW +'(Amity App) '
    amity = Amity()


    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room  <room_type> <room_name>..."""
        print(self.amity.create_room(arg['<room_type>'], arg['<room_name>']))


    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> <staff_role> [<wants_accommodation>]
        """
        if (arg['<staff_role>'].upper() == "FELLOW") or (arg['<staff_role>'].upper() == "STAFF"):
            person_name = arg['<first_name>'] + " " + arg['<last_name>']
            print(self.amity.add_person(person_name, arg['<staff_role>'], arg['<wants_accommodation>']))

        else:
            print(Fore.RED + "Hey! They need to be either STAFF or FELLOWS, no funny business!")

    @docopt_cmd
    def do_print_ids(self, arg):
        """Usage: print_ids [<fname>] [<lname>]
        """
        try:
            self.amity.print_ids(arg['<fname>'], arg['<lname>'])
        except ValueError:
            print("That's not nice, why are you trying to break me?")

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_identifier> <new_room_name>
        """
        print(self.amity.reallocate_person(int(arg['<person_identifier>']), arg['<new_room_name>']))

    @docopt_cmd
    def do_print_allocations(self, arg=None):
        """Usage: print_allocated [--o=<filename>]
        """
        print(self.amity.print_allocated(arg['--o']))

    @docopt_cmd
    def do_load_people(self, arg=None):
        """Usage: load_people [--o=<filename>]
        """
        print(self.amity.load_people(arg['--o']))
    @docopt_cmd
    def do_print_unallocated(self, arg=None):
        """Usage: print_unallocated [--o=<filename>]
        """
        print(self.amity.print_unallocated(arg['--o']))

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room [<room_name>]
        """
        print(self.amity.print_room(arg['<room_name>']))

    @docopt_cmd
    def do_delete_room(self, arg):
        """Usage: delete_room <room_name>
        """
        print(self.amity.delete_room(arg['<room_name>']))

    @docopt_cmd
    def do_delete_member(self, arg):
        """Usage: delete_person <person_id>
        """
        print(self.amity.delete_member(arg['<person_id>']))

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db=<sqlite_database>]
        """
        print(self.amity.save_state(arg['--db']))

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state [<sqlite_database>]
        """
        print(self.amity.load_state(arg['<sqlite_database>']))

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()



if __name__ == '__main__':
    fig = pyfiglet.Figlet('isometric2')
    print(Fore.CYAN + fig.renderText("Amity")+ "\n\n")
    print(Fore.YELLOW + __doc__)
    AmityCommandCentre().cmdloop()

