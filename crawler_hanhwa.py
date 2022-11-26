import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import random
import re
import numpy as np
import pandas as pd
import tqdm

# 크롬 드라이버 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('—headless')
chrome_options.add_argument('—no-sandbox')
chrome_options.add_argument("—single-process")
chrome_options.add_argument("—disable-dev-shm-usage")
chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument("disable-gpu")
driver = webdriver.Chrome(ChromeDriverManager(version='94.0.4606.61').install(),chrome_options=chrome_options)

# 데이터프레임 생성
data = pd.DataFrame(columns=['page','reportNo','title','summary','full_body'])

startpage = 1
endpage = 354
url_base = 'https://www.hanwhawm.com/main/research/main/list.cmd?depth3_id=anls1&mode=&viewclass=&p='
idx = 0

# 제목, 요약문, 본문 크롤링
for i in range(startpage,endpage+1):   # 리포트 목록 페이지 번호
    url = url_base + str(i)  # p: page
    driver.get(url) 
    time.sleep(2)
    
    for j in range(1,11):
        # 리포트 목록 페이지에서 리포트 한개 클릭 (한 페이지에 10개 리포트)  # li[1]~li[10]
        indiv_report = driver.find_element(By.XPATH, '//*[@id="content"]/div[3]/div[2]/ul/li['+ str(j) +']/div[1]/a')  
        indiv_report.click()
        time.sleep(2)
        
        # 리포트 화면에서 크롤링 
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        # 제목
        title = soup.find('div', attrs={'id':'boardTitle'}).text.strip()
        if ('weekly' in title) or ('주간' in title) or ('모닝콜' in title):
            # 요약문, 본문 공란으로 두기
            summ = ''
            result = ''
        else:
            try: 
                # 요약문
                summ = soup.find('div', attrs={'class':'research_bbs_top_mail'}).text.strip()
                # 본문
                bodyTable = soup.find('div', attrs={'class':'researchCont'}).find_all('table')
                result = []
                for body in bodyTable:
                    if bool(body.find('img')):  # 이미지 제목,캡션 등 제외
                        pass
                    else:
                        result.append(body.text.strip())
            except:
                try:
                    # 요약문
                    all_content = soup.find('div', attrs={'class':'researchCont'}).find_all('table')
                    summ = all_content[0].text.strip()
                    # 본문
                    result = []
                    for k in range(1, len(all_content)):
                        if bool(all_content[k].find('img')):
                            pass
                        else:
                            result.append(all_content[k].text.strip())
                except:
                    # 요약문, 본문 공란으로 두기
                    summ = ''
                    result = ''
                    
        # 데이터프레임에 입력
        title = re.sub(' +', ' ', title)
        summ = re.sub(' +', ' ', summ)
        result = ' '.join(result)
        result = re.sub(' +', ' ', result)
        result = re.sub('\n\n\n\n\n', ' ', result)
        result = re.sub('\n\n\n\n', ' ', result)
        data.loc[idx] = [i,j,title, summ, result]
        
        # 뒤로가기
        driver.back()
        time.sleep(2)
        idx+=1

data.to_csv('/home/nsun/nlp_project/hanhwa_reports.csv', header = True, index=False)