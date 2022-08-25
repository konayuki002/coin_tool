from coin_tool import CoinTool

coin_tool = CoinTool()

# initial commit 2022-08-25 (sample)
coin_tool.add("1h1", 2)
coin_tool.add("1h2", 1)

coin_tool.push(dry_run=True)

coin_tool.push()

# list coins
coin_tool.ls()
