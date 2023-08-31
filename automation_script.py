import csv
import time
import logging
from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

# def process_csv_to_webclient(csv_filepath, stop_event=None):
def process_csv_to_webclient(csv_filepath, username, password, phone_column_name, url, template, did, stop_event=None):

    log = logging.basicConfig(level=logging.INFO)
    # Initialize WebDriver
    driver = webdriver.Chrome()

    # Open the dynamic URL
    # url = "https://1179.3cx.cloud/webclient/#/login?next=%2Foffice"
    driver.get(url)

    # Wait for the username field to become visible
    wait = WebDriverWait(driver, 10)
    username_field = wait.until(EC.visibility_of_element_located((By.ID, "loginInput")))

    # Enter username
    # username_field.send_keys("13310")
    username_field.send_keys(username)

    # Wait for the password field to become visible
    password_field = wait.until(EC.visibility_of_element_located((By.ID, "passwordInput")))

    # Enter password
    # password_field.send_keys("75SVQO95zCfT7zp0")
    password_field.send_keys(password)

    # Locate the submit button by ID and click it
    submit_button = wait.until(EC.element_to_be_clickable((By.ID, "submitBtn")))
    submit_button.click()

    # Wait for the chat icon to become visible and click it
    chat_link = wait.until(EC.element_to_be_clickable((By.ID, "menuChat")))
    chat_link.click()

    # Wait for the page to load
    
    
    with open(csv_filepath, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            #print(row.keys())
            if stop_event and stop_event.is_set():
                break

            agent_phone = row[phone_column_name]
            if agent_phone:
                agent_phone_with_prefix = '+1' + agent_phone
                # this clicks on the plus sign to open the text options 
                new_chat_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-id='btnNewChat']")))
                
                new_chat_button.click()

                # this click on the SMS button to open the text field 
                send_sms_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-id='btnStartSmsChat']")))
                
                send_sms_button.click()
                
                #place number in text
                input_field = driver.find_element(By.ID, "inputChatCompose")
                
                input_field.send_keys(agent_phone_with_prefix)
                
                input_field.send_keys(Keys.RETURN)
                  # Wait before sending the message
                print(f"going to jump in xpath //app-provider-item")
            
           
                #provider_item = driver.find_element(By.XPATH, "//app-provider-item")
                provider_item = driver.find_element(By.XPATH, f"//small[contains(text(),'{did}')]")
                provider_item.click()
                
                print(f"right after the click")
                

                # Click on the phone number element
                print(f"right before the CSS_SELECTOR showParticipants")
                phone_number_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#showParticipants")))
                print(f"right after the CSS_SELECTOR showParticipants")
                
                print(f"after 4 seconds  CSS_SELECTOR showParticipants")
                phone_number_element.click()
                print(f"click completed for CSS_SELECTOR showParticipants")
                           
                # # Wait for the "Add" button to become clickable
                print(f"jumping in chatInfoAddBtn")
                add_button = wait.until(EC.element_to_be_clickable((By.ID, "chatInfoAddBtn")))
                
                # Click on the "Add" button
                add_button.click()

                # Find the name and address from the CSV row
                first_name = row['Owner 1 First Name']
                last_name = row['Owner 1 Last Name']
                address = row.get('Address')
                city = row['City']
                state = row['State']
                zip_code = row['Zip']

                # Find the input group for First Name
                first_name_input_group = driver.find_element(By.CLASS_NAME, "input-group")

                # Find the input field for First Name within the input group
                first_name_input = first_name_input_group.find_element(By.CSS_SELECTOR, "input[data-qa='input']")

                # Fill in the input field with the first name
                first_name_input.send_keys(first_name)

                # Find the input field for Last Name
                last_name_input_group = driver.find_element(By.CLASS_NAME, "input-group")

                # Find the input field for Last Name within the input group
                last_name_input = last_name_input_group.find_element(By.CSS_SELECTOR, "input[data-qa='input']")

                last_name_input.send_keys(last_name)

                # Click on the "OK" button
                ok_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-qa='modal-ok']")))
                ok_button.click()

                # Construct the message
                # message = (
                #     f"Hello {first_name} {last_name}, "
                #     f"I am Fred from MJ Real Estate Solves. I'm reaching out because I'm interested in purchasing the property located at {address}, {city}, {state} {zip_code}. "
                #     f"would you be open to selling."
                # )

                #Dynamic message 
                message = template.format(
                    first_name=first_name,
                    last_name=last_name,
                    address=address,
                    city=city,
                    state=state,
                    zip_code=zip_code
                )

                # Find the message input field and fill in the message
                message_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "message-input")))
                message_input.send_keys(message)

                # Click on the send button
                send_button = driver.find_element(By.ID, "sendMessageBtn")
                send_button.click()

                # Wait for a moment before proceeding to the next row
                time.sleep(2)

    # Close the driver:
    driver.quit()

