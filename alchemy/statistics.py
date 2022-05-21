__all__ = ['StatDeals', 'StatBooking']

from dataclasses import dataclass
from datetime import date, timedelta
from .callbacks import get_sells_stats, get_booking_stats
from typing import Union

categories = {'all': '',
              'flat': '- квартиры:   ',
              'house': '- дома:       ',
              'comm': '- земля:      ',
              'land': '- коммерция:  ',
              'other': '- всякое:     '}


@dataclass
class StatDeals:
    """ статистика по заключенным договорам """
    date_from: date
    date_to: date

    def __post_init__(self):
        self.all_count, self.all_price = get_sells_stats(self.date_from, self.date_to)[0]
        self.flat_count, self.flat_price = get_sells_stats(self.date_from, self.date_to, ['flat'])[0]
        self.house_count, self.house_price = get_sells_stats(self.date_from, self.date_to, ['house'])[0]
        self.comm_count, self.comm_price = get_sells_stats(self.date_from, self.date_to, ['comm'])[0]
        self.land_count, self.land_price = get_sells_stats(self.date_from, self.date_to, ['land'])[0]
        self.other_count, self.other_price = get_sells_stats(self.date_from, self.date_to, ['garage', 'storageroom'])[0]

    def get_stats(self):
        name_all = 'Договоры:     '
        return get_class_stats(self, name_all)


@dataclass
class StatBooking:
    """ статистика по платным и бесплатным броням """
    date_from: date
    date_to: date
    isBookingPaid: bool

    def __post_init__(self):
        self.all_count, self.all_price = get_booking_stats(self.date_from, self.date_to, self.isBookingPaid)[0]
        self.flat_count, self.flat_price = get_booking_stats(self.date_from, self.date_to, self.isBookingPaid, ['flat'])[0]
        self.house_count, self.house_price = get_booking_stats(self.date_from, self.date_to, self.isBookingPaid, ['house'])[0]
        self.comm_count, self.comm_price = get_booking_stats(self.date_from,  self.date_to, self.isBookingPaid, ['comm'])[0]
        self.land_count, self.land_price = get_booking_stats(self.date_from, self.date_to, self.isBookingPaid, ['land'])[0]
        self.other_count, self.other_price = get_booking_stats(self.date_from, self.date_to, self.isBookingPaid, ['garage', 'storageroom'])[0]

    def get_stats(self):
        if self.isBookingPaid:
            name_all = 'Плат. брони:  '
        else:
            name_all = 'Беспл. брони: '
        return get_class_stats(self, name_all)


def get_class_stats(cls: Union[StatDeals, StatBooking], name_all: str) -> str:
    return name_all + '\n'.join(filter(None, [get_stats_for_category(cls, key) for key in categories]))


def get_stats_for_category(cls: Union[StatDeals, StatBooking], category: str) -> str:
    category_count = getattr(cls, f'{category}_count')
    category_price = getattr(cls, f'{category}_price')
    free_spaces = ' ' * (max_len(cls) - len(str(category_count)))
    if category_count != 0 or category == 'all':
        return f'{categories[category]}{category_count} шт.{free_spaces}\\ {category_price} млн.'


def max_len(cls: Union[StatDeals, StatBooking]) -> int:
    result = max(len(str(cls.all_count)),
                 len(str(cls.flat_count)),
                 len(str(cls.house_count)),
                 len(str(cls.comm_count)),
                 len(str(cls.land_count)),
                 len(str(cls.other_count)))
    return result


def main():
    pass


if __name__ == '__main__':
    pass

