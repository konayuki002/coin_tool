from enum import Enum, IntEnum, unique
from functools import total_ordering
from logging import error
import re

@unique
class Price(IntEnum):
  One = 1
  Five = 5
  Ten = 10
  Fifty = 50
  Handred = 100
  FiveHandred = 500

  def str(self):
    return str(self.value) + " Yen"

  def str_short(self):
    return str(self.value)

@unique
@total_ordering
class Gengou(Enum):
  Showa = 1
  Heisei = 2
  Reiwa = 3

  @classmethod
  def from_str_short(cls, string):
    if string == "s":
      return Gengou.Showa
    elif string == "h":
      return Gengou.Heisei
    elif string == "r":
      return Gengou.Reiwa
    else:
      raise RuntimeError("Unknown Gengou string: " + string)

  def str(self):
    if self == Gengou.Showa:
      return "Showa"
    elif self == Gengou.Heisei:
      return "Heisei"
    else:
      return "Reiwa"

  def str_short(self):
    if self == Gengou.Showa:
      return "s"
    elif self == Gengou.Heisei:
      return "h"
    else:
      return "r"

  def __eq__(self, other):
    if not isinstance(other, Gengou):
      return NotImplemented
    return self.value == other.value

  def __lt__(self, other):
    if not isinstance(other, Gengou):
      return NotImplemented
    return self.value < other.value

  def __hash__(self) -> int:
    return super().__hash__()

@total_ordering
class Year():
  def __init__(self, gengou, year_int):
    self.gengou = gengou
    self.year_int = year_int

  @classmethod
  def create_from_str_short(cls, string):
    m = re.match(r'([shr])(\d*)', string)
    gengou = Gengou.from_str_short(m.group(1))
    year_int = int(m.group(2))
    return Year(gengou, year_int)

  def str(self):
    return self.gengou.str() + " " + str(self.year_int)

  def str_short(self):
    return self.gengou.str_short() + str(self.year_int)

  def __eq__(self, other):
    if not isinstance(other, Year):
      return NotImplemented
    return (self.gengou, self.year_int) == (other.gengou, other.year_int)

  def __lt__(self, other):
    if not isinstance(other, Year):
      return NotImplemented
    return (self.gengou, self.year_int) < (other.gengou, other.year_int)

  def __hash__(self):
    return hash(self.gengou) + hash(self.year_int)

class CoinType:
  def __init__(self, price, year, isNew=None):
    self.price = price
    self.year = year
    if price == Price.FiveHandred and year == Year(Gengou.Reiwa, 1) and not isNew:
      raise RuntimeError("'isNew' is must specified for 500 Yen, Reiwa 1 coin")
    else:
      self.isNew = isNew

  @classmethod
  def create_from_str_short(cls, string):
    m = re.match(r'(\d*)([shr]\d*)(new|old)?', string)
    price = Price(int(m.group(1)))
    year = Year.create_from_str_short(m.group(2))
    if m.group(3) is None:
      return CoinType(price, year)
    elif m.group(3) == "new":
      return CoinType(price, year, True)
    else:
      return CoinType(price, year, False)

  def str(self):
    if not self.isNew:
      return self.price.str() + ", " + self.year.str()
    else:
      return self.price.str() + ", " + self.year.str() + " " + ("new" if self.isNew else "old")

  def str_short(self):
    if not self.isNew:
      return self.price.str_short() + self.year.str_short()
    else:
      return self.price.str_short() + self.year.str_short() + ("new" if self.isNew else "old")

  def __eq__(self, other):
    return (self.price, self.year, self.isNew) == (other.price, other.year, other.isNew)
  
  def __ne__(self, other):
    return not (self == other)

  def __hash__(self):
    return hash(self.price) + hash(self.year) + hash(self.isNew)

if __name__ == '__main__':
  print(CoinType(Price.One, Year(Gengou.Heisei, 2)).str())
  print(CoinType(Price.One, Year(Gengou.Heisei, 2)).str_short())
  print(CoinType(Price.FiveHandred, Year(Gengou.Reiwa, 2)).str_short())
  print(CoinType(Price.FiveHandred, Year(Gengou.Reiwa, 1,), "new").str_short())

  coin1 = CoinType(Price.One, Year(Gengou.Heisei, 2))
  coin2 = CoinType(Price.One, Year(Gengou.Heisei, 2))
  coin3 = CoinType(Price.One, Year(Gengou.Reiwa, 2))

  print(coin1 == coin2)
  print(coin2 != coin3)

  rarlity = {
    Price.One : {
      CoinType(Price.One, Year(Gengou.Heisei, 2)): 100,
      CoinType(Price.One, Year(Gengou.Heisei, 1)): 90,
      CoinType(Price.One, Year(Gengou.Heisei, 3)): 80
    }
  }

  save = {
    CoinType(Price.One, Year(Gengou.Heisei, 2)): 10,
    CoinType(Price.One, Year(Gengou.Heisei, 1)): 2,
    CoinType(Price.One, Year(Gengou.Heisei, 3)): 3
  }

  print(rarlity)
  print(CoinType.create_from_str_short("1h1").str_short())
  print(CoinType.create_from_str_short("50s49").str_short())
  print(CoinType.create_from_str_short("500r1new").str_short())
  # print(CoinType.create_from_str_short("500r1").str_short()) raise error
