import requests
import lxml.html as html
import os
import datetime



HOME_URL='https://rpp.pe/ultimas-noticias'

XPATH_LINK_TO_ARTICLE = '//h2/a/@href'
XPATH_TITLE_TO_ARTICLE = '//*[@id="content"]/div[2]/div[1]/article/header/h1/text()'
XPATH_SUMARY_TO_ARTICLE = '//*[@id="content"]/div[2]/div[1]/article/header/div[1]/h2/text()'
XPATH_BODY_TO_ARTICLE = '//*[@id="article-body"]/p[not(@class)]/text()'

def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            
            try:
                title = parsed.xpath(XPATH_TITLE_TO_ARTICLE)[0]
                title = title.replace('\"','')
                title = title.replace('S/','PEN')
                sumary = parsed.xpath(XPATH_SUMARY_TO_ARTICLE)[0]
                body = parsed.xpath(XPATH_BODY_TO_ARTICLE)
            except IndexError:
                return
            with open(f'{today}/{title}.txt','w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(sumary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # print(links_to_notices)
            
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_notices:
                parse_notice(link, today)
            
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
    
def run():
    parse_home()
    
if __name__ == "__main__":
    run()
