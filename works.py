#1

def total_bill(amount):
    gst = amount * 0.18
    total = amount + gst
    return total
print(total_bill(5000)) 



def student_result(marks):
    avg = sum(marks) / len(marks)

    if avg >= 90:
        grade = "A"
    elif avg >= 75:
        grade = "B"
    elif avg >= 50:
        grade = "C"
    else:
        grade = "Fail"

    return avg, grade


print(student_result([80, 90, 85]))



def check_vote(age):
    if age >= 18:
        return "Eligible to vote"
    else:
        return "Not eligible"
print(check_vote(20))  




def final_price(price, discount):
    discount_amount = price * (discount / 100)
    return price - discount_amount


print(final_price(1000, 10))  # Output: 900.0




def smallest_number(numbers):
    return min(numbers)
print(smallest_number([5, 2, 8, 1]))  # Output: 1



def count_even(numbers):
    count = 0
    for num in numbers:
        if num % 2 == 0:
            count += 1
    return count
print(count_even([1, 2, 3, 4, 6])) 