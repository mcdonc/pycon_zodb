from pickle import load, dump

class Conference(object):
    def __init__(self, name, year):
        self.name = name
        self.year = year
    def title(self):
        return self.name.capitalize()

if __name__ == '__main__':
    f = open('data.pck', 'rb')
    pycon = load(f)
    print pycon.title(), pycon.year
    pycon.year = 2012
    out = open('data.pck', 'wb')
    dump(pycon, out)
    
    
