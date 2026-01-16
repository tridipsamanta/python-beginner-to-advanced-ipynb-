info = {
    "tridip" : 100,
    "sayan":90,
    "list" : [1,2,3,4],
     
}
print(info.keys())
print(info.values())
print(info.items())
info.update({'age':20,'gender':'male'})
print(info)
tridip = info.copy()
print(tridip)