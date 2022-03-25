from bs4 import BeautifulSoup
import urllib3
import os
import re
import requests

urllib3.disable_warnings()

class PokemonSpider(object):
    def __init__(self):
        self.index = "https://wiki.52poke.com/wiki/%E5%AE%9D%E5%8F%AF%E6%A2%A6%E5%88%97%E8%A1%A8%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%EF%BC%89/%E7%AE%80%E5%8D%95%E7%89%88"
        self.root = "https://wiki.52poke.com{}"
        self.headers = {'User-Agent': 'Mozilla/4.0'}
        self.pokemon_url=[]

    def get_pokemon_url(self):
        res = requests.get(url=self.index, verify=False)
        res.encoding = "utf-8"
        html_index = res.text
        soup = BeautifulSoup(html_index, "html.parser")
        pokemon_list = soup.findAll(name="a", attrs={"href": re.compile('^/wiki/[A-Za-z0-9]*?$'), "class": re.compile('mw-redirect')})
        for pokemon in pokemon_list:
            pokemon = str(pokemon)
            pattern = re.compile(r'href="(/wiki/[A-Za-z0-9]*?)"')
            self.pokemon_url.append(pattern.findall(pokemon))

    def get_pokemon_imgae(self, url):
        res = requests.get(url=url, verify=False)
        res.encoding = "utf-8"
        html = res.text
        soup = BeautifulSoup(html)
        image = soup.find(name='img', attrs={"width": '300'})
        # print(image)
        if image is None:
            image = soup.find('img', width='120')
        image_address = image.get('data-url')
        image_url = "https://s1.52poke.wiki{}".format(image_address[18:])
        return image_url

    def save_image(self, url, name):
        root = "./image"
        path = str(root) + "/" + str(name) + ".png"
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            requests.packages.urllib3.disable_warnings()
            res = requests.get(url=url, verify=False)
            with open(path, 'wb') as f:
                f.write(res.content)

    def run(self):
        self.get_pokemon_url()
        for sub_url in self.pokemon_url:
            if sub_url[0] == "/wiki/Pmlists":
                continue
            pokemon_url = self.root.format(sub_url[0])
            pokemon_name = sub_url[0][6:]
            image_url = self.get_pokemon_imgae(pokemon_url)
            self.save_image(image_url, pokemon_name);
            # break
            # print(pokemon_url)

spider = PokemonSpider()
spider.run()

# https://s1.52poke.wiki/wiki/thumb/2/21/001Bulbasaur.png/300px-001Bulbasaur.png
# https://s1.52poke.com/wiki/thumb/2/21/001Bulbasaur.png/300px-001Bulbasaur.png