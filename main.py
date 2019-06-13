from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import re

URL = 'http://publication.pravo.gov.ru/SignatoryAuthority/region17' #ссылка на ваш регион
COUNT = 3040 #всего документов на сайте по региону
OUTPUT_FILE = 'pravo_doc.csv' #выходной файл
PLUS_URL = 'http://publication.pravo.gov.ru{}'

def page_parser(soup):
    '''
    извлекаем данные из страницы
    :return page_doc ->set(title, url, file, type_file, page_doc, date, id)
    '''
    all_doc = []
    for item in soup.findAll("div", {"class": "tr"})[1:]:
        try:
            content = item.find( "div", {"class": "td vis"})
            title = content.find('a').text
            url = content.find( 'a' ).get('href')
            url = PLUS_URL.format(url)
            file = content.find('span', attrs={'class': 'notforprint'}).find('a').get('href')
            file = PLUS_URL.format(file)
            type_file = content.find( 'span', attrs={'class': 'notforprint'} ).find( 'a' ).text
            page_doc = content.find( 'span', attrs={'class': 'pagesindoccount'} ).text
            page_doc = re.findall('(\d+)', page_doc)[0]
            id = item.find( "div", {"class": "td vis notforprint"})\
                .find('span', attrs={'class': 'pagesindoccount information'}).text
            date = item.find( "div", {"class": "td vis notforprint"})\
                .findAll('span', attrs={'class': 'pagesindoccount information'})[1].text
            doc = (id, title, date, url, file, type_file, page_doc)
            all_doc.append(doc)
        except Exception as e:
            print (e)
    return all_doc

driver = r'D:\AnacodaProgect\geckodriver.exe' #драйвер для Firefox https://github.com/mozilla/geckodriver/releases
browser = webdriver.Firefox(executable_path=driver)
browser.get(URL)

page_count = []
with open(OUTPUT_FILE, 'w') as f:
    print('Начинаю парсить данные, ожидайте...')
    for pagination in range(1, (COUNT//30)+1):
        time.sleep(4)
        browser.find_element_by_class_name("page-nave-next").click()
        soup = bs( browser.page_source, 'lxml')
        for doc in (page_parser(soup)):
            stroka = '|'.join(doc)
            page_count.append(stroka)
            print ('Получено {} документов из {}'.format(len(page_count),COUNT))
            f.write(stroka + '\n')
            
print('Описательная часть {} правовых актов региона получена'.format(len(page_count)))
