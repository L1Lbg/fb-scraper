from data.allowed_emails import allowed_emails
from data.allowed_urls import allowed_urls
from bs4 import BeautifulSoup
import requests
import re
from .portscanner import tcp_scan

def scrape_user(html, bt):
    ui = {
        'NAME:':None,
        'BUSINESS TYPE':bt,
        'LOCATION':None,
        'WEBSITE':None,
        'EMAIL':None,
        'PROBLEMS':None,
    }

    bs = BeautifulSoup(html, 'html.parser')


    # ------------ GET ACCOUNT DETAILS    --------------------
    details = bs.find_all(class_='x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1nhvcw1 x1qjc9v5 xozqiw3 x1q0g3np xyamay9 xykv574 xbmpl8g x4cne27 xifccgj')
    try:
        ui['NAME'] = bs.find_all(class_='html-h1 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1vvkbs x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz')[0].text
    except Exception as e:
        #print(f'Could not find name')
        return None

    website_re = r"(?:www\.)?[a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})+(?:/[^ \n]*)?"
    for detail in details:
        # IF EMAIL IN PROFILE
        if '@' in detail.text:
            ui['EMAIL'] = detail.text

        # IF NO WEBSITE IN PROFILE
        if re.match(website_re, detail.text) == None:
            ui['WEBSITE'] = None
            ui['PROBLEMS'] = 'No website'
        # IF WEBSITE IN PROFILE
        if re.match(website_re, detail.text) != None:
            # CHECK IF WEBSITE IS IN ALLOWED LIST
            if any(url in detail.text for url in allowed_urls):
                ui['WEBSITE'] = None
                ui['PROBLEMS'] = 'No website'
            else:
                res = tcp_scan(detail.text)
                if res == False:
                    return None
                else:
                    ui['PROBLEMS']  = res
        
    # IF NO EMAIL FOUND, STOP SCRAPING
    if ui['EMAIL'] == None:
        return None


    # # ------------ PROCESS ACCOUNT DETAILS    --------------------
    # CHECK FOR WEBSITE IN EMAIL DOMAIN
    if ui['WEBSITE'] is None:
        split_email = ui['EMAIL'].split('@')[1]
        # IF EMAIL DOMAIN IS NOT COMMON
        if str(split_email).lower() not in allowed_emails:
            res = tcp_scan(split_email)
            # print(f"{split_email}: {res}")
            if res == False:
                return None
            else:
                ui['PROBLEMS']  = res


    else:
        return None

    # print(ui)
    return ui