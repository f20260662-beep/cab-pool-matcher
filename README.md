# Cab Pool Matcher

A command-line app that collects cab ride requests from students and matches them with cabs going to the same destination at the same time. When seats are short, senior students get priority.

## Requirements

- Python 3. No outside packages are needed.

## How to run

1. Put `main.py` and `cabs.json` in the same folder.
2. Open a terminal in that folder and run:

   ```bash
   python main.py
   ```

## Menu

1. Add a new cab request: enter destination, time slot, year and name.
2. View all cab requests: see waiting students and all cabs (open and left).
3. Find Matches: preview who would get a seat in each open cab. Nothing changes.
4. Dispatch Cab: send one open cab for a chosen trip with the students waiting for it.
5. Quit.

## The cab file (`cabs.json`)

A list of cabs. Each cab has four fields:

```json
[
  {"driver": "Ramesh", "seats": 4, "dest": "Delhi", "slot": "Morning"}
]
```

- `driver`: the driver's name
- `seats`: a whole number from 1 to 4
- `dest`: `Delhi` or `Jaipur`
- `slot`: `Morning`, `Afternoon`, `Evening` or `Night`

Cabs are used in the order they appear in the file. Entries with missing required fields or invalid seat counts, destinations or time slots are skipped with a warning. A missing file or invalid JSON syntax starts the app with no cabs and a message. Other validation limitations are listed below.

## How do matching and priority work?

The program has 8 priority queues, all kept in a dictionary called `queue`. Each heap corresponds to one of the 8 combinations of destination and time slot. A new request is added to its respective heap, but is not given a seat immediately.

I used Python's `heapq` module. Since `heappop()` removes the smallest entry, and I needed to select the highest year first, I stored the negative value of the year. Each request is stored as a tuple: `(-year, counter, request)`. Tuples compare index 0 first and only compare index 1 when there is a tie at index 0. The heap is not a fully sorted list; it keeps the smallest entry at the root.

The counter tells me the order in which a request was made. It gives each request a unique number, so same-year requests always have a definite order. `datetime.now()` can include microseconds, but timestamps alone do not guarantee uniqueness. I still use `datetime` to display the request time, formatted to seconds, when Option 2 is chosen.

## Option 3 vs Option 4

Option 3 is Find Matches. It shows who would be assigned to each open cab if the cabs were dispatched in file order, before any new requests were made. However, this is just a preview: no student is actually assigned a seat, and no cab leaves.

Option 4 is Dispatch Cab, which uses the actual `queue` dictionary. It chooses the first open cab matching the destination and time slot entered by me. If students are waiting, it removes up to the cab's capacity from the queue, adds them to the passenger list, and marks that one cab as having left.

## How does Find Matches keep the actual queue unchanged?

For Find Matches, I made another dictionary called `preview`, and copied each heap using `j.copy()`. Just assigning the same heap to another dictionary would still refer to the original list, so removing students from it would also change the actual queue.

Both Find Matches and Dispatch Cab use the same `pick_students()` function. The difference is that Find Matches passes the copied queues, while Dispatch Cab passes the actual queues.

Cabs are checked in the order they appear in the JSON file. If two cabs have the same destination and time slot, they pick students from the same copied heap one after another. Hence, the same student is not shown in two different cabs.

## Tricky Situations

### 1. What if a cab is only partially filled?

A cab does not have to be full before leaving. If a cab has 4 seats, but only 2 students are waiting for that trip, it leaves with those 2 students.

However, if no students are waiting, a message is shown and the cab remains open. Once a cab leaves, no more students can be added to it, even if it had empty seats.

### 2. What if no cabs are left?

If all cabs for a destination and time slot have already left, the program shows a message when I try to dispatch another cab for that trip.

The students are not removed from the queue. New requests can still be added, and they remain waiting during the current run of the program. Option 2 shows these requests, and Find Matches shows that they cannot currently be assigned a cab.

### 3. What if two students are in the same year?

If two students have the same year, their negative year values are also equal. Python then compares the next value in the tuple, which is the counter.

The student who requested first has a smaller counter, so that student gets a seat first. Since every request has a unique counter, Python never needs to compare the request objects themselves.

### 4. What happens with 1,000 requests?

For these explanations, let `n` be the number of students waiting for one particular trip, `N` be the total number of waiting students, and `C` be the number of cabs.

**Adding one request: O(log n)**

A new request is added using `heapq.heappush()`. The entry may need to move up the heap to reach its correct position. The height of the heap grows logarithmically, so this takes O(log n) time in the worst case. A binary heap has at most twice as many nodes on each successive level, so its height is proportional to log base 2 of n. A new entry starts at the bottom and, in the worst case, moves up to the root by comparing with its parent at each level. No branches are removed; the entry just moves up one path. Hence, there are O(log n) levels to cross. The logarithm's base does not change the Big-O classification, since changing the base only introduces a constant factor.

**Adding all 1,000 requests: O(N log N)**

My program adds requests individually. In the worst case, all students request the same trip, so each request is added to the same growing heap.

Hence, adding N requests takes O(N log N) time in the worst case. For this example, N is 1,000.

**Selecting students for one cab: O(log n)**

Each `heapq.heappop()` takes O(log n) time. A cab can take at most 4 students, so there are at most 4 removals.

This gives O(4 log n), which is written as O(log n), since 4 is a constant.

**Finding an open cab: O(C)**

The program checks the cab list one cab at a time. In the worst case, it checks every cab before finding a suitable one, or finding that none are available. Hence, this takes O(C) time.

**The complete dispatch operation: O(C + log n)**

Dispatch first searches for an open cab, and then selects up to 4 students from the relevant heap. Combining these steps gives O(C + log n).

These complexities describe the main operations, excluding the time spent entering input and printing output.

## Why I used JSON

I used JSON for the cab file because it is readable and lets me store each cab's details using named fields. I can add or change cabs without changing the Python code.

Python also has a built-in `json` module, so no outside packages are required.

## Current Limitations

The program currently does not save requests or cab departure details between runs. These are kept only in memory. Once the program closes, they are lost, and the next run loads all cabs as empty and open again.

The cab-file validation also has some limitations. Although missing fields and invalid seat counts, destinations and time slots are checked, some incorrectly structured JSON can still cause an error. Driver names and Boolean values for seats also need stricter validation.

For student names, the program currently accepts only letters in each name field. Hence, names containing hyphens or apostrophes are not accepted. A middle name can be skipped by entering `0`.