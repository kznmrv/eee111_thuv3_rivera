import sqlite3
from tkinter import ttk, messagebox, filedialog

class PlaylistDbSqlite:
    def __init__(self, dbName='Playlist.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Playlist (
                id TEXT PRIMARY KEY,
                title TEXT,
                artist TEXT,
                album TEXT)''')
        self.conn.commit()
        self.conn.close()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()        

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Playlist (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    artist TEXT,
                    album TEXT)''')
        self.commit_close()

    def fetch_playlist(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM Playlist')
        playlist = self.cursor.fetchall()
        self.conn.close()
        return playlist

    def insert_song(self, id, title, artist, album):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO Playlist (id, title, artist, album) VALUES (?, ?, ?, ?)',
                    (id, title, artist, album))
        self.commit_close()

    def delete_song(self, id):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM Playlist WHERE id = ?', (id,))
        self.commit_close()

    def update_song(self, new_title, new_artist, new_album, id):
        self.connect_cursor()
        self.cursor.execute('UPDATE Playlist SET title = ?, artist = ?, album = ? WHERE id = ?',
                    (new_title, new_artist, new_album, id))
        self.commit_close()

    def id_exists(self, id):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM Playlist WHERE id = ?', (id,))
        result = self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def export_csv(self):
        with open(self.csvFile, "w") as filehandle:
            playlist_entries = self.fetch_playlist()
            for entry in playlist_entries:
                print(entry)
                filehandle.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]}\n")
    
    def import_from_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')],
                                                title='Choose a CSV file to import')
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        values = line.strip().split(',')
                        if len(values) == 4:
                            id, title, artist, album = values
                            if not self.db.id_exists(id):
                                self.db.insert_song(id, title, artist, album)
                            else:
                                print(f"Skipping import for existing ID: {id}")
                        else:
                            print(f"Skipping invalid entry: {line}")
                self.add_to_treeview()
                messagebox.showinfo('Success', 'Data imported successfully')
            except Exception as e:
                messagebox.showerror('Error', f'Error importing data: {str(e)}')
        else:
            messagebox.showinfo('Info', 'Import canceled')

def test_PlaylistDb():
    iPlaylistDb = PlaylistDbSqlite(dbName='PlaylistSql.db')

    for entry in range(30):
        iPlaylistDb.insert_song(entry, f'Song{entry}', f'Artist{entry}', f'Album{entry}')
        assert iPlaylistDb.id_exists(entry)

    all_entries = iPlaylistDb.fetch_playlist()
    assert len(all_entries) == 30

    for entry in range(10, 20):
        iPlaylistDb.update_song(f'Song{entry}', f'Artist{entry}', f'New Album{entry}', entry)
        assert iPlaylistDb.id_exists(entry)

    all_entries = iPlaylistDb.fetch_playlist()
    assert len(all_entries) == 30

    for entry in range(10):
        iPlaylistDb.delete_song(entry)
        assert not iPlaylistDb.id_exists(entry) 

    all_entries = iPlaylistDb.fetch_playlist()
    assert len(all_entries) == 20