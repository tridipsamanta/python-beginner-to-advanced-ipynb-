# Sample data
list_of_tuples = [(), (), ('',), ('a', 'b'), ('a', 'b', 'c'), ('d',)]

# Remove empty tuples
filtered_list = [t for t in list_of_tuples if t]

# Print result
print(filtered_list)
