import tkinter as tk
from tkinter import ttk, messagebox, StringVar, END
from SongDbSqlite import PlaylistDbSqlite

class PlaylistGuiTk(tk.Tk):

    def __init__(self, dataBase=PlaylistDbSqlite('PlaylistAppDb.db')):
        super().__init__()
        self.db = dataBase

        self.title('Playlist Management System')
        self.geometry('1500x500')
        self.config(bg='#161C25')
        self.resizable(False, False)

        self.font1 = ('Arial', 20, 'bold')
        self.font2 = ('Arial', 12, 'bold')

        # Data Entry Form
        # 'ID' Label and Entry Widgets
        self.id_label = self.newCtkLabel('ID')
        self.id_label.place(x=20, y=40)
        self.id_entryVar = StringVar()
        self.id_entry = self.newCtkEntry(entryVariable=self.id_entryVar)
        self.id_entry.place(x=100, y=40)

        # 'Title' Label and Entry Widgets
        self.title_label = self.newCtkLabel('Title')
        self.title_label.place(x=20, y=100)
        self.title_entryVar = StringVar()
        self.title_entry = self.newCtkEntry(entryVariable=self.title_entryVar)
        self.title_entry.place(x=100, y=100)

        # 'Artist' Label and Entry Widgets
        self.artist_label = self.newCtkLabel('Artist')
        self.artist_label.place(x=20, y=160)
        self.artist_entryVar = StringVar()
        self.artist_entry = self.newCtkEntry(entryVariable=self.artist_entryVar)
        self.artist_entry.place(x=100, y=160)

        # 'Album' Label and Entry Widgets
        self.album_label = self.newCtkLabel('Album')
        self.album_label.place(x=20, y=220)
        self.album_entryVar = StringVar()
        self.album_entry = self.newCtkEntry(entryVariable=self.album_entryVar)
        self.album_entry.place(x=100, y=220)

        self.add_button = self.newCtkButton(text='Add Song',
                                onClickHandler=self.add_entry,
                                fgColor='#05A312',
                                hoverColor='#00850B',
                                borderColor='#05A312')
        self.add_button.place(x=50, y=350)

        self.new_button = self.newCtkButton(text='New Song',
                                onClickHandler=lambda:self.clear_form(True))
        self.new_button.place(x=50,y=400)

        self.update_button = self.newCtkButton(text='Update Song',
                                    onClickHandler=self.update_entry)
        self.update_button.place(x=360,y=400)

        self.delete_button = self.newCtkButton(text='Delete Song',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#E40404',
                                    hoverColor='#AE0000',
                                    borderColor='#E40404')
        self.delete_button.place(x=670,y=400)

        self.export_button = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv)
        self.export_button.place(x=980,y=400)

        # Tree View for Database Entries
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#fff',
                        background='#000',
                        fieldlbackground='#313837')

        self.style.map('Treeview', background=[('selected', '#1A8F2D')])

        self.tree = ttk.Treeview(self, height=15)
        self.tree['columns'] = ('ID', 'Title', 'Artist', 'Album')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', anchor=tk.CENTER, width=10)
        self.tree.column('Title', anchor=tk.CENTER, width=150)
        self.tree.column('Artist', anchor=tk.CENTER, width=150)
        self.tree.column('Album', anchor=tk.CENTER, width=150)

        self.tree.heading('ID', text='ID')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Artist', text='Artist')
        self.tree.heading('Album', text='Album')

        self.tree.place(x=360, y=20, width=1000, height=350)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    # new Label Widget
    def newCtkLabel(self, text='CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_BgColor='#161C25'

        widget = ttk.Label(self, 
                        text=text)
        return widget

    # new Entry Widget
    def newCtkEntry(self, text='CTK Label', entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=25

        widget = ttk.Entry(self, textvariable=entryVariable, width=widget_Width)
        return widget

    # new Button Widget
    def newCtkButton(self, text='CTK Button', onClickHandler=None, fgColor='#161C25', hoverColor='#FF5002', bgColor='#161C25', borderColor='#F15704'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=25
        widget_Function=onClickHandler

        widget = ttk.Button(self,
                            text=text,
                            command=widget_Function,
                            width=widget_Width)
       
        return widget

    # Handles
    def add_to_treeview(self):
        songs = self.db.fetch_playlist()
        self.tree.delete(*self.tree.get_children())
        for song in songs:
            print(song)
            self.tree.insert('', END, values=song)

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.id_entryVar.set('')
        self.title_entryVar.set('')
        self.artist_entryVar.set('')
        self.album_entryVar.set('')

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.id_entryVar.set(row[0])
            self.title_entryVar.set(row[1])
            self.artist_entryVar.set(row[2])
            self.album_entryVar.set(row[3])
        else:
            pass

    def add_entry(self):
        id=self.id_entryVar.get()
        title=self.title_entryVar.get()
        artist=self.artist_entryVar.get()
        album=self.album_entryVar.get()

        if not (id and title and artist and album):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.id_exists(id):
            messagebox.showerror('Error', 'ID already exists')
        else:
            self.db.insert_song(id, title, artist, album)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a song to delete')
        else:
            id = self.id_entryVar.get()
            self.db.delete_song(id)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a song to update')
        else:
            id=self.id_entryVar.get()
            title=self.title_entryVar.get()
            artist=self.artist_entryVar.get()
            album=self.album_entryVar.get()
            self.db.update_song(title, artist, album, id)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been updated')

    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.csv')

if __name__ == "__main__":
    app = PlaylistGuiTk()
    app.mainloop()