d = {'a':10,'b':20,'c':30,'d':40,'e':50,'f':60,'g':70,'h':80,'i':90,'j':100}
b = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10}
d.update(b)
print(d)    

# using dictionary unpacking
a = {'a':10,'b':20,'c':30,'d':40,'e':50,'f':60,'g':70,'h':80,'i':90,}
t = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,}
merged_dict = {**a, **t}
print(merged_dict)
     