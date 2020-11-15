import requests
from bs4 import BeautifulSoup


fics = []
class fanfic(object):
    
    def __init__(self, name, url, stop, is_empty = False):
        self.name = name
        self.url = url
        self.stop = stop
        self.is_empty = is_empty

    def get_html(self):
        try:
            result = requests.get(self.url)
            result.raise_for_status()
            return result.text
        except(requests.RequestException, ValueError):
            print('Server error')
            return False
     
    def check_parts(self):
        try: 
            soup = BeautifulSoup(self.get_html(), 'html.parser')
            if "fanfics.me" in self.url:
                li_list = soup.findAll('li', id = "chapter_")
            elif "ficbook.net" in self.url:
                li_list = soup.findAll('a', class_ = "part-link")
            parts = len(li_list)
            return parts
        except:
            print("Parsing error occurred")
            return 0
    
    def is_updated(self):
        if self.stop == self.check_parts():
            return False
        elif self.check_parts() == 0:
            self.is_empty = True
            return False
        return True


osen = fanfic('Осень на двоих 6', 'https://fanfics.me/fic131932', 8)
fics.append(osen)
test = fanfic('тест', 'https://ficbook.net/readfic/10077933', 2)
fics.append(test)

#print(test.is_updated(), test.is_empty)