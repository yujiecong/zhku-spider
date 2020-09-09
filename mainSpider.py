import requests
from bs4 import BeautifulSoup
import re
import zhkulogin
import os
import random
import hashlib
import time
import bs4
class zk_spider():
    def __init__(self):
        self.Login()
        self.Main()
        #主循环

    def Main(self):
        while 1:
            print('已经获取登录权限')
            year = str(time.localtime(time.time())[0])
            mouth = time.localtime(time.time())[1]
            # 判断当前月份，用来判断第上下学期
            if mouth > 8 or mouth < 3:
                options_seme = '0'
            else:
                options_seme = '1'
            print(f"当前为{year}年{mouth}月,{'上' if options_seme == '0' else '下'}学期")

            Input = input('输入任意键下一步,按1获得成绩,2获得课表,3网上正选抢公选课，4是公选结果,5是退选，6是重新登录')
            if Input == '1':
                self.Get_MyScore()
            elif Input == '2':
                seme = input('输入学年学期，例如20191,回车默认为本学期')
                if seme == '':
                    self.Get_curriculum(year + options_seme)
                else:
                    self.Get_curriculum(seme)
            elif Input == '3':
                options_type = input('请输入选课类型，0是专业限选，2是公共选修')
                self.Get_options(options_type, options_seme, year)
            elif Input == '4':
                self.Get_options_result()
            elif Input == '5':
                self.withdraw_course(options_seme, year)
            elif Input == '6':
                self.Login(hot=False)
    def get_cookies(self,mode):
        with open('cookies.cok', 'w')as f:
            while 1:
                self.zk_user.Get_login_cookies()
                self.zk_user.Get_code()
                if not self.zk_user.identify_code(mode):#如果没有返回1，那么就是识别失败重新开始。
                    continue
                #开始尝试登录
                login_success = self.zk_user.Try_Login_()
                if login_success:
                    # 这个跟cookie查成绩有关
                    self.zk_user.home_cookies['name'] = 'value'
                    break
            f.write(str(self.zk_user.home_cookies))
            print('登录cookie已保存')
    def Login(self,hot=True):
        #这里目前不完善
        select_mode = input('默认为自动登录(通过百度ocr识别验证码)，输入default手动登录')
        select_mode='auto' if select_mode=='' else 'default'

        if os.path.exists('cookies.cok') and hot:
            print('检测到本地已有cookies，开始使用本地cookies')
            self.zk_user = zhkulogin.zklogin()
            with open('cookies.cok','r')as f:
                fread=f.read()
                if fread=='':
                    print('cookies为空！！开始重新登录')
                    self.get_cookies(select_mode)
                else:
                    self.zk_user.home_cookies = eval(fread)
            if '无权' in requests.get(url='http://jw.zhku.edu.cn/wsxk/stu_xszx_rpt.aspx',cookies=self.zk_user.home_cookies).text:
                print('cookies已失效，开始重新登录')
                self.get_cookies(select_mode)
            else:
                print('cookies仍然有效')
        else:
            print('检测到本地没有cookies，重新获取中')
            self.get_cookies(select_mode)
    def Get_MyScore(self):
        # 打印入学以来即可
        MyScore_url = 'http://jw.zhku.edu.cn/xscj/Stu_MyScore_rpt.aspx'
        curriculum_data = {
            # 这个参数是什么？
            'SJ': '1',
            # 用fiddler可以看出来
            'btn_search': '检索'.encode('gbk'),
            # 入学以来
            'SelXNXQ': '0',
            'zfx_flag': '0',
            'zxf': '0'}
        # 这一步是为了更新cookies，一定的要
        score_html = requests.post(url=MyScore_url, cookies=self.zk_user.home_cookies, data=curriculum_data)
        # 需要匹配出来
        score_urls = re.findall(
            'Stu_MyScore_Drawimg.aspx\?x=\d{1,}&h=\d{1,}&w=\d{3,}&xnxq=\d{5}&xn=&xq=&rpt=\d{1}&rad=\d{1}&zfx=\d{1}&xh=\d{12}',
            score_html.text)
        for i, url in enumerate(score_urls):
            req = requests.get(url='http://jw.zhku.edu.cn/xscj/' + url, cookies=self.zk_user.home_cookies)
            with open('第%d个学期的成绩.jpg' % i, 'wb') as f:
                f.write(req.content)
                print('已获得第%d个学期的成绩' % i)
            os.system('第%d个学期的成绩.jpg' % i)
    def Get_curriculum(self, semester):
        curriculum_html = requests.get(url='http://jw.zhku.edu.cn/znpk/Pri_StuSel.aspx',
                                       cookies=self.zk_user.home_cookies)
        #以下可能非必要
        random_str = ''
        randomstring = 'abcdefghijklmnopqrstuvwxyz1234567890'
        for _ in range(15):
            random_str += random.choice(randomstring)
        hidyzm = re.search('[a-zw0-9]{31,31}', curriculum_html.text).group(0)
        #以上
        def get_hid_md5(r):
            code = "11347" + semester + r
            md5 = hashlib.md5()
            md5.update(code.encode('utf8'))
            return md5.hexdigest().upper()

        course_data = {'Sel_XNXQ': semester,
                       'rad': '0',
                       'px': '0',
                       'txt_yzm': '',
                       'hidyzm': hidyzm,
                       'hidsjyzm': get_hid_md5(random_str)}
        para = {'m': random_str}
        curriculum_html = requests.post(url='http://jw.zhku.edu.cn/znpk/Pri_StuSel_rpt.aspx',
                                        cookies=self.zk_user.home_cookies, data=course_data, params=para)
        # 同样的也要匹配出来
        #print(curriculum_html.text)
        curriculum_url = re.search('Pri_StuSel_Drawimg.aspx\?type=\d{1}&w=\d{,}&h=\d{,}&xnxq=\d{5}',
                                   curriculum_html.text).group(0)
        with open('{}.jpg'.format(semester), 'wb') as f:
            f.write(
                requests.get('http://jw.zhku.edu.cn/znpk/' + curriculum_url, cookies=self.zk_user.home_cookies).content)
            print('成功下载{}学期的课表'.format(semester[:-1]+('上' if semester[-1]=='0' else '下')))
        os.system('{}.jpg'.format(semester))
    def Get_options_result(self):
        options_result = requests.get(url='http://jw.zhku.edu.cn/wsxk/stu_zxjg_rxyl.aspx',
                                      cookies=self.zk_user.home_cookies)
        options_result_url = re.search('/znpk/DrawKbimg.aspx\?w=\d{3,4}&h=\d{3,4}&type=zxjg',
                                       options_result.text).group(0)
        result = requests.get(url='http://jw.zhku.edu.cn' + options_result_url, cookies=self.zk_user.home_cookies)
        with open('入学以来正选结果.jpg', 'wb')as f:
            f.write(result.content)
            print('成功下载入学以来正选结果.jpg')
        os.system('入学以来正选结果.jpg')
    def Get_options(self, options_type, options_seme, year):
        data = {
            # lx  是类型 0是本年级专业任选  2 是公共任选
            'sel_lx': options_type,
            'sel_xq': options_seme,
            'Submit': '检索'.encode('gbk'),  #
            'kc': ''
        }
        rpt = requests.post(url='http://jw.zhku.edu.cn/wsxk/stu_xszx_rpt.aspx', data=data,
                            cookies=self.zk_user.home_cookies)
        rpt_soup = BeautifulSoup(rpt.text, features="lxml")
        if options_type == '0':
            speciality = rpt_soup.find('input',{'id':'SelSpeciality'}).attrs['value']
            data['SelSpeciality'] = speciality
            #2019|1|130100|0|0|2018|3703|0
            course_value = re.findall('\d{4}\|\d{1}\|\d{6}\|\d{1}\|\d{1}\|\d{4}\|\d{4}\|\d{1}', rpt.text)
        elif options_type == '2':
            ##2019|1|000326|0|2|||1
            course_value = re.findall('\d{4}\|\d{1}\|\d{6}\|\d{1}\|\d{1}\|\|\|\d{1}', rpt.text)
        else:
            raise Exception('sb乱打数字')
        if course_value==[]:
            print('没有课可以选！！！！！！')
            return
        #这里有必要说一下，这sb教务网
        #是以B,H,B,H循环排列的信息，很恶心
        #这些算法我比较弱，哈哈算了
        #并且以下可能会失效，因为不是用的最好的方法
        B = rpt_soup.find_all('tr', {'class': 'B'})
        H = rpt_soup.find_all('tr', {'class': 'H'})
        course_list = list()
        count = 0
        temp = []
        Bi = 0
        Hi = 0
        for i in range(len(B) + len(H)):
            if i % 2 == 0:
                for bstring in B[Bi].stripped_strings:
                    temp.append(bstring)
                    count += 1
                if count % 6 == 0:
                    course_list.append(temp[:-2])
                    temp = []
                Bi += 1
            else:
                for hstring in H[Hi].stripped_strings:
                    temp.append(hstring)
                    count += 1
                if count % 6 == 0:
                    course_list.append(temp[:-2])
                    temp = []
                Hi += 1
        course_name = [l[0] for l in course_list]
        course_dict = {k: v for k, v in enumerate(course_value)}
        course_classification = [l[-1] for l in course_list]
        course_socre = [l[1] for l in course_list]
        course_time = [l[2] for l in course_list]
        for k, v in course_dict.items():
            print('输入{}--->>选{} 类别:{} 学分:{} 学时:{}'.format(k, course_name[k], course_classification[k], course_socre[k], course_time[k]))

        # # 然后打开选课的页面，就是选的是上课时间
        chooseskbj_url = 'http://jw.zhku.edu.cn/wsxk/stu_xszx_chooseskbj.aspx'
        while 1:
            xh = input('请输入想抢课的序号,输入q退出')
            if xh == 'q':
                break
            if not xh.isdigit() :
                print('请输入数字！！')
                continue
            elif eval(xh)<0 or eval(xh)>=len(B)+len(H):
                print('别乱输啊,我淦')
                continue
            chkKCvalue = rpt_soup.find('input', {'id': 'chkKC{}'.format(xh)}).attrs['value']
            course_params = {'lx': 'ZX',  # 正选
                             'id': course_value[eval(xh)],  # 课程id
                             'skbjval': '',
                             'xq': options_seme}
            course_info = requests.get(url=chooseskbj_url, cookies=self.zk_user.home_cookies, params=course_params)
            soup = BeautifulSoup(course_info.content.decode('gbk'), features="lxml")
            #网络课与实体课不一样，必须这样，不然报错，我也不知道咋统一起来
            #结构不一样，多了一个结点
            if '网络课' not in course_name[eval(xh)]:
                course_info_l = ['上课班组', '教师链接', '教师名字', '上课班号', '上课班级名称', '限选', '已选', '可选', '上课时间', '上课地点', '选定',
                                 '选课序号']
            else:
                course_info_l = ['上课班组', '教师名字', '上课班号', '上课班级名称', '限选', '已选', '可选', '上课时间', '上课地点', '选定',
                                 '选课序号']
            # 课程信息
            Btr = soup.find_all('tr', {'class': 'B'})
            Htr = soup.find_all('tr', {'class': 'H'})
            BHtr=list()
            bi = 0
            hi=0
            for tri in range(len(Btr)+len(Htr)):
                if tri%2==0:
                    BHtr.append(Btr[bi])
                    bi+=1
                else:
                    BHtr.append(Htr[hi])
                    hi+=1

            course_info_value = list()
            #顺序是BHBHBHBH...

            ci=0
            for tr_length in range(len(Btr)+len(Htr)):
                line = []
                for bhtdc in BHtr[tr_length].descendants:

                    if type(bhtdc) == bs4.Tag and bhtdc != '\n' and bhtdc.contents:
                        if 'input' in str(bhtdc):
                            if 'disabled' in str(bhtdc):
                                line.append('不可选')
                            else:
                                line.append('可选')
                            continue

                        bhtdcs = bhtdc.contents[0]
                        if type(bhtdcs) == bs4.NavigableString:
                            line.append(bhtdcs.replace('\n', '').strip())
                        else:
                            line.append('None')
                line.append('输入' + str(ci) + "选择这门")
                ci += 1
                course_info_value.append(line)
            print()
            print('课程名称为',course_name[eval(xh)])
            for infoi, info in enumerate(course_info_l):
                print(
                    '[{course_info:<{len}}\t'.format(course_info=info + ']', len=15 - len(info.encode('GBK', 'ignore')) + len(info)),
                    end='')
                for course_info_index in range(len(course_info_value)):
                    course_info = course_info_value[course_info_index][infoi]
                    print('[{details:<{len}}\t'.format(details=course_info + ']',
                                                       len=22 - len(course_info.encode('gbk', 'ignore')) + len(
                                                           course_info)), end='')
                print()
            print()
            xxxxxx_xxx_xxx_value = []
            bhl = [{'class': 'B'}, {'class': 'H'}]
            for bh in bhl:
                for tr in soup.find_all('tr', bh):
                    j = tr.find('input', {'name': 'J'})
                    Q = tr.find('input', {'name': 'Q'})
                    if j:
                        xxxxxx_xxx_xxx_value.append(j.attrs['value'])
                    if Q:
                        xxxxxx_xxx_xxx_value.append(Q.attrs['value'])
            choice_cource = input('请输入选择哪一个课程')
            if choice_cource.isdigit():
                if eval(choice_cource)<0 or eval(choice_cource)>=len(xxxxxx_xxx_xxx_value):
                    print('不要乱选！！')
                    continue
            else:
                print('不要乱选！！')
                continue
            # 提交网址
            submit_url = 'http://jw.zhku.edu.cn/wsxk/stu_xszx_rpt.aspx'
            # 这里不用管别的参数了，只要管需要选的课的信息即可。。了
            chkKCcode = rpt_soup.find("input", {"id": 'chkKC{}'.format(xh)})
            chkKCcode = chkKCcode.attrs['value']
            if options_type == '0':
                data = {
                    'sel_xnxq': year + options_seme,
                    'mcount': str(len(course_value)),
                    'sel_lx': options_type,
                    'SelSpeciality': speciality,
                    'id': ('TTT,' + xxxxxx_xxx_xxx_value[eval(choice_cource)].split('@')[1].split(';')[
                        0] + "¤" + chkKCcode + ',' + xxxxxx_xxx_xxx_value[eval(choice_cource)].split('@')[1].split(';')[
                               1] + '¤' + chkKCcode).encode('gbk'),
                    'yxsjct': '',
                    'sel_xq': options_seme,
                    'hid_ReturnStr': '',
                    'hid_N': ''
                }
            elif options_type == '2':
                data = {
                    'sel_xnxq': year + options_seme,
                    'mcount': str(len(course_value)),
                    'sel_lx': options_type,
                    'SelSpeciality': '',
                    'id': ('TTT,' + xxxxxx_xxx_xxx_value[eval(choice_cource)].split('@')[1] + '¤' + chkKCvalue).encode(
                        'gbk'),
                    'yxsjct': '',
                    'sel_xq': options_seme,
                    'hid_ReturnStr': '',
                    'hid_N': ''
                }
            for _ in range(len(course_value)):
                data['chkSKBJ{}'.format(_)] = ''
            data['chkSKBJ{}'.format(xh)] = xxxxxx_xxx_xxx_value[eval(choice_cource)].split('@')[1]
            data['chkKC{}'.format(xh)] = chkKCcode.encode('gbk')
            submit = requests.post(url=submit_url, cookies=self.zk_user.home_cookies,
                                   params={'func': '1'},
                                   data=data)
            print(re.search('<font.{1,}</font>', submit.text).group(0))
    def withdraw_course(self,options_seme, year):
        txjg=requests.get('http://jw.zhku.edu.cn/wsxk/stu_txjg_rpt.aspx',cookies=self.zk_user.home_cookies)
        soup = BeautifulSoup(txjg.text, features="lxml")
        inp = soup.find_all('input')
        course_value=list()
        for i in inp:
            if not 'disabled' in str(i):
                try:
                    if i.attrs['id'][:-1] == 'chkDel':
                        course_value.append(i.attrs['value'])
                except:
                    pass

        img_url="http://jw.zhku.edu.cn"+re.search('/znpk/DrawKbimg.aspx\?w=.{,4}&h=.{,4}&xn=.{,4}&xq=.{,1}&zfx=.{,1}&type=.{,5}',txjg.text).group(0)

        with open('withdraw_course.jpg','wb')as f:
            f.write(requests.get(img_url,cookies=self.zk_user.home_cookies).content)
        print('成功获得退选照片')
        os.system('withdraw_course.jpg')
        print('根据目前含有的课程编号选择！')
        for i,cv in enumerate(course_value):
            print('我是第{}个:->{}'.format(i,cv))

        tx=input('请输入是第几个')
        if eval(tx) not in range(0,2):
            raise Exception('你别乱搞')
        data={ 'chkDel5': course_value[eval(tx)],
        'chkCount': '15',
        'deleteValue': 'TTT,'+course_value[eval(tx)],
        'sel_xnxq': year+options_seme}
        final=requests.post(url='http://jw.zhku.edu.cn/wsxk/stu_txjg_rpt.aspx?func=1',cookies=self.zk_user.home_cookies,data=data)
        print(re.search('<font color=blue>.{,20}</font>',final.text).group(0))


zk_spider()
