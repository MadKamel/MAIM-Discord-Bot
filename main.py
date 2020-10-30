# Import functions
import os
import discord
from dotenv import load_dotenv

# Script from stackoverflow
# it allows on_member_join() to work
intents = discord.Intents.all()

# ENV File grabber
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")



# Start up Discord Bot Client
client = discord.Client(intents=intents)
print('MAIM is online.')

# Methods definitons
def loadchan(id):
  global client
  print('Channel #' + client.get_channel(id).name + ' loaded.')
  return client.get_channel(id)


# on_ready() method
@client.event
async def on_ready():
  for guild in client.guilds:
    if guild.name == GUILD:
      break

  # Welcome Message
  #await client.get_channel(766431090952634438).send('Please wait for an IT Operator to verify your identity before welcoming you in.')

  # Reset MAIM status
  await NewStatus('Manwich Security')
  

  # Channel definitions
  global PubAnnouncements
  global ITOpsSuggestions
  global ITOpsTODO
  global maimPubBroadcast
  global S1aInviteDump
  global S4aServerList
  global InfoSecUpdate
  global maimStatusUpdater
  global InfoSecNotify

  PubAnnouncements = loadchan(766381469672407082)
  ITOpsSuggestions = loadchan(767894422137864212)
  ITOpsTODO =  loadchan(766755542978134016)
  maimPubBroadcast = loadchan(766730428786409484)
  S1aInviteDump = loadchan(768167148899663902)
  S4aServerList = loadchan(768176557139034134)
  InfoSecUpdate = loadchan(768187677715464252)
  maimStatusUpdater = loadchan(768249204506099733)
  InfoSecNotify = loadchan(768279712190824448)


# on_invite_create() method
@client.event
async def on_invite_create(invite):
  if invite.max_age == 0:
    await ISLog(0, "inviter name: " + invite.inviter.name)
  else:
    await ISLog(1, "inviter name: " + invite.inviter.name)


# on_member_update() method
@client.event
async def on_member_update(before, after):
  if before.status != after.status:
    await ISNote("User [" + after.name + "] has changed their status:\nBefore: " + str(before.status) + "\nAfter: " + str(after.status))

# on_member_join() method
@client.event
async def on_member_join(member):
  await ISLog(2, "member name: " + member.name)



# on_message() method
@client.event
async def on_message(incoming):
  
  print('\n|========================================================')
  print('|Author:           ' + incoming.author.name)
  print('|Channel:         #' + incoming.channel.name)
  print('|========================================================')
  print('|' + incoming.content)
  print('|========================================================\n')
  
  # If bot didn't send message, do this.
  if client.user != incoming.author:
    global ITOpsSuggestions
    global ITOpsTODO
    global maimPubBroadcast
    global PubAnnouncements
    global S1aInviteDump
    global S4aServerList
    global maimStatusUpdater

    # IT Operations Suggestions Box
    if incoming.channel == ITOpsSuggestions:
      await incoming.channel.send('Your suggestion was sent!')
      await ITOpsTODO.send('<@&766377844003176519> ' + incoming.author.name + ' left a suggestion:\n' + '```' + incoming.content + '```')
    
    # IT Operations Broadcast
    elif incoming.channel == maimPubBroadcast:
      await PubAnnouncements.send('@here, there is a new announcement from <@!' + str(incoming.author.id) + '>:\n```' + incoming.content + '```')
      await incoming.delete()

    # Invite Storage
    elif incoming.channel == S1aInviteDump:
      if incoming.content[:19] == 'https://discord.gg/' and (len(incoming.content) == 25 or len(incoming.content) == 26):
        print('Server invite link found.')
        print(incoming.content)
        await S4aServerList.send(incoming.content)

      await incoming.delete()

    elif incoming.channel == maimStatusUpdater:
      await NewStatus(incoming.content)
      await incoming.delete()



# Warning Code list
WarningCodes = []
WarningCodes.append("user created invite link with unlimited duration")
WarningCodes.append("user created invite link with limited duration")
WarningCodes.append("new member has joined the server")


# Method definitions
async def ISLog(code, details="No details given."):
  global InfoSecUpdate
  await InfoSecUpdate.send('<@&766377844003176519>\nWARNING CODE: **' + str(code) + '**\nTYPE: ' + WarningCodes[code] + '\nDETAILS: ' + details + '')

async def NewStatus(activity):
  await client.change_presence(status=discord.Status.idle, activity=discord.Game(activity))

async def ISNote(note):
  global InfoSecNotify
  await InfoSecNotify.send(note)

# Run the client. (How could I forget???)
client.run(TOKEN)
