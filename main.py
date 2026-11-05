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
    print("Your destination has been saved successfully. You had chosen: ", end="")
    if dest == 1:
        print("Delhi Airport")
        dest = "Delhi"
    else:
        print ("Jaipur")
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
    print("Your time slot has been saved successfully. You had chosen: ", end="")
    slots = ["Morning", "Afternoon", "Evening", "Night"]
    slot = slots[slot - 1]
    print(slot)
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
    print(f"Your year has been saved successfully. You had chosen: Year {year}")
    return year

print(ask_destination(), ask_time_slot(), ask_year())