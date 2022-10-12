
import requests
import lxml.html as html
import os
import datetime

HOME_URL= 'https://www.larepublica.co/'

XPATH_LINK_ARTICLE = '/html/body//text-fill//a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]//h2/span/text()'
XPATH_BODY = '//*[contains(concat( " ", @class, " " ), concat( " ", "html-content", " " ))]//p/text()'
XPATH_SUMMARY = '//*[contains(concat( " ", @class, " " ), concat( " ", "lead", " " ))]//p/text()'

def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_news = parsed.xpath(XPATH_LINK_ARTICLE)

            today = datetime.date.today().strftime('%d_%m_$Y')
            print(today)

            if not os.path.isdir(today):
                os.mkdir(today)
            for link in links_to_news:
                parse_new(link,today)
            pass
        else:
            raise ValueError(f'Error!', {response.status_code})
    except ValueError as err: 
        print(err)


def  parse_new(link,today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            page = response.content.decode('utf-8') #full html 
            parsed_page = html.fromstring(page) #se parsea para poder aplicar xpath: => <Element html at 0x7fcf45fc41d0>
            try:
                title = parsed_page.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','').strip()
                summary = parsed_page.xpath(XPATH_SUMMARY)[0]
                body = parsed_page.xpath(XPATH_BODY)
            except:
                return

            with open(f'{today}/{title}.txt','w',encoding='utf-8') as file:
                file.write(title)
                file.write('\n\n')
                file.write(summary)
                file.write('\n\n')
                for parr in body:
                    file.write(parr)
                    file.write('\n')

        else:
            raise ValueError(f'Error!!: ',response.status_code)
    except ValueError as err:
        print(err)


def run():
    parse_home()
    

if __name__ == '__main__':
    run()