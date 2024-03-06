class match:
    def __init__( self ):
        self.b = 1

class test:
    def __init__ (self):
        self.m = match()

t = test()

print(t.m.b)
tmp = t.m
tmp.b = 3
print(t.m.b)

l = t

l.m.b = 4
print(t.m.b)