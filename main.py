from selenium import webdriver
import time
import data.reply

driver = webdriver.Chrome(executable_path='./chromedriver_win32/chromedriver')

driver.implicitly_wait(10)  # seconds

googleFormsURL = 'https://docs.google.com/forms/d/e/1FAIpQLScPXUcpuiFE00JLPYsABzE9tN005FSQAdQJ8A0af_POVZbi1w/viewform'

roomNum = data.reply.roomNum
name = data.reply.name
question1 = data.reply.question1
question2 = data.reply.question2
question3 = data.reply.question3

driver.get(googleFormsURL)

time.sleep(0.7)

questionRoomNum_text = driver.find_element_by_xpath(
    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div')

print(questionRoomNum_text.text)

questionRoomNum_input = driver.find_element_by_xpath(
    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')

questionRoomNum_input.send_keys(roomNum)

questionName_text = driver.find_element_by_xpath(
    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div')

print(questionName_text.text)

questionName_input = driver.find_element_by_xpath(
    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
questionName_input.send_keys(name)

question1_toggle1_text = driver.find_element_by_xpath(
    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div/span/div/div[1]/label/div/div[2]/div/span')
print(question1_toggle1_text.text)

question1_toggle1 = driver.find_element_by_xpath('//*[@id="i13"]/div[3]/div')
question1_toggle1.click()

question2_toggle1_text = driver.find_element_by_xpath(
    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div/span/div/div[1]/label/div/div[2]/div/span')
print(question2_toggle1_text.text)

question2_toggle1 = driver.find_element_by_xpath('//*[@id="i23"]/div[3]/div')
question2_toggle1.click()

question3_toggle1_text = driver.find_element_by_xpath(
    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div[1]/div/label/div/div[2]/div/span')
print(question3_toggle1_text.text)

question3_checkbox = driver.find_element_by_xpath('//*[@id="i34"]/div[2]')
question3_checkbox.click()
