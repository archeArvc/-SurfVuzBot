from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from lxml import etree



async def get_vuzes():
    async with aiohttp.ClientSession() as ses:
        response = await ses.get(url="https://vuzoteka.ru/%D0%B2%D1%83%D0%B7%D1%8B")
        sp = BeautifulSoup(await response.text(), "html.parser")
        dom = etree.HTML(str(sp))

        get_first_10_vuzes = dom.xpath("//a[@class='institute-search-title h3 color-l0']/@href")
        message = ""
        for i in range(len(get_first_10_vuzes)):
            if i > 9:
                break
            else:
                res = await asyncio.gather(get_vuze_info(f"https:{get_first_10_vuzes[i]}"))
                message += res[0]
        return message

async def get_vuze_info(link):
    async with aiohttp.ClientSession() as ses:
        response = await ses.get(url=link)
        sp = BeautifulSoup(await response.text(), "html.parser")
        dom = etree.HTML(str(sp))

        # Название вуза
        first_vuze_name = dom.xpath("//h1[@class='institute-title']/text()")[0].split(" ")[0]
        # ссылка на офф. сайт вуза
        try:
            get_link_for_vuze = dom.xpath("//div[@id='institute-info']/div/div/a/@href")[0]
        except:
            get_link_for_vuze = "ссылки нет"
        
        # рейтенговый номер
        get_rate_number = dom.xpath("//div[@class='label-part number-8 even last']/div[@class='institute-view-value emphasis']/div[1]/div/text()")[0]

        message = f"{first_vuze_name}: Рейтинг - {get_rate_number}; Ссылка: {get_link_for_vuze}\n"

        return message
    

async def top_your_city(city):
    async with aiohttp.ClientSession() as ses:
        response = await ses.get(url=f"https://vuzoteka.ru/%D0%B2%D1%83%D0%B7%D1%8B/{city}?sort=%D1%80%D0%B5%D0%B9%D1%82%D0%B8%D0%BD%D0%B3")
        sp = BeautifulSoup(await response.text(), "html.parser")
        dom = etree.HTML(str(sp))

        get_first_10_vuzes = dom.xpath("//a[@class='institute-search-title h3 color-l0']/@href")
        message = ""
        for i in range(len(get_first_10_vuzes)):
            if i > 9:
                break
            else:
                res = await asyncio.gather(get_vuze_info(f"https:{get_first_10_vuzes[i]}"))
                message += res[0]
        return message