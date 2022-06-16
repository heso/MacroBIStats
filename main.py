from datetime import date, timedelta, datetime as dt
from alchemy import StatDeals, StatBooking, get_target_leads_count
import telebot
import os
from telebot import types
import re

chat_id = os.environ.get('chat_id')
token = os.environ.get('telegram_token')
bot = telebot.TeleBot(token)
regexp_pattern = r'(\d{2}\.\d{2}\.\d{4})(\s*,\s*)(\d{2}\.\d{2}\.\d{4})'


markup = types.ReplyKeyboardMarkup(row_width=3)
btn_stat_today = types.KeyboardButton('статистика за сегодня')
btn_stat_yesterday = types.KeyboardButton('статистика за вчера')
btn_stat_period = types.KeyboardButton('статистика за период')

markup.add(btn_stat_today)
markup.add(btn_stat_yesterday)
markup.add(btn_stat_period)

# bot.send_message(chat_id, "статистика", reply_markup=markup)


def get_statistics(date_from, date_to):
    leads_count = get_target_leads_count(date_from, date_to)
    today_sells = StatDeals(date_from, date_to)
    booking_free = StatBooking(date_from, date_to, False)
    booking_paid = StatBooking(date_from, date_to, True)

    if date_from == date_to:
        interval = date_from.strftime('%d.%m.%Y')
    else:
        interval = f'`Период с` {date_from.strftime("%d.%m.%Y")} `по` {date_to.strftime("%d.%m.%Y")}'

    return (f'{interval}\n\n'
            f'`Лиды:         {leads_count} шт.\n\n'
            f'{booking_free.get_stats()}\n\n'
            f'{booking_paid.get_stats()}\n\n'
            f'{today_sells.get_stats()}`')


def test_statistics(message):
    return message.text in ['статистика за сегодня',
                            'статистика за вчера',
                            'статистика за период']


@bot.message_handler(func=test_statistics)
def send_statistics(message):
    cid = str(message.chat.id)
    if cid == chat_id:
        match message.text:
            case 'статистика за сегодня':
                date_stat = date.today()
                text = get_statistics(date_stat, date_stat)
            case 'статистика за вчера':
                date_stat = date.today() - timedelta(days=1)
                text = get_statistics(date_stat, date_stat)
            case 'статистика за период':
                text = '`Введите через запятую две даты в формате   дд.мм.гггг\nНапример:`\n12.09.2021, 02.10.2022'
        bot.send_message(chat_id, text, parse_mode='Markdown')


@bot.message_handler(regexp=regexp_pattern)
def send_statistics(message):
    cid = str(message.chat.id)
    if cid == chat_id:
        date_from = re.search(regexp_pattern, message.text).group(1)
        date_to = re.search(regexp_pattern, message.text).group(3)
        text = get_statistics(dt.strptime(date_from, '%d.%m.%Y').date(), dt.strptime(date_to, '%d.%m.%Y').date())

        bot.send_message(chat_id, text, parse_mode='Markdown')


bot.infinity_polling(timeout=10, long_polling_timeout=5)
