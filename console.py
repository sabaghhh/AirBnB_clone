#!/usr/bin/python3
"""
the entry point to the project
"""


import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models import storage
import re


_classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Place": Place,
        "Amenity": Amenity,
        "Review": Review
        }


def parse(line):
    """
    Parses an inpute and returns a list of strings
    """
    return re.findall(r'"(?:\\"|.)*?"|\S+', line)


def validate(line):
    """
    Validates and casts the input value to the
    appropriate attribute type
    """
    if (line[0] == '-' and line[1:].isnumeric()) or line.isnumeric():
        return int(line)
    elif (
            (line[0] == '-' and
                (all(char.isdigit() or char == '.') for char in line[1:]))
            and line.count('.') == 1):
        return float(line)
    elif all(char.isdigit() or char == '.' for char in line) \
            and line.count('.') == 1:
        return float(line)
    else:
        return str(line)


class HBNBCommand(cmd.Cmd):
    """
    the main class of the project
    """
    prompt = "(hbnb) "

    def do_EOF(self, line):
        """
        Quits the program when you press ctrl + D
        """
        print()
        return True

    def do_quit(self, line):
        """
        Quits the program when you type quit and press enter
        """
        return True

    def emptyline(self):
        """
        does nothing
        """
        pass

    def default(self, line):   # Still working on this
        """
        default function gets called when
        no other existing input gets entered
        """
        methods = {
                "all()": self.do_all
                }
        args = line.split(".")
        if args[0] not in _classes:
            print("Invalid Input")
        elif args[1] in methods:
            methods[args[1]](args[0])
        elif args[1] == "count()":
            count = 0
            obj_list = storage.all()
            for key in obj_list.keys():
                if key.split(".")[0] == args[0]:
                    count += 1
            print(count)
        else:
            print(f"Class {args[0]} doesnt have method {args[1]}")

    def do_create(self, line):
        """
        Create a new Instance of selected Model
        Usage: create <Class Name>
        """
        args = parse(line)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in _classes.keys():
            print("** class doesn't exist **")
        else:
            new_model = eval(args[0])()
            new_model.save()
            print(new_model.id)

    def do_show(self, line):
        """
        Prints the string representation of an instance
        based on the class name and id.
        Usage: show <Class Name> <Instance Id>
        """
        args = parse(line)
        model_list = storage.all()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in _classes.keys():
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in model_list.keys():
            print("** no instance found **")
        else:
            key = f"{args[0]}.{args[1]}"
            value = model_list[key]
            print(value)

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and id.
        Usage: destroy <Class Name> <Instance Id>
        """
        args = parse(line)
        model_list = storage.all()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in _classes.keys():
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in model_list.keys():
            print("** no instance found **")
        else:
            key = f"{args[0]}.{args[1]}"
            del (model_list[key])
            storage.save()

    def do_all(self, line):
        """
         Prints all string representation of all instances
         based or not on the class name.
         Usage: all OR all <Class Name>
        """
        args = parse(line)
        model_list = storage.all()
        obj_list = []
        if len(args) == 0:
            for key in model_list:
                str_value = str(model_list[key])
                obj_list.append(str_value)
            print(obj_list)
        elif args[0] not in _classes.keys():
            print("** class doesn't exist **")
        else:
            for key in model_list:
                if key.split(".")[0] == args[0]:
                    str_value = str(model_list[key])
                    obj_list.append(str_value)
            print(obj_list)

    def do_update(self, line):
        """
        Updates an instance based on the class name
        and id by adding or updating attribute
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        args = parse(line)
        model_list = storage.all()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in _classes.keys():
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in model_list.keys():
            print("** no instance found **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        else:
            k = f"{args[0]}.{args[1]}"
            for key, value in model_list.items():
                if key == k:
                    setattr(value, args[2], validate(args[3][1:-1]))
            model_list[k].save()

    def do_debug(self, line):
        """
        custom function used for further invistgation
        """
        model_list = storage.all()
        for key, value in model_list.items():
            print(key, value)
            for k, v in value.to_dict().items():
                print(k, v, type(v))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
