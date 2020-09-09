# zhku-spider
## Background
__学了点爬虫，于是就找来了教务网作为试验品，克服了许多困难，写出了个这个笨比玩意__
> 我能力有限也不是计算机出身，野路子代码多了去了，又不规范，知道各位都是大神，所以别骂了别骂了。。呜呜呜
## Requirement
```
import requests
from bs4 import BeautifulSoup
import re
import zhkulogin
import os
import random
import hashlib
import time
import bs4
```
## Demo
__其实还是有很多很多缺陷！！__
但是我懒得弄了，懒得维护了哈哈哈
主要在控制台的效果是这样的
***
![image](https://github.com/yujiecong/zhku-spider/tree/master/image/效果.png)
***
可以拿到课表
![image](https://github.com/yujiecong/zhku-spider/tree/master/image/20200.jpg)
***
可以拿到成绩,但是在这里的图片命名是有问题的。
不妨碍观看就好，嘻嘻懒得搞了
![image](https://github.com/yujiecong/zhku-spider/tree/master/image/第6个学期的成绩.jpg)
***
么么哒爱你们！！


## Usage
目前稳定的功能是获取课表和获取成绩，所谓的抢课还不是完全稳定，之前试过但由于参数太多，可能换个学期参数不一样，所以需要继续观察。

登录的验证码本来是有百度ocr来自动识别的，但是发现麻烦，而且比较看运气，还不如自己输。

就这点了，欢迎仲恺的同学发现并且pr！！

## Maintainers
___电子181余杰聪___
# END
___一切一切仅供学习使用[DOGE]___
