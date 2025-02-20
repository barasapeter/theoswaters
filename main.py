from PIL import Image

import customtkinter as ctk
from tkinter.messagebox import *
from tkinter import ttk
from typing import Union
import database, quick_variables

# App starts here..
class App(ctk.CTk):
    width = 900
    height = 600
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loggedin_username = ctk.StringVar()
        # Set the window properties
        self.geometry(f'{self.width}x{self.height}')
        self.wm_attributes('-alpha', 0.95)
        self.resizable(False, False)
        self.title('Water management System')
        # Create a beautiful backgrund image for the main screen
        ctk.CTkLabel(self, text=None, image=ctk.CTkImage(Image.open('./images/background.jpg'), size=(self.width, self.height))).grid(row=0, column=0, sticky='nwes')
        # Login form
        self.login_form = ctk.CTkFrame(self, border_width=1, border_color='green')
        self.login_form.grid(row=0, column=0, sticky='ns', pady=50)
        ctk.CTkLabel(self.login_form, text='WATER MANAGEMENT\nSYSTEM', font=ctk.CTkFont('Arial', 20, 'bold', 'roman')).grid(row=0, column=0, columnspan=2, padx=5, pady=(50, 50))
        ctk.CTkLabel(self.login_form, text=None, image=ctk.CTkImage(Image.open('./images/username_icon.png'), size=(30, 30))).grid(row=1, column=0, padx=1, pady=(0, 10))
        ctk.CTkLabel(self.login_form, text=None, image=ctk.CTkImage(Image.open('./images/lock.png'), size=(50, 30))).grid(row=2, column=0, padx=1, pady=(0, 10))
        # Username and password entry widgets
        self.user_name_entry = ctk.CTkEntry(self.login_form, width=200, placeholder_text='Username...')
        self.user_name_entry.grid(row=1, column=1, padx=(0, 10))
        self.password_entry = ctk.CTkEntry(self.login_form, width=200, show='•', placeholder_text='Password...')
        self.password_entry.grid(row=2, column=1, padx=(0, 10))
        # Dashboard contents
        self.dashboard = ctk.CTkFrame(self)
        self.leftsidebar = ctk.CTkFrame(self.dashboard)
        self.leftsidebar.pack(side='left', fill='y')
        self.mainbar = ctk.CTkFrame(self.dashboard)
        self.mainbar.pack()
        ctk.CTkLabel(self.mainbar, text=None, image=ctk.CTkImage(Image.open('./images/dash_background.jpg'), size=(self.width-140, self.height))).grid(row=0, column=0)
        self.dynamic_text = ctk.StringVar()
        self.dynamic_text.set('Home')
        self.tablabel = ctk.CTkLabel(self.mainbar, font=ctk.CTkFont(None, 24, 'bold'), width=400, height=54, textvariable=self.dynamic_text)
        self.tablabel.grid(row=0, column=0, sticky='nwe')
        self.open_dash_widgets: list[Union[ctk.CTkLabel, ctk.CTkFrame, ctk.CTkButton]] = []

        def trace_serialno_input(text_container):
            for field in [self.bottle_size_ent, self.bottle_unit_ent, self.bottle_cost_ent]:
                field.delete(0, 'end')
            if text_container.get() in bottle_records.keys():            
                self.bottle_size_ent.insert(0, bottle_records[sv.get()]['bottle size'])
                self.bottle_unit_ent.insert(0, bottle_records[sv.get()]['measurement unit'])
                self.bottle_cost_ent.insert(0, bottle_records[sv.get()]['cost'])
        
        # Tabs start here...
        self.customers_tab = ctk.CTkFrame(self.mainbar)     
        sv = ctk.StringVar()
        sv.trace('w', lambda name, index, mode, sv=sv: trace_serialno_input(sv))             
        self.bottles_tab = ctk.CTkFrame(self.mainbar, corner_radius=5, border_width=3, border_color='green')
        self.bottles_entry_frame = ctk.CTkFrame(self.bottles_tab)
        self.bottles_entry_frame.pack(expand='yes')
        ctk.CTkLabel(self.bottles_entry_frame, text='Serial NO').grid(row=0, column=0, padx=5)
        self.bottle_serialno_ent = ctk.CTkComboBox(self.bottles_entry_frame, variable=sv)
        self.bottle_serialno_ent.grid(row=0, column=1, pady=(10, 5))
        self.bottle_serialno_ent.set('')
        ctk.CTkLabel(self.bottles_entry_frame, text='Bottle size').grid(row=1, column=0)
        self.bottle_size_ent = ctk.CTkEntry(self.bottles_entry_frame)
        self.bottle_size_ent.grid(row=1, column=1, pady=(0, 5))
        ctk.CTkLabel(self.bottles_entry_frame, text='Unit').grid(row=2, column=0, padx=5)
        self.bottle_unit_ent = ctk.CTkEntry(self.bottles_entry_frame)
        self.bottle_unit_ent.grid(row=2, column=1, pady=(0, 5))
        ctk.CTkLabel(self.bottles_entry_frame, text='Cost').grid(row=3, column=0, padx=5)
        self.bottle_cost_ent = ctk.CTkEntry(self.bottles_entry_frame)
        self.bottle_cost_ent.grid(row=3, column=1, padx=5, pady=(0, 10))
        self.btns_frame = ctk.CTkFrame(self.bottles_tab)
        self.btns_frame.pack(pady=(0, 20))

        def save_bottle():
            response = database.add_bottle(self.loggedin_username.get(), self.bottle_serialno_ent.get(), self.bottle_size_ent.get(), self.bottle_unit_ent.get(), self.bottle_cost_ent.get())
            if 'Record has been added successfully!' in response:
                if askyesnocancel('TheosWaters', 'This action will add a new record in the database. Are you sure you wat to proceed?'):
                    database.cnx.commit()
                    self.bottles: list[tuple] = database.fetch_bottles(self.loggedin_username.get())
                    global bottle_records
                    bottle_records = {}
                    for record in self.bottles:
                        bottle_records[str(record[0])] = {
                            'bottle size': record[1],
                            'measurement unit': record[2],
                            'cost': record[3],
                        }
                    bottle_serial_numbers = list(bottle_records.keys())
                    self.bottle_serialno_ent.configure(values=bottle_serial_numbers)
                    self.refill_bottle_serialno_ent.configure(values=bottle_serial_numbers)
                    showinfo('TheosWaters', response)

            else:
                showinfo('TheosWaters', response)
        
        def delete_bottle():
            response = database.delete_bottle(self.loggedin_username.get(), self.bottle_serialno_ent.get())
            if 'success' in response:
                if askyesnocancel('TheosWaters', 'You are about to delete a record. Are you sure you want to proceed?'):
                    database.cnx.commit()
                    self.bottles: list[tuple] = database.fetch_bottles(self.loggedin_username.get())
                    global bottle_records
                    bottle_records = {}
                    for record in self.bottles:
                        bottle_records[str(record[0])] = {
                            'bottle size': record[1],
                            'measurement unit': record[2],
                            'cost': record[3],
                        }
                    bottle_serial_numbers = list(bottle_records.keys())
                    self.bottle_serialno_ent.configure(values=bottle_serial_numbers)
                    self.refill_bottle_serialno_ent.configure(values=bottle_serial_numbers)
                    self.bottle_serialno_ent.set('')
                    for field in [self.bottle_size_ent, self.bottle_unit_ent, self.bottle_cost_ent]:
                        field.delete(0, 'end')
                    showinfo('TheosWaters', response)
            else:
                showwarning('TheosWaters', response)

        self.save_bottle_button = ctk.CTkButton(self.btns_frame, hover_color='dark green', fg_color='transparent', border_width=3, height=40, text='SAVE', command=save_bottle)
        self.save_bottle_button.pack(side='left', padx=(0, 5))
        self.save_bottle_button = ctk.CTkButton(self.btns_frame, hover_color='dark red', height=40, fg_color='transparent', border_width=3, text='DELETE', command=delete_bottle)
        self.save_bottle_button.pack(side='right')
        
        def trace_refill_serial_ent(text_container):
            for field in [self.refill_bottle_size_ent, self.refill_bottle_unit_ent, self.refill_bottle_cost_ent]:
                field.delete(0, 'end')
            if text_container.get() in bottle_records.keys():            
                self.refill_bottle_size_ent.insert(0, bottle_records[sv2.get()]['bottle size'])
                self.refill_bottle_unit_ent.insert(0, bottle_records[sv2.get()]['measurement unit'])
                self.refill_bottle_cost_ent.insert(0, bottle_records[sv2.get()]['cost'])
        
        sv2 = ctk.StringVar()
        sv2.trace('w', lambda name, index, mode, sv2=sv2: trace_refill_serial_ent(sv2))
        self.refill_tab = ctk.CTkFrame(self.mainbar, border_color='#1FADFF', border_width=2)
        ctk.CTkLabel(self.refill_tab, text=quick_variables.CustomCalendar.date_today()).pack(pady=(1, 0))
        self.input_frame = ctk.CTkFrame(self.refill_tab, corner_radius=15)
        self.input_frame.pack(expand='yes', pady=10)        
        ctk.CTkLabel(self.input_frame, text='Serial NO').grid(row=0, column=0, padx=5, pady=5)
        self.refill_bottle_serialno_ent = ctk.CTkComboBox(self.input_frame, variable=sv2)
        self.refill_bottle_serialno_ent.grid(row=0, column=1, padx=(0, 5), pady=5)
        self.refill_bottle_serialno_ent.set('')
        ctk.CTkLabel(self.input_frame, text='Bottle size').grid(row=1, column=0, padx=5, pady=(0, 5))
        self.refill_bottle_size_ent = ctk.CTkEntry(self.input_frame)
        self.refill_bottle_size_ent.grid(row=1, column=1, padx=(0, 5), pady=(0, 5))
        ctk.CTkLabel(self.input_frame, text='Unit').grid(row=2, column=0, padx=5, pady=(0, 5))
        self.refill_bottle_unit_ent = ctk.CTkEntry(self.input_frame)
        self.refill_bottle_unit_ent.grid(row=2, column=1, padx=(0, 5), pady=(0, 5))
        ctk.CTkLabel(self.input_frame, text='Cost').grid(row=3, column=0, padx=5, pady=(0, 5))
        self.refill_bottle_cost_ent = ctk.CTkEntry(self.input_frame)
        self.refill_bottle_cost_ent.grid(row=3, column=1, padx=(0, 5), pady=(0, 5))
        self.refill_refill_button = ctk.CTkButton(self.refill_tab, height=40, fg_color='transparent', hover_color='#1FADFF', border_width=1, font=ctk.CTkFont('Rockwell Extra Bold', 16), text='Dispense', command=self.dispense)
        self.refill_refill_button.pack(side='bottom', fill='x', padx=10, pady=10)
        self.profile_button = ctk.CTkButton(self.mainbar, corner_radius=0, anchor='w', border_spacing=10, height=40, 
                      hover_color=("gray70", "gray30"), fg_color="transparent", 
                      image=ctk.CTkImage(Image.open('./images/username_icon.png'), size=(30, 30)), 
                      compound='right')
        self.profile_button.grid(row=0, column=0, sticky='ne')
        ctk.CTkButton(self.leftsidebar, corner_radius=0, anchor='w', border_spacing=10, height=40, text_color=("gray10", "gray90"),
                      hover_color=("gray70", "gray30"), fg_color="transparent", text='Home', 
                      image=ctk.CTkImage(Image.open('./images/home.png'), size=(30, 30)), compound='left', command=self.open_home).pack()
        ctk.CTkButton(self.leftsidebar, corner_radius=0, anchor='w', border_spacing=10, height=40, text_color=("gray10", "gray90"), 
                      hover_color=("gray70", "gray30"), fg_color="transparent", text='Customers', image=ctk.CTkImage(Image.open('./images/customers.png'), size=(30, 30)), 
                      compound='left', command=self.open_customers_tab).pack(pady=(100, 0))
        ctk.CTkButton(self.leftsidebar, corner_radius=0, anchor='w', border_spacing=10,  height=40, text_color=("gray10", "gray90"), 
                      hover_color=("gray70", "gray30"), fg_color="transparent", text='Bottles', 
                      image=ctk.CTkImage(Image.open('./images/cost_tag.png'), size=(50, 70)), 
                      compound='left',command=self.open_bottles_tab).pack(side='top')
        ctk.CTkButton(self.leftsidebar, corner_radius=0, anchor='w', border_spacing=10, height=40, text_color=("gray10", "gray90"), 
                      hover_color=("gray70", "gray30"), fg_color="transparent", text='Dispensor', command=self.open_refill_tab, 
                      image=ctk.CTkImage(Image.open('./images/bottle_refill.jpg'), size=(50, 50)), compound='left').pack(side='top')
        ctk.CTkButton(self.leftsidebar, anchor='w', border_spacing=10, corner_radius=0, height=40, text_color=("gray10", "gray90"), 
                      hover_color=("gray70", "gray30"), fg_color="transparent", text='Log out', image=ctk.CTkImage(Image.open('./images/logout.png')), 
                      compound='left', command=self.logout).pack(side='bottom')
        ctk.CTkButton(self.login_form, command=lambda: self.login(self.user_name_entry.get(), self.password_entry.get()), text='Log in').grid(row=3, column=1, padx=(0, 10), pady=(10, 0), sticky='e')

    def destroy_open_dash_widgets(self):
        '''Destroy all widgets in the dash'''
        for widget in self.open_dash_widgets:
            widget.grid_forget()
    
    def open_customers_tab(self):
        self.dynamic_text.set('Customers')
        self.destroy_open_dash_widgets()
        customers_table.grid(row=0, column=0)
        self.open_dash_widgets.append(customers_table)
    
    def open_bottles_tab(self):
        self.dynamic_text.set('Bottles')
        self.destroy_open_dash_widgets()
        self.bottles_tab.grid(row=0, column=0, sticky='nwse', padx=180, pady=180)
        self.open_dash_widgets.append(self.bottles_tab)
    
    def open_home(self):
        self.dynamic_text.set('Home')
        self.destroy_open_dash_widgets()
        sales_table.grid(row=0, column=0, )
        self.open_dash_widgets.append(sales_table)
    
    def open_refill_tab(self):
        self.dynamic_text.set('Refill bottles - customers')
        self.destroy_open_dash_widgets()
        self.refill_tab.grid(row=0, column=0, sticky='nwse', padx=180, pady=175)
        self.open_dash_widgets.append(self.refill_tab)
    
    def dispense(self):
        response = database.dispense(self.loggedin_username.get(), self.refill_bottle_serialno_ent.get(), self.refill_bottle_cost_ent.get())
        if 'Would you like to proceed?' in response:
            if askyesnocancel('TheosWaters', response):
                global sales_table
                sales_columns = [{'text': 'Number', 'stretch': False}, 
                             {'text': 'Bottle description', 'stretch': False}, 
                             {'text': 'Cost', 'stretch': False},
                             {'text': 'Date', 'stretch': False},
                             {'text': 'Day', 'stretch': False},
                             {'text': 'Time', 'stretch': False}]
                from ttkbootstrap.tableview import Tableview
                sales_table = Tableview(master=self.mainbar, height=30, stripecolor=('light blue', None), coldata=sales_columns, rowdata=database.fetch_sales(self.loggedin_username.get()), paginated=False, autofit=True, searchable=True, bootstyle='success')
                database.cnx.commit()
                self.refill_refill_button.configure(state='disabled')
                dispense_window = ctk.CTkToplevel()
                dispense_window.geometry('450x250')
                dispense_window.title('TheosWaters')
                dispense_window.resizable(False, False)
                dispense_window.wm_attributes('-topmost', True)
                progress_message = ctk.CTkLabel(dispense_window, font=ctk.CTkFont('Arial', 30, 'bold', 'roman'), text='Dispensing...')
                progress_message.pack(expand='yes')
                progressbar = ttk.Progressbar(dispense_window, maximum=100, mode='determinate', length=300)
                progressbar.pack(fill='x', expand='yes', padx=20, )
                progressbar.start(100)
                self.after(10500, lambda: [dispense_window.destroy(), self.refill_refill_button.configure(state='normal'), showinfo('TheosWaters', 'Completed successfully')])        
        else:
            showerror('TheosWaters', response)

    def login(self, username, password):
        '''Authenticates username and password, if successful the dashboard is displayed'''
        # username, password='abigail_thompson', 'C0mpl1c@tedP@$$' # For testing purposes. 
        if database.login_success(username, password):
            self.loggedin_username.set(username)
            self.profile_button.configure(text=self.loggedin_username.get())
            self.login_form.grid_forget()
            self.dashboard.grid(row=0, column=0, sticky='nwse')
            customer_columns = [{'text': 'Serial NO', 'stretch': False}, 
                                {'text': 'Full name', 'stretch': False}, 
                                {'text': 'Address', 'stretch': False},
                                {'text': 'Contact NO', 'stretch': False},
                                {'text': 'Date encoded', 'stretch': False}]
            sales_columns = [{'text': 'Number', 'stretch': False}, 
                             {'text': 'Bottle description', 'stretch': False}, 
                             {'text': 'Cost', 'stretch': False},
                             {'text': 'Date', 'stretch': False},
                             {'text': 'Day', 'stretch': False},
                             {'text': 'Time', 'stretch': False}]
            
            self.customers = database.fetch_customers(username)
            from ttkbootstrap.tableview import Tableview
            
            global bottle_records
            global bottle_serial_numbers
            global customers_table
            global sales_table

            customers_table = Tableview(master=self.mainbar, height=30, bootstyle='success', coldata=customer_columns, rowdata=self.customers, paginated=False, autofit=True, searchable=True)
            sales_table = Tableview(master=self.mainbar, height=30, bootstyle='success', stripecolor=('light blue', None), coldata=sales_columns, rowdata=database.fetch_sales(username), paginated=False, autofit=True, searchable=True)
            
            self.bottles: list[tuple] = database.fetch_bottles(username)
            bottle_records = {}
            for record in self.bottles:
                bottle_records[str(record[0])] = {
                    'bottle size': record[1],
                    'measurement unit': record[2],
                    'cost': record[3],
                }
            bottle_serial_numbers = list(bottle_records.keys())
            self.bottle_serialno_ent.configure(values=bottle_serial_numbers)
            self.refill_bottle_serialno_ent.configure(values=bottle_serial_numbers)

        else:
            showwarning('Water Management System', 'FAIL! Invalid username or password')
    
    def logout(self):
        '''Logs out the user'''
        if askyesnocancel('Water management system', 'This will log you out. Are you sure you want to log out?'):
            customers_table.grid_forget()
            self.bottle_serialno_ent.set('')
            self.refill_bottle_serialno_ent.set('')
            for field in [self.bottle_size_ent, self.bottle_unit_ent, self.bottle_cost_ent, self.refill_bottle_size_ent, self.refill_bottle_unit_ent, self.refill_bottle_cost_ent]:
                field.delete(0, 'end')
            self.dashboard.grid_forget()
            self.login_form.grid(row=0, column=0, sticky='ns', pady=50)
            self.destroy_open_dash_widgets()

ctk.set_appearance_mode('Dark') #?: I have optimized the UI for dark mode. Change to Light and see things get wonky
ctk.set_default_color_theme('dark-blue')
if __name__ == '__main__':
    app = App()
    app.mainloop()
# App ends here...
