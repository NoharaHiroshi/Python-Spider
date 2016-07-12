#! -*-coding:utf-8 -*-

from urllib import request, parse
from bs4 import BeautifulSoup as BS
import json
import datetime
import xlsxwriter

starttime = datetime.datetime.now()

url = r'http://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC'
# 拉钩网的招聘信息都是动态获取的，所以需要通过post来递交json信息，默认城市为北京

tag = ['companyName', 'companyShortName', 'positionName', 'education', 'salary', 'financeStage', 'companySize',
       'industryField', 'companyLabelList']  # 这是需要抓取的标签信息，包括公司名称，学历要求，薪资等等

tag_name = ['公司名称', '公司简称', '职位名称', '所需学历', '工资', '公司资质', '公司规模', '所属类别', '公司介绍']


def read_page(url, page_num, keyword):  # 模仿浏览器post需求信息，并读取返回后的页面信息
    page_headers = {
        'Host': 'www.lagou.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'Connection': 'keep-alive'
        }
    if page_num == 1:
        boo = 'true'
    else:
        boo = 'false'
    page_data = parse.urlencode([   # 通过页面分析，发现浏览器提交的FormData包括以下参数
        ('first', boo),
        ('pn', page_num),
        ('kd', keyword)
        ])
    req = request.Request(url, headers=page_headers)
    page = request.urlopen(req, data=page_data.encode('utf-8')).read()
    page = page.decode('utf-8')
    return page


def read_tag(page, tag):
    page_json = json.loads(page)
    page_json = page_json['content']['result']  # 通过分析获取的json信息可知，招聘信息包含在返回的result当中，其中包含了许多其他参数
    page_result = [num for num in range(15)]  # 构造一个容量为15的list占位，用以构造接下来的二维数组
    for i in range(15):
        page_result[i] = []  # 构造二维数组
        for page_tag in tag:
            page_result[i].append(page_json[i].get(page_tag))  # 遍历参数，将它们放置在同一个list当中
        page_result[i][8] = ','.join(page_result[i][8])
    return page_result   # 返回当前页的招聘信息


def read_max_page(page):  # 获取当前招聘关键词的最大页数，大于30的将会被覆盖，所以最多只能抓取30页的招聘信息
    page_json = json.loads(page)
    max_page_num = page_json['content']['totalPageCount']
    if max_page_num > 30:
        max_page_num = 30
    return max_page_num


def save_excel(fin_result, tag_name, file_name):  # 将抓取到的招聘信息存储到excel当中
    book = xlsxwriter.Workbook(r'C:\Users\Administrator\Desktop\%s.xls' % file_name)  # 默认存储在桌面上
    tmp = book.add_worksheet()
    row_num = len(fin_result)
    for i in range(1, row_num):
        if i == 1:
            tag_pos = 'A%s' % i
            tmp.write_row(tag_pos, tag_name)
        else:
            con_pos = 'A%s' % i
            content = fin_result[i-1]  # -1是因为被表格的表头所占
            tmp.write_row(con_pos, content)
    book.close()


if __name__ == '__main__':
    print('**********************************即将进行抓取**********************************')
    keyword = input('请输入您要搜索的语言类型：')
    fin_result = []  # 将每页的招聘信息汇总成一个最终的招聘信息
    max_page_num = read_max_page(read_page(url, 1, keyword))
    for page_num in range(1, max_page_num):
        print('******************************正在下载第%s页内容*********************************' % page_num)
        page = read_page(url, page_num, keyword)
        page_result = read_tag(page, tag)
        fin_result.extend(page_result)
    file_name = input('抓取完成，输入文件名保存：')
    save_excel(fin_result, tag_name, file_name)
    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds
    print('总共用时：%s s' % time)



