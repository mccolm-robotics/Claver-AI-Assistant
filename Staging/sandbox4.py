entities = {'bar': ['fried', 'chicken', 'crispy']}

print(entities)

if 'foo' in entities:
    entities['foo'].append('pork')
    print(entities['foo'])
else:
    entities['foo'] = ['horse']

print(entities)

for i in range(5):
    print(i)

val = 5
val +=1
print(val)