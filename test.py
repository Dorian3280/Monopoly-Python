import timeit
globals = {'a': ['a','b','c', 'd'], 'i': [0, 2]}
print(list(map(globals['a'].__getitem__, globals['i'])))
print([globals['a'][z] for z in globals['i']])

# print(min(timeit.repeat("map(a.__getitem__, i)", "", number=1000000, globals = {'a': ['a','b','c', 'd'], 'i': [0, 2]})))
# print(min(timeit.repeat("[a[z] for z in i]", "", number=1000000, globals = {'a': ['a','b','c', 'd'], 'i': [0, 2]})))
