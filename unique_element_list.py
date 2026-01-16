list = [3,3,2,5,6,6,1,1,2,5,7,8,9,56]
res = []
for i in list:
    if i not in res:
        res.append(i)
print(res)
