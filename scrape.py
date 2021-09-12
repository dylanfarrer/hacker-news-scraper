import requests
from scraper_gui import *
from bs4 import BeautifulSoup


#Convert the code just below to a method so it camn be recalled when the refrersh button is hiit.

res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.text, 'html.parser')
#this turns the string to html so it can be edited as thus
links = soup.select('.storylink')
subtext = soup.select('.subtext')

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key= lambda k:k['votes'], reverse=True)

def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})

    return sort_stories_by_votes(hn)

def nice_print(hnlist):
    for dic in hnlist:
        for key in dic:
            print(key,  '->', dic[key])
        print()

nice_print(create_custom_hn(links, subtext))
createGui(create_custom_hn(links, subtext))
