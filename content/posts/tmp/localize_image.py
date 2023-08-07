import glob
import markdown
from bs4 import BeautifulSoup
import urllib.request
import os
import requests
import re

def dl(url, fname):
    req = requests.get(url)
    file = open(fname, 'wb')
    for chunk in req.iter_content(100000):
        file.write(chunk)
    file.close()

for folder in glob.glob("*/"):
    post = os.path.join(folder, "index.md")
    
    if os.path.exists(post):
        print(post)
        content = open(post, "r", encoding="utf-8").read()
        #html = markdown.markdown(content)
        
        #soup = BeautifulSoup(html, 'html.parser')
        #img_tags = soup.find_all('img')

        #urls = [img['src'] for img in img_tags if "http" in img["src"]]
        urls = re.findall('(https?:\/\/[^\s]+(?:png|jpeg|jpg|webp|gif))',content)
        
        for link in urls:
            print("\t"+link)
            fname = "dl_"+os.path.basename(link)
            fname = fname.split("?")[0]
            if not os.path.exists(os.path.join(folder, os.path.join("images", fname))):
                try:
                    dl(
                        link, 
                        os.path.join(folder, os.path.join("images", fname))
                    )
                except Exception as e:
                    print(e) 
                    exit()
            
            content = content.replace(link, f"images/{fname}")
        
        open(post, "w", encoding="utf-8").write(content)