import sqlite3
import pprint

def updatehits():
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()

    bts = cur.execute('SELECT * FROM businessType;').fetchall()
    for bt in bts:
        profiles = cur.execute(f"SELECT * FROM profile WHERE businessType = '{bt[0]}';").fetchall()
        
        cur.execute(f"UPDATE businessType SET leads = '{len(profiles)}' WHERE name = '{bt[0]}'")
    con.commit()
    con.close()

if __name__ == '__main__':
    updatehits()
