def binary(key, arr):
    arr.sort() 
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == key:
            print("Element found at position:", mid)
            return
        elif arr[mid] < key:
            low = mid + 1
        else:
            high = mid - 1

    print("Element is not found in the array.")

# Main program
n = int(input("Enter array size: "))
arr = []
for i in range(n):
    value = int(input("Enter array element: "))
    arr.append(value)

key = int(input("Enter element to search: "))
binary(key, arr)
