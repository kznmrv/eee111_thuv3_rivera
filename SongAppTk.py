from SongDb import PlaylistDb
from SongGuiTk import PlaylistGuiTk

def main():
    db = PlaylistDb(init=False, dbName='SongDb.csv')
    app = PlaylistGuiTk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()