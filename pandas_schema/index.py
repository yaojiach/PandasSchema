from pandas_schema.errors import PanSchIndexError
from dataclasses import dataclass
from typing import Union
import numpy
import pandas
from enum import Enum

IndexValue = Union[numpy.string_, numpy.int_, str, int]
"""
A pandas index can either be an integer or string, or an array of either. This typing is a bit sketchy because really
a lot of things are accepted here
"""


class IndexType(Enum):
    POSITION = 0
    LABEL = 1


class PandasIndexer:
    """
    An index into a particular axis of a DataFrame. Attempts to recreate the behaviour of `df.ix[some_index]`
    """

    # valid_types = {'position', 'label'}
    index: IndexValue
    """
    The index to use, either an integer for position-based indexing, or a string for label-based indexing
    """
    type: IndexType
    """
    The type of indexing to use, either 'position' or 'label'
    """

    axis: int
    """
    The axis for the indexer
    """

    def __init__(self, index: IndexValue, typ: IndexType = None, axis: int = 1):
        self.index = index
        self.axis = axis

        if typ is not None:
            # If the type is provided, validate it
            if typ not in self.valid_types:
                raise PanSchIndexError('The index type was not one of {}'.format(' or '.join(self.valid_types)))
            else:
                self.type = typ
        else:
            # If the type isn't provided, guess it based on the datatype of the index
            if numpy.issubdtype(type(index), numpy.character):
                self.type = IndexType.LABEL
            elif numpy.issubdtype(type(index), numpy.int_):
                self.type = IndexType.POSITION
            else:
                raise PanSchIndexError('The index value was not either an integer or string, or an array of either of '
                                       'these')

    def __call__(self, df: pandas.DataFrame):
        """
        Apply this index
        :param df: The DataFrame to index
        :param axis: The axis to index along. axis=0 will select a row, and axis=1 will select a column
        """
        if self.type == IndexType.LABEL:
            return df.loc(axis=self.axis)[self.index]
        elif self.type == IndexType.POSITION:
            return df.iloc(axis=self.axis)[self.index]


class RowIndexer(PandasIndexer):
    def __init__(self, index: IndexValue, typ: IndexType = None):
        super().__init__(index=index, typ=typ, axis=0)


class ColumnIndexer(PandasIndexer):
    def __init__(self, index: IndexValue, typ: IndexType = None):
        super().__init__(index=index, typ=typ, axis=1)
