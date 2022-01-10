import requests
from bs4 import BeautifulSoup
import pprint
import sys

from requests.models import guess_json_utf

def sort_stories_by_votes(hn):
    return sorted(hn, key= lambda k: k['points'], reverse=True)

def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if vote:
            points = int(vote[0].getText().replace(' points', ''))
            if points >= 100:
                hn.append({'title' : title, 'link' : href,'points' : points})       
    return sort_stories_by_votes(hn)

def get_links_and_subtexts(num_of_pages):
    all_links = []
    all_subtext = []
    for page in range(num_of_pages):
        res = requests.get(f'https://news.ycombinator.com/news?p={page+1}')
        soup = BeautifulSoup(res.text, 'html.parser')
        links  = soup.select('.titlelink')
        subtext = soup.select('.subtext')
        all_links = all_links + links
        all_subtext = all_subtext + subtext
    return all_links, all_subtext

def main(num_of_pages):
    links, subtext = get_links_and_subtexts(num_of_pages)
    hnlist = create_custom_hn(links,subtext)

    for item in hnlist:
        print(f"{item['title']}\n  Link: {item['link']}\n  Points: {item['points']}")

if __name__ == '__main__':
    main(int(sys.argv[1]))