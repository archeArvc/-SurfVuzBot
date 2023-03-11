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

profiles_data = CallbackData("prof", "act")

ok_data = CallbackData("mesa", "type", "status")
ok_mrk = InlineKeyboardMarkup(row_width=1)
ok_mrk.add(InlineKeyboardButton("Хорошо", callback_data=ok_data.new(type = "ok", status = 0)))