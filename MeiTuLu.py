import requests
from lxml import etree
import time
import os


def writeToFile(content, number, context_name):
    with open(str(context_name) + '\\' + str(number) + '.jpg', 'wb') as f:
        try:
            f.write(content)
        except:
            print('淦!鬼知道为什么文件写入失败！可能搜的东西有问题或者网站改了。')


if __name__ == '__main__':
    input_content = ''
    want_mount = 1
    current_mount = 0
    sleep_time = 1
    exit_code = 'ass_hole'
    search_url = 'https://www.meitulu.com/search/'
    site_prefix = 'https://www.meitulu.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 '
                      'Safari/537.36 '
    }
    print('为了保证你的访问正常，我们设置下载间隔时间位1秒，可能有点小慢，但是足够你欣赏美图。')
    while True:
        print('----------------------------------------------------')
        input_content = input('请输入要搜索的内容(输入ass_hole退出程序):')
        if input_content == exit_code:
            break
        search_html = requests.get(search_url + str(input_content))
        search_html.encoding = 'utf-8'
        search_selector = etree.HTML(search_html.text)
        dataList = search_selector.xpath('/html/body/div[2]/div[2]/ul/li')
        current_mount = len(dataList)
        if current_mount == 0:
            print('该搜索字段没有找到任何美图。')
            continue
        print('一共找到了' + str(current_mount) + '个美图集。(好像最多就是20)')
        want_mount = int(input('请输入你想下载的图集数量(<' + str(current_mount) + '):'))
        if want_mount > current_mount:
            print('贪得无厌不可取，只给你下载' + str(current_mount) + '张')
            want_mount = current_mount
        for i in range(1, want_mount + 1):
            title = dataList[i].xpath('p[2]/a/text()')[0]
            if not os.path.isdir(title):
                os.mkdir(title)
            print('准备下载图集:' + title)
            content_url = dataList[i].xpath('a/@href')[0]
            last_page_url = ''
            current_page_url = content_url
            number = 0
            page = 1
            while current_page_url != last_page_url:
                print('正在下载第' + str(page) + '页的图片...')
                time.sleep(sleep_time)
                content_html = requests.get(current_page_url)
                content_html.encoding = 'utf-8'
                content_selector = etree.HTML(content_html.text)
                content_dataList = content_selector.xpath('/html/body/div[4]/center/img')
                for img_data in content_dataList:
                    img_src = img_data.xpath('@src')[0]
                    img = requests.get(img_src)
                    writeToFile(img.content, number, title)
                    number += 1
                last_page_url = current_page_url
                current_page_url = site_prefix + content_selector.xpath('/html/body/center/div/a')[-1].xpath('@href')[0]
                page += 1
