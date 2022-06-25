import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = [
    "bitter", "dismal", "heartbroken", "melancholy", "mournful", "pessimistic",
    "somber", "sorrowful", "sorry", "unhappy", "wistful", "bereaved", "blue",
    "cheerless", "dejected", "depressed", "despairing", "despondent",
    "disconsolate", "distressed", "doleful", "down", "down in dumps",
    "down in the mouth", "downcast", "forlorn", "gloomy", "glum",
    "grief-stricken", "grieved", "heartsick", "heavy-hearted", "hurting",
    "in doldrums", "in grief", "in the dumps", "languishing", "low",
    "low-spirited", "lugubrious", "morbid", "morose", "not happy",
    "out of sorts", "pensive", "sick at heart", "troubled", "weeping",
    "woebegone", "sad"
]

starter_encourangements = ["Cheer up!", "Hang in There.", "You are a great person!"]

if "responding" not in db.keys():
  db["responding"]=True

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + "  -" + json_data[0]['a']
    return quote


def update_encouragements(encouring_msg):
  if "encouragements" in db.keys():
    encouragements=db["encouragements"]
    encouragements.append(encouring_msg)
    db["encouragements"]=encouragements
  else:
    db["encouragements"]=[encouring_msg]

def delete_encouragement(index):
  encouragements=db["encouragements"]
  if len(encouragements)>index:
    del encouragements[index]
    db["encouragements"]=encouragements


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('$hello'):
        await message.channel.send('Hello')

    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
      options=starter_encourangements
      # keys=db["encouragements"]
      if "encouragements" in db.keys():
        options=options+db["encouragements"].value
        # print(options)
  
      if any(word in msg for word in sad_words):
          await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
      encouring_msg=msg.split("$new ",1)[1]
      update_encouragements(encouring_msg)
      await message.channel.send("New encouring message added.")

    if msg.startswith("$del"):
      encouragements=[]
      if "encouragements" in db.keys():
        index=int(msg.split("$del",1)[1])
        delete_encouragement(index)
        encouragements=db["encouragements"]
      await message.channel.send(encouragements)
    if msg.startswith("$list"):
      encouragements=[]
      if "encouragements" in db.keys():
        encouragements=db["encouragements"].value
      await message.channel.send(encouragements)

    if msg.startswith("$responding"):
      value=msg.split("$responding ",1)[1]

      if value.lower()=="true":
        db["responding"]=True
        await message.channel.send("Responding is on.")
      else:
        db["responding"]=False
        await message.channel.send("Responding is off.")

keep_alive()
client.run(os.environ['TOKEN'])
