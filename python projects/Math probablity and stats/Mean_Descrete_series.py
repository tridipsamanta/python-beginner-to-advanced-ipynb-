n = int(input('Enter number of Data values : '))

arr = []
f = []

for i in range(n):
    arr.append(int(input('Enter values : ')))

for i in range(n):
    f.append(int(input('Enter frequency : ')))

total_f = 0
for t in f:
    total_f += t

sum_fx = []
for i in range(n):
    sum_fx.append(arr[i] * f[i])

mean = 0
for s in sum_fx:
    mean += s

print('Mean =', mean / total_f)
