import PySimpleGUI as sg
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import names

sg.change_look_and_feel('Default 1')
# Changing the theme of the GUI

engine = create_engine('sqlite:///app.db', echo=True)
# Create SQL Engine and Base database
Base = declarative_base()

# Creating the layout for the GUI
entry_layout = [[sg.T('Please Enter the Employee Information Below')],
          [sg.T('First Name:', auto_size_text=False, size=(13, 1)), sg.In(key='first')],
          [sg.T('Last Name:', auto_size_text=False, size=(13, 1)), sg.In(key='last')],
          [sg.T('Favorite Color:', auto_size_text=False, size=(13, 1)), sg.In(key='color')],
          [sg.Button('Commit', button_color=('white', 'red'), key='commit'), sg.Button('Add', key='add'), sg.Button('Commit List', key='comlist', tooltip='Lists users already added but yet to be committed'), sg.Button('Clear Commit List', key='clcom', tooltip='Clears the commit list')],
          [sg.Output(size=(100, 20), key='output')],
                # size in (width, height)
          [sg.Button('List', key='list', tooltip='Lists all users in database'), sg.Button('Clear', key='clear', tooltip='Clears the output window'), sg.Cancel()]]

# Creating the window
window = sg.Window('Employee Database Entry', entry_layout)

# Creating the context manager to manage session open/close
class open_session():

    def __init__(self, eng):
        Session = sessionmaker(bind=eng)
        self.session = Session()
          
    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

# Creating the structure of the table 'employees'
class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    first = Column(String)
    last = Column(String)
    color = Column(String)

    # property decorator to have a fullname attribute if needed (currently only used in __repr__())
    # can access at any time
    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def __repr__(self):
        return "<User(id='%s', fullname='%s', color='%s')>" \
               % (self.id, self.fullname, self.color)

# Here we create all uncreated tables
# This line is not necessary is the table has already been created
# Let it stay in case I delete the database or something
Base.metadata.create_all(engine)

# ed_user = Employee(first='Edawrd', last='Johnson', color='Red')
# test object

# users = [Employee(first=names.get_first_name(), last=names.get_last_name(), color='Red') for num in range(1000)]
# test comprehension to populate database with dummy data

users = []


# Opening created context manager (create session object from the context manager's return session object)
with open_session(engine) as session:
    # Loop to read window
    while True:
        event, values = window.Read()
        window.Finalize()
        if event in (None, 'Cancel'):
            break
        if event == 'add' and values:
            user = (Employee(
                first=values['first'], last=values['last'], color=values['color']))
            users.append(user)
            print(f'--Added--\n{user}')
            window['first'].update('')
            window['last'].update('')
            window['color'].update('')
        if event == 'comlist':
            print('--Users to be Committed--')
            if users:
                for thing in users:
                    print(thing)
            else:
                print('None')
        if event == 'commit':
            session.add_all(users)
            session.flush()
            session.commit()
            print(f'--Committed--')
            for use in users:
                print(use)
            users = []
        if event == 'clcom':
            users = []
            print('--Commit List Cleared--')
        if event == 'list':
            all_in_db = session.query(Employee).order_by(Employee.id)
            if all_in_db:
                print('--Users in Database--')
                for item in all_in_db:
                    print(item)
            else:
                print('No Employees in Database')
        if event == 'clear':
            window['output'].update('')
    window.Close()
    # close window when loop ends for memory reasons


# for user in session.query(Employee).order_by(Employee.id):
    # print(user)
