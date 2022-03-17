from urllib import request, parse
import requests  
import time
import random
import re
import csv
from ua_info import ua_list

class TiebaSpider(object):
    def __init__(self):
        self.index='https://wiki.52poke.com/wiki/%E5%AE%9D%E5%8F%AF%E6%A2%A6%E5%88%97%E8%A1%A8%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%EF%BC%89/%E7%AE%80%E5%8D%95%E7%89%88'

    def get_html(self, url):
        headers = {'User-Agent':random.choice(ua_list)}
        html=requests.get(url=url, headers=headers)
        self.parse_html(html)
        return html

    def parse_html(self, html):
        re_han = '<div class="movie-item-info">.*?title="(.*?)".*?<p class="star">(.*?)</p>.*?class="releasetime">(.*?)</p>'
        pattern = re.compile(re_han, re.S)
        r_list = pattern.findall(html)
        self.save_html(r_list)
    
    def save_html(self, r_list):
        with open('maoyan.csv', 'a', newline='', encoding="utf-8") as f:
            writer=csv.writer(f)
            for r in r_list:
                name_ = r[0].strip()
                star = r[1].strip()[3: ]
                time_ = r[2].strip()[5:15]
                L = [name_, star, time_]
                writer.writerow(L)
                print(name_, time_, star)


    def run(self):
        for offset in range(0, 100, 10):
            url = self.url.format(offset)
            self.get_html(url)
            time.sleep(random.uniform(1,2))


if __name__=='__main__':
    try:
        spider=TiebaSpider()
        spider.run()
    except Exception as e:
        print("Error:", e)








"""ua = UserAgent()
print(ua.firefox)
"""
"""query_string = {
    'wd' : "爬虫"
}

result = parse.urlencode(query_string)
string = parse.unquote(result)
url = 'http://www.baidu.com/s/?{}'.format(result)
print(string)
print(url)"""

"""
def get_url(word):
    url = 'http://www.baidu.com/s?{}'
    params = parse.urlencode({'wd':word})
    url = url.format(params)
    return url

def request_url(url, filename):
    # ua = UserAgent()
    # headers = ua.chrome
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}
    req = request.Request(url=url, headers=headers)
    res = request.urlopen(req)
    html = res.read().decode('utf-8')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
if __name__ == '__main__':
    word = input('plz:')
    url = get_url(word)
    filename = word + '.html'
    request_url(url, filename)"""

