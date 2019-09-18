import discord
import os
import json
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

print('Make sure you have all the data in the data/data.json')
directory = os.path.dirname(os.path.realpath(__file__))
data = open(os.path.join(directory,'data','data.json'),'r')
data = json.loads(data.read())

id = int(data['id'])
idx = 'x'*len(str(id))
token = data['token']
tokenx = 'x'*len(token)
perm = int(data['perm'])
username = data['username']
userid = str(data['userid'])
userx = username+'#'+userid
command = data['command']
separator = ' '
url = f'https://discordapp.com/oauth2/authorize?client_id={id}&scope=bot&permissions={perm}'
print('Make sure you registered the bot: '+ url)
ai = False
chatbot = ChatBot('Discord Bot')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')
name = 'bot'

client = discord.Client()

@client.event #event decorator/wrapper
async def on_ready():
    global name
    name = str(client.user)
    print(f'We have logged in as {client.user}')

@client.event
async  def on_message(message):
    global ai, name, userx, command
    print(f'{message.channel}: {message.author}: {message.content}')
    data = []
    data = message.content.split(' ')
    if str(message.author) != name and ai == True and message.content.startswith(command) != True and str(message.channel).startswith('ai'):
        await message.channel.send(chatbot.get_response(str(message.content)))
    if str(message.author) == userx:
        if message.content.startswith(command):
            await message.delete()
        if command+'bot' == data[0]:
            if len(data)>2:
                if '-ai' == data[1]:
                    if '-on' == data[2]:
                        ai = True
                    if 'off' == data[2]:
                        ai = False
                if '-send' == data[1]:
                    bot = data
                    bot.remove('$bot')
                    bot.remove('-send')
                    await message.channel.send(separator.join(bot))
            if len(data)>1:
                if '-help' == data[1]:
                    await message.channel.send(f'```{command}bot commands\n-help = list of commands\n-close = close the bot program\n-data = get data about the bot, args:[-name, -id, (-tok, -token), (-perm, -permission), None]\n-send = send a message as the bot```')
                if '-close' == data[1]:
                    await client.close()
                if '-data' == data[1]:
                    if len(data)>2:
                        if '-name' in data:
                            await message.channel.send(f'```name: {name}```')
                        if '-id' in data:
                            await message.channel.send(f'```bot id: {idx}```')
                        if '-token' in data or '-tok' in data:
                            await message.channel.send(f'```token: {tokenx}```')
                        if '-perm' in data or '-permission' in data:
                            await message.channel.send(f'```permissions level: {perm}```')
                    else:
                        await message.channel.send(f'```name: {name}\nbot id: {idx}\ntoken: {tokenx}\npermissions level: {perm}```')

client.run(token)