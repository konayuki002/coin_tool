from coin_type import CoinType, Gengou, Price

TREAT_TBD_AS_RARE = True

class IssuedNumber():
  def __init__(self, price, dict):
    self.price = price
    self.dict = dict # None for TBD

  def issued_less_than(self, one_coin_type, other_coin_type):
    if self.dict[one_coin_type] == None:
      one_issued = 0 if TREAT_TBD_AS_RARE else float('inf')
    else:
      one_issued = self.dict[one_coin_type]

    if self.dict[other_coin_type] == None:
      other_issued = 0 if TREAT_TBD_AS_RARE else float('inf')
    else:
      other_issued = self.dict[other_coin_type]

    return one_coin_type < other_coin_type

issued_number_one = {
  CoinType.create_from_str_short("1h2"): 100,
  CoinType.create_from_str_short("1h1"): 90,
  CoinType.create_from_str_short("1h3"): 80
}

issued_number_five_handred = {
  CoinType.create_from_str_short("500r1new"): 100,
  CoinType.create_from_str_short("500r2"): 30,
}

issued_number = {
  Price.One: issued_number_one, 
  Price.FiveHandred: issued_number_five_handred
}
