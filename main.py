from datetime import date, timedelta
from alchemy import StatDeals, StatBooking, get_target_leads_count
from telebot import TeleBot
import os


def main(use_telegram: bool = True):
    today = date.today()
    # yesterday = date.today() - timedelta(days=2)

    leads_count = get_target_leads_count(today, today)
    today_sells = StatDeals(today, today)
    booking_free = StatBooking(today, today, False)
    booking_paid = StatBooking(today, today, True)

    msg = (f'{today}\n\n'
           f'`Лиды:         {leads_count} шт.\n\n'
           f'{booking_free.get_stats()}\n\n'
           f'{booking_paid.get_stats()}\n\n'
           f'{today_sells.get_stats()}`')
    if use_telegram:
        bot = TeleBot(os.environ.get('telegram_token'))
        bot.send_message(os.environ.get('chat_id'), msg, parse_mode='Markdown')
    else:
        print(msg)


if __name__ == '__main__':
    main(1==1)
