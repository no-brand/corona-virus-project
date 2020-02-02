from dao.sheets import *
import pandas as pd


class KoreanTrail:
    def __init__(self):
        self.spread_sheet_id = '1xJ-VxfKWByj4HyGQjNWyvFgEopbIQSwhPBvzWUFHnko'
        self.sheet_range = 'korea'
        self.data = SheetService().get(spread_sheet_id=self.spread_sheet_id,
                                       doc_range=self.sheet_range)
        assert self.data is not None
        assert isinstance(self.data, list)
        self.columns = self.data[0]
        self.__data = self.data[1:]
        self.__dataframe = pd.DataFrame(self.__data,
                                        index=None,
                                        columns=self.columns)
        self.__type_cast()

    def __type_cast(self):
        self.__dataframe = self.__dataframe.astype({
            'id': 'int32', 'age': 'int32',
            'contact': 'int64', 'trace': 'int32',
            'latitude': 'float64', 'longitude': 'float64'
        })

    @property
    def dataframe(self):
        return self.__dataframe
