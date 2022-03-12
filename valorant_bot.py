import re
import os
import discord
import string
import random
import asyncio
import rso_request
import shop

client = discord.Client()
rso_channels = []

STORE_KEY = ['store', 'ストア', 'ショップ', '']


@client.event
async def on_ready():
    print('connect')
    await client.change_presence(activity = discord.Game(name = 'valorant store', activity = discord.Streaming))

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if client.user in message.mentions:
        global connectChannel
        if 'ばいばい' in message.content:
            await client.logout()
            return

        # RSO登録用チャンネルだったら無視
        elif message.channel in rso_channels:
          return

        # RSO情報の登録
        elif '登録' in message.content:
          channel = await create_private_channel(message)
          while True:
            if channel != None:
              break
          text = 'ユーザー名とパスワードを空白区切りでどうぞ'
          await reply(channel, text, message.author.mention)
          return

        # RSO情報の削除
        elif '削除' in message.content:
         success = rso_request.delete_userdata(str(message.author.id))
         text = '削除に成功しました' if success else '削除に失敗しました'
         await reply(message.channel, text)

        # ストア情報を取ってくる
        elif re.sub('<@!\d+>\S*?', '', message.content) in STORE_KEY or re.sub('<@!\d+>\S*?', '', message.content) == '':
          rso = rso_request.get_userdata(str(message.author.id))
          if rso == None:
            text = 'まずはメンションをつけて「登録」と発言してくれよな'
            await reply(message.channel, text)
            return

          skin_data = shop.get_skin_data(rso)
          if len(skin_data) == 0:
            text = 'ストア情報の取得に失敗しちゃった…'
            await reply(message.channel, text)
            return

          emojis = client.emojis
          emoji_VP = ''
          for emoji in emojis:
            if 'VP' == str(emoji.name):
              emoji_VP = ('<:VP:{0}>').format(emoji.id)
              break
          for skin in skin_data:
            await reply_embed(message.channel, '{0}　{1} {2}'.format(skin[0], emoji_VP, skin[1]), skin[2])

        else:
          name = re.sub('<@!\d+>\S*?', message.content, '')
          await message.mentions.edit(nick = name)
          text = '名前を変更したぜ'
          await reply(message.channel, text)
          return
        
    # RSO登録用チャンネル内で発言があった場合
    elif message.channel in rso_channels:
      try:
        username, password = message.content.split()
      except:
        text = '空白区切りでユーザー名とパスワードですぞ'
        await reply(message.channel, text)
        return

      rso = rso_request.get_rso_data(username, password)
      if rso == None:
        text = 'ログインに失敗したのでもう一回頼む'
        await reply(message.channel, text)
      else:
        text = '認証に成功したのでbotがつかえるようになったよ。このチャンネルは自動で消しときます'
        await reply(message.channel, text)
        await delete_channel(message.channel)
        rso_request.set_userdata(message.author.id, username, password)
        return

# ランダム文字列の生成
def randomname(num):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(num)]
   return ''.join(randlst)

# 認証用のプライベートチャンネルの作成
async def create_private_channel(message):
  guild = client.get_guild(int(os.environ['GUILD_ID']))
  overwrites = {
    guild.default_role: discord.PermissionOverwrite(read_messages=False),
    guild.me: discord.PermissionOverwrite(read_messages=True)
  }
  channel = await guild.create_text_channel('registration_{0}'.format(randomname(5)), overwrites = overwrites)
  await channel.set_permissions(message.author, read_messages = True, send_messages = True)

  rso_channels.append(channel)  

  return channel

# チャンネルの削除
async def delete_channel(channel):
  await asyncio.sleep(5)
  await channel.delete()
  rso_channels.remove(channel)

# 返信
async def reply(channel, text, mention = None):
  if mention != None:
    await channel.send('{0} \n {1}'.format(mention, text), file = None)
  else:
    await channel.send(text)

# embedを使って送信
async def reply_embed(channel, title, image_url):
  embed = discord.Embed(title = title, color = 0x4169e1)
  #embed.set_thumbnail(url = image_url)
  embed.set_image(url = image_url)
  await channel.send(embed = embed)


client.run(os.environ['DISCORD_TOKEN'])

