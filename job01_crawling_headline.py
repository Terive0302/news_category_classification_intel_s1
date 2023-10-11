from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'
# 정치탭 링크


headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
# resp = requests.get(url, headers = headers) # requests는 url에 요청하고 url로부터 응답을 받아옴
# # 하지만 몇 웹페이지에서 막아놓음 따라서 브라우저라고 속여야 함 4:04 / user Agent 정보가 있어야 됨
#
# # print(list(resp))
# print(type(resp))
# soup = BeautifulSoup(resp.text, 'html.parser') # HTML문서 형태로 바꿔줌
# # print(soup)
# title_tags = soup.select('.sh_text_headline') # class가지고 요소들을 가지고 올 때는 .을 찍음
# print(title_tags)
# print(len(title_tags))
# print(type(title_tags[0]))
# titles = []
# for title_tags in title_tags:
#     titles.append(re.compile('[^가-힣|a-z|A-Z]').sub(' ', title_tags.text)) # re는 따로 떼어낼 때 씀
#     # ^는 처음부터 라는 뜻, sub는 빼라는 뜻 [^가-힣|a-z|A-Z] 빼고 ' ' 공백을 넣어라 4:30
# print(titles)
# print(len(titles))

df_titles = pd.DataFrame() # 비어있는 데이터 프레임
re_title = re.compile('[^가-힣]|a-z|A-Z')

for i in range(6):
    resp = requests.get('https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i), headers = headers)
    # 100이면 정치 101이면 경제 ... 식이기 때문에 뒷자리만 포매팅
    soup = BeautifulSoup(resp.text, 'html.parser')  # HTML문서 형태로 바꿔줌
    title_tags = soup.select('.sh_text_headline') # class가지고 요소들을 가지고 올 때는 .을 찍음
    titles = []
    for title_tags in title_tags:
        titles.append(re_title.sub(' ', title_tags.text)) # re는 따로 떼어낼 때 씀

    df_section_titles = pd.DataFrame(titles, columns = ['titles'])
    # 컬럼이 하나인 데이터프레임 생성, 컬럼의 이름은 titles, 카테고리가 들어가야 함
    df_section_titles['category'] = category[i] # i = 0 정치, i =  1 경제
    # 정치뉴스 제목 - 정치 이런 형태로 들어감
    df_titles = pd.concat([df_titles, df_section_titles], axis = 'rows', ignore_index = True)
    # 빈 데이터 프레임에 이어 붙일 것임
    # 9:20 30

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts()) # value_counts() 유니크한 값의 갯수를 세줌
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index = False)
    # datetime은 시간 관련 패키지, now는 현재 시간 ms로 알려줌 strftime은 시간을 문자열로 변환
    # csv파일 저장할 때 index는 필요없으니 false