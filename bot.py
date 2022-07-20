from binance.exceptions import *
import yaml
from pyrogram import Client, filters
from binance_api import main, price, balance

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
            main(str(str(command[2]+ "usdt")), float(command[3]), "buy")
            TEXT = "Successfully bought" + " " + str(command[3]) + "$" + " " + str(command[2]).upper()
            message.reply_text(TEXT)
        except BinanceAPIException as e:
            message.reply_text(f"Failed to bought! \n\n Error:  \n {e}")

    elif "sell" in value and count_value == 4:
        try:
            main(str(str(command[2]+ "usdt")), float(command[3]), "sell")
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
            await message.reply_text(e)
            await message.reply_text(text=f"Failed!\n \nerror: \n {e}")


    else:
        await message.reply_text("Look like you entered wrong command")
        await message.reply_text("Enter like [/c {price/bal} {coin}]")

@bot.on_message(filters.private & filters.command(["s", "status"]))
def status(bot, message) -> str:
    if not check_users(message):
        return
    message.reply_text("Bot is OK!")

bot.run()
