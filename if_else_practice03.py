p1 ="Make a lot of money"
p2 = "buy now"
p3 = "subscribe this"
p4 = "click this"

mes = input("Enter a messege : ")

if((p1 in mes) or (p2 in mes) or (p3 in mes ) or (p4 in mes)): print("this is a spam messege")
else : print("this is not a spam messege")