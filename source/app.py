#!/Users/ehsc1997/anaconda3/bin/python3
import os
from source.file_handler import start_dict, save_to_file
from source.roundObject import Round
from source.input_cleaner import name_cleaner, number_cleaner


def start_app():

    user_exit = False

    menu_options = {1: "List of people", 2: "List of drinks", 3: "List of people and drinks", 4: "Edit people",
                    5: "Edit drinks", 6: "List of preferences", 7: "Edit preferences", 8: "Start round",
                    9: "View last round", 10: "Exit"}

    edit_list_options = {1: "ADD", 2: "REMOVE"}

    edit_preferences_options = {1: "ADD/CHANGE", 2: "REMOVE"}

    edit_round_options = {1: "ADD/CHANGE", 2: "REMOVE", 3: "COMPLETE"}

    filepath = "data/"

    people_dict = start_dict(filepath + "people.txt")
    drinks_dict = start_dict(filepath + "drinks.txt")
    preferences_dict = start_dict(filepath + "preferences.txt")
    last_order_dict = start_dict(filepath + "last_order.txt")

    while not user_exit:

        os.system("clear")

        user_selection = draw_menu(menu_options, draw_brIW())
        user_selection = int(user_selection)

        if user_selection > len(menu_options) or user_selection <= 0:
            input("\nPlease only enter a number from the options provided. Press 'Enter' to try again.")
            continue

        elif user_selection == 1:
            os.system("clear")
            draw_table("people", people_dict)

        elif user_selection == 2:
            os.system("clear")
            draw_table("drinks", drinks_dict)

        elif user_selection == 3:
            os.system("clear")
            draw_table("people and drinks", [people_dict, drinks_dict], 2)

        elif user_selection == 4:
            os.system("clear")
            ids = draw_table("people", people_dict)
            editing_choice = edit_menu(edit_list_options)
            if editing_choice == "ADD":
                people_dict = add_data("people", people_dict)
            elif editing_choice == "REMOVE":
                people_dict = remove_data("people", people_dict, ids, preferences=preferences_dict)

        elif user_selection == 5:
            os.system("clear")
            ids = draw_table("drinks", drinks_dict)
            editing_choice = edit_menu(edit_list_options)
            if editing_choice == "ADD":
                drinks_dict = add_data("drinks", drinks_dict)
            elif editing_choice == "REMOVE":
                drinks_dict = remove_data("drinks", drinks_dict, ids, preferences=preferences_dict)

        elif user_selection == 6:
            os.system("clear")
            preferences_data = ids_to_data(preferences_dict, people_dict, drinks_dict)
            draw_table("preferences", preferences_data, 2)

        elif user_selection == 7:
            os.system("clear")
            preferences_data = ids_to_data(preferences_dict, people_dict, drinks_dict)
            draw_table("preferences", preferences_data, 2)
            editing_choice = edit_menu(edit_preferences_options)
            if editing_choice == "ADD/CHANGE":
                preferences_dict = add_entries(preferences_dict, "preferences", people_dict, drinks_dict)
            elif editing_choice == "REMOVE":
                preferences_dict = remove_entries(preferences_dict, "preferences", people_dict, drinks_dict)

        elif user_selection == 8:
            os.system("clear")
            round_menu(edit_round_options, people_dict, drinks_dict)

        elif user_selection == 9:
            os.system("clear")
            last_order_data = ids_to_data(last_order_dict, people_dict, drinks_dict)
            draw_table("orders", last_order_data, 2)

        elif user_selection == 10:
            exit_screen()
            user_exit = True

        if user_selection != 10:
            input("Press ENTER to return to the Main Menu.")




def draw_brIW():
    return '''Welcome to BrIW v2.0 beta

                                 ____      _____        __
                                | __ ) _ _|_ _\ \      / /
                                |  _ \| '__| | \ \ /\ / / 
            /~~~~~~~~/|         | |_) | |  | |  \ V  V /  
           / /######/ / |       |____/|_| |___|  \_/\_/   
          / /______/ /  |   
         ============ /||     
         |__________|/ ||     
          |\__,,__/    ||
          | __,,__     ||
          |_\====/%____||
         /| /~~~~\ %  / |
        /_|/      \%_/  |
        | |        | | /
        |__\______/__|/

        ~~~~~~~~~~~~~~

What would you like to do? Choose from the following options:\n'''


def draw_menu(menu_options, drawing="", message="Please enter the number of your selection: "):

    if drawing != "":
        print(drawing)

    for option in menu_options:
        print(f"[{option}] {menu_options[option]}")
        if option == 3 or option == 5 or option == 7 or option == 9:
            print()
    print()

    user_selection = input(message)

    if user_selection.isdigit():
        user_selection = int(user_selection)
    else:
        user_selection = 0

    return user_selection


