from mimetypes import common_types
from coin_case import CoinCase
from coin_type import CoinType
import copy
from issued import issued_number

class CoinTool:
  def __init__(self, safe_size=50) -> None:
    self.wallet = CoinCase("wallet")
    self.safe = CoinCase("safe", safe_size)

  def add(self, string, count=1):
    split_string = string.split()
    for _string in split_string:
      coin_type = CoinType.create_from_str_short(_string)
      self.wallet.append(coin_type, count)

  def remove(self, string, count=1):
    split_string = string.split()
    for _string in split_string:
      coin_type = CoinType.create_from_str_short(_string)
      self.wallet.remove(coin_type, count)

  def ls(self):
    self.wallet.ls()
    self.safe.ls()

  def push(self, dry_run=False):
    if dry_run:
      wallet_copy = copy.deepcopy(self.wallet)
      safe_copy = copy.deepcopy(self.safe)

    new_wallet = CoinCase("new wallet")

    while len(self.wallet.dict) > 0:
      coin_type = list(self.wallet.dict.keys())[0]
      if self.safe.is_full_for_price(coin_type.price):
        most_common_type = self.safe.find_most_common_for_price(coin_type.price)
        if(issued_number[coin_type.price][coin_type] < issued_number[most_common_type.price][most_common_type]):
          self.safe.remove(most_common_type)
          new_wallet.append(most_common_type)
          self.wallet.remove(coin_type)
          self.safe.append(coin_type)
        else:
          self.wallet.remove(coin_type)
          new_wallet.append(coin_type)
      else:
        self.wallet.remove(coin_type)
        self.safe.append(coin_type)

    self.wallet = new_wallet
    self.wallet.name = "wallet"

    if dry_run:
      print("dry-run; if ls() after push:")
      self.ls()

      print("Number of coins moves to wallet")
      wallet_difference = self.wallet.difference(wallet_copy)
      for coin_type, diff in wallet_difference.items():
        print(f'{coin_type.str_short():>12}: {diff:>2}')

      print("Number of coins moves to safe")
      safe_difference = self.safe.difference(safe_copy)
      for coin_type, diff in safe_difference.items():
        print(f'{coin_type.str_short():>12}: {diff:>2}')

      self.wallet = wallet_copy
      self.safe = safe_copy

if __name__ == '__main__':
  coin_tool = CoinTool()

  coin_tool.add("1h1", 2)
  coin_tool.add("1h2", 1)
  coin_tool.add("500r1", 1)
  coin_tool.add("500r1 500r2")
  coin_tool.remove("1h1")
  coin_tool.ls()

  print("push")

  coin_tool.push(dry_run=True)

  coin_tool.ls()
