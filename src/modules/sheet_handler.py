from typing import Literal, Union
import pandas as pd
from pandas import Series
from io import StringIO


class InvalidFileType(Exception):
    pass


class SheetHandler:
    def __init__(self,
                 file: Union[str, bytes],
                 option: Literal[1, 2],
                 origin: str = "Origem",
                 destination: str = "Destino"):
        # self._combination: Dict[str, List] = {}
        # self._opt = {1: self._permutation, 2: self._compare}
        self._file = file
        self._origin = origin
        self._destination = destination

        # Defined on the file_check method
        self.dataframe = None
        self._file_check()
        self._columns_reader()
        # self._opt[option]()

    # def _permutation(self):
    #     """Method that create a dictionary with all the destinations to each origin. (No size limitation)."""
    #     for o in self.origin:
    #         self._combination[o] = []
    #         for d in self.destination:
    #             self._combination[o].append(d)
    #
    # def _compare(self):
    #     """Method to create the dictionary with origin and destination line by line from the dataframe."""
    #     if len(self.origin) == len(self.destination):
    #         for o, d in zip(self.origin, self.destination):
    #             if o in self._combination.keys() and d not in self._combination[o]:
    #                 self._combination[o].append(d)
    #             elif o not in self._combination.keys():
    #                 self._combination[o] = [d]
    #     else:
    #         raise TypeError("Option not allowed!\nDifferent number of origins and destinations.")

    def _process_dataframe(self) -> None:
        """Method to process the bytes and update the
        file atribute to the processed file."""
        # File Bytes
        processed_file = StringIO(str(self._file, 'utf-8'))
        self._file = processed_file

    def _file_check(self) -> None:
        """Method to open and read file."""
        if isinstance(self._file, bytes):
            self._process_dataframe()

        if self._file.endswith('.xlsx'):
            self.dataframe = pd.read_excel(self._file)

        elif self._file.endswith('.csv'):
            self.dataframe = pd.read_csv(self._file)

        else:
            raise InvalidFileType(
                'The program does not recognize the file type: '
                , self._file.split('.')[-1])

    def _columns_reader(self) -> None:
        """Read the columns that contain the origin cities and destinations cities"""
        if hasattr(self, 'dataframe') and isinstance(self.dataframe, pd.DataFrame):
            self._origin_col = self.dataframe[self._origin]
            self._destination_col = self.dataframe[self._destination]
        else:
            print("Could not read the dataframe.")

    # @property
    # def cities_combination(self):
    #     """Return the dictionary with the origins and destinations."""
    #     return self._combination

    @property
    def origin(self) -> Series:
        """Return the Origin dataframe column"""
        if self._origin_col is not None:
            return self._origin_col
        else:
            raise TypeError('The program could not return the origin column.')

    @property
    def destination(self) -> Series:
        """Return the destination dataframe column"""
        if self._destination_col is not None:
            return self._destination_col
        else:
            raise TypeError(
                'The program could not return the destination column.')

