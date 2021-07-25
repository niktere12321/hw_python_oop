import datetime as dt
"""Импортировали библиотеку"""


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = dt.date.today()
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = str(date)
            date_format = '%d.%m.%Y'
            moment = dt.datetime.strptime(self.date, date_format)
            self.date = moment.date()


class Calculator:
    def __init__(self, limit: float):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stat = 0
        today = dt.date.today()
        for record in self.records:
            if record.date == today:
                today_stat += record.amount
        return today_stat

    def get_week_stats(self):
        week_stat = 0
        today = dt.date.today()
        w = dt.timedelta(days=7)
        week = today - w
        for record in self.records:
            if record.date >= week and record.date <= today:
                week_stat += record.amount
        return week_stat


class CashCalculator(Calculator):
    EURO_RATE = float(70)
    USD_RATE = float(60)
    RUB_RATE = 1

    def get_today_cash_remained(self, currency):
        cash = (float(self.limit) - float(self.get_today_stats()))
        currencies = {'usd': ('USD', CashCalculator.USD_RATE),
                      'eur': ('Euro', CashCalculator.EURO_RATE),
                      'rub': ('руб', CashCalculator.RUB_RATE)}
        name, rate = currencies[currency]
        cash = round(cash / rate, 2)
        if cash > 0:
            return (f'На сегодня осталось {cash} {name}')
        if cash == 0:
            return ('Денег нет, держись')
        if cash <= 0:
            cash1 = -cash
            return (f'Денег нет, держись: твой долг - {cash1} {name}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calr_today = self.get_today_stats()
        calor_lim = self.limit
        eda = calor_lim - calr_today
        if calr_today < calor_lim:
            return(f'Сегодня можно съесть что-нибудь ещё, '
                   f'но с общей калорийностью не более {eda} '
                   f'кКал')
        else:
            return('Хватит есть!')


cash_calculator = CashCalculator(1000)


cash_calculator.add_record(Record(amount=145, comment='кофе'))
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))
print(cash_calculator.get_today_cash_remained('rub'))
print(cash_calculator.get_today_stats())
print(cash_calculator.get_week_stats())
print(cash_calculator.get_today_cash_remained('eur'))
print(cash_calculator.get_today_cash_remained('usd'))
calories = CaloriesCalculator(3000)
calories.add_record(Record(100, 'роллы'))
calories.add_record(Record(10, 'пицца', '21.09.2021'))
calories.add_record(Record(300, 'Гамубургер', '22.09.2021'))
print(calories.get_today_stats())
print(calories.get_week_stats())
print(calories.get_calories_remained())
