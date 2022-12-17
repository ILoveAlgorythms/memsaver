import pandas as pd
from config import TABLE


class database:
    def __init__(self):
        self.data = pd.read_csv(TABLE)

    def get(self, username, code):  # гет по юзеру и коду
        a = self.data[self.data['user'] == username][self.data['code'] == code]
        return a.id.iloc[0], a.type.iloc[0]  # id мема, тип

    def add(self, user, code, id, type):
        """
         Добавляет мем

        @param user: username сохраняемого челоека
        @param code: кодовое слово
        @param id: id мема
        @param type: type мема
        """
        input = (user,  code,  id,  type)
        self.data.loc[len(self.data)] = input
        with open(TABLE, 'a') as file:
            for i in input[:-1]:
                file.write(i + ',')
            file.write(input[-1] + ',')

    def clear(self, user, code=''):
        self.data.drop(self.data[
                           (self.data['user'] == user) &
                           ((self.data['code'] == code) | (len(code) == 0))
                           ].index, inplace=True)
        self.data.to_csv(TABLE, index=False)

    def replace(self, user, code, id, type):
        """
        Заменяет мем у кодового слова

        @param user: username сохраняемого челоека
        @param code: кодовое слово, по которому хотим заменить
        @param id: id мема
        @param type: type мема
        """