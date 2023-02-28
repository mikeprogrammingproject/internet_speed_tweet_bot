from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

SPEED_TEST_WEBSITE = "https://fast.com/th/"
TWITTER = "https://twitter.com/home"

# Your Twitter account
# Sometimes Twitter will ask for you Twitter ID too, so you need to provide both email and id.
TWITTER_EMAIL = "YOUR TWITTER EMAIL"
TWITTER_ID = "YOUR TWITTER ID"
TWITTER_PASSWORD = "YOUR TWITTER PASSWORD"

# Set your internet download and upload speed threshold.
# If tested speed is below these numbers, tweet function will trigger and post the speed test result from website.
DOWNLOAD_SPEED = 1000
UPLOAD_SPEED = 1000


def get_internet_speed():
    speedtest_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    speedtest_driver.get(SPEED_TEST_WEBSITE)
    time.sleep(30)
    speed_test = True
    while speed_test:
        try:
            more_info = speedtest_driver.find_element(By.XPATH, '//*[@id="show-more-details-link"]')
            more_info.click()
            time.sleep(15)
            speed_test = False
        except ElementNotInteractableException:
            time.sleep(5)
        except NoSuchElementException:
            time.sleep(5)
    download_speed = speedtest_driver.find_element(By.ID, "speed-value")
    upload_speed = speedtest_driver.find_element(By.ID, "upload-value")
    print(f"download: {download_speed.text}\nupload: {upload_speed.text}")
    return download_speed.text, upload_speed.text


class InternetSpeedTwitterBot:
    def __init__(self):
        self.down, self.up = get_internet_speed()

    def tweet(self):
        twitter_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        twitter_driver.get(TWITTER)
        time.sleep(10)
        email = twitter_driver.find_element(By.XPATH,
                                            '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div['
                                            '2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
        email.send_keys(TWITTER_EMAIL)
        email.send_keys(Keys.ENTER)
        time.sleep(3)
        if twitter_driver.find_element(By.XPATH,
                                       '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div['
                                       '2]/div[1]/div/div[2]/label/div/div[2]/div/input'):
            try:
                twitter_id = twitter_driver.find_element(By.XPATH,
                                                         '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div['
                                                         '2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div['
                                                         '2]/div/input')
                twitter_id.send_keys(TWITTER_ID)
                twitter_id.send_keys(Keys.ENTER)
            except NoSuchElementException:
                pass
        time.sleep(3)
        password = twitter_driver.find_element(By.XPATH,
                                               '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div['
                                               '2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div['
                                               '2]/div[1]/input')
        password.send_keys(TWITTER_PASSWORD)
        password.send_keys(Keys.ENTER)
        time.sleep(3)
        try:
            close_security = twitter_driver.find_element(By.XPATH,
                                                         '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div['
                                                         '2]/div/div[1]/div/div/div/div[1]/div')
            close_security.click()
        except NoSuchElementException:
            pass
        time.sleep(5)
        write_tweet = twitter_driver.find_element(By.XPATH,
                                                  '/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a')
        write_tweet.click()
        time.sleep(5)
        tweet_msg = twitter_driver.find_element(By.XPATH,
                                                '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div['
                                                '2]/div[2]/div/div/div/div[3]/div/div[1]/div/div/div/div/div[2]/div['
                                                '1]/div/div/div/div/div/div[2]/div/div/div/div/label/div['
                                                '1]/div/div/div/div/div/div[2]/div')
        tweet_msg.send_keys(f"Download Speed: {self.down}Mb/s\nUpload Speed: {self.up}Mb/s\nPost by TweetBot")
        time.sleep(5)
        send_tweet = twitter_driver.find_element(By.XPATH,
                                                 '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div['
                                                 '2]/div[2]/div/div/div/div[3]/div/div[1]/div/div/div/div/div[2]/div['
                                                 '3]/div/div/div[2]/div[4]')
        send_tweet.click()
        time.sleep(5)
        twitter_driver.close()


bot = InternetSpeedTwitterBot()

if int(bot.down) < DOWNLOAD_SPEED or int(bot.up) < UPLOAD_SPEED:
    bot.tweet()
