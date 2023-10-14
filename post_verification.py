import re
import tweepy
import scrapy
from scrapy.crawler import CrawlerProcess
import requests
from config import consumer_key,consumer_secret,access_token,access_token_secret

def verify_url(url):
    twitter_pattern = re.compile(r'https?://twitter\.com/[^/]+/status/\d+')
    linkedin_pattern = re.compile(r'https?://www\.linkedin\.com/feed/update/\w+')

    if twitter_pattern.match(url):
        return 'twitter'
    elif linkedin_pattern.match(url):
        return 'linkedin'
    else:
        return None


# Set up the tweepy client (you'd get these keys from your Twitter developer portal)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def verify_tweet_format(tweet_id):
    try:
        tweet = api.get_status(tweet_id)
    except tweepy.errors.Forbidden as e:
        print("Error: Access to Twitter API endpoint is forbidden. You might need to request Elevated Access.")
        return None
    content = tweet.text
    if "day #" in content and "#30_days_challenge" in content:
        return True
    return False


# Scrapy Spider for LinkedIn
class LinkedInSpider(scrapy.Spider):
    name = "linkedin_verifier"
    start_urls = []

    def __init__(self, url=None, *args, **kwargs):
        super(LinkedInSpider, self).__init__(*args, **kwargs)
        if url:
            self.start_urls.append(url)

    def parse(self, response):
        post_content = response.xpath('//div[contains(@class, "post-content")]/text()').get()
        if "day #1" in post_content and "#30_days_challenge" in post_content:
            self.log('Verified Post: %s' % response.url)

def verify_linkedin_post(url):
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0'})
    process.crawl(LinkedInSpider, url=url)
    process.start()

def verify_post(url):
    platform = verify_url(url)
    if platform == 'twitter':
        tweet_id = url.split('/')[-1]
        return verify_tweet_format(tweet_id)
    elif platform == 'linkedin':
        return verify_linkedin_post(url)
    else:
        return False  # Invalid URL or not from Twitter/LinkedIn


