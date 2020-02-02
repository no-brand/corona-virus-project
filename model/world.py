from dao.sheets import *
import pandas as pd


class WorldCase:
    def __init__(self):
        self.spread_sheet_id = '1yZv9w9zRKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w'
        self.data = SheetService().get(spread_sheet_id=self.spread_sheet_id)
        assert self.data is not None
        assert isinstance(self.data, list)
        self.columns = self.data[0]
        self.__data = self.data[1:]
        self.__dataframe = pd.DataFrame(self.__data,
                                        index=None,
                                        columns=self.columns)
        self.__type_cast()

    def __type_cast(self):
        self.__dataframe['Confirmed'] = pd.to_numeric(self.__dataframe['Confirmed']).fillna(0).astype('int64')
        self.__dataframe['Deaths'] = pd.to_numeric(self.__dataframe['Deaths']).fillna(0).astype('int64')
        self.__dataframe['Recovered'] = pd.to_numeric(self.__dataframe['Recovered']).fillna(0).astype('int64')

    @property
    def dataframe(self):
        return self.__dataframe
