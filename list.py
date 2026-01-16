fruits = ['apple', 'banana']
fruits.append('cherry')
print(fruits)  # ['apple', 'banana', 'cherry']

fruits.insert(1, 'orange')
print(fruits)  # ['apple', 'orange', 'banana', 'cherry']

fruits.remove('banana')
print(fruits)  # ['apple', 'orange', 'cherry']

fruits.pop()       # removes 'cherry'
fruits.pop(0)      # removes 'apple'

numbers = [3, 1, 4, 2]
numbers.sort()
print(numbers)  # [1, 2, 3, 4]

numbers.reverse()
print(numbers)  # [4, 3, 2, 1]
names = ['Alice', 'Bob', 'Charlie']
print(names.index('Bob'))  # 1
nums = [1, 2, 2, 3, 2]
print(nums.count(2))  # 3
a = [1, 2]
b = [3, 4]
a.extend(b)
print(a)  # [1, 2, 3, 4]