def find_width(data, cols=1):

    largest_item = 0

    if cols == 1:
        for item in data:
            item_size = len(item)
            if item_size > largest_item:
                largest_item = item_size
    else:
        for data_list in data:
            for item in data_list:
                item_size = len(item)
                if item_size > largest_item:
                    largest_item = item_size

    return largest_item


def separator(data, word=""):
    cols = len(data)
    width = find_width(data[0:-1], cols)
    spacing = " "*(width - len(word))
    return spacing


def largest_dict(dict_set, cols=1):
    longest_dict = len(dict_set)
    if cols > 1:
        for dict_num in range(0, len(dict_set)):
            dict_length = len(dict_set[dict_num])
            if dict_length > longest_dict:
                longest_dict = dict_length
    return longest_dict


def largest_space(data, title, cols=1):
    max_lengths = []
    if cols == 1:
        data_width = find_width(data, cols)
        max_lengths.append(data_width)
    else:
        for list_num in range(0, cols):
            data_width = find_width(data[list_num])
            max_lengths.append(data_width)
    final_width = sum(max_lengths)

    title_width = find_width([title])  # requires an array input

    if final_width >= title_width:
        letter_space = final_width
    else:
        letter_space = title_width

    return letter_space


def draw_line(cols=1, letter_space=0, largest_index=1):
    tabs_and_spaces = 7 * cols + 8 * (cols - 1)
    little_overhang = 2 * "="
    print("=" * tabs_and_spaces + "=" * letter_space + "==" * largest_index * cols + little_overhang)


def draw_header(title, cols=1, extra_space=0, largest_index=1):
    draw_line(cols, extra_space, largest_index)
    print(title.upper())
    draw_line(cols, extra_space, largest_index)


def draw_data(data, cols=1, largest_index=1):
    ids = []
    if cols == 1:
        index = 0
        for user_id, item in data.items():
            index += 1
            print(f"[{index}]\t", data[user_id])
            ids.append(user_id)
        return ids
    else:
        for dataset_num in range(0, len(data)):
            data_list = []
            if isinstance(data[dataset_num], dict):
                data_list = dict_to_list(data, 2)
                ids = list(data[0].keys())
            elif isinstance(data[dataset_num], list):
                data_list = data
                ids = "Returning ids for a list of data has not yet been implemented."

            for index in range(0, largest_dict(data, cols)):
                for dict_num in range(0, cols):
                    if len(data[dict_num]) > index:
                        spacing = separator(data_list, data_list[dict_num][index])
                        print(f"[{index + 1}]\t", data_list[dict_num][index], end=spacing+" \t")
                    else:
                        spacing = " " * find_width(data_list) + " " + "  "*cols
                        print(" "*largest_index + "\t" + spacing, end=" "*largest_index + " \t")
                print()
            return ids


def draw_footer(cols=1, extra_space=0, largest_index=1):
    draw_line(cols, extra_space, largest_index)
    print()


def dict_to_list(data, cols=1):
    data_list = []
    if cols == 1:
        data_list += list(data.values())
    else:
        for dictionary in data:
            data_list.append(list(dictionary.values()))
    return data_list


def draw_table(title, data, cols=1):

    data_list = []
    if cols == 1:
        if isinstance(data, dict):
            list_to_add = list(data.values())
        elif isinstance(data, list):
            list_to_add = data
        data_list += list_to_add
    else:
        for data_col in data:
            list_to_add = []
            if isinstance(data_col, dict):
                list_to_add = list(data_col.values())
            if isinstance(data_col, list):
                list_to_add = data_col
            data_list.append(list_to_add)

    extra_space = largest_space(data_list, title, cols)

    largest_index = len(str(largest_dict(data, cols)))

    draw_header(title, cols, extra_space, largest_index)

    ids = draw_data(data, cols, largest_index)

    draw_footer(cols, extra_space, largest_index)

    return ids


def add_data(data_name, data):

    os.system("clear")

    ids = draw_table(data_name, data)

    added_data = input(f"\nPlease enter the name of the {data_name} you would like to ADD, separated by commas: ")
    print()

    added_data = name_cleaner(added_data)

    if added_data == "":
        return data

    if isinstance(data, list):
        data += added_data
    elif isinstance(data, dict):
        data = update_data(data_name, added_data, data, ids, mode="add")

    return data


