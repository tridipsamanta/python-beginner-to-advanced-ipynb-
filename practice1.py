# binary search......

n = int(input("Enter how many number you want : "))
arr = []
for i in range(n):
    arr.append(int(input(f"Enter {i+1} element : ")))
def selection_sort(arr):
    for i in range(n):
        min_index = i
        for j in range(i+1,n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i],arr[min_index] = arr[min_index],arr[i]
    return arr

result = selection_sort(arr)

if result :
    print(result)
            
