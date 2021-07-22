# -*- coding: utf8 -*-


class Calendar:

    month = 0

    def __init__(self, month = 0):
        self.month = month

    def get_month(self):
        month_array = { 1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june', 7: 'july',
                        8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'}
        # month_array = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь', 7: 'Июль',
        # 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}
        return month_array[self.month]