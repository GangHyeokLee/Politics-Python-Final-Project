import re
import requests
from bs4 import BeautifulSoup
from GT import get_page_text
from konlpy.tag import Okt
from collections import Counter
import pytagcloud

gen = 20
page = 1

url1 = "https://opinion.lawmaking.go.kr"
url2 = "/gcom/nsmLmSts/out?scBlNm=scBlNm_blNm&sugCd=" + str(gen) + "&pageIndex=" + str(page)

req = requests.get(url1 + url2)
html = req.content
soup = BeautifulSoup(html, 'html.parser')

total_page_num = str(soup.select('.tbl_top_area'))
total_page_num = "".join(re.findall("\\d+", total_page_num[-81:-76]))
total_page_num = int(total_page_num)

print(str(total_page_num) + "\n")

total = get_page_text(int(gen), page, total_page_num)

print("\nCrawling Complete\n")

l_name = total[1]
total = total[0]

total = " ".join(total)
l_name = " ".join(l_name)

stop_word = ['법률', '규정', '법', '개정', '일부', '용어', '대안', '안', '관한', '및', '관']

for i in stop_word:
    total = total.replace(i, '')
    l_name = l_name.replace(i, '')

t = Okt()

nouns = t.nouns(total)
count = Counter(nouns)

l_nouns = t.nouns(l_name)
l_count = Counter(l_nouns)

tag = count.most_common(100)
l_tag = l_count.most_common(100)

taglist = pytagcloud.make_tags(tag, maxsize=100)
l_taglist = pytagcloud.make_tags(l_tag, maxsize=150)
pytagcloud.create_tag_image(taglist, "{}대_국회_가결법안_요약.png".format(gen), size=(1024, 960), fontname='NotoSansCJKkr-DemiLight', rectangular=False)
pytagcloud.create_tag_image(l_taglist, "{}대_국회_가결법안명.png".format(gen), size=(1024, 960), fontname='NotoSansCJKkr-DemiLight', rectangular=False)
