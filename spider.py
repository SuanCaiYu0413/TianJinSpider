import re
import copy
import time
from lxml import etree

import requests


class DownLoader(object):
    def __init__(self):
        self.retry = {}
        # 重试次数
        self.retry_count = 5

    def get_html(self, url):
        try:
            req = requests.get(url, timeout=200)
            print(repr(req) + req.url)
            return req
        except Exception as e:
            print(repr(e) + '\n{}'.format(url))
            if self.retry.get(url):
                self.retry[url] += 1
            else:
                self.retry[url] = 1
            if self.retry.get(url) >= self.retry_count:
                return None
            time.sleep(2)
            return self.get_html(url)

    def post_html(self, url, data=None):
        if not data:
            data = {}
        try:
            req = requests.post(url=url, data=data, timeout=200)
            print(repr(req) + req.url)
            return req
        except Exception as e:
            print(repr(e) + '\n{}'.format(url))
            if self.retry.get(url):
                self.retry[url] += 1
            else:
                self.retry[url] = 1
            if self.retry.get(url) >= self.retry_count:
                return None
            time.sleep(2)
            return self.post_html(url, data)


class Crawl(object):

    def __init__(self, start_url):
        self.start_url = start_url
        self.result_item = {}
        self.result = []
        self.down = DownLoader()

    def get_project_urls(self, name):
        html = self.down.get_html(self.start_url).content
        select = etree.HTML(html.decode('utf8'))
        infos = select.xpath("//ul[@class='piclist']/li/div[@class='r_ptext clearfix']")
        self.loop_projects(infos, name)
        return self.result

    def loop_projects(self, infos, name):
        for info in infos:
            projectcaption = info.xpath("./div[@class='rpt_top']/h3/a/text()")
            project_url = info.xpath("./div[@class='rpt_top']/h3/a/@href")
            if project_url:
                project_url = project_url[0].replace('fcdt.aspx?mnutitle=&SelMnu=FCSJ_XMXX_JBXX',
                                                     'LouDongList.aspx?selmnu=FCSJ_XMXX_LPB')
                project_url = 'http://www.tjfdc.com.cn/Pages/fcdt/{}'.format(project_url)
                self.result_item['projectcaption'] = projectcaption

                if name not in projectcaption:
                    continue
                self.join_project(project_url)

    def join_project(self, project_url):
        project_html = self.down.get_html(project_url).content
        se = etree.HTML(project_html.decode('utf8'))
        while True:
            infos1 = se.xpath('//*[@id="divLouDongList"]/div/table/tr')[2:]
            page = se.xpath('//span[@id="LouDongList1_SplitPageIconModule1_lblCurrentPage"]/font/text()')
            if page:
                page = se.xpath('//span[@id="LouDongList1_SplitPageIconModule1_lblCurrentPage"]/text()')
            pages = se.xpath('//span[@id="LouDongList1_SplitPageIconModule1_lblPageCount"]/font/text()')
            if pages:
                pages = se.xpath('//span[@id="LouDongList1_SplitPageIconModule1_lblPageCount"]/text()')
            page = 1 if page == [] else page[0]
            pages = 1 if pages == [] else pages[0]
            __VIEWSTATE1 = se.xpath('//input[@id="__VIEWSTATE"]/@value')[0]
            __EVENTVALIDATION1 = se.xpath('//input[@id="__EVENTVALIDATION"]/@value')[0]
            self.loop_loudong(__VIEWSTATE1, __EVENTVALIDATION1, infos1, project_url)
            if page < pages:
                data = {
                    '__EVENTTARGET': 'LouDongList1$SplitPageIconModule1$lbnNextPage',
                    '__EVENTARGUMENT': '',
                    '__VIEWSTATE': __VIEWSTATE1,
                    '__VIEWSTATEGENERATOR': '27A26CDA',
                    '__EVENTVALIDATION': __EVENTVALIDATION1,
                    'hidDoing': '',
                    'txtJD': '',
                    'txtWD': '',
                    'txtProName': ''
                }
                f_req = self.down.post_html(project_url, data)
                se = etree.HTML(f_req.content.decode('utf8'))
            else:
                break

    def loop_loudong(self, __VIEWSTATE1, __EVENTVALIDATION1, infos, project_url):
        for info in infos:
            self.result_item['blockcaption'] = info.xpath('./td[1]/span/text()')
            self.result_item['blocknum'] = info.xpath('./td[2]/a/font/text()')
            self.result_item['periodcaption'] = info.xpath('./td[3]/span/text()')
            self.result_item['opentime'] = info.xpath('./td[4]/span/text()')
            self.result_item['blcok_houseprice'] = info.xpath('./td[5]/span/text()')
            self.result_item['blcok_otherprice'] = info.xpath('./td[6]/span/text()')
            self.result_item['selling_blocks'] = info.xpath('./td[5]/span/text()')

            block_id = info.xpath('./td[2]/a/@id')
            if block_id:
                block_id = block_id[0]
            else:
                continue

            block_id = block_id.replace('_', '$') if block_id else ''
            data = {
                '__EVENTTARGET': block_id,
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': __VIEWSTATE1,
                '__VIEWSTATEGENERATOR': '27A26CDA',
                '__EVENTVALIDATION': __EVENTVALIDATION1,
                'hidDoing': '',
                'txtJD': '',
                'txtWD': '',
                'txtProName': ''
            }
            print(info.xpath('./td[2]/a/font/text()'))
            self.join_loudong(data, project_url)

    def join_loudong(self, data, url):
        req = self.down.post_html(url, data)
        html2 = req.content.decode('utf8')
        se1 = etree.HTML(html2)
        ceel_ids = se1.xpath('//*[@id="divLouDongInfo"]/div/div[2]/div/table/tr[2]/td/a')
        __VIEWSTATE = se1.xpath('//input[@id="__VIEWSTATE"]/@value')[0]
        __EVENTVALIDATION = se1.xpath('//input[@id="__EVENTVALIDATION"]/@value')[0]

        self.loop_cell(__VIEWSTATE, __EVENTVALIDATION, ceel_ids, req.url)

    def loop_cell(self, __VIEWSTATE, __EVENTVALIDATION, cell_ids, url):
        for cell in cell_ids:
            self.result_item['region'] = cell.xpath('//*[@id="LouDongInfo"]/tr[3]/td[2]/span/text()')
            self.result_item['project_address'] = cell.xpath('//*[@id="LouDongInfo"]/tr[3]/td[4]/span/text()')
            self.result_item['developers'] = cell.xpath('//*[@id="LouDongInfo"]/tr[2]/td[6]/span/text()')

            cell_id = cell.xpath('./@href')[0]
            cell_id = re.findall("\('(.*?)'", cell_id)
            if cell_id:
                cell_id = cell_id[0]
            else:
                continue
            data = {
                '__EVENTTARGET': cell_id,
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': __VIEWSTATE,
                '__VIEWSTATEGENERATOR': '27A26CDA',
                '__EVENTVALIDATION': __EVENTVALIDATION,
                'hidDoing': '',
                'txtJD': '',
                'txtWD': '',
                'txtProName': ''
            }
            self.join_cell(data, url)

    def join_cell(self, data, url):
        req = self.down.post_html(url, data)
        se3 = etree.HTML(req.content.decode('utf8'))
        infos3 = se3.xpath('//*[@id="LouDongInfo1_dgData"]/tr/td/font/a')
        self.loop_romm(infos3)

    def loop_romm(self, infos):
        for info in infos:
            room_link = info.xpath('./@onclick')[0]
            room_links = re.findall(r'window.showModalDialog\("(.+)",window,', room_link)

            if room_links:
                room_link = room_links[0]
            self.result_item['room_link'] = room_link
            for item in self.result_item.items():
                if isinstance(item[1], list):
                    self.result_item[item[0]] = '' if len(item[1]) == 0 else item[1][0]
            self.result.append(copy.deepcopy(self.result_item))


if __name__ == "__main__":
    pass