def remove_data(data_name, data, preferences):

    os.system("clear")

    ids = draw_table(data_name, data)

    removed_data = input(f"\nPlease enter the number of the {data_name} you would like to REMOVE, separated by commas: ")
    print()

    removed_data = number_cleaner(removed_data)

    if isinstance(data, list):
        for item in removed_data:
            if item < len(data):
                removed_data.remove(item)
    elif isinstance(data, dict):
        data = update_data(data_name, removed_data, data, ids, mode="remove", preferences=preferences)

    return data


def add_entry_menu(data_name, dictionary):

    ids = draw_table(data_name, dictionary)

    added_data = input(f"\nPlease enter the numbers of the {data_name} you would like to ADD/CHANGE, separated by commas: ")
    print()

    added_data = number_cleaner(added_data)

    invalid_data = []
    for item in added_data:
        if item > len(ids):
            invalid_data.append(item)

    for invalid_entry in invalid_data:
        added_data.remove(invalid_entry)
        input(f"Entry out of range. Ignored the following entry: {invalid_entry}\n\nPress ENTER to continue.\n")

    os.system("clear")

    return ids, added_data


def draw_selected_people(people_dict, selected_people, people_ids):
    print("\n(\tPEOPLE SELECTED:\t", end="")
    for index in selected_people:
        user_id = people_ids[index - 1]
        print(f"[{index}] {people_dict[user_id]} \t", end="")
    print(")\n")


def add_entries(dictionary, dictionary_file, people_dict, drinks_dict):

    while True:

        people_ids, added_people = add_entry_menu("people", people_dict)

        if len(added_people) != 0:

            draw_selected_people(people_dict, added_people, people_ids)

            drink_ids, added_drinks = add_entry_menu("drinks", drinks_dict)

            if len(added_people) == len(added_drinks):
                for index in range(0, len(added_people)):
                    people_id = people_ids[added_people[index] - 1]
                    drink_id = drink_ids[added_drinks[index] - 1]
                    dictionary.update({people_id: drink_id})

                save_to_file(dictionary_file, dictionary)
                return dictionary

            else:
                back = input("You must assign a drink for each person. Please add the same number of people as drinks. "
                             "Press ENTER to try again, or [X] to exit: ")
                back = back.strip()
                os.system("clear")
                if back.upper() == "X":
                    print()
                    return dictionary

        else:
            back = input("You must select at least 1 person. Press ENTER to try again, or [X] to exit: ")
            back = back.strip()
            os.system("clear")
            if back.upper() == "X":
                print()
                return dictionary


def remove_entries(dictionary, dictionary_name, people_dict, drinks_dict):

    os.system("clear")

    dictionary_data = ids_to_data(dictionary, people_dict, drinks_dict)
    draw_table(dictionary_name, dictionary_data, 2)
    ids = []
    for user_id in dictionary.keys():
        ids.append(user_id)

    removed_data = input(f"\nPlease enter the numbers of the people whose {dictionary_name} you would like to REMOVE, "
                         f"separated by commas: ")
    print()

    if removed_data.strip() != "" and not removed_data.isalpha():
        removed_data = number_cleaner(removed_data)
    else:
        return dictionary

    if isinstance(dictionary, list):
        for item in removed_data:
            dictionary.remove(item)
    elif isinstance(dictionary, dict):
        data = update_data("preferences", removed_data, dictionary, ids, "remove")

    return data


def exit_screen():

    os.system("clear")

    exit_message = """
Thanks for using our app, hope you have enjoyed the experience!


                    *****************
               ******               ******
           ****                           ****
        ****                                 ***
      ***                                       ***
     **           ***               ***           **
   **           *******           *******          ***
  **            *******           *******            **
 **             *******           *******             **
 **               ***               ***               **
**                                                     **
**       *                                     *       **
**      **                                     **      **
 **   ****                                     ****   **
 **      **                                   **      **
  **       ***                             ***       **
   ***       ****                       ****       ***
     **         ******             ******         **
      ***            ***************            ***
        ****                                 ****
           ****                           ****
               ******               ******
                    *****************

    
Contact us to report bugs, for help or troubleshooting, or just to give us feedback on our app!
    
Email: ahsc1997@gmail.com
Phone: 07803407324
    
Copyright: Eduardo Salazar, 2019"""

    print(exit_message)
    exit()


def update_data_add(input_data, ids, dictionary):
    highest_id = 0
    for item in input_data:
        if highest_id == 0:
            for user_id in ids:
                if user_id > highest_id:
                    highest_id = user_id
        if item != "":
            new_entry = {highest_id + 1: item}
            dictionary.update(new_entry)
            highest_id += 1

    return dictionary


