import discord
import asyncio
import requests
import random
import praw
import datetime
import string

token = "token"

reddit = praw.Reddit(client_id='gZYW4noix22UQA',
                     client_secret="-HsFfCrXNm59gONekaqD-qugkP4",
                     user_agent='Discord:com.theNerds.discordBot:v0 (by /u/iansan5653)')

# Adds a prefix to the trigger for testing
trigPref = ""

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in')

# SCPBotCode

@client.event
async def on_message(message):
    trigMessage = message.content.lower()
# ScpBotCode
    SCPCodes = [t for t in trigMessage.split() if t.startswith('scp-') or t.startswith('SCP-') or t.startswith('Scp-')]
    if SCPCodes:
        await client.send_typing(message.channel)
        msg = SCPCodes[0].split('-', 2)
        if len(msg[1]) <= 4 and len(msg[1]) >= 3 and msg[1].isdigit():
            if(len(msg) > 2):
                scpurl = 'http://www.scp-wiki.net/scp-' + msg[1] + '-' + msg[2]
            else:
                scpurl = 'http://www.scp-wiki.net/scp-' + msg[1]

            tmp_msg = await client.send_message(message.channel, '**Link:** ' + scpurl + ' *Checking for existence...*')
            scp = requests.get(scpurl)
            if scp.status_code == 200:
                await client.edit_message(tmp_msg, '**Link:** ' + scpurl + ' *SCP exists!*')

                # Someday images may get sent. Not today.
                    # tree = BeautifulSoup(scp.text, "lxml")
                    # img_link = tree.find_all('div', class_="scp-image-block")[0].img.get('src')
                    # await client.send_file(message.channel, img_link, filename='SCP-' + msg[1] + '_img', content=None, tts=False)

            elif scp.status_code == 404:
                await client.edit_message(tmp_msg, '~~**Link:** ' + scpurl + '~~ *SCP does not exist.*')
            else:
                await client.edit_message(tmp_msg, '**Link:** ' + scpurl + ' *Unable to determine if this SCP exists.*')
        else:
            await client.send_message(message.channel, 'SCP must be a 3 or 4 digit number. Example: `SCP-1175`')
# AyyLmaoBotCode
    elif trigMessage.startswith(trigPref + 'ayy'):
        await client.send_message(message.channel, 'lmao')
# StarWarsTitleBotCode
    elif trigMessage.startswith(trigPref + 'sw'):
        msg = message.content.split(' ', 1)[1]
        if len(msg) == 1 and msg.isdigit() and int(msg) >= 0 and int(msg) <= 9:
            titles = {
                1: 'The Phantom Menace',
                2: 'Attack of the Clones',
                3: 'Revenge of the Sith',
                4: 'A New Hope',
                5: 'The Empire Strikes Back',
                6: 'Return of the Jedi',
                7: 'The Force Awakens',
                8: 'The Last Jedi',
                9: '[TBA]'
            }
            await client.send_message(message.channel, 'That Star Wars movie is called *' + titles[int(msg)] + '*.')
# LoadingBarBotCode
    elif trigMessage.startswith(trigPref + '!load'):
        x = random.randrange(0, 10)
        loading = await client.send_message(message.channel, '`0%   -------------------`')
        await asyncio.sleep(x)
        await client.edit_message(loading, '`10%  ||------------------`')
        await asyncio.sleep(x)
        await client.edit_message(loading, '`20%  ||||----------------`')
        await asyncio.sleep(x)
        await client.edit_message(loading, '`30%  ||||||--------------`')
        await asyncio.sleep(x)
        await client.edit_message(loading, '`40%  ||||||||------------`')
        await asyncio.sleep(x)
        await client.edit_message(loading, '`50%  ||||||||||----------`')
        await asyncio.sleep(x)
        await client.edit_message(loading, '`60%  ||||||||||||--------`')
        await asyncio.sleep(x)
        await client.edit_message(loading, '`70%  ||||||||||||||------`')
        await asyncio.sleep(x)
        await client.edit_message(loading, '`80%  ||||||||||||||||----`')
        await asyncio.sleep(x)
        await client.edit_message(loading, '`90%  ||||||||||||||||||--`')
        await asyncio.sleep(x)
        await client.edit_message(loading, '`95%  |||||||||||||||||||-`')
        await asyncio.sleep(x)
        await client.edit_message(loading, '`100% ||||||||||||||||||||`')
        await client.send_message(message.channel, 'Loading Complete!')
# PizzaOrderBotCode
    elif trigMessage.startswith(trigPref + '`sudo order pizza`'):
        await client.send_message(message.channel, ':pizza:')
