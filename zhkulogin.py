import os
import requests
import hashlib
from aip import AipOcr
class zklogin():
    def Get_login_cookies(self,hot=True):
        self.home_cookies = dict(requests.get(
            url='http://jw.zhku.edu.cn/home.aspx',
            headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36',
            'Host': 'jw.zhku.edu.cn'}).cookies)
        print(self.home_cookies)
    def Get_code(self):
        # 验证码 url
        Codeurl = 'http://jw.zhku.edu.cn/sys/ValidateCode.aspx'
        Code_headers = {
            'Host': 'jw.zhku.edu.cn',
            'Referer': 'http://jw.zhku.edu.cn/_data/login_home.aspx',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36'
        }
        self.Code_path = 'yzm.jpg'
        self.Code_response = requests.get(
            url=Codeurl,
            headers=Code_headers,
            cookies=self.home_cookies)
        with open(self.Code_path, 'wb') as f:
            f.write(self.Code_response.content)
            print('成功下载验证码')

    def identify_code(self,select_mode):
        # //一天限量200次我佛了
        print(select_mode)
        if select_mode=='default':
            os.system(self.Code_path)
            code = input('请输入验证码')
            self.Get_md5(code)
            return 1
        elif select_mode=='auto':
            APP_ID = '15411469'
            API_KEY = 'nUUTMGL66bzhbI8DYZGYW3vQ'
            SECRET_KEY = 'OvEV50n2EUAdiq1qsDIhNCWljdc0nPWO'
            aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
            options = {
                'detect_direction': 'true',
                'language_type': 'ENG',
            }
            with open(self.Code_path, 'rb') as fp:
                Code_Image_data = fp.read()
            result = aipOcr.webImage(Code_Image_data, options)
            print(result)
            if result.get('words_result'):
                code = result.get('words_result')[0].get('words').replace(' ', '')
                print('验证马是:' + code)
                self.Get_md5(code)
                return 1
            else:
                self.Md5__Code = ''
                return
    def Try_Login_(self):


        self.account=input('输入你的学号')
        self.pwd=input('你的密码')


        self.Get_pwd_md5(self.pwd)
        login_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'jw.zhku.edu.cn',
            'Origin': 'http://jw.zhku.edu.cn',
            'Referer': 'http://jw.zhku.edu.cn/_data/home_login.aspx',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36'}
        data = {
            'typeName': 'ѧ��',
            'dsdsdsdsdxcxdfgfg': self.Md5_pwd_Code,
            'fgfggfdgtyuuyyuuckjg': self.Md5__Code,
            'Sel_Type': 'STU',
            'txt_asmcdefsddsd': self.account,
            'txt_pewerwedsdfsdff': '',
            'txt_sdertfgsadscxcadsads': '',
            'txt_mm_lxpd': '',
            'txt_psasas': '����������'}
        login = requests.post(
            url="http://jw.zhku.edu.cn/_data/login_home.aspx",
            headers=login_headers,
            data=data,
            cookies=self.home_cookies)

        print('正在尝试登陆')
        if '正在加载' in login.text:
            print('登录成功')
            return True
        else:
            print('验证码不对，再来')
            return False
    def Get_pwd_md5(self,pwd):
        #md5(document.all.txt_asmcdefsddsd.value + md5(obj.value).substring(0, 30).toUpperCase() + '11347').substring(0, 30).toUpperCase()]
        md5 = hashlib.md5()
        md5.update(pwd.encode('utf8'))
        md5_ = self.account+md5.hexdigest()[0:30].upper()
        md5_ = md5_ + '11347'
        md52 = hashlib.md5()
        md52.update(md5_.encode('utf8'))
        self.Md5_pwd_Code = md52.hexdigest()[0:30].upper()
    def Get_md5(self, Code):
        #验证码md5加密
        code = Code.upper()
        md5 = hashlib.md5()
        md5.update(code.encode('utf8'))
        md5_ = md5.hexdigest().upper()
        md5_ = md5_[0:30] + '11347'
        md55 = hashlib.md5()
        md55.update(md5_.encode('utf8'))
        self.Md5__Code = md55.hexdigest()[0:30].upper()
t=zklogin()
