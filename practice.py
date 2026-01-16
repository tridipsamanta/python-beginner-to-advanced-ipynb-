
#1 .....
my_list = [10,20,30]

#2....
list1 = []
n = int(input("How many number : "))
for i in range(n):
    num = input("Enter elements : ")
    list1.append(num)
print(list1)

#3...
list2 = [1,2,3,4,5]
print(len(list2))

#4....
list4 = [10,20,30,40,50]
print('First element : ',list4[0],'Last element : ',list4[-1])
#5.....
list3 = ['mango','banana','apple','orrange']
fruit = 'mango'
print(fruit in list3)

#6.....
list5 = [1,2,3,4,5,6,7,8,9,10]
sum = 0
for i in list5:
    sum += i
print('Sum of all element in. the list : ',sum)

#7.......
list5 = [1,2,3,4,5,6,7,8,9,10]
print("Largest element : ",max(list5))

#8...
list5 = [1,2,3,4,5,6,7,8,9,10]
print("Largest element : ",min(list5))

#9.....
list5 = [1,2,3,4,5,6,7,8,9,10]
for i in list5:
    if i%2 == 0:
        print('even : ',i)
    elif i%2 != 0:
        print('odd : ',i)

#10........
list5 = [1,2,3,4,5,6,7,8,9,10]
print('reverse list print : ',list5[::-1])

#11..
list5 = [10,3,5,7,9,2,8]
print('reverse list print : ',list5[::-1])
