__all__ = ['StatDeals', 'StatBooking']

from dataclasses import dataclass
from datetime import date, timedelta
from .callbacks import get_sells_stats, get_booking_stats


@dataclass
class StatDeals:
    date_from: date
    date_to: date

    def __post_init__(self):
        self.flat_count, self.flat_price = get_sells_stats(self.date_from, self.date_to, ['flat'])[0]
        self.house_count, self.house_price = get_sells_stats(self.date_from, self.date_to, ['house'])[0]
        self.comm_count, self.comm_price = get_sells_stats(self.date_from, self.date_to, ['comm'])[0]
        self.land_count, self.land_price = get_sells_stats(self.date_from, self.date_to, ['land'])[0]
        self.other_count, self.other_price = get_sells_stats(self.date_from, self.date_to, ['garage', 'storageroom'])[0]

    @property
    def max_len(self):
        result = max(len(str(self.flat_count)),
                     len(str(self.house_count)),
                     len(str(self.comm_count)),
                     len(str(self.land_count)),
                     len(str(self.other_count)))
        return result


@dataclass
class StatBooking:
    date_from: date
    date_to: date
    isBookingPaid: bool

    def __post_init__(self):
        self.flat_count, self.flat_price = get_booking_stats(self.date_from, self.date_to, self.isBookingPaid, ['flat'])[0]
        self.house_count, self.house_price = get_booking_stats(self.date_from, self.date_to, self.isBookingPaid, ['house'])[0]
        self.comm_count, self.comm_price = get_booking_stats(self.date_from,  self.date_to, self.isBookingPaid, ['comm'])[0]
        self.land_count, self.land_price = get_booking_stats(self.date_from, self.date_to, self.isBookingPaid, ['land'])[0]
        self.other_count, self.other_price = get_booking_stats(self.date_from, self.date_to, self.isBookingPaid, ['garage', 'storageroom'])[0]

    @property
    def max_len(self):
        result = max(len(str(self.flat_count)),
                     len(str(self.house_count)),
                     len(str(self.comm_count)),
                     len(str(self.land_count)),
                     len(str(self.other_count)))
        return result


def main():
    yesterday = date.today() - timedelta(days=1)
    booking_paid_statistics = StatBooking(yesterday, yesterday, False)

    print(booking_paid_statistics.max_len)


if __name__ == '__main__':
    pass

