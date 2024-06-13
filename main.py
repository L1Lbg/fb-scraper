from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from scripts.scrape_user import scrape_user
from scripts.find_pages import find_pages
from scripts.updatehits import updatehits
from urllib.parse import quote
from selenium import webdriver
from datetime import datetime
from colorama import Fore
import threading
import sqlite3
import random
import time
import json
import sys
import os
from dotenv import load_dotenv
import os
load_dotenv()


start_time = time.time()

tt = 3 # ESTIMATED TIME PER PROFILE
ppp = 0.000157 # ESTIMATED PROFILES PER PIXEL

# DATA
EMAIL = os.getenv('FB_USER')
PASS = os.getenv('FB_PASS')

try:
        length = int(sys.argv[1]) # BUSINESS CATEGORIES SEARCHED THROUGH
except:
        print(Fore.RED + "You have to enter a number after the argument 'main.py' (Example: " + Fore.YELLOW + "'python main.py 10'" + Fore.RED + ")" + Fore.RESET)
        exit()

lvl = 20 * 50_000 # PIXELS TO SCROLL IN QUERY PAGE

biz_types_used = list()
profiles = list()

if length == 0 or lvl == 0:
        raise "Minimum length/level is 1"

def main(length, worker_id):
        # DRIVER CONFIGURATIONS
        options = Options()
        options.headless = True
        options.add_argument("--lang=en-US")
        options.add_argument("--disable-infobars")
        options.add_argument("start-minimized")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-extensions")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("prefs", {\
                "profile.default_content_setting_values.notifications":1
                })
        driver = webdriver.Chrome(options=options)

        # ----------------- LOG-IN ---------------------
        driver.get('https://facebook.com/login')
        driver.find_element(By.CSS_SELECTOR, "[aria-label='Decline optional cookies']").click()

        # enter form data and submit
        driver.find_element(By.ID, 'email').send_keys(EMAIL)
        driver.find_element(By.ID, 'pass').send_keys(PASS)
        driver.find_element(By.ID, 'loginbutton').click()
        time.sleep(5)        

        for i in range(int(length)):
                # ----------------- CHOOSE BUSINESS TYPE -----------
                con = sqlite3.connect("db.sqlite3")
                cur = con.cursor()
                res = cur.execute("SELECT * FROM businessType WHERE used = '0';").fetchall()    
                con.close()
                
                if len(res) == 0:
                        print(Fore.RED + 'No unused business types left.\nExiting...')
                        exit()
                biz_type = res[random.randint(0,len(res) - 1)][0]  
                # ----------------- ANNOUNCE TIME ----------------
                diff = time.time() - start_time
                print(f'{Fore.YELLOW}[{str(datetime.now()).split('.')[0]} - WORKER {worker_id}] {round(    ((i) /length)*100,    2)}% completed ({i}/{length}).') # CONVERT TO mm:ss
                # -------------------- QUERYING PAGES -------------------
                query = quote(biz_type)
                driver.get(f'https://facebook.com/search/pages/?q={query}')
                time.sleep(0.5)
                for i in range(int(lvl / 50_000)):
                        driver.execute_script(f'scrollBy(0,{50000})')
                        time.sleep(1.5)
                # -------------------- PROCESSING PAGES --------------------
                users = find_pages(driver.page_source)
                
                # -------------------- QUERYING PROFILES --------------------
                ud = list()
                for user in users:
                        driver.get(user)
                        time.sleep(0.5)
                        res = scrape_user(driver.page_source, biz_type)
                        if res is not None:
                                try:
                                        profiles.append(res)
                                except Exception as e:
                                        # print(f'{Fore.WHITE} Error: {e}')
                                        # print(res['EMAIL'])
                                        pass  

        print(f"{Fore.GREEN}[{str(datetime.now()).split('.')[0]} - WORKER {worker_id}] 100% completed ({length}/{length}).")
        driver.quit()


if __name__ == '__main__':
        # DO A REPARTITION OF THREADS IN AN EQUAL WAY
        list_of = list()
        threads_num = 6

        et = (lvl * ppp * tt * length) / threads_num
        print(f"{Fore.BLUE}[INFO] ETC: {int(et/60)} minute(s) {int(et%60)} second(s).")

        for i in range(threads_num):
                list_of.append(0)

        while sum(list_of) < length:
                for i in range(len(list_of)):
                        if sum(list_of) < length:
                                list_of[i] += 1
                        else:
                                break


        # ---------------- START THREADS --------------------
        threads = list()
        for i in range(threads_num):
                thread = threading.Thread(target=main, args=(list_of[i],i+1))
                threads.append(thread)
                threads[-1].start()
                time.sleep(2)
        for thread in threads:
                thread.join()


        end_time = time.time()
        diff = int(end_time - start_time)
        print(f"{Fore.CYAN}[{str(datetime.now()).split('.')[0]} - MAIN] 100% completed ({length}/{length}). Took {int(diff / 60)} minute(s) {int(diff % 60)} second(s). Total profile(s) found: {len(profiles)}.")


        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        for profile in profiles:
                try:
                        cur.execute(f'INSERT INTO profile VALUES ("{profile['NAME']}","{profile['BUSINESS TYPE']}","{profile['LOCATION']}","{profile['WEBSITE']}","{profile['EMAIL']}","emailsubject","emailbody","{profile['PROBLEMS']}","0","");')
                except Exception as e:
                        # print(f"{Fore.WHITE}{e}")
                        pass

        for bt in biz_types_used:
                cur.execute(f"UPDATE businessType SET used = '1' WHERE name = '{biz_type}'")

        con.commit()
        con.close()

        print("Updating hits...")
        updatehits()
        print('Updated hits!')