def sum_of_n(n):
    if(n==1):
        return 1
    else:
        return sum_of_n(n-1)+n
    
n = int(input("Enter a positive number : "))
print(sum_of_n(n))