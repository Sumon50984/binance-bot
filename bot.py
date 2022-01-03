from binance.exceptions import *
import yaml
from pyrogram import Client, filters
from binance_api import main, price, balance

file = "config.yml"
with open(file) as file:
   auth = yaml.load(file, Loader=yaml.FullLoader)

bot = Client("my_bot", bot_token= auth['bot_token'], api_id=auth['api_id'], api_hash=auth['api_hash'])

def check_user(message):
    user = message.from_user.id
    user_id = auth['user_id']
    if str(user) not in str(user_id):
      return False
    else:
      return True

@bot.on_message(filters.command(["trade", "t"]) & filters.private)
def trade(bot, message):
  if not check_user(message):
    return
  value  = message.text.lower()
  value_checker  = len(message.command)
  command  = message.command

  if "buy" in value and value_checker == 4:
      try:
        main(str(str(command[2]+ "usdt")), float(command[3]), "buy")
        TEXT = "Successfully bought" + " " + str(command[3]) + "$" + " " + str(command[2]).upper()
        message.reply_text(TEXT)
      except BinanceAPIException as e:
        message.reply_text(e)
        message.reply_text("failed! to bought")

  elif "sell" in value and value_checker == 4:
      try:
        main(str(str(command[2]+ "usdt")), float(command[3]), "sell")
        TEXT = "Successfully sold" + " " + str(command[3]) + "$" + " " + str(command[2]).upper()
        message.reply_text(TEXT)
      except BinanceAPIException as e:
        message.reply_text(e)
        message.reply_text("Failed! to sold")
  else:
        message.reply_text( "Not understand, Enter like [/trade {buy/sell} {coin} {amount in usd}")

@bot.on_message(filters.private & filters.command(["check", "c"]))
async def lastprice(bot, message):
         if not check_user(message):
           return

         value = message.text.lower()
         value_checker  = len(message.command)
         command  = message.command
         if "price" in value and value_checker == 3 and str(command[2]) != " ":
           try:
             finaly = price(str(str(command[2]+ "usdt")))
             reply = str(command[2]).upper() + " " +  "price is" + " " + str(finaly)
             await message.reply_text(reply)
           except BinanceAPIException as e:
             await message.reply_text(e)
             await message.reply_text(text="Failed!")

         elif "bal" in value and value_checker == 3:
            try:
                text = balance(str(command[2]))
                await message.reply_text(text)
            except BinanceAPIException as e:
               await message.reply_text(e)
               await message.reply_text(text="Failed!")

         else:
             await message.reply_text("Look like you entered wrong command")
             await message.reply_text("Enter like [/c {price/bal} {coin}]")

@bot.on_message(filters.private & filters.command(["s", "status"]))
def status(bot, message):
  if not check_user(message):
    return
  message.reply_text("Bot is OK!")

bot.run()

