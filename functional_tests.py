from selenium import webdriver
import unittest

##
# 뿡상이는 씨(CSS)알못이지만 최선을 다 해서 꾸민 로그인 페이지가 제법 그럴싸하게 나와서 몹시나 흡족한다.
# 혼자만 보기 너무 아까워서 친구들에게 한 번 둘러보라고 강요를 한다.
# 협박을 당한 친구는 어쩔 수 없이 해당 웹 사이트를 확인하러 간다.
##


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    # def tearDown(self):
    #     self.browser.quit()

    def connect_bbungsang_web_page(self):
        self.browser.get('http://used-book-store-dev.ap-northeast-2.elasticbeanstalk.com/')

        ##
        # 웹 페이지 타이틀과 헤더가 'BongDal Login'을 표시하고 있다.
        ##

        # 웹 페이지 타이틀에 "Django" 라는 단어가 있는지 확인(test assertion 생성)
        self.assertIn('BongDal Login', self.browser.title)
        self.fail('Finish the test!')

    ##
    # 회원가입을 하기 귀찮은 친구1은 페이스북 로그인을 시도한다.
    # 페이스북 페이지에서 로그인을 하고, 로그인이 된 상태로
    # 뿡상이 애플리케이션 메인 페이지로 이동하게 된다.
    # 뿡상이에게 정보가 털린 친구1은 기분이 상한 채로 웹 페이지를 닫는다.
    ##

    def click_facebook_login_button(self):
        self.browser.find_element_by_class_name('btn-facebook').click()


if __name__ == '__main__':
    unittest.main(warnings='ignore')

    # nvt = NewVisitorTest()
    # nvt.setUp()
    # nvt.connect_bbungsang_web_page()
    # nvt.click_facebook_login_button()
