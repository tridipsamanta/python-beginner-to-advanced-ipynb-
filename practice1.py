# binary search......

n = int(input("Enter how many number you want : "))
arr = []
for i in range(n):
    arr.append(int(input(f"Enter {i+1} element : ")))
key = int(input("Enter the element to search : "))
def binary_search(arr,key):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low+high)//2
        if arr[mid]==key:
            print("Element found at index : ",mid)
            break
        elif arr[mid] < key:
            low = mid + 1
        else:
            high = mid - 1
    else:
        print("Element not found..")
result = binary_search(arr,key)
if result:
    print(result)
