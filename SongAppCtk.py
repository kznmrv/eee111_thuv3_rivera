from SongDb import PlaylistDb
from src.SongGuiCtk import EmpGuiCtk

def main():
    db = PlaylistDb(init=False, dbName='SongDb.csv')
    app = EmpGuiCtk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()