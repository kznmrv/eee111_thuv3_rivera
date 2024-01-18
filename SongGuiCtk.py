import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from SongDbSqlite import PlaylistDbSqlite

class EmpGuiCtk(customtkinter.CTk):

    def __init__(self, dataBase=PlaylistDbSqlite('AppDb.db')):
        super().__init__()
        self.db = dataBase

        self.title('Employee Management System')
        self.geometry('1500x500')
        self.config(bg='#161C25')
        self.resizable(False, False)

        self.font1 = ('Arial', 20, 'bold')
        self.font2 = ('Arial', 12, 'bold')

        # Data Entry Form
        # 'ID' Label and Entry Widgets
        self.id_label = self.newCtkLabel('ID')
        self.id_label.place(x=20, y=40)
        self.id_entry = self.newCtkEntry()
        self.id_entry.place(x=100, y=40)

        # 'Name' Label and Entry Widgets
        self.name_label = self.newCtkLabel('Name')
        self.name_label.place(x=20, y=100)
        self.name_entry = self.newCtkEntry()
        self.name_entry.place(x=100, y=100)

        # 'Role' Label and Combo Box Widgets
        self.role_label = self.newCtkLabel('Role')
        self.role_label.place(x=20, y=160)
        self.role_cboxVar = StringVar()
        self.role_cboxOptions = ['SW-Engineer', 'HW-Engineer', 'FW-Engineer', 'Layout-Engineer', 'Project-Manager', 'System-Architect']
        self.role_cbox = self.newCtkComboBox(options=self.role_cboxOptions, 
                                    entryVariable=self.role_cboxVar)
        self.role_cbox.place(x=100, y=160)

        # 'Gender' Label and Combo Box Widgets
        self.gender_label = self.newCtkLabel('Gender')
        self.gender_label.place(x=20, y=220)
        self.gender_cboxVar = StringVar()
        self.gender_cboxOptions = ['Male', 'Female']
        self.gender_cbox = self.newCtkComboBox(options=self.gender_cboxOptions, 
                                    entryVariable=self.gender_cboxVar)
        self.gender_cbox.place(x=100, y=220)

        # 'Status' Label and Combo Box Widgets
        self.status_label = self.newCtkLabel('Status')
        self.status_label.place(x=20, y=280)
        self.status_cboxVar = StringVar()
        self.status_cboxOptions = ['On-Site', 'Remote', 'Sick-Leave', 'On-Leave', 'On-Trip', 'On-Training']
        self.status_cbox = self.newCtkComboBox(options=self.status_cboxOptions, 
                                    entryVariable=self.status_cboxVar)
        self.status_cbox.place(x=100, y=280)


        self.add_button = self.newCtkButton(text='Add Employee',
                                onClickHandler=self.add_entry,
                                fgColor='#05A312',
                                hoverColor='#00850B',
                                borderColor='#05A312')
        self.add_button.place(x=50,y=350)

        self.new_button = self.newCtkButton(text='New Employee',
                                onClickHandler=lambda:self.clear_form(True))
        self.new_button.place(x=50,y=400)

        self.update_button = self.newCtkButton(text='Update Employee',
                                    onClickHandler=self.update_entry)
        self.update_button.place(x=360,y=400)

        self.delete_button = self.newCtkButton(text='Delete Employee',
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
        self.tree['columns'] = ('ID', 'Name', 'Role', 'Gender', 'Status')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', anchor=tk.CENTER, width=10)
        self.tree.column('Name', anchor=tk.CENTER, width=150)
        self.tree.column('Role', anchor=tk.CENTER, width=150)
        self.tree.column('Gender', anchor=tk.CENTER, width=10)
        self.tree.column('Status', anchor=tk.CENTER, width=150)

        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Role', text='Role')
        self.tree.heading('Gender', text='Gender')
        self.tree.heading('Status', text='Status')

        self.tree.place(x=360, y=20, width=1000, height=350)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    # new Label Widget
    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_BgColor='#161C25'

        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                    bg_color=widget_BgColor)
        return widget

    # new Entry Widget
    def newCtkEntry(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=250

        widget = customtkinter.CTkEntry(self,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    border_color=widget_BorderColor,
                                    border_width=widget_BorderWidth,
                                    width=widget_Width)
        return widget

    # new Combo Box Widget
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_DropdownHoverColor='#0C9295'
        widget_ButtonColor='#0C9295'
        widget_ButtonHoverColor='#0C9295'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=250
        widget_Options=options

        widget = customtkinter.CTkComboBox(self,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        border_color=widget_BorderColor,
                                        width=widget_Width,
                                        variable=entryVariable,
                                        values=options,
                                        state='readonly')
        
        # set default value to 1st option
        widget.set(options[0])

        return widget

    # new Button Widget
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#161C25', hoverColor='#FF5002', bgColor='#161C25', borderColor='#F15704'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=260
        widget_Function=onClickHandler

        widget = customtkinter.CTkButton(self,
                                        text=text,
                                        command=widget_Function,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        hover_color=widget_HoverColor,
                                        bg_color=widget_BackgroundColor,
                                        border_color=widget_BorderColor,
                                        border_width=widget_BorderWidth,
                                        cursor=widget_Cursor,
                                        corner_radius=widget_CornerRadius,
                                        width=widget_Width)
       
        return widget

    # Handles
    def add_to_treeview(self):
        employees = self.db.fetch_employees()
        self.tree.delete(*self.tree.get_children())
        for employee in employees:
            print(employee)
            self.tree.insert('', END, values=employee)

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.id_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.role_cboxVar.set('SW-Engineer')
        self.gender_cboxVar.set('Male')
        self.status_cboxVar.set('On-Site')

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.id_entry.insert(0, row[0])
            self.name_entry.insert(0, row[1])
            self.role_cboxVar.set(row[2])
            self.gender_cboxVar.set(row[3])
            self.status_cboxVar.set(row[4])
        else:
            pass

    def add_entry(self):
        id=self.id_entry.get()
        name=self.name_entry.get()
        role=self.role_cboxVar.get()
        gender=self.gender_cboxVar.get()
        status=self.status_cboxVar.get()

        if not (id and name and role and gender and status):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.id_exists(id):
            messagebox.showerror('Error', 'ID already exists')
        else:
            self.db.insert_employee(id, name, role, gender, status)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an employee to delete')
        else:
            id = self.id_entry.get()
            self.db.delete_employee(id)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an employee to update')
        else:
            id=self.id_entry.get()
            name=self.name_entry.get()
            role=self.role_cboxVar.get()
            gender=self.gender_cboxVar.get()
            status=self.status_cboxVar.get()
            self.db.update_employee(name, role, gender, status, id)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been updated')

    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.csv')





