while True:
    a = int(input('Enter first number: '))
    b = int(input('Enter second number : '))
    print('Choose an operator : ')
    print('1 for - add(+)')
    print('2 for - subtraction(-)')
    print('3 for - multiplication(X)')
    print('4 for - division(/)')
    symbol = int(input('Enter (1/2/3/4) : '))
    def calculation(a,b,s):
        if s==1:
            return a+b
        elif s==2:
            return a-b
        elif s==3:
            return a*b
        elif s==4:
            return a/b
        else:
            return 
    
    result = calculation(a,b,symbol)
    if result:
        print('Output : ',result)
        continue
    else:
        print('Invalid input , try again...')
    
