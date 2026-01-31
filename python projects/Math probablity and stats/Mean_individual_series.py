n = int(input('Enter number of Data values : '))
arr = []
for i in range(n):
    arr.append(int(input('Enter values : ')))
sum = 0
for j in arr:
    sum += j
print('Mean = ',sum/n)