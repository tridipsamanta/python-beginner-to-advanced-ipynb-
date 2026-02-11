#positional arguments
def add(a,b):
    print(a+b)

add(10,2)

#keword arguments
def student(name,roll):
    print(name,roll)
student(roll=2616,name='Tridip')
# default arguments
def show(name='User'):
    print('Hello',name)
show()
show('Tridip')
#variable length arguments
def total(*numbers):
    sum = 0
    for i in numbers:
        sum += i
    print(sum)
total(10,20,30,40)
#keyword variable length arguments
def details(**info):
    for key,value in info.items():
        print(key,value)
details(name='Tridip',roll=2616,dept='BCA')