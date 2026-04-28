nums = [10, 20, 30, 20, 40]
count_20 = nums.count(20)
nums.remove(20)
nums.append(50)
print("Count:", count_20)
print("Updated List:", nums)

data = [5, 10, 15, 20, 25]

print("Maximum:", max(data))
print("Minimum:", min(data))
print("Sum:", sum(data))

items = [1, 2, 3]

# Add two elements
items.append(4)
items.append(5)

# Remove last element
items.pop()


items.reverse()

print("Final List:", items)
student = {"A": 50, "B": 60}

student["C"] = 70
student["A"] = 80
print("Values:", student.values())
print("Updated Dictionary:", student)