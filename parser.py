import requests
from bs4 import BeautifulSoup as bs

file_out = 'base.txt'

START_PAGE = 'http://publication.pravo.gov.ru/SignatoryAuthority/region17'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

params = {'method': 'GET',
          'credentials': 'include',
          'X-Requested-With': 'XMLHttpRequest'}

s = requests.Session()
s.params.update(params)
s.headers.update(headers)
s.proxies.update({})


def get_page(url):
    data = s.get(url).text
    soup = bs(data, 'lxml')
    return soup


def get_pagi():
    """Получаем количество страниц"""
    page = get_page(START_PAGE)
    data = page.find('div', {'class': 'page-nave-count'}).text
    item_count = int(data.split()[-1])
    return item_count


def get_items(data_soup):
    """извлекаем данные из страницы"""
    docs = []
    for items in data_soup.findAll('div', {'class': 'tr'}):
        data = items.findAll('a', {'class': 'choosedocument'})
        file = items.find('a', {'class': 'navigation'})
        if data:
            for i in data:
                url_doc = 'http://publication.pravo.gov.ru{}'.format(i.get('href'))
                title_doc = i.text
                file_url = 'http://publication.pravo.gov.ru{}'.format(file.get('href'))
                if title_doc:
                    doc = {'title': title_doc, 'url': url_doc, 'file': file_url}
                    docs.append(doc)
    return docs


with open(file_out, 'w', encoding='utf-8') as f:
    for page in range(1, get_pagi()//30):
        url = 'http://publication.pravo.gov.ru/Search/DocumentSearchResult?SearchObject.IsShowAppendPageCountList=true&' \
             'SearchObject.IsLastUpdateList=true&SearchObject.NavigationSignatoryAuthorityCode=region17&' \
             'SearchObject.NavigationSignatoryAuthorityId=&SearchObject.NavigationSignatoryAuthorityCategory=&' \
             'SearchObject.SelectedSignatoryAuthorityId=00000000-0000-0000-0000-000000000000&SearchObject.RangeSize=30&' \
             'SearchObject.CurrentPageNumber={}&_=1597736552634'.format(page)
        soup = get_page(url)
        for i in get_items(soup):
            print(i)
            f.write(str(i) + '\n')
