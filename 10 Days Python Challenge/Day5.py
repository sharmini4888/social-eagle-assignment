task=["eat breakfast","do exercise","study python","take a nap"]
print("Today's Tasks:", task)
task.append("read a book")
print("Updated Tasks:", task)
for t in task:
    print("-", t)
    if t=="study python":
        print("  (Important Task!)") 
print("lenght of task", len(task))   
print("count of do exercise:", task.count("do exercise"))
print("index of take a nap:", task.index("take a nap"))
print("Is 'go shopping' in tasks?", "take a nap" in task)
for i in task:
    if i=="take a nap":
        task.pop(task.index(i))
print("Tasks after removing 'take a nap':", task)