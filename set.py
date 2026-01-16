a = {1,2,3,4,5,6}
b = {4,5,6,7,8,9}
print(a)
print(b)


a.add(10)
print(a)

b.add(100)
print(b)

a.remove(10)
b.remove(100)
print(a,b)

#set operation .....

print(a.union(b))
print(a.intersection(b))

print(a.difference(b))
print(a.symmetric_difference(b)) 
print(a.isdisjoint(b))  # False

