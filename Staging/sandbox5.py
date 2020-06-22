class Test:
    __value = None

    @staticmethod
    def init(value):
        Test.__value = value

    @staticmethod
    def getValue():
        return Test.__value

x = Test()
print(x.getValue())
x.init("hello world")
print(x.getValue())

