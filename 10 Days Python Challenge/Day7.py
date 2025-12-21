set1 = {"cherry", "mango", "grapes"}
set2 = {"mango", "banana", "orange"}

print("Set 1:", set1)
print("Set 2:", set2)   

common = set1 & set2
print("Common elements:", common)
all_elements = set1 | set2
print("All unique elements:", all_elements)
fro = frozenset(set1)
print("Frozenset:", fro)

set1.add("kiwi")
print("Set 1 after adding 'kiwi':", set1)
set2.remove("banana")
print("Set 2 after removing 'banana':", set2)
set1.update(["peach", "plum"])
print("Set 1 after updating with 'peach' and 'plum':", set1)
set2.discard("orange")
print("Set 2 after discarding 'orange':", set2)
symmetric_diff = set1.symmetric_difference(set2)
print("Symmetric difference between Set 1 and Set 2:", symmetric_diff)
for item in set1:
    print("-", item)
print(fro)   
for item in fro:
    print("*", item)    
    if item=="mango":
        print("  (Found mango in frozenset!)")
        frozenset_added = frozenset.union(fro, {"kiwi"})
        print("Frozenset after attempting to add 'kiwi':", frozenset_added)

