import requests
from bs4 import BeautifulSoup

base_url = 'http://www.nytimes.com'
r = requests.get(base_url)
soup = BeautifulSoup(r.text, "html.parser")


for story_heading in soup.find_all("olympics"):
    if story_heading.a:
        print(story_heading.a.text.replace("\n", " ").strip())
        print("a")
    else:
        print(story_heading.contents[0].strip())
        print("b")
