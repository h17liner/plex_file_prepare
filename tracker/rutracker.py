import requests
import PTN
from urlparse import urlparse, parse_qs
from bs4 import BeautifulSoup


class RutrackerPage(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    }

    categories_map = {
        '2': 'Movies',
        '18': 'TV-Shows',
        '8': 'Music',
    }

    def __init__(self, page_url):
        self.data = self.get_html(page_url)

    def get_html(self, url):
        response = requests.get(url, headers=self.headers)

        return BeautifulSoup(response.content, 'html.parser')

    def get_title(self):
        soup = self.data
        return soup.find("a", {"id": "topic-title"}).string

    def parsed_data(self):
        raw_title = self.get_title()
        return PTN.parse(raw_title)

    def title(self, lang='ru'):
        data = self.parsed_data()
        title = data.get('title')
        title_list = [x.strip() for x in title.split('/')]

        if lang == 'en':
            return title_list[len(title_list)-1]

        return title_list[0]

    def quality(self):
        data = self.parsed_data()
        return data.get('quality')

    def year(self):
        data = self.parsed_data()
        return data.get('year')

    def get_from_category_map(self, category_id):
        return self.categories_map.get(category_id, 'Other')

    def categories(self, native_name=False):
        attr = 'nav w100 pad_2'
        soup = self.data
        link = soup.find('td', {'class': attr}).a.find_next_sibling('a')
        parse_href = urlparse(link['href'])

        category_id = parse_qs(parse_href.query)['c'][0]

        category_name = self.get_from_category_map(category_id)
        if native_name:
            category_name = link.string

        return category_id, category_name