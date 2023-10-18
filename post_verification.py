import re
import logging
from discord.ext import commands
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from config import sauce_options_un
from config import sauce_options_access_key

# Set up logging (this is just a basic setup, adjust as needed)
logging.basicConfig(level=logging.INFO)
challenge_pattern = re.compile(r'#(\d+)_of_(\d+)_day_challenge', re.IGNORECASE)

class PostVerification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def verify_url(url):
        twitter_pattern = re.compile(r'https?://twitter\.com/[^/]+/status/\d+')
        linkedin_pattern = re.compile(r'https?://www\.linkedin\.com/feed/update/urn:li:activity:\d+/?')

        logging.info(f"Verifying URL: {url}")
        if twitter_pattern.match(url):
            return 'twitter'
        elif linkedin_pattern.match(url):
            return 'linkedin'
        else:
            return None

    @staticmethod
    def verify_post(url, day, total_days):
        platform = PostVerification.verify_url(url)  # Use class name to reference static method
        if platform == 'linkedin':
            return PostVerification.verify_linkedin_post_selenium(url, day, total_days)  # Same here
        else:
            return False  # Invalid URL or not from LinkedIn

    @staticmethod
    def construct_xpath(day, total_days):
        return f'//a[contains(text(), "#{day}_of_{total_days}_day_challenge")]'

    # @staticmethod
    # def verify_linkedin_post_selenium_serverless(url, day, total_days):
    #     chrome_options = Options()
    #     chrome_options.add_argument('--headless')
    #     chrome_options.add_argument('--no-sandbox')
    #     chrome_options.add_argument('--disable-dev-shm-usage')
    #     driver = webdriver.Chrome(options=chrome_options)
    #
    #     driver.get(url)
    #     wait = WebDriverWait(driver, 20)
    #
    #     try:
    #         # Construct dynamic XPath
    #         xpath_dynamic = PostVerification.construct_xpath(day, total_days)
    #         post_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath_dynamic)))
    #         post_content = post_element.text
    #         logging.info(f"Post Content: {post_content}")
    #         match = challenge_pattern.search(post_content)
    #         if match:
    #             day, total_days = map(int, match.groups())
    #             if 1 <= day <= total_days:
    #                 driver.close()
    #                 return True
    #     except (NoSuchElementException, TimeoutException):
    #         driver.close()
    #         return False
    #
    #     driver.close()
    #     return False

    @staticmethod
    def verify_linkedin_post_selenium(urll, day, total_days):
        # Sauce Labs setup
        options = ChromeOptions()
        options.browser_version = 'latest'
        options.platform_name = 'Windows 11'
        sauce_options = {}
        sauce_options['username'] = sauce_options_un
        sauce_options['accessKey'] = sauce_options_access_key
        sauce_options['build'] = 'selenium-build-EFO3B'
        sauce_options['name'] = 'LinkedIn Verification Test'  # Name for the test on Sauce Labs
        options.set_capability('sauce:options', sauce_options)

        url = "https://ondemand.eu-central-1.saucelabs.com:443/wd/hub"
        driver = webdriver.Remote(command_executor=url, options=options)

        driver.get(urll)
        wait = WebDriverWait(driver, 60)
        try:
            # Construct dynamic XPath
            xpath_dynamic = PostVerification.construct_xpath(day, total_days)
            post_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath_dynamic)))
            post_content = post_element.text
            logging.info(f"Post Content: {post_content}")
            match = challenge_pattern.search(post_content)
            if match:
                day, total_days = map(int, match.groups())
                if 1 <= day <= total_days:
                    driver.close()
                    return True
        except (NoSuchElementException, TimeoutException):
            driver.close()
            return False

        driver.close()
        return False

    @staticmethod
    def verify_linkedin_post_selenium___ss(url, day, total_days):
        driver = WebDriver()
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        try:
            # Construct dynamic XPath
            xpath_dynamic = PostVerification.construct_xpath(day, total_days)
            post_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath_dynamic)))
            post_content = post_element.text
            logging.info(f"Post Content: {post_content}")
            match = challenge_pattern.search(post_content)
            if match:
                day, total_days = map(int, match.groups())
                if 1 <= day <= total_days:
                    driver.close()
                    return True
        except (NoSuchElementException, TimeoutException):
            driver.close()
            return False

        driver.close()
        return False

async def setup(bot):
    await bot.add_cog(PostVerification(bot))

