# Cleaned up version of the user-provided python script

import os
import time
import random
import datetime
import sys
import requests
import imaplib
import email
import nltk
from nltk.corpus import words
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
import json
import undetected_chromedriver as uc

# Variables
nltk.download('words')
word_list = words.words()  
cwd = os.getcwd()

# Add your email domains here
working_domains = ["@xanthocya.online","@unpaganizesc.online","@tweaga.online","@hexastemo.online","@bedriddenpre.online",
                   "@chilal.online","@shelterw.online","@mayingbr.store","@broadaxenh.store","@acetumswa.store","@wegolfot.store",
                   "@salmwoodflatule.store","@ejusdomen.store","@abnegatefeathe.store","@heartbr.online","@keraph.online",
                   "@heartbr.site","@calandriapa.site","@resparklechrono.online","@resparklechrono.site","@calandriapa.online",
                   "@btsfanarts.site","@aquavibes.store", "@aquavibes.shop","@magmavibes.store","@magmavibes.site","@btsstore.site",
                   "@btsfanarts.store","@sdfwerwer34.site","@deinefettemum.store","@deinefettemum.site","@dummerhund.site",
                   "@unblottedg.online","@cakeedit.online","@leavelessem.online","@boardaward.click","@thurif.click","@nosohem.click",
                   "@saleswoma.click","@shibarse.online","@shibarse.click","@romaniumplung.click","@romaniumplung.online"]

# Telegram Bot Token
api_token = '5616024717:AAGRMs9HqPyn1YbrwS7QW8DkHFEJy0R6mVo'
chat_id = '5196018306'

def generate_username():
    """
    Generate a random username with length between 6 and 15.
    """
    username_length = random.randint(6, 15)
    username_words = random.choices(word_list, k=username_length//3 + 1)
    username = ''.join([word.capitalize() for word in username_words])[:username_length]
    
    return username

def send_message_telegram(text):
    """
    Send messages to a Telegram account.
    """
    api_url = f'https://api.telegram.org/bot{api_token}/sendMessage'
    params = {'chat_id': chat_id, 'text': text}
    response = requests.post(api_url, data=params)

def print_and_log(text, account, error=False):
    """
    Print log with current timestamp and account name.
    """
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"[{time_now}] --- [{account}] --- {text}"
    print(message)

def dump_cookies(driver, account):
    """
    Save the cookies to avoid login issues for bots. We're using the cookies to login instead of filling out the login-form.    
    """
    cookies = driver.get_cookies()
    if os.path.exists(f'{cwd}/cookies') == False:
        os.mkdir(f'{cwd}/cookies')
    with open(f'{cwd}/cookies/{account}.json', 'w', newline='') as outputdata:
        json.dump(cookies, outputdata) 

def save_username_to_file(account):
    """
    Add the created username to the newaccounts txt file.
    """
    with open('/var/www/AccCreation/kickaccounts.txt', 'a') as f:
        f.write(f"{account}\n")


def fill_register_form(driver, accountname, domain):
    """
    Click the register button on the page.
    """
    try:
        Register_Button = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, 'signup-button')))
        driver.execute_script("arguments[0].click();", Register_Button)
    except:
        driver.close()

    """
    Fill the registration form on the page.
    """
    action = ActionChains(driver)
    try:
        Email_Form = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, 'input-element')))
        driver.execute_script("arguments[0].click();", Email_Form)
        action.send_keys(accountname).send_keys(domain).perform()                                        # Enter Account Name
        action.send_keys(Keys.TAB).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()    # Month
        time.sleep(0.7)
        action.send_keys(Keys.TAB).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()    # Day
        time.sleep(0.7)
        action.send_keys(Keys.TAB).send_keys(Keys.ARROW_UP).send_keys(Keys.ARROW_UP).send_keys(Keys.ENTER).perform()    # Year
        time.sleep(0.7)
        action.send_keys(Keys.TAB).send_keys(accountname).perform()                                                         # Account Name
        time.sleep(0.7)
        action.send_keys(Keys.TAB).send_keys("BotAccount123!").perform()                                                    # Password
        time.sleep(0.3)
        action.send_keys(Keys.TAB).send_keys("BotAccount123!").perform()                                                    # Password Confirmation
        time.sleep(0.3)
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        driver.execute_script("arguments[0].click();", submit_button)
        receive_by_mail = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Receive')]")))
        time.sleep(0.5)
        receive_by_mail.click()
        time.sleep(1)
        # KICK ADDED SOMETHING TO PREVENT ME FROM CLICKING INTO KICK CODE INPUT - WE BYPASSING THIS BY GOING BACK TO THE REGISTER FROM AND FORTH TO THE KICK CODE INPUT
        action.send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
        time.sleep(1)
        action.send_keys(Keys.ENTER).perform()
        time.sleep(1)
        action.send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
        time.sleep(1)

        print_and_log("KICK REGISTER FORM - SUCCESSFULLY FILLED!", accountname)
    except Exception as e:
        print_and_log(f"KICK REGISTER FORM - ERROR! {e}", accountname)
        driver.quit()

