from pdb import runcall
from coin_type import CoinType
from issued import issued_number

class CoinCase:
  def  __init__(self, name, max_counts=None):
    self.name = name
    self.dict = {}
    self.max_counts = max_counts

  def append(self, coin_type, count=1):
    if count <= 0:
      raise RuntimeError("Number of coins to append should be more than zero")

    if self.max_counts is not None and (self.dict.get(coin_type) or 0) + count > self.max_counts:
        raise RuntimeError("Number of coins after append coin is more than maximum")

    if self.dict.get(coin_type) is None:
      self.dict[coin_type] = 0

    self.dict[coin_type] += count

  def remove(self, coin_type, count=1):
    if self.dict[coin_type] >= count:
      self.dict[coin_type] -= count
      if self.dict[coin_type] == 0:
        del self.dict[coin_type]
    else:
      raise RuntimeError("Number of coins to remove is more than that of ones in the coin case")

  def ls(self):
    print(self.name)
    if len(self.dict) == 0:
      print("    No coins")
    sum = 0
    sum_for_price = {}
    sorted_items = list(sorted(self.dict.items(), key=(lambda item: item[0].year), reverse=True))
    sorted_items = list(sorted(sorted_items, key=(lambda item: item[0].price), reverse=True))
    for coin_type, count in sorted_items:
      sum += count
      sum_for_price[coin_type.price] = (sum_for_price.get(coin_type.price) or 0) + count
      print(f'{coin_type.str_short():>12}: {count:>2}')
    print ("sum: ", sum)
    print ("sum for price", sum_for_price)

  def is_full_for_price(self, price):
    sum = 0
    for coin_type, count in self.dict.items():
      if coin_type.price == price:
        sum += count
    return sum == self.max_counts

  def find_most_common_for_price(self, price):
    if self.max_counts == 0:
      raise RuntimeError("No candidates for max_counts = 0 CoinCase")

    types = list(filter(lambda t: t.price == price, self.dict.keys()))

    if len(types) == 0:
      raise RuntimeError("No candidates for no coins for the price: " + price.str())

    return list(sorted(types, key=(lambda t: (issued_number[price][t]) or 0 )))[-1]

  def difference(self, other):
    union_keys = self.dict.keys() | other.dict.keys()
    result = {}
    for coin_type in union_keys:
      result[coin_type] = (self.dict.get(coin_type) or 0) - (other.dict.get(coin_type) or 0)
      if result.get(coin_type) == 0:
        del result[coin_type]

    return result

if __name__ == '__main__':
  coin_case = CoinCase({CoinType.create_from_str_short("1h1"):3
  , CoinType.create_from_str_short("500r1new"):10
  })

  coin_case.ls()

  coin_case.append(CoinType.create_from_str_short("500r1new"))

  coin_case.ls()

  coin_case.remove(CoinType.create_from_str_short("500r1new"))

  coin_case.ls()

  # coin_case.remove(CoinType.create_from_str_short("500r1new"), 11) // raise error

  coin_case.remove(CoinType.create_from_str_short("500r1new"), 10)

  coin_case.ls()
