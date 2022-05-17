from datetime import date, timedelta
from alchemy import get_target_leads_count, get_sells_price_and_count, get_booking_price_and_count
import telebot
import os


def main():
    today = date.today()
    yesterday = date.today() - timedelta(days=1)

    # всего продаж
    today_sells = get_sells_price_and_count(today, today)
    # целевых заявок вчера
    yesterday_target_leads = get_target_leads_count(yesterday, yesterday)
    # целевых заявок сегодня
    today_target_leads = get_target_leads_count(today, today)
    # бесплатных броней сегодня
    today_booking_free_count = get_booking_price_and_count(today, today, booking_paid=False)
    # платных броней сегодня
    today_booking_paid_count = get_booking_price_and_count(today, today, booking_paid=True)

    max_len = max(len(str(today_booking_free_count[0][0])),
                  len(str(today_sells[0][0])),
                  len(str(today_booking_paid_count[0][0])))

    booking_free_spaces = ' ' * (max_len - len(str(today_booking_free_count[0][0])))
    booking_paid_spaces = ' ' * (max_len - len(str(today_booking_paid_count[0][0])))
    sells_spaces = ' ' * (max_len - len(str(today_sells[0][0])))


    msg = (f'{today}\n\n`'
        f'Лиды:         {today_target_leads} шт.\n'
        f'Беспл. брони: {today_booking_free_count[0][0]} шт.{booking_free_spaces}\\ {round(today_booking_free_count[0][1]/10**6,1)} млн.\n'
        f'Плат. брони:  {today_booking_paid_count[0][0]} шт.{booking_paid_spaces}\\ {round(today_booking_paid_count[0][1]/10**6,1)} млн.\n\n'
        f'Договоры:     {today_sells[0][0]} шт.{sells_spaces}\\ {round(today_sells[0][1]/10**6,1)} млн.\n`'
    )

    bot = telebot.TeleBot(os.environ.get('telegram_token'))
    bot.send_message(os.environ.get('chat_id'),  msg , parse_mode='Markdown')


if __name__ == '__main__':
    main()