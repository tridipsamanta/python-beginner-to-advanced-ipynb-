sample_list = [(10,20,40),(40,50,60),(70,80,90)]

updated_list = [t[:-1] + (100,) for t in sample_list]
print(updated_list)