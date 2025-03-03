COIN-NEW-GET = 💰 Надішліть назву монети з платформи Binance Solana = SOL, Bitcoin = BTC:
# 🔧 Set Coin difference
# ⏳ Set Coin check time
COIN-NEW-FIND_FAIL = ❌ Алгоритм не зміг розпізнати монету, спробуйте ще раз:
COIN-NEW-FIND_SUCCESS = ✅ Знайшли монету <b>{$coin_label}</b> за одиницю <b>{$price}$</b>
COIN-NEW-FAIL = ❌ Не вийшло додати монету <b>{$coin_label}</b> до трек-листа
COIN-NEW-SUCCESS = 🎉 Монета <b>{$coin_label}</b> успішно додана до трек-листа

COIN-DELETE = 🗑 Видалити монету
COIN-DELETE-CONFIRM = ⚠️ Підтвердіть видалення <b>{$coin}</b>
COIN-DELETE-FAIL = ❌ Не вийшло видалити монету <b>{$coin}</b>
COIN-DELETE-SUCCESS = ✅ <b>{$coin}</b> успішно видалено

COIN-DIFFERENCE = 📉 Змінити різницю ціни
COIN-DIFFERENCE-SET = 🔢 Встановіть різницю ціни для <b>{$coin}</b> від вартості в <b>{$price}$</b> (від 0.01 до 1000) або в процентному співвідношенні (1% - 100%) із знаком % в кінці:
COIN-DIFFERENCE-VALUE_ERROR = ⚠️ Формат має бути числом від 0.01 до 1000 або 1% - 100% із знаком %, спробуйте ще раз:
COIN-DIFFERENCE-FAIL = ❌ Не вийшло встановити нову різницю для <b>{$coin}</b>
COIN-DIFFERENCE-SUCCESS = ✅ Різницю в <b>{$difference} $ = {$percent}%</b> від вартості в <b>{$price}$</b> встановлено для <b>{$coin}</b>

COIN-CHECK_TIME-SET = ⏰ Встановіть час перевірки ціни (від 1 до 180 хвилин):
COIN-CHECK_TIME-VALUE_ERROR = ⚠️ Формат має бути числом від 1 до 180, спробуйте ще раз:
COIN-CHECK_TIME-FAIL = ❌ Не вийшло встановити час перевірки
COIN-CHECK_TIME-SUCCESS = ✅ Час перевірки <b>{$check_time} хвилин</b> успішно встановлено

COIN-MY_COINS = 💎 Ваші монети
COIN-NOT_EXIST = ⚠️ Монети вже не існує у вашому списку
COIN-DETAIL = 📊 <b>{$coin_label}</b> #{$id}
    ---------------------------------------
    🆔 coin: <b>{$coinname}</b>
    💲 Остання ціна: <b>{$last_value}$</b>
    📉 Різниця ціни: <b>{$difference} $</b>
