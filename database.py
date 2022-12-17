import pandas as pd
from config import TABLE


class database:
    def __init__(self):
        self.data = pd.read_csv(TABLE)

    def get(self, username, code):
        """
        Получить мем по кодовому слову

        @param user: username пользвателя
        @param code: кодовое слово

        @returns: tupple (content_id, content_type), None если не существует
        """
        a = self.data[(self.data['user'] == username) & (self.data['code'] == code)]
        if a.shape[0]:
            return a.id.iloc[0], a.type.iloc[0]
        return None, None

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
            file.write(input[-1] + '\n')

    def clear(self, user, code=''):
        """
        Удаляет мем по кодовому слову. Если кодового слова нет, удаляет все мемы пользователя

        @param user: username пользователя
        @param code: кодовое слово, по которому происходит удаление. Если пустая строка, удаля.тся все мемы пользователя
        """
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
        self.data.loc[(self.data.user == user) & (self.data.code == code), 'id'] = id
        self.data.loc[(self.data.user == user) & (self.data.code == code), 'type'] = type
        self.data.to_csv(TABLE, index=False)