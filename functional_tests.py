from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

# 웹 페이지 타이틀에 "Django" 라는 단어가 있는지 확인(test assertion 생성)
assert 'BongDal Login' in browser.title