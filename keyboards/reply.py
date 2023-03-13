from aiogram.types import *

# основная клавиатура
main = ReplyKeyboardMarkup(resize_keyboard=True)
searching = KeyboardButton("Поиск🔬")
top = KeyboardButton("Топы вузов🆒")
filters_main = KeyboardButton("Фильтры")
main.add(searching, top, filters_main)
back = KeyboardButton("Назад")

# топы вузов
toper = ReplyKeyboardMarkup(resize_keyboard=True)
top_your_city = KeyboardButton("Топ вузов вашего города")
top_russia = KeyboardButton("Топ 10 вузов России")
toper.add(top_your_city, top_russia).add(back)

# поиск
searcing_bottom = ReplyKeyboardMarkup(resize_keyboard=True)
for_filters = KeyboardButton("Поиск по фильтрам")
for_speciality = KeyboardButton("Поиск по специальности")
searcing_bottom.add(for_filters, for_speciality).add(back)

# фильтры
filters_mrk = ReplyKeyboardMarkup(resize_keyboard=True)
subjects = KeyboardButton("Предметы")
city = KeyboardButton("Город")
profiles = KeyboardButton("Профиль")
dop_ex = KeyboardButton("Входные экз.")
speciality = KeyboardButton("Специальность")
filters_mrk.add(subjects, city).add(speciality, dop_ex).add(profiles, back)


# количество предметов
count = ReplyKeyboardMarkup(resize_keyboard=True)
one_kb = KeyboardButton("один")
two_kb = KeyboardButton("два")
three_kb = KeyboardButton("три")
count.add(one_kb, two_kb, three_kb)