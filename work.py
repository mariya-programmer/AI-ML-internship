num =-7
if num>0:
    print("positive number")
elif num<0:
    print("negative number")
else:
    print("zero")

#2

age=18
if age >=18:
    print("eligible to vote")
else:
    print("you are not eligable to vote")

#3

num = int(input("Enter a number: "))

if num % 2 == 0:
    print("Even number")
else:
    print("Odd number")

#4

char="i"

if char in ['a', 'e', 'i', 'o', 'u']:
    print("Vowel")
else:
    print("Consonant")

    #5

a = 8
b = 10

if a > b:
    print("Largest number is:", a)
else:
    print("Largest number is:", b)

#6
a =70
b = 60
c =78

if a > b and a > c:
    print("Largest is:", a)
elif b > c:
    print("Largest is:", b)
else:
    print("Largest is:", c)