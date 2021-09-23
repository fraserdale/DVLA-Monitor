from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from twilio.rest import Client

#twilio creds
accountSid = ''
authToken = ''
twilioFrom =''

#DVLA info
dates = []
drivingLicenseNumber = ''
referenceNumber = ''

#number(s) to recieve alerts
numbers = []

loop = True
while loop:
    chrome_options = Options() 
    chrome_options.add_argument("--headless")  

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://driverpracticaltest.direct.gov.uk/login?execution=e1s4")
    driver.find_element_by_id(
        'driving-licence-number').send_keys(drivingLicenseNumber)
    driver.find_element_by_id('application-reference-number').send_keys(referenceNumber)
    driver.find_element_by_id('booking-login').click()
    time.sleep(1)
    driver.find_element_by_id('date-time-change').click()
    time.sleep(1)
    driver.find_element_by_id('driving-licence-submit').click()
    x = driver.page_source

    soup = BeautifulSoup(x, "html.parser")
    hold = soup.findAll("label", {"class": "SlotPicker-slot-label"})

    for item in hold:
        date = (
            (item.find("input", {"class": "SlotPicker-slot"}))['data-datetime-label'])
        if date not in dates:
            print('################################')
            print(date)
            print('################################')
            dates.append(date)
            account_sid = accountSid
            auth_token = authToken
            client = Client(account_sid, auth_token)


            for x in numbers:
                message = client.messages \
                    .create(
                        body="New test on: " + date ,
                        from_=twilioFrom,
                        to=x,
                    )
    print(dates[0])
    time.sleep(60)
