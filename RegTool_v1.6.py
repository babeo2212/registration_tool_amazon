from tkinter.constants import E, S
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os
import sys
import pandas as pd
import time
import random
import re
import warnings
import requests
from lxml.html import fromstring
import tkinter as tk
from tkinter import filedialog
import logging
import email
from datetime import datetime
import csv
from itertools import cycle
import pyotp # library for getting OTP code
from imapclient import IMAPClient
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import zipfile
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import threading

'''
Version 1.6 log: 
- Change OTP site from https://otpsim.com to https://chootp.com/
'''
def headers():
    warnings.filterwarnings("ignore")
    print('= '*60)
    print('REGISTER TOOL AMAZON.COM'.center(120))
    print('COPYRIGHT © THUY TEAM'.center(120))
    print('version 1.60'.center(120))
    print('\n')
    print('Support Email: vutienhung2212@gmail.com'.center(120))
    print('= '*60) 

def changeDirectory():
        '''
        Change current saving directory to ./Dowloads/Etsy_ratings.
        '''
        os.chdir('C:'+os.environ.get('HOMEPATH') + '\\Downloads')
        try: 
            os.mkdir('Etsy_ratings')
        except Exception:
            pass
        os.chdir('C:'+os.environ.get('HOMEPATH') + '\\Downloads\\Etsy_ratings')
        print('Please get your .csv file at directory: %s.' % os.getcwd())

