class Foo:
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return 'Foo instance id: {}'.format(self.id)

class Bar:
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return 'Bar instance id: {}'.format(self.id)

class Baz:
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return 'Baz instance id: {}'.format(self.id)

foo_1 = Foo("to go")
foo_2 = Foo("to clean")
foo_3 = Foo("to avoid")
foo_4 = Foo("to destroy")
bar_1 = Bar("the bathroom")
bar_2 = Bar("the kitchen")
bar_3 = Bar("the bedroom")
bar_4 = Bar("the basement")
bar_5 = Bar("the garage")

my_dictionary = {Foo: [foo_1, foo_2, foo_3, foo_4], Bar: [bar_1, bar_2, bar_3, bar_4, bar_5]}

# for model_type in my_dictionary:
#     for entity in my_dictionary[model_type]:
#         print(entity.printID())

if Foo in my_dictionary:
    for entity in my_dictionary[Foo]:
        print(entity)
    my_dictionary[Foo].append(Foo("to dirty"))
    for entity in my_dictionary[Foo]:
        print(entity)

if Baz in my_dictionary:
    print("Should not see this")
    for entity in my_dictionary[Baz]:
        print(entity)
else:
    my_dictionary[Baz] = [Baz("big test")]


print("\nNow testing for Baz")
if Baz in my_dictionary:
    for entity in my_dictionary[Baz]:
        print(entity)
for unit in my_dictionary:
    print(unit)


