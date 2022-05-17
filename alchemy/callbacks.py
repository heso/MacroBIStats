__all__ = ["get_sells_count", "get_booking_price_and_count", "get_target_leads_count"]

from .models import Deals, Leads, get_session
from datetime import date
from sqlalchemy import func


def get_sells_count(date_from: date = date(2000, 1, 1),
                    date_to: date = date.today()):
    with get_session().begin() as session:
        return session.query(Deals).filter(Deals.agreement_date >= date_from,
                                           Deals.agreement_date <= date_to).count()


def get_target_leads_count(date_from: date = date(2000, 1, 1),
                           date_to: date = date.today()):
    with get_session().begin() as session:
        return session.query(Leads). \
               filter(Leads.date_added >= date_from,
                      Leads.date_added <= date_to,
                      Leads.status != '0',
                      Leads.status != '3',
                      Leads.status != '5').count()


def get_booking_price_and_count(date_from: date = date(2000, 1, 1),
                            date_to: date = date.today(),
                            booking_free: bool = True):

    with get_session().begin() as session:
        return session.query(func.count(Deals.id),
                             func.coalesce(func.sum(Deals.summ), 0)). \
               filter(Deals.status_modified_date >= date_from,
                      Deals.status_modified_date <= date_to,
                      Deals.status == 105,
                      Deals.is_payed_reserve == int(booking_free)).all()


if __name__ == '__main__':
    pass