import requests
import lxml.html as html


HOME_URL='https://rpp.pe/ultimas-noticias'

XPATH_LINK_TO_ARTICLE = '//h2/a/@href'
XPATH_TITLE_TO_ARTICLE = '//*[@id="content"]/div[2]/div[1]/article/header/h1/text()'
XPATH_SUMARY_TO_ARTICLE = '//*[@id="content"]/div[2]/div[1]/article/header/div[1]/h2/text()'
XPATH_BODY_TO_ARTICLE = '//*[@id="article-body"]/p[not(@class)]/text()'

def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            print(links_to_notices)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
    
def run():
    parse_home()
    
if __name__ == "__main__":
    run()
