from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# 크롬드라이버대신에 이거 씀
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime


options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"

options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")
# options.add_argument('headless') # headless하면 웹브라우저를 안보여줌, 코딩할 때는 볼 필요가 있어서 주석
# options.add_argument('window-size=1920x1080') # 디폴트값 쓰면 됨
# options.add_argument("disable-gpu") # gpu 없음
# options.add_argument("--no-sandbox") # 리눅스에서 할 때만

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())

# chrome driver
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경


category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
pages = [110, 110, 110, 75, 110, 72] # 각각의 섹션이 몇 페이지까지 있는지
# 카테고리 별로 비슷한 숫자로 맞춰주는게 좋음, 단, 데이터가 적어지면 안됨 / 110페이지까지 해보자, 72, 75페이지는 쩔수없음
# 데이터를 손해를 보긴 하지만 2200개면 학습하기엔 충분할 것임
df_titles = pd.DataFrame()
for l in range(len(pages)):
    section_url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}".format(l)
    titles = []
    for k in range(1, 3): # pages[0]하면 정치, +1해야 110페이지까지 긁어옴
        url = section_url + "#&date=%2000:00:00&page={}".format(k)
        driver.get(url)
        time.sleep(0.5) # StaleElementReferenceException오류가 나와서 타임슬립을 넣음 11:31
        for i in range(1, 5):
            for j in range(1, 6):
                title = driver.find_element('xpath', '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'
                                            .format(i, j)).text
                title = re.compile('[^가-힣]').sub(' ', title) # 한글만 하자
                titles.append(title)
    df_section_title = pd.DataFrame(titles, columns = ['titles'])
    df_section_title['category'] = category[l]
    df_titles = pd.concat([df_titles, df_section_title], ignore_index = True)
df_titles.to_csv('./crawling_data/crawling_data.csv', index = False)

# print(titles) # 리스트로 저장됨
# print(len(titles))
print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())

# //*[@id="section_body"]/ul[1]/li[1]/dl/dt[2]/a -> Xpath는 요소마다 유니크함
# //*[@id="section_body"]/ul[2]/li[1]/dl/dt[2]/a
# //*[@id="section_body"]/ul[4]/li[5]/dl/dt[2]/a
# xpath 인덱스는 1부터 시작함
# li인덱스가 1에서 5까지 가면 ul 인덱스가 1상승, li 1로 초기화