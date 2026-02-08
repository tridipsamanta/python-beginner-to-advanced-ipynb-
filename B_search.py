def binary_search(arr,key):
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