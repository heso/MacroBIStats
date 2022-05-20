__all__ = ['get_sells_stats', 'get_booking_stats', 'get_target_leads_count']

from .models import Deals, Leads, TypesTranslations, get_session
from datetime import date
from sqlalchemy import func


def get_sells_stats(date_from: date = date(2000, 1, 1),
                    date_to: date = date.today(),
                    category: list = None):
    with get_session().begin() as session:
        if not category:
            category = get_all_categories()
        return session.query(func.count(Deals.id),
                             func.round(func.coalesce(func.sum(Deals.summ), 0)/10**6, 1)). \
                       filter(Deals.agreement_date >= date_from,
                              Deals.agreement_date <= date_to,
                              Deals.category.in_(category))


def get_target_leads_count(date_from: date = date(2000, 1, 1),
                           date_to: date = date.today(),
                           category: list = None):
    if not category:
        category = get_all_categories()
    with get_session().begin() as session:
        return session.query(Leads). \
               filter(Leads.date_added >= date_from,
                      Leads.date_added <= date_to,
                      Leads.status.not_in(['0', '3', '5']),
                      Leads.category.in_(category)).count()


def get_booking_stats(date_from: date = date(2000, 1, 1),
                            date_to: date = date.today(),
                            booking_paid: bool = True,
                            category: list = None):
    if not category:
        category = get_all_categories()
    with get_session().begin() as session:
        return session.query(func.count(Deals.id),
                             func.round(func.coalesce(func.sum(Deals.summ), 0)/10**6, 1)). \
               filter(Deals.status_modified_date >= date_from,
                      Deals.status_modified_date <= date_to,
                      Deals.status == 105,
                      Deals.is_payed_reserve == int(booking_paid),
                      Deals.category.in_(category)).all()


def get_all_categories():
    with get_session().begin() as session:
        list_category = session.query(TypesTranslations.type_eng).all()
    return [category[0] for category in list_category]


if __name__ == '__main__':
    pass