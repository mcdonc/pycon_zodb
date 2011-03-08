from persistent import Persistent

class Conference(Persistent):
    def __init__(self, name, year):
        self.name = name
        self.year = year
    def title(self):
        return self.name.capitalize()

if __name__ == '__main__':
    from ZODB.FileStorage import FileStorage
    from ZODB.DB import DB
    fs = FileStorage('data.fs')
    db = DB(fs)
    conn = db.open()
    root = conn.root()
    pycon = root['pycon']
    print pycon.title()
    
