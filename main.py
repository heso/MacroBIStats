from datetime import date, timedelta
from alchemy import get_target_leads_count, get_sells_count, get_booking_price_and_count


def get_today():
    return date.today()


def get_yesterday():
    return date.today() - timedelta(days=1)


def main():
    # всего продаж
    total_sells = get_sells_count()
    # продажи вчера
    yesterday_sells = get_sells_count(get_yesterday(), get_yesterday())
    # продажи сегодня
    today_sells = get_sells_count(get_today(), get_today())

    # целевых заявок вчера
    yesterday_target_leads = get_target_leads_count(get_yesterday(), get_yesterday())
    # целевых заявок сегодня
    today_target_leads = get_target_leads_count(get_today(), get_today())

    # бесплатных броней вчера
    yesterday_booking_free_count = get_booking_price_and_count(get_yesterday(), get_yesterday(), True)
    # платных броней вчера
    yesterday_booking_paid_count = get_booking_price_and_count(get_yesterday(), get_yesterday(), False)

    # бесплатных броней сегодня
    today_booking_free_count = get_booking_price_and_count(get_today(), get_today(), True)
    # платных броней сегодня
    today_booking_paid_count = get_booking_price_and_count(get_today(), get_today(), False)

    msg = (
        f'всего продаж - {total_sells}\n'
        f'продаж вчера - {yesterday_sells}\n'
        f'продаж сегодня - {today_sells}\n'
        f'целевых заявок вчера - {yesterday_target_leads}\n'
        f'целевых заявок сегодня - {today_target_leads}\n'
        f'бесплатных броней сегодня: кол-во - {today_booking_free_count[0][0]}, сумма - {today_booking_free_count[0][1]}\n'
        f'бесплатных броней вчера: кол-во - {yesterday_booking_free_count[0][0]}, сумма - {yesterday_booking_free_count[0][1]}\n'
        f'платных броней сегодня: кол-во - {today_booking_paid_count[0][0]}, сумма - {today_booking_paid_count[0][1]}\n'
        f'платных броней вчера: кол-во - {yesterday_booking_paid_count[0][0]}, сумма - {yesterday_booking_paid_count[0][1]}\n'
    )

    print (msg)
    # telegram = get_notifier('telegram')
    # telegram.notify(message=msg, token=os.environ.get('telegram_token'), chat_id=os.environ.get('chat_id'))

    # bot = telebot.TeleBot(os.environ.get('telegram_token'))
    # bot.send_message(os.environ.get('chat_id'), msg)


if __name__ == '__main__':
    main()