a = ['a', 'b', 'c']
b = [1, 2, 3]
c = []

for i, j in zip(a, b):
    d = {}
    d['name'] = i
    d['count'] = j
    c.append(d)
print(c)
