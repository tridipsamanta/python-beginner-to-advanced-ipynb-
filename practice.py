n = int(input("Enter array length : "))
arr = []
for i in range(n):
    print(f"Enter {i+1} element : ")
    arr.append(int(input()))
key = int(input("Enter key element : "))

def linear_recursive(arr,key,index):
     if index == len(arr):
          return -1
     if arr[index] == key:
          return index
     return linear_recursive(arr,key,index+1)
print("found at : ",linear_recursive(arr,key,0))
     