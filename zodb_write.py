from persistent import Persistent

class Conference(Persistent):
    def __init__(self, name, year):
        self.name = name
        self.year = year
    def title(self):
        return self.name.capitalize()

if __name__ == '__main__':
    import transaction
    from ZODB.FileStorage import FileStorage
    from ZODB.DB import DB
    fs = FileStorage('data.fs')
    db = DB(fs)
    conn = db.open()
    root = conn.root()
    pycon = Conference('pycon', 2011)
    print pycon.title(), pycon.year
    root['pycon'] = pycon
    transaction.commit()
