import PySimpleGUI as sg
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import names

sg.change_look_and_feel('Default 1')

engine = create_engine('sqlite:///app.db', echo=True)
Base = declarative_base()


entry_layout = [[sg.T('Please Enter the Employee Information Below')],
          [sg.T('First Name:', auto_size_text=False, size=(13, 1)), sg.In(key='first')],
          [sg.T('Last Name:', auto_size_text=False, size=(13, 1)), sg.In(key='last')],
          [sg.T('Favorite Color:', auto_size_text=False, size=(13, 1)), sg.In(key='color')],
          [sg.Button('Commit', button_color=('white', 'red'), key='commit'), sg.Button('Add', key='add'), sg.Button('Commit List', key='comlist', tooltip='Lists users already added but yet to be committed'), sg.Button('Clear Commit List', key='clcom', tooltip='Clears the commit list')],
          [sg.Output(size=(100, 20), key='output')],
                # size in (width, height)
          [sg.Button('List', key='list', tooltip='Lists all users in database'), sg.Button('Clear', key='clear', tooltip='Clears the output window'), sg.Cancel()]]

window = sg.Window('Employee Database Entry', entry_layout)


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    first = Column(String)
    last = Column(String)
    color = Column(String)


    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def __repr__(self):
        return "<User(id='%s', first='%s', last='%s', color='%s')>" \
               % (self.id, self.first, self.last, self.color)


Base.metadata.create_all(engine)

# ed_user = Employee(first='Edawrd', last='Johnson', color='Red')
# test object

# users = [Employee(first=names.get_first_name(), last=names.get_last_name(), color='Red') for num in range(100)]
# test comprehension to populate database with dummy data

users = []

Session = sessionmaker(bind=engine)
session = Session()
#session.add_all(users)

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

#session.flush()
#session.commit()



#for user in session.query(Employee).order_by(Employee.id):
    #print(user)


session.close()