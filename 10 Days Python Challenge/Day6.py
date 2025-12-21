# Dictionary 1: Student marks
dict1 = {
    "A": 85,
    "B": 78,
    "C": 92
}

# Dictionary 2: Student grades
dict2 = {
    "Alice": "B",
    "Bob": "C",
    "Charlie": "A",
    "Diana": "A+"
}

print("Dictionary 1:", dict1)
print("Dictionary 2:", dict2)

# Method 1: Using update() - modifies dict1
dict1_copy = dict1.copy()
dict1_copy.update(dict2)
print("\nAfter update():", dict1_copy)

# Method 2: Using ** operator (Python 3.5+)
merged = {**dict1, **dict2}
print("Merged with **:", merged)

# Method 3: Using | operator (Python 3.9+)
merged2 = dict1 | dict2
print("Merged with |:", merged2)

# Method 4: Manual merge with loop
merged3 = {}
for key, value in dict1.items():
    merged3[key] = value
for key, value in dict2.items():
    merged3[key] = value
print("Merged with loop:", merged3)