def get_kick_code(driver, accountname):
    """
    Open the temporary mail.
    """

    time.sleep(random.randint(10, 15))

    action = ActionChains(driver)
   
    try:

        # Connect to the Roundcube IMAP server
        imap_server = 'gama.belldns.com'
        username = 'spam_emails@themysterypanda.info'
        password = 'iS9cZ4dkjSDmDE9'

        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(username, password)

        # Select the mailbox/folder you want to access
        mailbox = 'INBOX'
        imap.select(mailbox)

        # Search for emails addressed to a specific recipient
        status, data = imap.search(None, f'(TO "{accountname}")')

        # Get the list of email IDs
        email_ids = data[0].split()

        # Fetch the most recent email
        latest_email_id = email_ids[-1]
        status, email_data = imap.fetch(latest_email_id, '(RFC822)')

        # Process the email data
        raw_email = email_data[0][1]
        email_message = email.message_from_bytes(raw_email)
        # Print the subject
        # Extract the subject
        subject = email_message['Subject']
        subject_text = subject[:6]
        print_and_log(f"KICK CODE - {subject_text}", accountname)

        # Close the connection
        imap.logout()

        for letter in subject_text:
            action.send_keys(letter).perform()
            time.sleep(0.2) 

    except:
        print_and_log(f"KICK CODE - ERROR", accountname)
        driver.close()



def accept_terms_of_condition(driver):
    """
    Accept the terms of condition.
    """
    time.sleep(1)
    try:
        # This is mostly not working for whatever reason. 
        Submit_Button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Accept')]")))
        Submit_Button.click()
    except:
        # Here we use some TABS instead to get to the Accept-Button and hit Enter
        action = ActionChains(driver)
        action.send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).perform()
        action.send_keys(Keys.ENTER).perform()        

def follow_channel(driver, account):
    """
    Check if the login was successful and follow channel.
    """
    try:
        # Check if login button is present. If it is present, the login was not successful - We close the session
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, 'login-button')))
        print_and_log(f"ERROR CREATING ACCOUNT!", account)
        driver.quit()
    except:
        print_and_log(f"ACCOUNT SUCCESSFULLY CREATED!", account)
        save_username_to_file(account)
        time.sleep(3)
        try:
            channel_url = f"https://kick.com/{channel_name}"
            driver.get(channel_url)
            follow_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Follow')]")))
            time.sleep(2)
            driver.execute_script("arguments[0].click();", follow_button)
            print_and_log(f"SUCCESSFULLY FOLLOWED {channel_name}", account)
            time.sleep(2)
        except:
            print_and_log(f"ERROR FOLLOWING {channel_name.upper()}", account)
        time.sleep(1)
        driver.delete_all_cookies()
        time.sleep(2)
        driver.quit()
        send_message_telegram(f"Successfully Completed Account Creation for {account}")


def create_accounts(amount_of_bots, channel_name):
    """
    Create accounts for a given amount of bots and a channel name.
    """
    for i in range(int(amount_of_bots)):
        try:
            account = generate_username()


            chosen_domain = random.choice(working_domains)

            #random_user = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random.randint(500, 599)}.36 (KHTML, like Gecko) Chrome/{random.randint(80, 89)}.0.{random.randint(4000, 5000)}.{random.randint(1, 100)} Safari/{random.randint(500, 599)}.36'

            options = uc.ChromeOptions()
            options.add_argument("https://kick.com")  
            options.add_argument(f'--proxy-server=http://p.webshare.io:9999')
            options.add_argument(f'--no-sandbox')
            options.add_argument(f'--headless=new')

            # set options to prevent Chrome from showing the "Chrome is being controlled by automated test software" notification
            options.add_argument('--disable-logging')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-web-security")
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)
            driver = uc.Chrome(options=options)

            # Check if the proxy is blocked and close the chrome instance
            if "blocked" in driver.page_source:
                driver.quit()

            else:

                print_and_log(f"STARTED TO CREATE ACCOUNT ...", account)
                fill_register_form(driver, account, chosen_domain)
                get_kick_code(driver, account)
                accept_terms_of_condition(driver)
                dump_cookies(driver, account)
                # Add a small delay to allow time to login. 3 seconds are enough
                time.sleep(random.uniform(3, 5))  # Add random delay between actions
                follow_channel(driver, account)

        except Exception as e:
            print_and_log(f"ERROR CREATING ACCOUNT!", account)
            driver.quit()
            continue

if __name__ == "__main__":
    amount_of_bots, channel_name = sys.argv[1:]
    create_accounts(amount_of_bots, channel_name)
