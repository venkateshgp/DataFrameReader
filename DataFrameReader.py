class DataFrameReader:
  def __init__(self, df):
    self._df = df
    self._row = None
    self._columns = df.columns.tolist()
    self.reset()
    self.row_index = 0

  def __getattr__(self, key):
    return self.__getitem__(key)

  def read(self) -> bool:
    self._row = next(self._iterator, None)
    self.row_index += 1
    return self._row is not None

  def columns(self):
    return self._columns

  def reset(self) -> None:
    self._iterator = self._df.itertuples()

  def get_index(self):
    return self._row[0]

  def index(self):
    return self._row[0]

  def to_dict(self, columns: List[str] = None):
    return self.row(columns=columns)

  def tolist(self, cols) -> List[object]:
    return [self.__getitem__(c) for c in cols]

  def row(self, columns: List[str] = None) -> Dict[str, object]:
    cols = set(self._columns if columns is None else columns)
    return {c : self.__getitem__(c) for c in self._columns if c in cols}

  def __getitem__(self, key) -> object:
    # the df index of the row is at index 0
    try:
        if type(key) is list:
            ix = [self._columns.index(key) + 1 for k in key]
        else:
            ix = self._columns.index(key) + 1
        return self._row[ix]
    except BaseException as e:
        return None

  def __next__(self) -> 'DataFrameReader':
    if self.read():
        return self
    else:
        raise StopIteration

  def __iter__(self) -> 'DataFrameReader':
    return self