COIN-NEW-GET = 💰 Please send the coin name from the Binance platform (e.g., Solana = SOL, Bitcoin = BTC):
# 🔧 Set Coin difference
# ⏳ Set Coin check time
COIN-NEW-FIND_FAIL = ❌ The algorithm could not recognize the coin, please try again:
COIN-NEW-FIND_SUCCESS = ✅ Found the coin <b>{$coin_label}</b> at a unit price of <b>{$price}$</b>
COIN-NEW-FAIL = ❌ Failed to add coin <b>{$coin_label}</b> to the watchlist
COIN-NEW-SUCCESS = 🎉 Coin <b>{$coin_label}</b> has been successfully added to the watchlist

COIN-DELETE = 🗑 Delete coin
COIN-DELETE-CONFIRM = ⚠️ Please confirm deletion of <b>{$coin}</b>
COIN-DELETE-FAIL = ❌ Failed to delete coin <b>{$coin}</b>
COIN-DELETE-SUCCESS = ✅ <b>{$coin}</b> has been successfully deleted

COIN-DIFFERENCE = 📉 Change price difference
COIN-DIFFERENCE-SET = 🔢 Set the price difference for <b>{$coin}</b> relative to the value of <b>{$price}$</b> (from 0.01 to 1000) or as a percentage (1% - 100%) with a '%' sign at the end:
COIN-DIFFERENCE-VALUE_ERROR = ⚠️ The format must be a number from 0.01 to 1000 or 1% - 100% with a '%' sign; please try again:
COIN-DIFFERENCE-FAIL = ❌ Failed to set a new difference for <b>{$coin}</b>
COIN-DIFFERENCE-SUCCESS = ✅ The difference of <b>{$difference} $ = {$percent}%</b> relative to the value of <b>{$price}$</b> has been set for <b>{$coin}</b>

COIN-CHECK_TIME-SET = ⏰ Set the price check interval (from 1 to 180 minutes):
COIN-CHECK_TIME-VALUE_ERROR = ⚠️ The format must be a number from 1 to 180; please try again:
COIN-CHECK_TIME-FAIL = ❌ Failed to set the price check interval
COIN-CHECK_TIME-SUCCESS = ✅ Price check interval of <b>{$check_time} minutes</b> has been successfully set

COIN-MY_COINS = 💎 Your coins
COIN-NOT_EXIST = ⚠️ The coin no longer exists in your list
COIN-DETAIL = 📊 <b>{$coin_label}</b> #{$id}
    ---------------------------------------
    🆔 coin: <b>{$coinname}</b>
    💲 Last price: <b>{$last_value}$</b>
    📉 Price difference: <b>{$difference} $</b>
