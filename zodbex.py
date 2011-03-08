from pickle import dump

class Conference(object):
    def __init__(self, name):
        self.name = name
    def capitalize(self):
        return self.name.capitalize()

if __name__ == '__main__':
    pycon = Conference('pycon')
    f = open('data.pck', 'wb')
    s = dump(pycon, f)
    
