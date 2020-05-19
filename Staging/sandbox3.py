from random import randint

# Exercise in creating alternate constructors
# https://stackoverflow.com/questions/682504/what-is-a-clean-pythonic-way-to-have-multiple-constructors-in-python
# https://stackoverflow.com/questions/136097/difference-between-staticmethod-and-classmethod

class Foo:
    my_var = None
    def __init__(self, num_holes):
        print(num_holes," holes in my cheese")
        print("my var: ", self.my_var)

    @classmethod
    def fromRandom(cls):
        cls.my_var = 5
        return cls(randint(0, 100))


# test = Foo.fromRandom()

print(Foo.my_var)
Foo.my_var = 10
print(Foo.my_var)