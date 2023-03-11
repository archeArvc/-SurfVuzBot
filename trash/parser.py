#!/usr/bin/python
# -*- coding: utf-8 -*-
import aiohttp
from bs4 import BeautifulSoup
import asyncio
from lxml import etree
import json
from pprint import pprint
from playwright.async_api import async_playwright


async def vuzoteka(city, subjects):
    async with aiohttp.ClientSession() as ses:
        # получаем html страницу с сайта
        response = await ses.get(url="https://vuzoteka.ru/%D0%B2%D1%83%D0%B7%D1%8B/%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%B0")
        if response.status == 200:
                
            # подключаем bs4 для разбора html'ки
            sp = BeautifulSoup(await response.text(), "html.parser")
            dom = etree.HTML(str(sp))


            geter_link = dom.xpath('//div[@class="label-part main-top-region first"]/div[@class="label-value"]/a/text()')
            ity_link = dom.xpath('//div[@class="label-part main-top-region first"]/div[@class="label-value"]/a/@href')
            citilink = []
            await ses.close()
            title_set = set()
            for y in range(len(geter_link)):
                if city == geter_link[y]:
                    result = await asyncio.gather(city_parse(url=f"https:{ity_link[y]}"))
                    for re in result[0]:
                        for ss in re['subs']:
                            if ss in subjects.split(" "):
                                rr = await asyncio.gather(get_links_vuzes(f"https:{re['link']}"))
                                for all in rr[0]:
                                    for link in all:
                                        title_set.add(link)
            all_vuzes = []
            for links in title_set:
                result = await asyncio.gather(get_vuzes_info(links))
                all_vuzes.append(result[0])
            
            return all_vuzes

async def city_parse(url):
    async with aiohttp.ClientSession() as ses:
        response = await ses.get(url=url)
        sp = BeautifulSoup(await response.text(), "html.parser")

        result = await asyncio.gather(plwrt(url=url))
        ls = []
        # print(result[0])
        for i in result[0]:
            ff = i['subs'].split(", ")
            # pprint(ff)
            if "русский язык" in ff:
                ff.remove("русский язык")
            if "математика" in ff:
                ff.remove("математика")
            if "информатика и ИКТ" in ff:
                ff.remove('информатика и ИКТ')
                ff.append("информатика")
            if "дополнительные испытания" in ff:
                ff.remove("дополнительные испытания")
                ff.append("входные")
            if "иностранный язык" in ff:
                ff.remove("иностранный язык")
                ff.append("английский")
            ls.append({
                "subs": ff,
                "link": i['link']
                })
        return ls

async def get_links_vuzes(url):
    async with aiohttp.ClientSession() as ses:
        response = await ses.get(url=url)
        sp = BeautifulSoup(await response.text(), "html.parser")
        dom = etree.HTML(str(sp))
        retr_inf = []
        link = dom.xpath("//a[@class='institute-search-title h3 color-l0']/@href")
        retr_inf.append(link)

        return retr_inf


async def get_vuzes_info(url):
    async with aiohttp.ClientSession() as ses:
        response = await ses.get(url=f"https:{url}")
        sp = BeautifulSoup(await response.text(), "html.parser")
        dom = etree.HTML(str(sp))

        title = dom.xpath("//h1[@class='institute-title']/text()")
        rate = dom.xpath("//div[@class='label-part number-8 even last']/div[@class='institute-view-value emphasis']/div/div[1]/text()")
        date = dom.xpath("//div[@class='label-part number-5']/div[@class='institute-view-value emphasis']/text()")
        students = dom.xpath("//div[@class='label-part number-6 even']/div[@class='institute-view-value emphasis']/text()")
        ege = dom.xpath("//div[@class='label-part number-7']/div[@class='institute-view-value emphasis']/text()")
        logo = dom.xpath("//div[@class='institute-logo']/img/@src")
        link_to_vuze = dom.xpath("//div[@id='institute-info']/div[1]/div[2]/a/@href")
        try:
            dom.xpath("//div[@class='label-part number-1']/div[@class='institute-view-value']/div[@class='yes-own-0']")
            data_soc = "да"
        except:
            data_soc = "нет"

        if not link_to_vuze:
            link_to_vuze = ['нет']

        return {
            "title": title[0],
            "social": data_soc,
            "date": date[0],
            "students": students[0],
            "ege": ege[0],
            "rate": rate[0],
            "logo": logo[0],
            "link": link_to_vuze[0]
        }


async def plwrt(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, wait_until='domcontentloaded')
        await page.get_by_role("link", name="все предметы егэ").click()
        await page.wait_for_timeout(100)
        await page.get_by_text("ещё").click()
        lctr = await page.content()
        sp = BeautifulSoup(lctr, "lxml")
        dom = etree.HTML(str(sp))
        intr = dom.xpath('//div[@class="inner-a3"]/a/text()')
        intr_link = dom.xpath('//div[@class="inner-a3"]/a/@href')
        ass = []
        for i in range(len(intr)):
            ass.append({
                "subs": intr[i],
                "link": intr_link[i]
            })
        return ass
    
# if __name__ == '__main__':
#     asyncio.run(vuzoteka('Москва', "физика биология"))