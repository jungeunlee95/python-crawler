def f(x):
    return x**2


it = map(lambda x: print(x, end=' '), [1, 2, 3, 4])
# next(it)
# next(it)
# next(it)
# next(it)

lst = list(map(lambda x: x**2, [1, 2, 3, 4]))
print(lst)
print('\n===========================')

list(map(lambda x: print(x, end=' '), [1, 2, 3, 4]))

print('\n-----------filter--------------')
lst = list(filter(lambda x:x%2==0, [1,2,3,4]))
print(lst)