import sqlite3

# connect to database
conn = sqlite3.connect('database.db')
c = conn.cursor()

###################### Functions
def init_db():
    print("\n\n")
    try:
        print("Initializing Database")
        c.execute(""" CREATE TABLE cars (
                    name text,
                    plate text
                    ) """)
        conn.commit()
    except:
        print("Already initialized")
        print("If you want to create a new database, delete existing databaase file ")


def add_row():
    print("\n\n")
    name  = input("Enter Name  : ")
    plate = input("Enter Plate : ")
    c.execute("INSERT INTO cars VALUES (?, ?)", (name, plate))
    conn.commit()

def show_data():
    print("\n\n")
    c.execute("SELECT * FROM cars")
    s = c.fetchone()
    while s is not None:
        print(s)
        s = c.fetchone()

###################### Main
if __name__ == '__main__':
    while True:
        print("\n\n")
        print("1 -> Init Database")
        print("2 -> input data")
        print("3 -> Show data")
        print("4 -> Exit")

        i = input("Command: ")

        if i is "1":
            init_db()
        elif i is "2":
            add_row()
        elif i is "3":
            show_data()
        elif i is "4":
            conn.close()
            exit()
