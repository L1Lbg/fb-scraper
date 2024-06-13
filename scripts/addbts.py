import sqlite3
import os
from pathlib import Path

def addbts():
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    os.chdir(Path(__file__).parent.absolute().parent.absolute())



    bizs = open('./data/bizs.txt', 'r').readlines()


    for biz in bizs:
        try:
            cur.execute(f"INSERT INTO businessType VALUES('{biz}','0','0');")
        except Exception as e:
            # print(f'Biz: {biz}, Error: {e}')
            pass

    con.commit()

if __name__ == '__main__':
    addbts()