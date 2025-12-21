"""
marks=int(input("Enter the marks: "))

    

if marks > 90:
       print ("grade = A")
elif marks > 80:
        print("grade = B")
elif marks > 70:
        print("C")
elif marks == 70:
        print("D")
else:
        print("Detained")
        
"""
"""
age=int(input("Enter the age: "))
voteridno=input("Enter the voter id no: ")
if age >= 18:
    if voteridno !="":
        print("Eligible to vote")
    elif voteridno =="":
        print("Voter id no is mandatory")   
else:
    print("Not eligible to vote")
    """
age=int(input("Enter the age: "))
gender=(input("enter the gender:"))
if age >= 18:
    line="female" if gender=="F" else "Male" if gender =="M" else "other"
    print("Eligible to vote as",line)
else:
    print("Not eligible to vote")