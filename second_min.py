list = [1,35,2,67,3,-45,0,12]

min = list[0]
res = min
for tridip in list:
    if tridip <= min:
        res = min
        min = tridip
    elif tridip < res:
        res = tridip

print(min,res)