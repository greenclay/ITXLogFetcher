__author__ = 'Administrator'

class Pet():
    def __init__(self):
        self.color = "red"

    def nameme(self):
        pass
        # self.name = "bob"

class Dog(Pet):
    name = "bob"
    def __init__(self):
        Pet.__init__(self)


class MyClass:
    static_elem = 123

    def __init__(self):
        self.object_elem = 456

c1 = MyClass()
c2 = MyClass()

print c1.static_elem, c1.object_elem

print c2.static_elem, c2.object_elem

# Nothing new so far ...

# Let's try changing the static element
MyClass.static_elem = 999

print c1.static_elem, c1.object_elem
print c2.static_elem, c2.object_elem


d = Dog()
t = Dog()
t.nameme()
print t.color + " - name: " + t.name
t.name = "cindy"
t.grr = "true"
Dog.name = "ASDF"
print t.color + " - name: " + t.name
print d.name
print t.grr

