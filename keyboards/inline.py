from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

subsidii = [
    {"subject": "Физика", "strc": "phys"},
    {"subject": "Информатика", "strc": "inf"},
    {"subject": "Биология", "strc": "bio"},
    {"subject": "Химия", "strc": "ximi"},
    {"subject": "Иностранный", "strc": "eng"},
    {"subject": "География", "strc": "geo"},
    {"subject": "Обществознание", "strc": "social"},
    {"subject": "Литература", "strc": "litr"},
    {"subject": "История", "strc": "history"},
]

def convert(sub1, sub2 = "#", sub3 = "#"):
    data = ""
    for i in subsidii:
        if sub1 in i['strc']:
            data += f"{i['subject']} "
        if sub2 in i['strc']:
            data += f"{i['subject']} "
        if sub3 in i['strc']:
            data += f"{i['subject']} "
    return data

preset1 = CallbackData("ss1", "sub1")
preset2 = CallbackData("ss2", "sub2")
preset3 = CallbackData("ss3", "sub3")


def get_subs_array_one():
    subs = InlineKeyboardMarkup(row_width=3)
    array = []
    for sus in subsidii:
        array.append(
            InlineKeyboardButton(f"{sus['subject']}", callback_data=preset1.new(
            sub1 = f"{sus['strc']}",
        ))) 
    subs.add(*array)
    return subs

def get_subs_array_two():
    subs = InlineKeyboardMarkup(row_width=3)
    array = []
    for sus in subsidii:
        array.append(
            InlineKeyboardButton(f"{sus['subject']}", callback_data=preset2.new(
            sub2 = f"{sus['strc']}",
        ))) 
    subs.add(*array)
    return subs

def get_subs_array_three():
    subs = InlineKeyboardMarkup(row_width=3)
    array = []
    for sus in subsidii:
        array.append(
            InlineKeyboardButton(f"{sus['subject']}", callback_data=preset3.new(
            sub3 = f"{sus['strc']}",
        ))) 
    subs.add(*array)
    return subs

bs_inline = InlineKeyboardMarkup(row_width=3)
bs = CallbackData("count", "cc")

bs_inline.add(
    InlineKeyboardButton(f"1", callback_data=bs.new(
        cc = "1"
    )),
    InlineKeyboardButton(f"2", callback_data=bs.new(
        cc = "2"
    )),
    InlineKeyboardButton(f"3", callback_data=bs.new(
        cc = "3"
    ))
)


profiles_data = CallbackData("prof", "act")

ok_data = CallbackData("mesa", "type", "status")
ok_mrk = InlineKeyboardMarkup(row_width=1)
ok_mrk.add(InlineKeyboardButton("Хорошо", callback_data=ok_data.new(type = "ok", status = 0)))