import requests
import re
from bs4 import BeautifulSoup


def get_page_text(gen, start_page, end_page):
    contents = [[], []]

    url1 = "https://opinion.lawmaking.go.kr"

    while int(start_page) <= int(end_page):
        print("Processing Page: " + str(start_page))
        req = requests.get(url1 + "/gcom/nsmLmSts/out?scBlNm=scBlNm_blNm&sugCd=" + str(gen) + "&pageIndex=" + str(start_page))
        html = req.content
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('table', {'class': 'tbl_typeA'})

        law_name = table.find_all('tr')
        app_list = []

        # 가결된 법안만 추출
        for i in range(0, len(law_name)):
            if law_name[i].find_all('td') != [] and ('원안가결' or '수정가결') in str(law_name[i].find_all('td')[4]):
                app_list.append(law_name[i].find('a'))

        # 페이지에 있는 의안명, 법안 요약 추출
        for a in app_list:
            lawbSeq = str("".join(re.findall("\\d+", a['onclick'])))
            popup_link = "/gcom/nsmLmSts/out/" + lawbSeq + "/detailRP"
            popup_link = url1 + popup_link

            reqp = requests.get(popup_link)
            htmlp = reqp.content
            soupp = BeautifulSoup(htmlp, 'html.parser')

            contents[0].append(soupp.find('pre').text)  # 법안 요약 입력
            contents[1].append(a.text)                  # 의안명 입력

        start_page = start_page + 1

    return contents
