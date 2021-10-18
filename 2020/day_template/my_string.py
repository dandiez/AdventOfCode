class _str():

    def __init__(self, _string):
        self._str = _string

    def __getitem__(self, item):
        return self._str[item]

    def __setitem__(self, key, value):
        print(self._str, key, value)
        s = str(value)
        if len(s) != 1:
            raise ValueError("Item assignment is only supported if the length of the value is 1.")
        if not (0 <= key < len(self._str)):
            raise KeyError("Cannot replace a character outside of the string")
        self._str = self._str[:key - 1] + s + self._str[key:]
        print("changed to", self._str)
        print(self.__repr__)

    def __getattribute__(self, item):
        print("__getattribute__ called for ", item)
        return super(_str, self).__getattribute__(item)

    def __getattr__(self, item):
        print("__getattr__ called for ", item)
        return super(str, self._str).__getattribute__(item)

    def __str__(self):
        return str.__str__(self._str)

    def __eq__(self, other):
        return str.__eq__(self._str, other)


a = _str("hello world")
print(a.__dict__)
print(dir(a))
print(a)

print(a.upper())

print("just print", a)
print(a[2])

a[3] = "f"

print("a", a)

assert a == "heflo world"
