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
