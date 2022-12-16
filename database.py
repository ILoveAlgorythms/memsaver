import pandas as pd
from config import TABLE


class database:
    def __init__(self):
        self.data = pd.read_csv(TABLE)

    def get(self, username, code):  # гет по юзеру и коду
        a = self.data[self.data['user'] == username][self.data['code'] == code]
        return a.id[0], a.type[0]

    def add(self, input):  # добавить по таплу
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
