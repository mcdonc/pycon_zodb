from pickle import dump

class Conference(object):
    def __init__(self, name, year):
        self.name = name
        self.year = year
    def title(self):
        return self.name.capitalize()

if __name__ == '__main__':
    pycon = Conference('pycon', 2011)
    print pycon.title(), pycon.year # Pycon 2011
    f = open('data.pck', 'wb')
    pycon = dump(pycon, f)
    
