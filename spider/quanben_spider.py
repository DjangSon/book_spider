from bs4 import BeautifulSoup
import json
import requests
from db import dbHelper


class Spider(object):
    def __init__(self):
        self.dbHeper = dbHelper()
        self.url = 'https://www.qb5.la/quanben/'
        self.__head = {'User-Agent':'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19',}
        
    def parse_novel_content(self, url):
        http = requests.get(url, verify=False)
        text = http.text
        soup = BeautifulSoup(text, 'lxml')
        content = soup.find('div', id='content')
        other = soup.find('div', id='content').find_next()
        content = str(content).replace(str(other), '')
        content = content.replace('<div id="content"> 全本小说网 www.qb5.la，最快更新最新章节！<br/><br/>', '')
        content = content.replace('</div>', '')
        content = content.replace('<br/><br/>', "\n")
        return content
    
    def parse_novel_chapter(self, url, novel_name):
        http = requests.get(url, verify=False)
        text = http.text
        soup = BeautifulSoup(text, 'lxml')
        author = soup.find('div', id="info").small.a.get_text()
        sql = "INSERT INTO novel (novel_name,author) VALUES ('%s','%s')" % (novel_name, author)
        novel_id = self.dbHeper.insert(sql)
        print(novel_id)
        dd = soup.find('dl', class_="zjlist").find_all('dd')
        for a_tag in dd:
            chapter_name = a_tag.text
            if chapter_name:
                link = url + str(a_tag.a.get('href'))
                content = self.parse_novel_content(link)
                sql = "INSERT INTO chapter (novel_id,chapter_name,chapter_content) VALUES (%s,'%s','%s')" % (novel_id, chapter_name, content)
                self.dbHeper.insert(sql)
    
    def every_page_novel(self):
        url = self.url + '1'
        http = requests.get(url, verify=False)
        text = http.text
        soup = BeautifulSoup(text, 'lxml')
        ul = soup.find('ul', "titlelist").children
        for li in ul:
            novel_name = li.a.text
            href = li.a.get('href')
            self.parse_novel_chapter(href, novel_name)
            break


a_spider = Spider()
a_spider.every_page_novel()