# RandomNumberGenCode
    elif trigMessage.startswith(trigPref + '!rand'):
        msgsplit = message.content.split(' ', 3)
        minval = msgsplit[1]
        maxval = msgsplit[2]

        if minval.isdigit() and maxval.isdigit():
            value = random.randrange(int(minval), int(maxval))
            await client.send_message(message.channel, 'Your number is: **' + str(value) + '**.')
        else:
            await client.send_message(message.channel, 'Invalid command, use syntax `!rand minimum maximum`.')
# RedditBotCode
    elif trigMessage.startswith(trigPref + 'r '):
        subreddit = message.content.split(' ', 1)[1]
        await client.send_message(message.channel, 'https://www.reddit.com/r/' + subreddit)

    elif trigMessage.startswith(trigPref + 'u '):
        user = message.content.split(' ', 1)[1]
        await client.send_message(message.channel, 'https://www.reddit.com/u/' + user)
        r_user = reddit.redditor(user)
        print(r_user.submissions.new())
        await client.send_message(message.channel, 'Link Karma: **' + str(r_user.link_karma) + '**')
        await client.send_message(message.channel, 'Comment Karma: **' + str(r_user.comment_karma) + '**')

    elif trigMessage.startswith(trigPref + '!u '):
        user = message.content.split(' ', 1)[1]
        await client.send_message(message.channel, 'https://www.reddit.com/u/' + user)
        r_user = reddit.redditor(user)
        r_u_posts = r_user.submissions.new(limit=5)
        posts_message = ''
        for submission in r_u_posts:
            time = datetime.datetime.fromtimestamp(submission.created)
            posts_message = posts_message + '\n**(' + str(submission.score) + ')** ' + str(time) + ': *' + submission.title + '*\n' + submission.shortlink
        await client.send_message(message.channel, 'Link Karma: **' + str(r_user.link_karma) + '** | Comment Karma: **' + str(r_user.comment_karma) + '** | Recent Posts:')
        await client.send_message(message.channel, posts_message)
# RandomIntegerSpam
    elif trigMessage.startswith(trigPref + '!numberspam'):
        loop = 1
        while loop == 1:
            y = random.randrange(1, 100)
            await client.send_message(message.channel, y)
# PasswordGen
    elif trigMessage.startswith(trigPref + '!p'):
        passsplit = message.content.split(' ', 1)
        passlen = int(passsplit[1])
        randtextstr = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(passlen))
        await client.send_message(message.channel, 'Your password is: ' + randtextstr)
# LennyCode
    elif trigMessage.startswith(trigPref + 'lenny'):
        await client.send_message(message.channel, '( ͡° ͜ʖ ͡°)')
# DiceRoll
    elif trigMessage.startswith(trigPref + '!roll'):
            dieRoll = random.randrange(1, 20)
            await client.send_message(message.channel, dieRoll)
# WikipediaSearch
    elif trigMessage.startswith(trigPref + 'wiki'):
        wikiSplit = message.content.split(' ')
        wikiSplit.pop(0)
        wikiLink = 'https://en.wikipedia.org/wiki/'
        wiki = "_".join(wikiSplit)
        await client.send_message(message.channel, wikiLink + wiki)
# Magic8Ball
    elif trigMessage.startswith(trigPref + 'magic8ball'):
        await client.send_message(message.channel, 'To use the Magic 8 Ball, type !8ball and your question...')
    elif trigMessage.startswith(trigPref + '!8ball'):
        answers = ['It is certain',
                   'It is decidedly so',
                   'Without a doubt',
                   'Yes, definitely',
                   'You may rely on it',
                   'As I see it, yes',
                   'Most likely',
                   'Outlook is good',
                   'Yes',
                   'Signs point towards yes',
                   'My vision is hazy, please try again',
                   "I don't want to answer that...",
                   'It would be better to tell you that information at a later date...',
                   'I have no idea',
                   'Concentrate harder, and ask again',
                   "Don't count on it",
                   'I see "no"',
                   '*(counter-terrorist voice)* Negative',
                   'Outlook is bleak at best',
                   'I am very doubtful',
                   "Ha, don't kid yourself"]
        chosenans = random.choice(answers)
        await client.send_message(message.channel, chosenans)
# Error
    elif trigMessage.startswith(trigPref + 'help'):
        await client.send_message(message.channel, 'ERROR CANNOT PROCESS FUNCTION REPORT TO AN ADMINISTRATOR IMMEDIATELY')
#Safe
    elif trigMessage.startswith(trigPref + 'scp are you safe from external code injection?'):
        await client.send_message(message.channel, 'Yep :ho_mlady:')
# No problem
    elif trigMessage == 'thank you':
        await client.send_message(message.channel, 'You\'re welcome.')
client.run(token)