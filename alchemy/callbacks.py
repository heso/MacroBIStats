__all__ = ['get_sells_stats', 'get_booking_stats', 'get_target_leads_count']

from .models import Deals, Leads, TypesTranslations, get_session
from datetime import date
from sqlalchemy import func
from sqlalchemy import and_, or_


def get_sells_stats(date_from: date = date(2000, 1, 1),
                    date_to: date = date.today(),
                    category: list = None):
    if not category:
        category = get_all_categories()

    with get_session().begin() as session:
        result = session.query(func.count(Deals.id),
                             func.round(func.coalesce(func.sum(Deals.summ), 0) / 10 ** 6, 1)). \
                       filter(Deals.agreement_date >= date_from,
                              Deals.agreement_date <= date_to,
                              Deals.category.in_(category))
    return result


def get_target_leads_count(date_from: date = date(2000, 1, 1),
                           date_to: date = date.today(),
                           category: list = None):
    if not category:
        category = get_all_categories()
    with get_session().begin() as session:
        result = session.query(Leads). \
                       filter(Leads.date_added >= date_from,
                              Leads.date_added <= date_to,
                              Leads.status.not_in(['0', '3', '5']),
                              Leads.category.in_(category)).count()
    return result


def get_booking_stats(date_from: date = date(2000, 1, 1),
                      date_to: date = date.today(),
                      booking_paid: bool = True,
                      category: list = None):

    if not category:
        category = get_all_categories()

    conditions = [Deals.status_modified_date.between(date_from, date_to),
                  Deals.category.in_(category)]

    if booking_paid:
        conditions.append(or_(and_(Deals.status == 105,
                                   Deals.is_payed_reserve == 1),
                              Deals.status == 110))
    else:
        conditions.append(and_(Deals.status == 105,
                               Deals.is_payed_reserve == 0))

    with get_session().begin() as session:
        result = session.query(func.count(Deals.id),
                               func.round(func.coalesce(func.sum(Deals.summ), 0) / 10 ** 6, 1)). \
                       filter(*conditions)
    return result


def get_all_categories():
    with get_session().begin() as session:
        list_category = session.query(TypesTranslations.type_eng).all()
    return [category[0] for category in list_category]


if __name__ == '__main__':
    pass
