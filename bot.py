from binance.exceptions import *
import yaml
from pyrogram import Client, filters
from binance_api import byeSell, price, balance, client

file = "config.yml"
with open(file) as file:
    auth = yaml.load(file, Loader=yaml.FullLoader)

bot = Client("my_bot", bot_token= auth['bot_token'], api_id=auth['api_id'],api_hash=auth['api_hash'])


def check_users(message) -> bool:
    if str(message.from_user.id) not in str(auth['users_id']):
        return False
    else:
        return True

@bot.on_message(filters.command(["trade", "t"]) & filters.private)
def trade(bot, message) -> str:
    if not check_users(message):
        return
    value  = message.text.lower()
    count_value  = len(message.command)
    command  = message.command

    if "buy" in value and count_value == 4:
        try:
            byeSell(str(str(command[2]+ "usdt")), float(command[3]), "buy")
            TEXT = "Successfully bought" + " " + str(command[3]) + "$" + " " + str(command[2]).upper()
            message.reply_text(TEXT)
        except BinanceAPIException as e:
            message.reply_text(f"Failed to bought! \n\n Error:  \n {e}")

    elif "sell" in value and count_value == 4:
        try:
            byeSell(str(str(command[2]+ "usdt")), float(command[3]), "sell")
            TEXT = "Successfully sold" + " " + str(command[3]) + "$" + " " + str(command[2]).upper()
            message.reply_text(TEXT)
        except BinanceAPIException as e:
            message.reply_text(f"Failed to sold! \n\n error: \n {e}")

    else:
        message.reply_text( "Not understand, Enter like [/trade {buy/sell} {coin} {amount in usd}")

@bot.on_message(filters.private & filters.command(["check", "c"]))
async def lastprice(bot, message) -> str:
    if not check_users(message):
        return

    value = message.text.lower()
    count_value = len(message.command)
    command  = message.command

    if "price" in value and count_value == 3 and str(command[2]) != " ":
        try:
            finaly = price(str(str(command[2]+ "usdt")))
            reply = str(command[2]).upper() + " " +  "price is" + " " + str(finaly)
            await message.reply_text(reply)
        except BinanceAPIException as e:
            await message.reply_text(text=f"Failed! \n \n error: \n {s}")

    elif "bal" in value and count_value == 3:
        try:
            text = balance(str(command[2]))
            await message.reply_text(text)
        except BinanceAPIException as e:
            await message.reply_text(text=f"Failed!\n \nerror: \n {e}")


    else:
        await message.reply_text("Look like you entered wrong command")
        await message.reply_text("Enter like [/c {price/bal} {coin}]")

@bot.on_message(filters.private & filters.command(["s", "status"]))
def status(bot, message) -> str:
    if not check_users(message):
        return
    message.reply_text("Bot is Ok!")
    message.reply_text("Pinging Binance")
    message.reply_text(f"Binance: {client.get_system_status()['msg']}")

@bot.on_message(filters.private & filters.command(["convert", "con"]))
def convert_price(bot, message):
    if not check_users(message):
        return
    comms = message.command
    coin1 = price(str(comms[2] + "USDT").upper())
    coin2 = price(str(comms[3] + "USDT").upper())
    conv = int(comms[1]) * float(coin1)  / float(coin2)


    if len(message.command) == 4:
        message.reply_text(f"{comms[1]} {comms[2].upper()} = {conv} {comms[3].upper()}")
    else:
        message.reply_text("You did something wrong")

@bot.on_message(filters.private & filters.command(["instant", "i"]))
def instant(bot, message):
# Instantly sell all amounts of a coin
    if not check_users(message):
        return

    comms = message.command
    all_ = client.get_asset_balance(comms[2])['free']
#    rm = 0.01 * (float(all_) / 100)
    if not len(comms) ==3:
        return

    try:
        if "sell" in comms[1]:
            byeSell(str(comms[2]) + "USDT", format(float(all_), (".4f")), "sell")
            message.reply_text("Sold")

    except BinanceAPIException as e:
        message.reply_text(e)


bot.run()
