from persistent import Persistent
from repoze.folder import Folder

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
    folder = Folder()
    root = conn.root()
    root['folder'] = folder
    pycon = Conference('pycon', 2011)
    folder['pycon'] = pycon
    print pycon.title(), pycon.year
    transaction.commit()
