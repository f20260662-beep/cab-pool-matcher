from datetime import datetime
import json
import heapq

WIDTH = 110
queue = {}
for i in ["Delhi", "Jaipur"]:
    for j in ["Morning", "Afternoon", "Evening", "Night"]:
        queue[(i, j)] = []

def banner(title):
    return f" {title} ".center(WIDTH, "-")

class RideRequest:
    count = 0
    
    def __init__(self, name, dest, slot, year):
        self.name = name
        self.dest = dest
        self.slot = slot
        self.year = year
        time = datetime.now()
        self.timeshow = time.strftime("%d-%m-%Y %H:%M:%S")
        self.counter = RideRequest.count + 1
        RideRequest.count += 1
    
    def __str__(self):
        return f"#{self.counter} | Name: {self.name} | Destination: {self.dest} | Time Slot: {self.slot} | Year {self.year} | Requested at {self.timeshow}"

class Cab:
    def __init__(self, driver, seats, dest, slot):
        self.driver = driver
        self.seats = seats
        self.has_left = False
        self.dest = dest
        self.slot = slot
        self.passengers = []
    
    def __str__(self):
        left = "Yes" if self.has_left else "No"
        return f"Driver: {self.driver} | Destination: {self.dest} | Time Slot: {self.slot} | Seats Taken: {len(self.passengers)}/{self.seats} | Has Left?: {left}"

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

def load_cabs():
    cabs = []
    try:
        with open("cabs.json") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("File Error: File not found")
        return cabs
    except json.JSONDecodeError:
        print("JSON Error: Check for any misplaced commas in the file")
        return cabs
    
    for i in data:
        try:
            if not isinstance(i["seats"], int) or i["seats"] < 1 or i["seats"] > 4:
                print(f"Cab entry with Driver - {i['driver']} has invalid number of seats. Entry Skipped")
                continue
            elif i["dest"] != "Delhi" and i["dest"] != "Jaipur":
                print(f"Cab entry with Driver - {i['driver']} has invalid Destination. Entry Skipped")
                continue
            elif i["slot"] not in ["Morning", "Afternoon", "Evening", "Night"]:
                print(f"Cab entry with Driver - {i['driver']} has invalid Time Slot. Entry Skipped")
                continue
            else:
                cab = Cab(i["driver"], i["seats"], i["dest"], i["slot"])
                cabs.append(cab)
        except KeyError:
            print("A cab entry had invalid input, so it was skipped. Check for any blank entries")
            continue
    return cabs

def pick_students(cab, queue):
    free = cab.seats - len(cab.passengers)
    chosen = []
    while queue[(cab.dest, cab.slot)] and len(chosen) < free:
        chosen.append(heapq.heappop(queue[(cab.dest, cab.slot)])[2])
    return chosen

def find_matches(waiting, cabs):
    preview = {}
    for i, j in queue.items():
        preview[i] = j
    cab_open = False

    print(banner("MATCH PREVIEW"))
    print()
    for cab in cabs:
        if not cab.has_left:
            cab_open = True
            chosen = pick_students(cab, preview)
            for request in chosen:
                claimed.add(request.counter)
            print("CAB DETAILS: " + str(cab))
            print()
            if not chosen:
                print("No student waiting for this trip.")
            else:
                print("This cab would take the Passengers:")
                for ind, passenger in enumerate(chosen, 1):
                    print(f"{ind}. {passenger.name} - Year {passenger.year}")
            print("----------x" * int(WIDTH / 11))
    if not cab_open:
        print("No open cabs available right now")

    print(banner("USERS STILL AWAITING"))
    print()
    awaiting = False
    for request in all_waiting(preview):
        print(str(request))
        print()
        awaiting = True
    if not awaiting:
        print("No students awaiting")

def all_waiting(queue):
    pairs = []
    for heap in queue.values():
        for entry in heap:
            pairs.append((entry[1], entry[2]))
    pairs.sort()
    return [request for counter, request in pairs]

def dispatch_cab(queue, cabs):
    print("You will now be dispatching a cab matching the Destination and Time Slot you enter.\n")
    dest = ask_destination()
    slot = ask_time_slot()
    cab_found = False
    for cab in cabs:
        if dest == cab.dest and slot == cab.slot and not cab.has_left:
            cab_found = True
            chosen = pick_students(cab, queue)
            if not chosen:
                print(f"For cab with Driver: {cab.driver}, no students have applied")
                return
            else:
                for i in chosen:
                    cab.passengers.append(i)
                print(f"""Cab with details: {str(cab)}
left with the students:""")
                for i in cab.passengers:
                    print(f"{i.name} - Year {i.year}")
                cab.has_left = True
                return
        
    if not cab_found:
        print("No cab found for the following filters.")
    
print("Welcome to the BITS Pilani Cab Service!")
opens = True
cabs = load_cabs()

while opens:
    try:
        option = int(input(f'''
{banner("MENU")}
1) Add a new cab request
2) View all cab requests
3) Find Matches
4) Dispatch Cab
5) Quit the application
   
Choose the option you want to continue with (1, 2, 3, 4 or 5): '''))
        if option < 1 or option > 5:
            print("Choose only from 1, 2, 3, 4 or 5, according to the menu")
            continue
        else:
            opens = False
    except ValueError:
        print("Choose only from 1, 2, 3, 4 or 5, according to the menu")
        continue
    
    if option == 1:
        print()
        destination = ask_destination()
        print()
        timeslot = ask_time_slot()
        print()
        year = ask_year()
        print()
        user = ask_name()
        print()
        print(f'''Your details have been saved successfully. Verify them below:
Destination: {destination}
Time: {timeslot}
Year of Study: {year}
Name: {user}''')
        user_details = RideRequest(user, destination, timeslot, year)
        heapq.heappush(queue[(user_details.dest, user_details.slot)], (-user_details.year, user_details.counter, user_details))
        
    elif option == 2:
        waiting = all_waiting(queue)
        print(banner("CAB REQUESTS") + "\n")
        if not waiting:
            print("No cab requests for now!")
        else:
            for i in waiting:
                print(str(i) + "\n")
        print()
        print(banner("CABS AVAILABLE") + "\n")
        avail = 0
        for i in cabs:
            if not i.has_left:
                print(str(i) + "\n")
                avail += 1
        if avail == 0:
            print("None yet!\n")
            
        print()
        print(banner("CABS LEFT") + "\n")
        left = 0
        for i in cabs:
            if i.has_left:
                print(str(i) + "\n")
                left += 1
        if left == 0:
            print("None yet!\n")
    
    elif option == 3:
        find_matches(queue, cabs)
    
    elif option == 4:
        dispatch_cab(queue, cabs)
        
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