def update_data_remove(data_name, input_data, ids, dictionary, preferences):
    for item in input_data:
        if item > len(ids):
            input_data.remove(item)
            print(f"Entry out of range. Ignored the following entries: {item}")
    for choice in input_data:
        index = choice - 1
        people = list(preferences.keys())
        drinks = list(preferences.values())
        prohibited = people if data_name == "people" else drinks
        if ids[index] in prohibited:
            print("\nERROR: One or more of your selected items cannot be removed. These have been ignored.")
            print("Please delete any items from any active preferences before attempting to delete them.")
            print("Please return to Main Menu and try again once your preferences have been amended.")
        else:
            dictionary.pop(ids[index])

    return dictionary


def update_data(data_name, input_data, dictionary, ids=[], mode="add", preferences={}):

    if mode == "add":
        dictionary = update_data_add(input_data, ids, dictionary)

    elif mode == "remove":
        dictionary = update_data_remove(data_name, input_data, ids, dictionary, preferences)

    save_to_file(data_name, dictionary)

    return dictionary


def edit_menu(possible_options):
    prompt = f"Please enter your selection number. Number [1] to {possible_options[1]}, or [2] to {possible_options[2]}: "
    selected_option = 0
    incorrect_input = True
    while incorrect_input:
        selected_option = draw_menu(possible_options, message=prompt)
        if selected_option <= 0 or selected_option > len(possible_options):
            incorrect_input = True
            input("Please enter the number of your selection only. Press ENTER to try again.")
        else:
            incorrect_input = False

    return possible_options[selected_option]


def round_intro(round_instance, drinks_dict):
    while True:
        os.system("clear")

        ids = draw_table("drinks", drinks_dict)
        brewer_drink_id = round_instance.welcome(ids, drinks_dict)

        if brewer_drink_id == -1:
            continue
        elif brewer_drink_id == 0:
            return round_instance
        else:
            round_instance.add_order(round_instance.brewer_id, brewer_drink_id)
            return round_instance


def round_menu(menu_options, people_dict, drinks_dict):

    round_instance = initialise_round(people_dict)

    if round_instance == 0:
        return

    round_instance = round_intro(round_instance, drinks_dict)

    while round_instance.active:
        os.system("clear")
        orders_dict = ids_to_data(round_instance.orders, people_dict, drinks_dict)

        draw_table("orders", orders_dict, 2)
        editing_choice = draw_menu(menu_options)

        os.system("clear")

        if editing_choice == 1:
            round_instance.orders = add_entries(round_instance.orders, "orders", people_dict, drinks_dict)

        elif editing_choice == 2:
            round_instance.orders = remove_entries(round_instance.orders, "orders", people_dict, drinks_dict)

        elif editing_choice == 3:
            final_order = round_instance.close_round()
            final_order_data = ids_to_data(final_order, people_dict, drinks_dict)
            print("The final order is:\n")
            print(final_order)
            print(drinks_dict)
            print(people_dict)
            draw_table("orders", final_order_data, 2)
            save_to_file("orders", final_order)

        else:
            input("Please enter a number from the following options. Press ENTER to try again.")


def ids_to_data(dictionary, people_dict, drinks_dict):
    drink_data = []
    user_data = []

    for user_id, drink_id in dictionary.items():
        # Could add an exception if drink_id or user_id doesn't match any current value
        drink_data.append(drinks_dict[drink_id])
        user_data.append(people_dict[user_id])
    dictionary_data = [user_data, drink_data]

    return dictionary_data


def initialise_round(people_dict):
    while True:
        os.system("clear")
        ids = draw_table("people", people_dict)
        brewer_chosen = input('''What number is your name?    
(If it is not on the list, type X to return to main menu.)
Name Number: ''')
        if brewer_chosen.upper() == "X":
            return 0
        else:
            brewer_chosen = number_cleaner(brewer_chosen)

        if len(brewer_chosen) == 1:
            brewer_index = brewer_chosen[0] - 1
            if brewer_index < len(ids) and brewer_index != -1:
                brewer_id = ids[brewer_index]
                new_round = Round(people_dict[brewer_id], brewer_id)
                return new_round
            else:
                user_exit = input('''Please make sure your name is on the list, please exit and add it if it is not.
                 
Press ENTER to try again or type X to exit: ''')
                if user_exit.upper() == "X":
                    return 0
        else:
            user_exit = input('''Please only enter one number. Do not include words or special characters (!@£$%%^&*).
    
Press ENTER to go back and try again, or type X to exit: ''')
            if user_exit.upper() == "X":
                return 0


if __name__ == "__main__":
    start_app()
