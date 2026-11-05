def ask_destination():
    check = True
    while check:
        try:
            dest = int(input('''Choose your destination:
1: Delhi Airport
2: Jaipur
Enter the digit corresponding to your choice: '''))
            if dest == 1 or dest == 2:
                check = False
            else:
                print("Please choose amongst 1 or 2 only.")
                print()
        except ValueError:
            print("Invalid Input. Please enter only 1 or 2")
            print()
    if dest == 1:
        dest = "Delhi"
    else:
        dest = "Jaipur"
    return dest

def ask_time_slot():
    check = True
    while check:
        try:
            slot = int(input('''Choose your time slot from the following:
1: Morning
2: Afternoon
3: Evening
4: Night
Enter the digit corresponding to your choice: '''))
            if slot >= 1 and slot <= 4:
                check = False
            else:
                print("Please choose amongst 1, 2, 3 or 4 only.")
                print()
        except ValueError:
            print("Invalid Input. Please enter only amongst 1, 2, 3 or 4")
            print()
    slots = ["Morning", "Afternoon", "Evening", "Night"]
    slot = slots[slot - 1]
    return slot

def ask_year():
    check = True
    while check:
        try:
            year = int(input("Enter your current year. Enter amongst 1, 2, 3, 4 or 5 - corresponding to your year: "))
            if year >= 1 and year <= 5:
                check = False
            else:
                print("Please enter a valid year.")
                print()
        except ValueError:
            print("Invalid Input. Enter amongst 1, 2, 3, 4 or 5 only")
            print()
    return year

def ask_name():
    check_1 = check_2 = check_3 = middle = True
    while check_1:
        fname = input("Enter your first name: ").strip()
        if fname.isalpha():
            fname = fname.capitalize()
            check_1 = False
        else:
            print("Invalid first name input. Please try again")
    
    while check_2:
        mname = input("Enter your middle name. If NA, enter 0: ").strip()
        if mname == "0":
            middle = False
            check_2 = False
        elif mname.isalpha():
            mname = mname.capitalize()
            check_2 = False
        else:
            print("Invalid middle name input. Please try again")
    
    while check_3:
        lname = input("Enter your last name: ").strip()
        if lname.isalpha():
            lname = lname.capitalize()
            check_3 = False
        else:
            print("Invalid last name input. Please try again")
    
    if middle:
        username = fname + " " + mname + " " + lname
    else:
        username = fname + " " + lname
    return username

print("Welcome to the BITS Pilani Cab Service!")
opens = True

while opens:
    try:
        option = int(input('''
-------------------------MENU----------------------------
1) Add a new cab request
2) View all cab requests
3) Quit the application

Choose the option you want to continue with (1, 2 or 3): '''))
        if option < 1 or option > 3:
            print("Choose only from 1, 2 or 3, according to the menu")
            continue
        else:
            opens = False
    except ValueError:
        print("Choose only from 1, 2 or 3, according to the menu")
        continue
    
    if option == 1:
        print()
        destination = ask_destination()
        print()
        timeslot = ask_time_slot()
        print()
        saal = ask_year()
        print()
        user = ask_name()
        print()
        print(f'''Your details have been saved successfully. Verify them below:
Destination: {destination}
Time: {timeslot}
Year of Study: {saal}
Name: {user}''')
    elif option == 2:
        print("Work in Progress")
    else:
        print("Thank you for using our service!")
        break
    
    repeat = True
    while repeat:
        work = input("Do you want to go back to the menu? (Y/N): ")
        if work.capitalize() != "Y" and work.capitalize() != "N":
            print("Invalid input. Please try again")
        elif work.capitalize() == "Y":
            opens = True
            repeat = False
        else:
            repeat = False
            print("Thank you for using our service!")
