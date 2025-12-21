def add(a, b):
    return a + b

def subtract(a, b):
    return a - b  

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Cannot divide by zero"
    return a / b

def modulus(a, b):
    if b == 0:
        return "Error: Cannot divide by zero"
    return a % b

def calculator():
    print("\n=== Simple Calculator ===")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Modulus")
    print("6. Exit")
    
    choice = input("Enter your choice (1-6): ")
    
    if choice == "6":
        print("Thank you for using calculator!")
        return False
    
    if choice in ["1", "2", "3", "4", "5"]:
        a = int(input("Enter first number: "))
        b = int(input("Enter second number: "))
        
        if choice == "1":
            print(f"Result: {a} + {b} = {add(a, b)}")
        elif choice == "2":
            print(f"Result: {a} - {b} = {subtract(a, b)}")
        elif choice == "3":
            print(f"Result: {a} * {b} = {multiply(a, b)}")
        elif choice == "4":
            print(f"Result: {a} / {b} = {divide(a, b)}")
        elif choice == "5":
            print(f"Result: {a} % {b} = {modulus(a, b)}")
        return True
    else:
        print("Invalid choice!")
        return True

# Main program
if __name__ == "__main__":
    while calculator():
        pass