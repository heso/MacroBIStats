from datetime import date, timedelta
from alchemy import StatDeals, StatBooking
import telebot
import os


def main(use_telegram: bool = True):
    today = date.today()
    yesterday = date.today() - timedelta(days=1)

    today = yesterday

    # всего продаж
    today_sells = StatDeals(today, today)
    # целевых заявок сегодня
    # today_target_leads = get_target_leads_count(today, today)
    # бесплатных броней сегодня
    booking_free = StatBooking(today, today, False)
    # платных броней сегодня
    booking_paid = StatBooking(today, today, True)

    booking_free_spaces = ' ' * (booking_free.max_len - len(str(booking_free.flat_count)))
    booking_paid_spaces = ' ' * (booking_paid.max_len - len(str(booking_paid.flat_count)))
    sells_spaces = ' ' * (today_sells.max_len - len(str(today_sells.flat_count)))

    msg = f'''Беспл. брони: {booking_free.flat_count} шт.{booking_free_spaces}\\ {booking_free.flat_price} млн.\n
              Плат. брони:  {booking_paid.flat_count} шт.{booking_paid_spaces}\\ {booking_paid.flat_price} млн.\n
              Договоры:     {today_sells.flat_count} шт.{sells_spaces}\\ {today_sells.flat_price} млн/'''

    if use_telegram:
        bot = telebot.TeleBot(os.environ.get('telegram_token'))
        bot.send_message(os.environ.get('chat_id'), msg, parse_mode='Markdown')
    else:
        print(msg)


if __name__ == '__main__':
    main(False)
