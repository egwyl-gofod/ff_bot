import requests
import os
import telebot
from bs4 import BeautifulSoup

me = os.getenv("ME")
token = os.getenv("TOKEN")
channel = os.getenv("CHANNEL")
#url = "https://api.telegram.org/bot" + token + "/"


class fanfic(object):
    
    def __init__(self, name, url, stop, html):
        self.name = name
        self.url = url
        self.stop = stop
        self.html = self.get_html()

    def get_html(self):
        try:
            result = requests.get(self.url)
            result.raise_for_status()
            return result.text
        except(requests.RequestException, ValueError):
            print('Server error')
            return False
     
    def check_parts(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        if "fanfics.me" in self.url:
            li_list = soup.findAll('li', id = "chapter_")
        elif "ficbook.net" in self.url:
            li_list = soup.findAll('li', class_ = "part-link")
        parts = len(li_list)
        return parts
    
    def is_updated(self):
        if self.stop != self.check_parts():
            return True
        return False
    
