import sqlite3
import time
import os

def resetdb():
    os.chdir(Path(__file__).parent.absolute().parent.absolute())

    # EMPTY DATABASE FILE
    open('db.sqlite3', 'w').write('')

    # CONNECT
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    # CREATE TABLE
    cur.execute("""
        CREATE TABLE profile
        (
            'name','businessType','location','website','email','emailSubject','emailBody','problems','contacted',

            CONSTRAINT unique_email UNIQUE (email)
        )
        ;
    """)
    cur.execute("""
        CREATE TABLE businessType
        (   
            'name','used','hits',

            CONSTRAINT unique_name UNIQUE (name)
        )
        ;
    """)
    print('Reset Complete!')

    con.commit()


if __name__ == '__main__':
    resetdb()