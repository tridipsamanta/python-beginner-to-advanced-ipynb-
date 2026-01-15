def insertion_sort_recursive(arr,n):
    if n<=1:
        return
    
    insertion_sort_recursive(arr,n-1)

    key = arr[n-1]
    j = n-2

    while j>= 0 and arr[j] > key:
        arr[j+1] = arr[j]
        j -= 1
    arr[j+1] = key


n = int(input("Enter array length : "))
arr = []
print("Enter elements : ")
for i in range(n):
    arr.append(int(input()))

insertion_sort_recursive(arr,n)
print(arr)