class RegisterTool:

    def __init__(self, name):
        self.name = name
        self.main()

    # @disable_debug_messages
    def main(self):
        ''' Main function. Do not touch this.'''
        # logging.debug('Start of main')
        
        global i, info, proxies
        i = 0
        try:
            info, proxies = self.fetch_files_info()
        except:
            return
        while i < (info.shape[0]):
            try:
                browser = self.initiate_web_browser()
                if not browser:
                    print('''Critical error. No connection was found. Quitting application.
                            >>>>>>>>>> Report to IT for support. <<<<<<<<<<<''')
                    return
                self.log_in_amz(browser)
                # logging.debug(f'End of loop number: {i} of main().')
                browser.quit()
                i += 1
            except Exception as err:
                print(f'Error in main: {err}, of {self.name},\
                     \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
                browser.quit()
                i += 1
                continue
        print('End of file.'.center(120))
        # logging.debug('End of main')
        return

    def change_IP_address(self, proxies):
        '''Function use to change IP randomly.'''
        # Add proxy to web arguments
        proxy = next(proxies)
        return proxy

    def test_proxy(self, browser):
        ''' Test with a given proxy'''
        
        browser.get('https://merch.amazon.com/')
        try:
            if browser.find_elements_by_class_name('error-code'):
                browser.refresh()
                if browser.find_elements_by_class_name('error-code'):
                    return
                else:
                    pass
                
            starttime = time.perf_counter()
            WebDriverWait(browser, 40).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//h1[@class="header"]')))

            WebDriverWait(browser, 40).until(
                EC.presence_of_all_elements_located(
                    (By.TAG_NAME, 'div')))

            WebDriverWait(browser, 40).until(
                EC.presence_of_all_elements_located(
                    (By.TAG_NAME, 'a')))

            WebDriverWait(browser, 40).until(
                EC.presence_of_all_elements_located(
                    (By.TAG_NAME, 'input')))

            WebDriverWait(browser, 40).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//img[@class="landing-image-container"]')))
            try:
                WebDriverWait(browser, 60).until(
                    EC.visibility_of_element_located(
                        (By.LINK_TEXT, 'Sign up')))
            except:
                pass
            
            WebDriverWait(browser, 40).until(
                EC.element_to_be_clickable(
                    (By.LINK_TEXT, 'Program Materials License Agreement')))

            WebDriverWait(browser, 40).until(
                EC.element_to_be_clickable(
                    (By.LINK_TEXT, 'Templates')))
            
            WebDriverWait(browser, 40).until(
                EC.element_to_be_clickable(
                    (By.LINK_TEXT, 'Service Agreement')))
            
            WebDriverWait(browser, 40).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[@type="button"]')))

            endtime = time.perf_counter()
            if (endtime - starttime) <= 30:
                print(f'Proxy: {PROXY} is good for registering.')
                return True
            else:
                print(f'Proxy: {PROXY} is not good for registering. Commencing change to another proxy.')
                
                return False
        except Exception as err:
            print(f'Error in test_proxy: , {err}, of {self.name},\
                \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            print(f'Proxy: {PROXY} is not good for registering. Commencing change to another proxy.')
            
            return False

    def initiate_web_browser(self):
        ''' This function is to initiate the Chrome web browser'''
        # logging.debug('Start of initiate_web_browser')
        # Open Chrome Options
        try:
            global PROXY
            while True:
                # Get access code
                access_code = self.change_IP_address(proxies).split(':')
                
                HOST = access_code[0]
                PORT = access_code[1]
                USER_NAME = access_code[2]
                PASS_WORD = access_code[3]

                PROXY = HOST + ":" + PORT
                manifest_json = """
                {
                    "version": "1.0.0",
                    "manifest_version": 2,
                    "name": "Chrome Proxy",
                    "permissions": [
                        "proxy",
                        "tabs",
                        "unlimitedStorage",
                        "storage",
                        "<all_urls>",
                        "webRequest",
                        "webRequestBlocking"
                    ],
                    "background": {
                        "scripts": ["background.js"]
                    },
                    "minimum_chrome_version":"22.0.0"
                }
                """

                background_js = '''
                var config = {
                        mode: "fixed_servers",
                        rules: {
                        singleProxy: {
                            scheme: "http",
                            host: "%s",
                            port: parseInt(%s)
                        },
                        bypassList: ["localhost"]
                        }
                    };

                chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

                function callbackFn(details) {
                    return {
                        authCredentials: {
                            username: "%s",
                            password: "%s"
                        }
                    };
                }

                chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
                );''' % (HOST, PORT, USER_NAME, PASS_WORD)

                pluginfile = 'proxy_auth_plugin.zip'
                options = webdriver.ChromeOptions()
                # Add extension as a zip file
                with zipfile.ZipFile(pluginfile, 'w') as zp:
                    zp.writestr("manifest.json", manifest_json)
                    zp.writestr("background.js", background_js)
                options.add_extension(pluginfile)
            
                if getattr(sys, 'frozen', False): 
                    # executed as a bundled exe, the driver is in the extracted folder
                    chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
                    browser = webdriver.Chrome(chromedriver_path, chrome_options=options)
                else:
                    # executed as a simple script, the driver should be in `PATH` bc
                    browser = webdriver.Chrome(
                            executable_path="D:\\Hung\\Drivers\\chromedriver.exe", 
                            chrome_options=options)
                # Test proxy
                test_result = self.test_proxy(browser)
                if test_result:
                    return browser
                elif test_result == False:
                    browser.quit()
                elif test_result == None:
                    return
            # logging.debug('End of initiate_web_browser')
        except Exception as err:
            print(f'Error in initiate_web_browser: {err}, of {self.name}, \
                \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            return

    def fetch_files_info(self):
        ''' Return the info files'''
        
        try:
            # logging.debug('Start of fetch_files')
            root = tk.Tk()
            root.withdraw()
            # Open file reader
            files = filedialog.askopenfilenames(title='Import files')
            if not files:
                return
            while True:
                if len(files) == 1 or len(files) >= 3:
                    print(f'Arguments takes two, get {len(files)} file(s).')
                    files = filedialog.askopenfilenames(title='Import files')
                    if not files:
                        return
                elif len(files) == 2:
                    file_1 = os.path.basename(files[0]) # Get file name
                    file_2 = os.path.basename(files[1])
                    if not re.match('info_', file_1) or not re.match('proxies_', file_2):
                        print('Files mismatch.')
                        files = filedialog.askopenfilenames(title='Import files')
                        if not files:
                            return
                    else: 
                        break
                else:
                    break
            # Parse info into pandas Dataframe
            try:
                info = pd.read_csv(files[0], header=0, encoding='utf-8')
            except:
                info = pd.read_csv(files[0], header=0, encoding='latin')
            # Handle proxies
            proxies = pd.read_csv(files[1], sep="\n", header=None)
            proxies = proxies.iloc[:,0].to_list()
            print(proxies)
            random.shuffle(proxies) # shuffle proxies for randomness
            proxies = cycle(proxies)
            # logging.debug('End of fetch_files')
            return info, proxies
        except Exception as err:
            print(f'Error in fetch_files_info: {err}, of {self.name}, \
                \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            return

    def read_fetch_files_info(self, info, i=0):
        ''' Return the info: first_name, last_name, email_add, pass_word, full_name.'''
        try:
            # logging.debug('Start of read_fetch_files_info')     
            country = info.iloc[i, 0].strip()
            first_name = info.iloc[i, 1].strip()
            last_name = info.iloc[i, 2].strip()
            full_name = first_name + " " + last_name
            address_1 = info.iloc[i, 3].strip()
            city = info.iloc[i, 4].strip()
            state = info.iloc[i, 5].strip()
            zipcode = str(info.iloc[i, 6])
            phone = str(info.iloc[i, 7])
            name_of_bank = info.iloc[i, 9]
            email_add = info.iloc[i, 13].strip()
            pass_word = info.iloc[i, 14].strip()
            if not email_add or not pass_word:
                print('Email and/or password NULL in file. Please input in source file.')
                return
                
            if country == 'United States':
                try:
                    bank_acc = str(int(eval(info.iloc[i, 10])))
                except:
                    bank_acc = str(int(info.iloc[i, 10]))
            else:
                bank_acc = str(info.iloc[i, 10])

            routing = str(info.iloc[i, 11]).strip()
            if country == 'United States':
                if len(routing) == 8:
                    routing = '0' + routing
            ssn_ = str(info.iloc[i, 12]).strip()
            if country == 'United States':
                if len(ssn_) == 8:
                    ssn_ = '0' + ssn_
            
            # logging.debug('End of read_fetch_files_info')
            return first_name, last_name, email_add, pass_word, full_name, \
                country, address_1, city, state, zipcode, \
                phone, name_of_bank, bank_acc, routing, ssn_
        except Exception as err:
            print(f'Error in read_fetch_files_info: {err}, of {self.name}, \
            \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            return

    def read2_fetch_files_info(self, info, i=0):
        ''' Return the info: first_name, last_name, email_add, pass_word, full_name.'''
        # logging.debug('Start of read2_fetch_files_info')
        try:
            org_name = info.iloc[i, 15]
            add_info = info.iloc[i, 16]
            website = info.iloc[i, 17]
            # logging.debug('End of read2_fetch_files_info')
            return org_name, add_info, website
        except Exception as err:
            print('Error in read2_fetch_files_info: {err}, of {self.name}, \
                \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            return

    def sign_up_and_create_account(self, browser):
        ''' First step of register account. Click Sign in and create new account.'''
        try:
            _, _, email_add, pass_word, full_name, \
                _, _, _, _, _, _, _, _, _, _ = self.read_fetch_files_info(info, i)
            try:
                html_elem = browser.find_element_by_tag_name('html')
                html_elem.send_keys(Keys.END)
            except:
                browser.refresh()
            time.sleep(5)
            for _ in range(0, 9):
                html_elem.send_keys(Keys.UP)

            try:
                browser.find_element_by_link_text('Sign up').click() # --> click Sign up
            except Exception as err:
                browser.refresh()
                _ = input(f'''Error: {err}.
                'If not click on Sign up. Click Sign Up and press Enter.''')

            time.sleep(3)
            try:
                WebDriverWait(browser, 30).until(
                    EC.presence_of_all_elements_located(
                        (By.ID, 'createAccountSubmit')))
                browser.find_element_by_id('createAccountSubmit').click() # --> click createAccount
            except:
                _ = input('If not find Create Account . Click on Create Account and press Enter.')

            WebDriverWait(browser, 60).until(
                EC.presence_of_all_elements_located(
                    (By.TAG_NAME, 'input')))
            time.sleep(2)
            WebDriverWait(browser, 60).until(
                EC.element_to_be_clickable(
                    (By.XPATH, 
                    '//input[@type="text" and @id="ap_customer_name"]'
                    ))).send_keys(full_name) # Type Name
            
            time.sleep(5)

            browser.find_element_by_xpath(
                '//input[@type="email" and @id="ap_email"]'
                ).send_keys(email_add) # Type Email Address
            time.sleep(2)

            browser.find_element_by_xpath(
                '//input[@type="password" and @id="ap_password"]'
                ).send_keys(pass_word) # Type Password

            time.sleep(2)
            browser.find_element_by_xpath(
                '//input[@type="password" and @id="ap_password_check"]'
                ).send_keys(pass_word) # Retype password

            time.sleep(2)
            browser.find_element_by_xpath(
                '//input[@id="continue" and @type="submit"]'
                ).click()

        except Exception as err:
            print(f'Error in Sign up and Create Account: {err}, of {self.name}, \
                \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            _ = input('''If encounter this error, please do following steps:
            1. Click Sign Up.
            2. Click Create your Amazon account.
            3. Input Account Information (Name, Email, Password).
            4. Click Create account and hit Enter to continue.''')
        
    def solve_puzzle(self, browser):
        ''' 
            This function uses to solve puzzle.
        '''
        time.sleep(10)
        try:
            try:
                WebDriverWait(browser, 60).until(
                    EC.presence_of_all_elements_located(
                        (By.TAG_NAME, 'html')))

                WebDriverWait(browser, 60).until(
                    EC.presence_of_all_elements_located(
                        (By.TAG_NAME, 'iframe')))

                WebDriverWait(browser, 60).until(
                    EC.presence_of_element_located(
                        (By.XPATH, 
                        "//iframe[@id='cvf-arkose-frame']"
                        )))
            except:
                pass
            iframe1 = browser.find_element_by_xpath("//iframe[@id='cvf-arkose-frame']")
            browser.switch_to.frame(iframe1)
            try:
                WebDriverWait(browser, 60).until(
                    EC.presence_of_all_elements_located(
                        (By.TAG_NAME, 'iframe')))
                time.sleep(1)
            except:
                time.sleep(5)
            iframe2 = browser.find_element_by_xpath("//iframe[@id='fc-iframe-wrap']")
            browser.switch_to.frame(iframe2)
            try:
                WebDriverWait(browser, 60).until(
                    EC.presence_of_all_elements_located(
                        (By.TAG_NAME, 'iframe')))
            except:
                time.sleep(5)
            iframe3 = browser.find_element_by_xpath("//iframe[@id='CaptchaFrame']")
            browser.switch_to.frame(iframe3)
            try:
                WebDriverWait(browser, 60).until(
                    EC.presence_of_all_elements_located(
                        (By.LINK_TEXT, 'Solve Puzzle'))).click() # --> Click on solve puzzle
            except:
                time.sleep(5)
            try:
                browser.find_element_by_link_text('Solve Puzzle').click()
            except:
                pass
            _ = input('This is Solve puzzle Section. Press Enter if you are finished.')
            return
        except Exception as err:
            print(f'Error in solve_puzzle: {err}, of {self.name}, \
                \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            _ = input('Press enter to continue.')

    def get_email_otp(self, email_add, pass_word):
        ''' This function is to get email OTP password.'''
        time.sleep(15)
        try:
            with IMAPClient(host='outlook.office365.com', port=993, use_uid=True) as server:
                # log in
                server.login(email_add, pass_word)
                server.select_folder('INBOX')
                # messages = server.search(['FROM', 'account-update@amazon.com'])
                messages = server.search(['ALL'])
            # for each unseen email in the inbox
                if messages:
                    if len(messages) == 1 :
                        for _, message_data in server.fetch(messages, ['RFC822']).items():
                            email_message = email.message_from_bytes(message_data[b'RFC822'])

                            for part in email_message.get_payload():
                                # Convert a byte like to a string
                                otp_string = str(part.get_payload(decode=True), 
                                                part.get_content_charset(), "ignore")
                                # Use BeautifulSoup to rear html string
                                soup = BeautifulSoup(otp_string, "lxml")

                                # Get text from otp class
                                otp_pass = soup.find(class_='otp').text

                                return otp_pass   
                    else:
                        # Get the newest mail
                        max_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                        msgid_max = 0
                        
                        for msgid, data in server.fetch(messages,['ENVELOPE']).items():
                            if data[b'ENVELOPE'].date >= max_date:
                                max_date = data[b'ENVELOPE'].date
                                msgid_max = msgid

                        for msgid, message_data in server.fetch(messages, ['RFC822']).items():
                            if msgid == msgid_max:
                                email_message = email.message_from_bytes(message_data[b'RFC822'])
                                for part in email_message.get_payload():
                                    # Convert a byte like to a string
                                    otp_string = str(part.get_payload(decode=True), 
                                                    part.get_content_charset(), "ignore")
                                    # Use BeautifulSoup to rear html string
                                    soup = BeautifulSoup(otp_string, "lxml")
                                    # Get text from otp class
                                    otp_pass = soup.find(class_='otp').text
                                    return otp_pass
                else:
                    return
        except Exception as err:
            print(f'Can not log in to Email Address: {err}, of {self.name}, \
                \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            _ = input('Press enter to continue.')
            return 

    def fill_email_otp(self, browser):
        ''' This function to fill email OTP which get from get_email_otp() function.'''
        try:
            _, _, email_add, pass_word, _, _, _, _, _, _, \
            _, _, _, _, _ = self.read_fetch_files_info(info, i)
            time.sleep(1)
            ans_to_wait = 'y'
            while ans_to_wait == 'y':
                otp_pass = self.get_email_otp(email_add, pass_word)
                if not otp_pass:
                    ans_to_wait = input(
                        'There is no OTP in mail. Do you want to wait for 15s more?[Y|N]'
                        ).lower()
                    if ans_to_wait == 'n':
                        return
                else:
                    break
            # Fill otp from email
            browser.find_element_by_xpath(
                '//input[@type="text" and @name="code"]'
                ).send_keys(otp_pass)
            time.sleep(2)
            # Send click
            browser.find_element_by_xpath(
                '//input[@class="a-button-input" and @type="submit"]'
                ).click()
        except Exception as err:
            print(f'Error in Get and Fill Email OTP: {err}, of {self.name}, \
                \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            _ = input('Press enter to continue.')
            return

    def add_mobile_number(self, browser):
        ''' Select value in a select box where asked for telephone number'''
        try:
            try:
                select_id = Select(browser.find_element_by_xpath(
                    '//select[@name="cvf_phone_cc" and @id="cvf_phone_cc_native"]'))
            except:
                WebDriverWait(browser, 50).until(
                    EC.presence_of_element_located(
                        (By.XPATH, 
                        '//select[@name="cvf_phone_cc" and @id="cvf_phone_cc_native"]'
                        )))
                select_id = Select(browser.find_element_by_xpath(
                    '//select[@name="cvf_phone_cc" and @id="cvf_phone_cc_native"]'))
            time.sleep(2)
            select_id.select_by_value("VN")
            select_id.select_by_value("VN")
            time.sleep(2)
            if browser.find_elements_by_link_text("Vietnam +84"):
                browser.find_element_by_link_text("Vietnam +84").click()

            time.sleep(2)
            phone_number, session_number = self.get_tel()
            time.sleep(5)
            browser.find_element_by_xpath(
                '//input[@type="tel" and @name="cvf_phone_num"]'
                ).send_keys(phone_number)
            time.sleep(5)
            browser.find_element_by_xpath(
                '//input[@name="cvf_action"and @type="submit"]'
                ).click()
            return phone_number, session_number
        except Exception as err:
            print(f'Error in add_mobile_number: {err}, of {self.name}, \
                \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            _ = input('Press enter to continue.')
            return 

    def add_mobile_otp(self, browser, phone_number, session_number):
        ''' 
        This function gets OTP from function get_tel() and fill into a box.
        If no OTP returns, function returns None.
        '''
        try:
            time.sleep(10)
            otp_tel = self.get_tel(phone_number, session_number)
            if otp_tel:
                browser.find_element_by_xpath(
                    '//input[@type="text" and @name="code"]'
                    ).send_keys(otp_tel)
                time.sleep(3)
                browser.find_element_by_xpath(
                    '//input[@name="cvf_action" and @type="submit"]'
                    ).click() # --> click Send OTP
                WebDriverWait(browser, 50).until(
                    EC.presence_of_all_elements_located(
                        (By.TAG_NAME, 'div')))
                return otp_tel
            else:
                return
        except Exception as err:
            print(f'Error in Getting mobile phone OTP: {err}, of {self.name}, \
                \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            _ = input('Press enter to continue.')
            return

    def add_mobile_number_and_otp_combined(self, browser):
        ''' 
        Get phone number then otp from which and send it. 
        If none, return None.
        '''
        global phone_number
        try:
            WebDriverWait(browser, 40).until(
                EC.presence_of_all_elements_located(
                    (By.TAG_NAME, 'div')))
            phone_number, session_number = self.add_mobile_number(browser)
            a = self.add_mobile_otp(browser, phone_number, session_number)
            count = 0
            while not a or browser.title == 'Authentication required':
                if browser.find_elements_by_partial_link_text('Change'):
                    try:
                        browser.find_element_by_partial_link_text('Change').click()
                        WebDriverWait(browser, 40).until(
                            EC.presence_of_all_elements_located(
                                (By.TAG_NAME, 'div')))
                        phone_number, session_number = self.add_mobile_number(browser)

                        a = self.add_mobile_otp(browser, phone_number, session_number)
                    except:
                        browser.get('https://www.amazon.com/ap/cvf/verify')
                        WebDriverWait(browser, 40).until(
                            EC.presence_of_all_elements_located(
                                (By.TAG_NAME, 'div')))
                        phone_number, session_number = self.add_mobile_number(browser)
                        time.sleep(5)
                        a = self.add_mobile_otp(browser, phone_number, session_number)
                else:
                    WebDriverWait(browser, 40).until(
                        EC.presence_of_all_elements_located(
                            (By.TAG_NAME, 'div')))
                    phone_number, session_number = self.add_mobile_number(browser)
                    time.sleep(5)
                    a = self.add_mobile_otp(browser, phone_number, session_number)
                count += 1
                if count == 3:
                    print(f'Exceeding {count} telephone numbers. Please get phone manually.' , 
                    '\n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
                    _ = input('Press enter to continue.')
                    return
            return a
        except Exception as err:
            print(f'Error in add_mobile_number_and_otp_combined: {err}, of {self.name},\
                  \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            _ = input('Press enter to continue.')
            return
                    
    def get_tel(self, phone_number=None, session_number=None):
        ''' This function is getting otp and telephone number.
        {'Id': 12, 'Name': 'Amazon', 'Description': 'Amazon', 'Price': 1000}'''
        token= '9446c33c-afaf-49f6-91d8-478e95f38727'
        serviceid = '29' # Amazon 
        
        # Pick random network
        ran_num = random.randint(1, 3)
        dic_network = {1 : 'VIETTEL', 2: 'VIETNAMMOBILE', 3: 'MOBIPHONE'}
        print(dic_network[ran_num])
        network = dic_network[ran_num]
        user_name_prxy = ""
        pass_word_prxy = ""
        try:
            if not phone_number and not session_number:
                url_request_service = f'http://api.codesim.net/api/CodeSim/DangKy_GiaoDich?apikey={token}&dichvu_id={serviceid}&so_sms_nhan=1' 
                # request_service = requests.get(url_request_service, 
                #                             auth=HTTPBasicAuth(user_name_prxy, 
                #                                                 pass_word_prxy))
                request_service = requests.get(url_request_service)
                
                if request_service.status_code == 200:
                    data = request_service.json()
                    try:
                        phone_number = data["data"]["phoneNumber"]
                        session_number = data["data"]["id_giaodich"]
                        return phone_number, session_number
                    except:
                        return
                else:
                    print(f'Status code: , {request_service.status_code}, \
                        \n>>>>>>>>> Critical Error. Report to IT support. <<<<<<<<<<')
                    return
            else:
                url_request_session = f'http://api.codesim.net/api/CodeSim/KiemTraGiaoDich?apikey={token}&giaodich_id={session_number}'
                request_session = requests.get(url_request_session)
                time.sleep(10)
                if request_session.status_code == 200:
                    data = request_session.json()
                    try:
                        messages = data['data']['listSms']
                        if messages:
                            message = messages[0]['smsContent']
                            otp_tel = re.match('\d{6}', message).group()
                            return otp_tel
                    except:
                        print('No OTP returned. Try next Telephone number.')
                        return

                else:
                    print(f'Bad status code: ,{request_session.status_code},\
                        \n>>>>>>>>> Critical Error. Report to IT support. <<<<<<<<<<<<')
                    return
        except Exception as err:
            print(f'Status code: {request_session.status_code},\
                \n Error in get_tel: {err}, of {self.name},\
                \n>>>>>>>>> Critical Error. Report to IT support. <<<<<<<<<<<<')
            _ = input('Press enter to continue.')
            return

    def accept_services(self, browser):
        ''' This function finds and clicks on Accepts button. '''
        try:
            browser.find_element_by_tag_name('html').send_keys(Keys.END)
            if browser.find_elements_by_xpath(
                '//button[@class="btn btn-primary"]'):
                time.sleep(5)
                browser.find_element_by_xpath(
                    '//button[@class="btn btn-primary"]'
                    ).click() # --> Click on Accept to Terms
        except Exception as err:
            print(f'Error in accept_services: {err}, of {self.name},\
                \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            _ = input('Press enter to continue.')

    def fill_form(self, browser):
        '''
        This function fills main information.
        '''
        try:
            _ , _ , email_add, _ , full_name, country, address_1, \
                city, state, zipcode, phone, name_of_bank, bank_acc, \
                routing, _ = self.read_fetch_files_info(info, i)

            try:
                time.sleep(2)
                # Input Country/Region
                select = Select(browser.find_element_by_xpath(
                    '//select[@name="profileForm.addressForm.countryCode"]'))

                browser.find_elements_by_xpath(
                    '//input[@type="text" and @placeholder="Please choose"]'
                    )[0].send_keys(country)
                
                select.select_by_visible_text(country)
            
            except Exception as err:
                print('1:', err)
                pass
            # Input Business Name = Full name
            time.sleep(3)
            browser.find_element_by_xpath(
                '//input[@type="text" and @id="address-company-input"]'
                ).send_keys(full_name)

            # Input Address Line 1
            time.sleep(3)
            browser.find_element_by_xpath(
                '//input[@type="text" and @id="address-address-line-1-input"]'
                ).send_keys(address_1)

            # Input City
            time.sleep(3)
            browser.find_element_by_xpath(
                '//input[@type="text" and @id="address-city-input"]'
                ).send_keys(city)

            # State/Province/Region
            if country == 'United States':
                try:
                    time.sleep(3)
                    select = Select(browser.find_element_by_xpath(
                        '//select[@name="profileForm.addressForm.stateOrRegion.enumeratedValues[US]"]'))
                    
                    browser.find_elements_by_xpath(
                        '//input[@type="text" and @placeholder="Please choose"]'
                        )[2].send_keys(state)

                    select.select_by_index(0)
                    
                except Exception as err:
                    print('2:', err)
                    pass
            else:
                browser.find_element_by_xpath(
                    '//input[@type="text" and @id="address-state-or-region-input-open"]'
                    ).send_keys(state)

            try:
                # Input Postal code
                time.sleep(3)
                browser.find_element_by_xpath(
                    '//input[@type="text" and @id="address-postal-code-input"]'
                    ).send_keys(zipcode)
            except:
                _ = input('Error Input Postal code. Press any keys to continue.')
                pass

            try:
                # Input Phone
                time.sleep(3)
                browser.find_element_by_xpath(
                    '//input[@type="text" and @id="address-phone-input"]'
                    ).click()
                browser.find_element_by_xpath(
                    '//input[@type="text" and @id="address-phone-input"]'
                    ).send_keys(phone)
            except:
                _ = input('Error Input Phone. Press enter to continue.')
                pass
            # Business email address
            time.sleep(3)
            browser.find_element_by_xpath(
                '//input[@type="text" and @id="address-email-input"]'
                ).send_keys(email_add)

            # Select bank Tell us about your bank
            time.sleep(3)
            try:
                select = Select(browser.find_element_by_xpath('//select[@name="bankCountryCode"]'))
                
                browser.find_elements_by_xpath(
                    '//input[@type="text" and @placeholder="Please choose"]'
                    )[4].send_keys(country)

                select.select_by_visible_text(country)
                
            except Exception as err:
                print('3:', err)
                pass
            
            for _ in range(0, 9):
                browser.find_element_by_tag_name('html').send_keys(Keys.DOWN)
        
            # Account holder name
            time.sleep(3)
            browser.find_element_by_xpath(
                '//input[@type="text" and @id="bank-account-account-holder-name-input"]'
                ).send_keys(full_name)
            
            if country == 'United States':
                # Account number
                time.sleep(3)
                browser.find_element_by_xpath(
                    '//input[@type="text" and @id="bank-account-account-number-input"]'
                    ).send_keys(bank_acc)

                # Account number reentry
                time.sleep(2)
                browser.find_element_by_xpath(
                    '//input[@type="text" and @id="bank-account-account-number-input-reentry"]'
                    ).send_keys(bank_acc)

                # Routing number
                time.sleep(2)
                browser.find_element_by_xpath(
                    '//input[@type="text" and @id="bank-account-routing-number-input"]'
                    ).send_keys(routing)
                
                # Name of bank
                time.sleep(2)
                browser.find_element_by_xpath(
                    '//input[@type="text" and @id="bank-account-bank-name-input-open"]'
                    ).send_keys(name_of_bank)
                # Check if routing number is correct 
                time.sleep(2)
                if browser.find_elements_by_xpath('//div[@class="a-alert-content"]'):
                    pass

            # Case if country is NOT USA              
            else:
                try:
                    # Account number
                    time.sleep(3)
                    browser.find_element_by_xpath(
                        '//input[@type="text" and @id="bank-account-iban-input"]'
                        ).send_keys(bank_acc)
                    # Routing number
                    time.sleep(3)
                    browser.find_element_by_xpath(
                        '//input[@type="text" and @id="bank-account-bic-input"]'
                        ).send_keys(routing)
                    # Name of bank
                    time.sleep(3)
                    browser.find_element_by_xpath(
                        '//input[@type="text" and @id="bank-account-bank-name-input-open"]'
                        ).send_keys(name_of_bank)
                except:
                    _ = input('Error Input Phone. Press enter to continue.')
           
            # Save bank information
            browser.find_element_by_xpath(
                '//input[@data-action="bank-account-save" and @type="submit"]'
                ).click() # --> Click Add
            try:
                WebDriverWait(browser, 50).until(
                    EC.presence_of_element_located(
                        (By.XPATH, 
                        '//input[@data-action="ramp-primary-action-save" and \
                                @class="a-button-input a-declarative primary-continue" and \
                                @type="submit"]'
                        )))
            except:
                pass

            time.sleep(5)
            browser.find_element_by_tag_name('html').send_keys(Keys.END)

            time.sleep(5)
            # Click Save & Continue button
            browser.find_element_by_xpath(
                '//input[@data-action="ramp-primary-action-save" and \
                @class="a-button-input a-declarative primary-continue" and \
                @type="submit"]'
                ).click()
        except Exception as err:
            print(f'''Error in My Account Page: {err}, of {self.name},
            >>>>>>>>>> Report to IT for support. <<<<<<<<<<<

            If encounter this error, please do following steps:
            1. Fill ALL information in "My Account Page".
            2. Check information if it's valid.
            3. Click Save and continue.''')
            self.manual_process()
            return

    def fill_tax(self, browser):
        ''' Fill tax information.'''
        try:
            _, _, _, _, full_name, country, _, _, \
                _, _, _, _, _, _, ssn_ = self.read_fetch_files_info(info, i)
            time.sleep(3)
            browser.find_element_by_partial_link_text(
                'Complete Tax Information'
                ).click() # --> Click Complete Tax Information

            if country == "United States": # This section is for US account
                # For U.S. tax purposes, are you a U.S. person?
                time.sleep(5)
                WebDriverWait(browser, 60).until(
                    EC.presence_of_element_located(
                        (By.XPATH, 
                        '//input[@name="true" and @type="submit"]'
                        )))

                browser.find_element_by_xpath(
                    '//input[@name="true" and @type="submit"]'
                    ).click() # --> click Yes

                browser.find_element_by_tag_name('html').send_keys(Keys.END)
                # Tax Identity Information
                time.sleep(2)
                browser.find_element_by_xpath(
                    '//input[@type="text" and @name="BusinessOrTradeName"]'
                    ).send_keys(full_name)
                
                # Tax ID
                time.sleep(2)
                browser.find_element_by_xpath(
                    '//input[@type="text" and @name="SSN"]'
                    ).send_keys(ssn_)

                # Click continue
                time.sleep(2)
                browser.find_element_by_xpath(
                    '//button[@class="a-button-text" and @id="a-autoid-12-announce"]'
                    ).click()
                for _ in range(0, 25):
                    browser.find_element_by_tag_name('html').send_keys(Keys.DOWN)
                
                # Give Electronic Signature
                time.sleep(7)
                browser.find_element_by_xpath(
                    '//input[@type="text" and @name="ElectronicSignatureW9Name"]'
                    ).send_keys(full_name)
                
                time.sleep(5)
                browser.find_element_by_tag_name('html').send_keys(Keys.END)

                if browser.find_elements_by_xpath(
                    '//button[@class="a-button-text" and @type="button" and @id="a-autoid-91-announce"]'
                    ):
                    browser.find_element_by_xpath(
                        '//button[@class="a-button-text" and @type="button" and @id="a-autoid-91-announce"]'
                            ).click() # --> Click Save and Preview
                else:
                    browser.find_element_by_xpath(
                        '//button[@class="a-button-text" and @type="button" and @id="a-autoid-93-announce"]'
                        ).click() # --> Click Save and Preview

                WebDriverWait(browser, 60).until(
                    EC.presence_of_all_elements_located(
                        (By.TAG_NAME, 'div')))
                
                try:
                    WebDriverWait(browser, 60).until(
                        EC.presence_of_all_elements_located(
                            (By.TAG_NAME, 'li')))
                except:
                    pass
                
                # if something wrong in the address
                time.sleep(5)
                count_submit_form = 0
                for button in browser.find_elements_by_xpath(
                                                '//button[@class="a-button-text"]'):
                        # time.sleep(1)
                        if re.match('Submit Form', button.text):
                            time.sleep(1)
                            count_submit_form += 1
                            break
                if count_submit_form == 0:
                    try:
                        WebDriverWait(browser, 60).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, 
                                '//input[@type="checkbox" and @name="USAddressValidationOverride"]'
                                )))
                        time.sleep(3)
                        if browser.find_elements_by_xpath(
                            '//input[@type="checkbox" and @name="USAddressValidationOverride"]'):
                            browser.find_element_by_xpath(
                                '//input[@type="checkbox" and @name="USAddressValidationOverride"]'
                                ).click() # Click on check box
                            time.sleep(2)

                        WebDriverWait(browser, 60).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, 
                                '//button[@id="editableContent_USAddressEditableContentQuestion_button_done"]'
                                ))).click() # Click Done

                        WebDriverWait(browser, 60).until(
                            EC.presence_of_all_elements_located(
                                (By.TAG_NAME, 'button'))) 
                        for button in browser.find_elements_by_xpath(
                            '//button[@class="a-button-text"]'):
                            time.sleep(1)
                            if re.match('Continue', button.text):
                                button.click() # Click Continue
                        WebDriverWait(browser, 60).until(
                            EC.presence_of_all_elements_located(
                                (By.TAG_NAME, 'button')))
                        browser.find_element_by_tag_name('html').send_keys(Keys.END)                
                        for button in browser.find_elements_by_xpath(
                            '//button[@class="a-button-text"]'):
                            time.sleep(1)
                            if re.findall('" Save and Preview "', button.text):
                                button.click() # Click "Save and Preview"
                    except Exception as err:
                        print(f'{err}')
                        _ = input('Press Save and Preview then Enter.')

                time.sleep(6)
                browser.find_element_by_tag_name('html').send_keys(Keys.END)
                # Tax Form Screen
                try:
                    WebDriverWait(browser, 60).until(
                        EC.presence_of_all_elements_located(
                            (By.TAG_NAME, 'button')))
                except:
                    pass

                time.sleep(2)
                try:
                    browser.find_elements_by_xpath(
                        '//button[@class="a-button-text"]'
                        )[1].click() # --> Click Submit form
                except:
                    for button in browser.find_elements_by_xpath(
                                                '//button[@class="a-button-text"]'):
                        # time.sleep(1)
                        if re.match('Submit Form', button.text):
                            button.click() # --> Click Submit form
                time.sleep(2)
                WebDriverWait(browser, 50).until(
                    EC.presence_of_element_located(
                        (By.XPATH, 
                        '//button[@id="exit-button-id"]'
                        ))).click() # click Exit
                
            else: # This section is for Non US account
                # For U.S. tax purposes, are you a U.S. person?
                time.sleep(5)
                WebDriverWait(browser, 50).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, 
                        '//input[@name="false" and @type="submit"]'
                        )))
                browser.find_element_by_xpath(
                    '//input[@name="false" and @type="submit"]'
                    ).click() # --> click No
                
                # Are you acting as an intermediary agent, or other person receiving payment on 
                # behalf of another person or as a flow-through entity?
                time.sleep(2)
                browser.find_element_by_xpath(
                    '//input[@name="false" and @aria-labelledby="toggleButtonId_IsIntermediaryAgent_false-announce"]'
                    ).click() # --> click No
                # Tax Identity Information    
                time.sleep(2)
                for _ in range(0, 8):
                    browser.find_element_by_tag_name('html').send_keys(Keys.DOWN)
                try:
                    WebDriverWait(browser, 50).until(
                        EC.visibility_of_element_located(
                            (By.XPATH, 
                            '//select[@name="CountryOfCitizenshipCodeResidence"]'
                            )))
                except:
                    pass

                select = Select(browser.find_element_by_xpath(
                    '//select[@name="CountryOfCitizenshipCodeResidence"]'))
                select.select_by_visible_text(country)
                # input tax number
                
                time.sleep(2)
                browser.find_element_by_xpath(
                    '//input[@type="text" and @name="ForeignTINUnifiedUSInterview"]'
                    ).send_keys(ssn_)
                try:
                    # Click continue
                    time.sleep(2)
                    browser.find_element_by_xpath(
                        '//button[@class="a-button-text" and @id="a-autoid-29-announce"]'
                        ).click() # --> click Continue
                except:
                    _ = input('Error. Press Enter to continue.')
                
                # Press button down
                time.sleep(3)
                for _ in range(0, 10):
                    browser.find_element_by_tag_name('html').send_keys(Keys.DOWN)
                
                # Claim of Tax Treaty Benefits
                time.sleep(3)
                select = Select(browser.find_element_by_xpath(
                    '//select[@name="TreatyClaim9aCountryCode"]'))
                select.select_by_visible_text(country)

                try:
                    time.sleep(2)
                    browser.find_element_by_xpath(
                        '//button[@type="button" and @id="a-autoid-83-announce"]'
                        ).click() # --> Press confirm
                except:
                    _ = input('Error. Press Enter to continue.')
                # Sign
                time.sleep(2)
                browser.find_element_by_tag_name('html').send_keys(Keys.END)
                try:
                    browser.find_element_by_xpath(
                        '//input[@type="text" and @name="ElectronicSignatureW8BenName"]'
                        ).send_keys(full_name)
                except:
                    _ = input('Error. Press Enter to continue.')
                
                try:
                    WebDriverWait(browser, 60).until(
                        EC.visibility_of_element_located(
                            (By.XPATH, 
                            '//button[@class="a-button-text" and @type="button" and @id="a-autoid-93-announce"]'
                            )))
                # Save and preview
                    time.sleep(2)
                    browser.find_element_by_tag_name('html').send_keys(Keys.END)
                    browser.find_element_by_xpath(
                        '//button[@class="a-button-text" and @type="button" and @id="a-autoid-93-announce"]'
                        ).click() # --> Click Save and Preview
                except:
                    _ = input('Error. Press Enter to continue.')
                
                # If something wrong with the address    
                try:
                    WebDriverWait(browser, 20).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, 
                            '//input[@type="checkbox" and @name="NonUSPermAddressOverride"]'
                            )))
                    time.sleep(3)
                    if browser.find_elements_by_xpath(
                        '//input[@type="checkbox" and @name="NonUSPermAddressOverride"]'):
                        browser.find_element_by_xpath(
                            '//input[@type="checkbox" and @name="NonUSPermAddressOverride"]'
                            ).click() # Click on check box
                        time.sleep(2)

                    WebDriverWait(browser, 60).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, 
                            '//button[@id="editableContent_NonUSPermanentAddressEditableContentQuestion_button_done"]'
                            ))).click() # Click Done

                    WebDriverWait(browser, 60).until(
                        EC.presence_of_all_elements_located(
                            (By.TAG_NAME, 'button'))) 
                    for button in browser.find_elements_by_xpath(
                        '//button[@class="a-button-text"]'):
                        time.sleep(1)
                        if re.match('Continue', button.text):
                            button.click() # Click Continue
                    WebDriverWait(browser, 60).until(
                        EC.element_to_be_clickable(
                            (By.TAG_NAME, 'button')))
                    browser.find_element_by_tag_name('html').send_keys(Keys.END)

                    for button in browser.find_elements_by_xpath(
                        '//button[@class="a-button-text"]'):
                        time.sleep(1)
                        if re.match('Confirm', button.text):
                            button.click() # Click Confirm 
                    browser.find_element_by_tag_name('html').send_keys(Keys.END)        
                    for button in browser.find_elements_by_xpath(
                        '//button[@class="a-button-text"]'):
                        time.sleep(1)
                        if re.findall('Save and Preview', button.text):
                            button.click() # Click "Save and Preview"
                except:
                    _ = input('Error. Press Enter to continue.')

                try:
                    WebDriverWait(browser, 60).until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, 
                            '//button[@class="a-button-text"]'
                            )))
                except:
                    _ = input('Error. Press Enter to continue.')
                
                browser.find_element_by_tag_name('html').send_keys(Keys.END)
                browser.find_elements_by_xpath(
                    '//button[@class="a-button-text"]'
                    )[1].click() # --> Click Submit form

                WebDriverWait(browser, 60).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, 
                        '//button[@id="exit-button-id"]'
                        ))).click() # --> Click Exit Interview
                
        except Exception as err:
            print(f'''Error in Interviewing Tax Form: {err}, of {self.name},
            >>>>>>>>>> Report to IT for support. <<<<<<<<<<<'

            If encounter this error, please do following steps:
            1. Fill ALL information in "Tax form Interview".
            2. Check information if it's valid.
            3. Click "Save and Preview".
            4. Click "Submit form".
            5. Click "Exit Interview".
            6. Hit Enter to continue.''')
            self.manual_process()


    def delete_tel_number(self, browser, barcode):
        ''' This function runs after filling info to delete Mobile phone number'''
        try:
            time.sleep(3)
            WebDriverWait(browser, 40).until(
                EC.presence_of_all_elements_located(
                    (By.TAG_NAME, 'input')))
            # Check if Add mobile number:
            if browser.find_elements_by_xpath(
                '//span[@class="a-button-text" and @id="a-autoid-3-announce"]'):
                if browser.find_element_by_xpath(
                    '//span[@class="a-button-text" and @id="a-autoid-3-announce"]'
                    ).text.strip() == "Add":
                    return
            # if Ask to Sign in Amazon.com
            if browser.find_elements_by_xpath('//h1[@class="a-spacing-small"]'):
                self.sign_in_amzdotcom(browser)

            # If require password OTP:
            time.sleep(5)
            if browser.find_elements_by_xpath(
                '//input[@id="auth-send-code" and @class="a-button-input"]'):
                time.sleep(5)
                browser.find_element_by_xpath(
                    '//input[@id="auth-send-code" and @class="a-button-input"]'
                    ).click() # Click Send OTP
                time.sleep(3)
                totp = self.get_totp(barcode)
                browser.find_element_by_xpath(
                    '//input[@type="tel" and @id="auth-mfa-otpcode"]'
                    ).send_keys(totp) # Enter OTP number

                browser.find_element_by_xpath(
                    '//input[@class="a-button-input" and @id="auth-signin-button"]'
                    ).click() # Enter OTP number   
                
            WebDriverWait(browser, 40).until(
                EC.presence_of_element_located(
                    (By.XPATH, 
                    '//input[@id="auth-cnep-edit-phone-button" and @type="submit"]'
                    )))
            
            browser.find_element_by_xpath(
                '//input[@id="auth-cnep-edit-phone-button" and @type="submit"]'
                ).click() # --> click on Edit

            WebDriverWait(browser, 40).until(
                EC.presence_of_all_elements_located(
                    (By.TAG_NAME, 'div')))

            WebDriverWait(browser, 40).until(
                EC.presence_of_all_elements_located(
                    (By.TAG_NAME, 'button')))
            # Two step verification
            time.sleep(5)
            if browser.title == 'Two-Step Verification':
                self.resend_old_number(browser)

            time.sleep(5)
            browser.find_element_by_xpath(
                '//button[@type="submit" and @class="auth-html-button-inside-link"]'
                ).click() # --> Click Delete
            WebDriverWait(browser, 40).until(
                EC.presence_of_all_elements_located(
                    (By.TAG_NAME, 'input')))
            time.sleep(5)
            browser.find_element_by_xpath(
                '//input[@id="ap-remove-mobile-claim-submit-button" and @name="deleteMobilePhone"]'
                ).click() # --> Click Yes Delete

        except Exception as err:
            print(f'Error in delete_tel_number: {err}, of {self.name},\
                \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            _ = input('Press enter to continue.')
            return
        
    def two_step_verify(self, browser):
        try:
            # Go to https://www.amazon.com/gp/css/account/info/view.html
            browser.execute_script("window.open('');")
            time.sleep(3)
            # Switch to the new window
            browser.switch_to.window(browser.window_handles[1])
            browser.get("https://www.amazon.com/gp/css/account/info/view.html")

            WebDriverWait(browser, 60).until(
                EC.presence_of_all_elements_located(
                    (By.TAG_NAME, 'div')))
            # Sign in Amazon.com
            if browser.find_elements_by_xpath('//h1[@class="a-spacing-small"]'):
                self.sign_in_amzdotcom(browser) 

            WebDriverWait(browser, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, 
                    '//input[@id="auth-cnep-advanced-security-settings-button" and @type="submit"]'
                    )))
            time.sleep(5)
            browser.find_element_by_xpath(
                '//input[@id="auth-cnep-advanced-security-settings-button" and @type="submit"]'
                ).click() # --> Click Edit two step verification

            time.sleep(5)
            # Press Add new phone or Authenticator App
            
            browser.find_element_by_link_text('Add new phone or Authenticator App').click()
            time.sleep(5)
            if not browser.find_elements_by_xpath(
                '//div[@class="a-section a-padding-base a-text-left"]'
                ):
                self.sign_in_amzdotcom(browser)
            # browser.find_element_by_xpath(
            #     '//i[@class="a-icon a-accordion-radio a-icon-radio-inactive"]'
            #     ).click() # Click to choose other authenticator

            WebDriverWait(browser, 40).until(
                EC.presence_of_element_located(
                    (By.LINK_TEXT, "Can't scan the barcode?")
                    ))
            browser.find_element_by_link_text("Can't scan the barcode?").click() # click on "Can't scan the barcode?"
            time.sleep(5)
            barcode = browser.find_element_by_xpath(
                '//span[@id="sia-auth-app-formatted-secret"]'
                ).text # Copy barcode number
            barcode = barcode.replace(' ','') # Replace blanks with non-blanks
            # Get TOTP from barcode:
            try:
                time.sleep(2)
                totp = self.get_totp(barcode)
                # Input OTP 
                browser.find_element_by_xpath(
                    '//input[@type="text" and @name="verificationCode"]'
                    ).send_keys(totp)
        
                time.sleep(1)
                # Click Verify OTP and continue
                browser.find_element_by_xpath(
                    '//input[@id="ch-auth-app-submit" and @class="a-button-input"]'
                    ).click()
            except:
                totp = self.get_totp(barcode)
                _ = input(f'OTP may be timeout. Input new OTP: {totp} and Press Enter to continue.')
                # Click Verify OTP and continue
                browser.find_element_by_xpath(
                    '//input[@id="ch-auth-app-submit" and @class="a-button-input"]'
                    ).click()
                
            WebDriverWait(browser, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, 
                    '//a[@class="a-link-normal ch-settings-remove-phone"]'
                    )))
            # Click Remove
            try:
                browser.find_element_by_xpath(
                    '//a[@class="a-link-normal ch-settings-remove-phone"]'
                    ).click()
            except:
                _ = input('Press enter to continue.')
            time.sleep(3)
            WebDriverWait(browser, 40).until(
                EC.presence_of_all_elements_located(
                    (By.TAG_NAME, 'input')))
            # Click remove this number
            try:
                browser.find_element_by_xpath(
                    '//input[@id="confirm-remove-dialog-backup-0-submit" and @type="submit"]'
                    ).click()
            except:
                browser.find_element_by_xpath(
                    '//input[@id="confirm-remove-dialog-backup-1-submit" and @type="submit"]'
                    ).click()
            
            WebDriverWait(browser, 40).until(
                EC.presence_of_element_located(
                    (By.XPATH, 
                    '//a[@id="ch-breadcrumb-cas" and @class="a-link-normal"]'
                    )))

            browser.find_element_by_xpath(
                '//a[@id="ch-breadcrumb-cas" and @class="a-link-normal"]'
                ).click() # --> Click Login & security
            return barcode  
        except Exception as err:
            print(f'Error in two_step_verify: {err}, of {self.name},\
                \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            _ = input('Press enter to continue.')

    def get_totp(self, barcode):
        ''' Get TOTP for verification two step'''
        try:
            totp = pyotp.TOTP(barcode).now()
            print(totp)
            return totp
        except Exception as err:
            print(f'Error in get_totp: {err}, of {self.name},\
                 \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            _ = input('Press enter to continue.')

    def sign_up_form(self, browser):
        ''' Sign up Form if fill in info is passed.'''
        try:
            org_name, add_info, website = self.read2_fetch_files_info(info, i)
            # Input Industry type
            try:
                select = Select(browser.find_element_by_xpath(
                    '//select[@formcontrolname="industryType"]'))
            except:
                WebDriverWait(browser, 50).until(
                    EC.presence_of_element_located(
                        (By.XPATH, 
                        '//select[@formcontrolname="industryType"]'
                        )))
                select = Select(browser.find_element_by_xpath(
                    '//select[@formcontrolname="industryType"]'))
            # Small Business Novelty T-shirt Business
            dict_bus = {0:"Small Business", 1:"Novelty T-shirt Business"}
            ran_num = random.randint(0, 1)
            select.select_by_value(dict_bus[ran_num])

            for _ in range(0, 9):
                browser.find_element_by_tag_name('html').send_keys(Keys.DOWN)
            # Input Organization Name
            time.sleep(2)
            browser.find_element_by_xpath(
                '//input[@formcontrolname="orgName"]'
                ).send_keys(org_name)
            # Input Additional Information
            time.sleep(20)
            browser.find_element_by_xpath(
                '//textarea[@formcontrolname="additionalInfo"]'
                ).send_keys(add_info)
            # Input Website (optional)
            time.sleep(2)
            browser.find_element_by_xpath(
                '//input[@formcontrolname="websiteOpt"]'
                ).send_keys(website)
            browser.find_element_by_tag_name('html').send_keys(Keys.END)
            _ = input('Press enter to continue.')
        except Exception as err:
            print(f'Error in sign_up_form: {err}, of {self.name},\
                \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            self.manual_process()
        return

    def sign_in_amzdotcom(self, browser):
        try:
            time.sleep(5)
            
            _, _, _, pass_word, _, _, _, _, _, _,\
                 _, _, _, _, _ = self.read_fetch_files_info(info, i)
            WebDriverWait(browser, 40).until(
                EC.presence_of_all_elements_located(
                    (By.TAG_NAME, 'html')))
            if browser.find_elements_by_xpath(
                '//input[@type="password" and @id="ap_password"]'):
                time.sleep(1)
                browser.find_element_by_xpath(
                    '//input[@type="password" and @id="ap_password"]'
                    ).send_keys(pass_word)
            
            if browser.find_elements_by_xpath(
                '//input[@id="signInSubmit" and @type="submit"]'):
                time.sleep(2)
                browser.find_element_by_xpath(
                    '//input[@id="signInSubmit" and @type="submit"]'
                    ).click() # --> Click SignIn
            
            # if Add mobile number pops up:
            if browser.find_elements_by_partial_link_text('Not now'):
                time.sleep(5)
                browser.find_element_by_partial_link_text('Not now').click()
            # If check mail for security:
            if browser.find_elements_by_xpath(
                    '//span[@class="a-size-base-plus transaction-approval-word-break a-text-bold"]'
                    ):
                for notify_text in browser.find_elements_by_xpath(
                    '//span[@class="a-size-base-plus transaction-approval-word-break a-text-bold"]'
                    ):
                    time.sleep(1)
                    if notify_text.text == 'For your security, approve the notification sent to:':
                        # Get link mail from amazon
                        link = self.get_link_senttoemail_sign_in_amzdotcom()
                        browser.get(link)
                        WebDriverWait(browser, 40).until(
                            EC.presence_of_all_elements_located(
                                (By.TAG_NAME, 'a')))
                        time.sleep(1)
                        browser.find_element_by_xpath(
                            '//input[@name="customerResponseApproveButton" and @type="submit"]'
                            ).click() # -->click Approve
                        break
            elif browser.find_elements_by_xpath(
                    '//span[@class="a-size-medium transaction-approval-word-break a-text-bold"]'
                    ):
                for notify_text in browser.find_elements_by_xpath(
                    '//span[@class="a-size-medium transaction-approval-word-break a-text-bold"]'
                    ):
                    time.sleep(1)
                    if notify_text.text == 'For your security, approve the notification sent to:':
                        # Get link mail from amazon
                        link = self.get_link_senttoemail_sign_in_amzdotcom()
                        browser.get(link)
                        WebDriverWait(browser, 40).until(
                            EC.presence_of_all_elements_located(
                                (By.TAG_NAME, 'a')))
                        time.sleep(1)
                        browser.find_element_by_xpath(
                            '//input[@name="customerResponseApproveButton" and @type="submit"]'
                            ).click() # -->click Approve
                        break
        except Exception as err:
            print(f'Error in sign_in_amzdotcom: {err}, of {self.name},\
                 \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            self.manual_process()
            return

    def get_link_senttoemail_sign_in_amzdotcom(self):
        ''' Get link from amazon to confirm user.'''
        try:
            time.sleep(15)
            with IMAPClient(host='outlook.office365.com', port=993, use_uid=True) as server:
                _, _, email_add, pass_word, _, _, _, _, \
                    _, _, _, _, _, _, _ = self.read_fetch_files_info(info, i)
                server.login(email_add, pass_word)
                server.select_folder('INBOX') # search in INBOX
                messages = server.search(['FROM', 'account-update@amazon.com']) # FROM: account-update@amazon.com
            # for each unseen email in the inbox
                if messages:
                    max_date = datetime.now().replace(
                        hour=0, minute=0, second=0, microsecond=0
                        )
                    msgid_max = 0
                    
                    for msgid, data in server.fetch(messages,['ENVELOPE']).items():
                        if data[b'ENVELOPE'].date >= max_date:
                            max_date = data[b'ENVELOPE'].date
                            msgid_max = msgid

                    for msgid, message_data in server.fetch(messages, ['RFC822']).items():
                        if msgid == msgid_max:
                            email_message = email.message_from_bytes(message_data[b'RFC822'])
                            for part in email_message.get_payload():
                                # Convert a byte like to a string
                                otp_string = str(part.get_payload(decode=True), 
                                                part.get_content_charset(), "ignore")
                                # Use BeautifulSoup to rear html string
                                soup = BeautifulSoup(otp_string, "lxml")
                                # Get link from a
                                for a in soup.findAll('a'):
                                    if re.match('^https://www.amazon.com/', a.text.strip()):
                                        return a.text.strip()
                else:
                    return
        except Exception as err:
            print(f'Error in get_link_senttoemail_sign_in_amzdotcom: {err}, of {self.name},\
                 \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            self.manual_process()
            return

    def write_barcode_to_csv(self, email_add, barcode):
        ''' Write down barcode '''
        _, _, _, pass_word, _, \
        _, _, _, _, _, \
        _, _, _, _, _ = self.read_fetch_files_info(info, i)
        try:
            if os.path.isfile('barcode.csv'):
                with open('barcode.csv', 'a', encoding='utf-8', newline='') as f:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow([email_add, pass_word, barcode])
            else:
                with open('barcode.csv', 'w', encoding='utf-8', newline='') as f:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow(['Email', 'Pass word', 'Barcode number'])
                    csv_writer.writerow([email_add, pass_word, barcode])
        except Exception as err:
            print(f'Error in write_barcode_to_csv: {err}, of {self.name},\
                 \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            pass

    def resend_old_number(self, browser):
        ''' This function to resend OTP code from the old tel number'''
        try:
            # Retake phone number
            session_number = self.get_tel(phone_number)
            time.sleep(5)
            browser.find_element_by_xpath(
                '//input[@id="auth-send-code"]'
                ).click() # --> Click get OTP
            otp_tel = self.get_tel(phone_number, session_number)
            # Input OTP code with old number
            time.sleep(5)
            if otp_tel:
                browser.find_element_by_xpath(
                    '//input[@type="tel" and @id="auth-mfa-otpcode"]'
                    ).send_keys(otp_tel)
            browser.find_element_by_xpath(
                '//input[@id="auth-signin-button"]'
                ).click()
        except Exception as err:
            print(f'Error in resend_old_number: {err}, of {self.name},\
                 \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            _ = input(f'Trying number {phone_number} but fail. Press enter to continue.')


    def log_in_amz(self, browser):
        ''' This function is for logging in merch.Amazon.com'''
        try:
            # logging.debug('Start of log_in_amz')
            _, _, email_add, _, _, _, _, _, _, _, \
                _, _, _, _, _ = self.read_fetch_files_info(info, i)

            time.sleep(5)
            self.sign_up_and_create_account(browser)

            WebDriverWait(browser, 60).until(
                EC.presence_of_all_elements_located(
                    (By.TAG_NAME, 'div')))

            # Bypass 3 iframes
            if browser.find_elements_by_xpath(
                "//iframe[@id='cvf-arkose-frame']"):
                self.solve_puzzle(browser)

            WebDriverWait(browser, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, 
                    '//input[@type="text" and @name="code"]'
                    )))
            # Fill email browser step
            self.fill_email_otp(browser)
            
            # Fill verification mobile number
            time.sleep(5)
            try:
                WebDriverWait(browser, 40).until(
                    EC.presence_of_all_elements_located(
                        (By.TAG_NAME, 'select')))
                if browser.find_elements_by_xpath(
                    '//select[@name="cvf_phone_cc" and @id="cvf_phone_cc_native"]'):
                    a = self.add_mobile_number_and_otp_combined(browser)
                    if not a:
                        ans = input('''Critical error in Verifying telephone number. 
                        Do you want to move to next info [Y|N]? (This info can no longer use)''')
                        if ans.lower() == 'y':
                            return
                        else:
                            _ = input('''If No, please: 
                                    1. Enter phone and OTP manually. 
                                    2. Press Send OTP and hit Enter to continue.''')
            except: 
                _ = input('''Error in verifying telephone number. 
                1. Enter phone and OTP manually. 
                2. Press Send OTP and hit enter to continue.''')
                pass
            
            try:    
                WebDriverWait(browser, 40).until(
                    EC.presence_of_element_located(
                        (By.XPATH, 
                        '//button[@class="btn btn-primary"]'
                        )))
            except:
                if browser.find_elements_by_tag_name('h4'):
                    for h4 in browser.find_elements_by_tag_name('h4'):
                        if re.match('Are you an existing customer?', h4.text):
                            _ = input('''Criticial Error. Start registering another account info 
                            (This info can no longer use). Press enter to continue.''')
                            return

            # Terms:
            self.accept_services(browser)
            
            # Sign up for a Merch by Amazon account screen
            try:
                WebDriverWait(browser, 60).until(
                    EC.presence_of_element_located(
                        (By.XPATH, 
                        '//a[@class="btn btn-primary mt-small"]'
                        )))

                time.sleep(5)
                if browser.find_elements_by_xpath(
                    '//a[@class="btn btn-primary mt-small"]'):
                    browser.find_element_by_xpath(
                        '//a[@class="btn btn-primary mt-small"]'
                        ).click() # --> Click Continue
            except:
                pass
            # Two step Verification (if-any)
            time.sleep(6)
            try:
                WebDriverWait(browser, 50).until(
                    EC.presence_of_all_elements_located(
                        (By.TAG_NAME, 'select')))
                if browser.title == 'Amazon Two-Step Verification':
                    self.add_mobile_number_and_otp_combined(browser)
            except: 
                pass
            try:
                WebDriverWait(browser, 50).until(
                    EC.presence_of_all_elements_located(
                        (By.PARTIAL_LINK_TEXT, 'My Account')))
            except:
                _ = input('Does not recognize MY ACCOUNT Main page. Press Enter when get into MY ACCOUNT Main page.')
            # Fill in forms
            if browser.find_elements_by_partial_link_text('My Account'):
                self.fill_form(browser)

            # Escape to Sign up for a Merch by Amazon account screen
            time.sleep(10)
            try:
                WebDriverWait(browser, 60).until(
                    EC.presence_of_element_located(
                        (By.XPATH, 
                        '//a[@class="btn btn-primary mt-small"]'
                        )))
            except:
                _ = input('Information Error. Please input correct information. \
                    \nPress "Save and Continue" button then Press enter to continue.')
            
            WebDriverWait(browser, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, 
                    '//a[@class="btn btn-primary mt-small"]'
                    )))
            if browser.find_elements_by_xpath(
                '//a[@class="btn btn-primary mt-small"]'):
                browser.find_element_by_xpath(
                    '//a[@class="btn btn-primary mt-small"]'
                    ).click() #--> Click Continue

            WebDriverWait(browser, 60).until(
                EC.presence_of_all_elements_located(
                    (By.TAG_NAME, 'div')))

            # Interview tax form
            time.sleep(6)
            browser.find_element_by_tag_name('html').send_keys(Keys.END)
            time.sleep(1)
            if browser.find_elements_by_partial_link_text('Complete Tax Information'):
                self.fill_tax(browser)
            
            try:
                WebDriverWait(browser, 60).until(
                    EC.presence_of_element_located(
                        (By.PARTIAL_LINK_TEXT, 'My Account')))
            except:
                _ = input(
                    'Does not recognize MY ACCOUNT Main page. Press Enter when get into MY ACCOUNT Main page.'
                    )

            time.sleep(5)
            browser.find_element_by_tag_name('html').send_keys(Keys.END)
            time.sleep(2)
            try:
                browser.find_element_by_xpath(
                    '//input[@data-action="ramp-primary-action-save" and\
                    @aria-labelledby="primary-action-save-and-continue-announce"]'
                    ).click() #--> Click "Save and Continue"
            except:
               _ = input(
                    'Does not recognize "Save and Continue" button. Press Enter when get into MY ACCOUNT Main page.'
                    ) 
            
            # Need a ALL CHECK here
            WebDriverWait(browser, 50).until(
                EC.presence_of_all_elements_located(
                    (By.TAG_NAME, 'html')))
            WebDriverWait(browser, 50).until(
                EC.presence_of_all_elements_located(
                    (By.TAG_NAME, 'div')))
            WebDriverWait(browser, 50).until(
                EC.presence_of_all_elements_located(
                    (By.TAG_NAME, 'h1')))
            time.sleep(5)
            try: 
                if browser.find_elements_by_xpath(
                    '//div[@class="col-9"]'
                    )[0].find_element_by_tag_name('h1').text == "Sign up Form":
                    self.sign_up_form(browser)
            except:
                if re.match('Merch by Amazon', browser.title):
                    self.sign_up_form(browser)

            # Two verification step
            barcode = self.two_step_verify(browser)
            self.write_barcode_to_csv(email_add, barcode)
            # Step Delete phone number
            self.delete_tel_number(browser, barcode)

            # Press "Done"
            if browser.find_elements_by_xpath(
                '//a[@id="auth-cnep-done-button"]'):
                browser.find_element_by_xpath(
                    '//a[@id="auth-cnep-done-button"]'
                    ).click()

        except Exception as err:
            print(f'Error in log_in_amz: {err}, of {self.name},\
                 \n>>>>>>>>>> Report to IT for support. <<<<<<<<<<<')
            self.manual_process()
            return

    # def disable_debug_messages(func):
    #     def wrapper(*args, **kwargs):
    #         prev_state = logger.disabled
    #         logger.disabled = True
    #         result = func(*args, **kwargs)
    #         logger.disabled = prev_state
    #         return result
    #     return wrapper

    def manual_process(self):
        ''' Error Handling Function.
        When there are any error that can not be catched whilst reg acc, 
        this function is the last error handling for manually reg acc.'''
        ans_manual = input('You have entered manual mode.\
            \nDo you want to reg account manually for this step? [Y|N]'.center(120)).lower()

        if ans_manual == 'n':
            return
        else:
            _, _, email_add, pass_word, full_name, \
            country, address_1, city, state, zipcode, \
            phone, name_of_bank, bank_acc, routing, ssn_ = self.read_fetch_files_info(info, i)
            org_name, add_info, website = self.read2_fetch_files_info(info, i)
            print('-'*60)
            print('Manual Process. You may need these info:')
            print(f'Email address: {email_add}, \nPass word: {pass_word}, \
            \nFull name: {full_name}, \nCountry: {country}, \nAddress: {address_1},\
            \nCity: {city}, \nState: {state}, \nZipCode: {zipcode},\nPhone: {phone},\
            \nName of Bank: {name_of_bank}, \nBank Account: {bank_acc}, \nRouting: {routing},\
            \nSSN: {ssn_}, \nOrganaization Name: {org_name}, \nAdditional info: {add_info}, \nWebsite: {website}')
            print('-'*60)
            _ = input('Press any key when you finish reg acc'.center(120)).lower()
            return

if __name__ == '__main__':
    global logger
    logger = logging.getLogger()
    logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')
    logging.debug('Start of program.')
    headers()
    # Execute the program
    chrome1 = RegisterTool('chrome1')
        
    logging.debug('End of program.')