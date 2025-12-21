'''
students={"sharmini":25,"kavi":24,"anju":23}
for name, age in students.items():
    print(name,":",age)
    '''
    
fruits = ["apple", "banana", "mango"]
vegetables = ["carrot", "potato", "onion"]

fruit_veg_map = {}

for fruit, veg in zip(fruits, vegetables):
    fruit_veg_map[fruit] = veg

print(fruit_veg_map)

