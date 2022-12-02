from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler,filters
from telegram import *
from telegram.constants import ParseMode
#from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext
import json
import stripe
import psycopg2
stripe.api_key = "sk_test_51M2rqGITV27aYUdhCpJp3IUmIHF9RgbZUUVHdbanHPA85wgiaYMjWg8OJbaGYuwpehdAzJ0DjJ3vLEMy98a4nFZl00V7kFy5x4"
drive_id='1-JtstcTGro6S0S9zQqBqqKayUoTdNB0N'
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#soullabs = "5540797060:AAEuYIQzk4LaWXkG8BJWNdGRt_-qlAvcZss"
soullabs = "5855809302:AAGaZX7__rCZsbb_pqu0VAm2r76HO1pcqhU"
#updater = Updater(soullabs,use_context=True)
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

from moviepy.editor import VideoFileClip,AudioFileClip,CompositeAudioClip,afx,vfx,VideoClip
import urllib
import time
import locale
#import util
from datetime import datetime, timedelta
from urllib.parse import quote
import socket
import requests
import random
import os
import sqlite3 as sq
import re
from PIL import Image,ImageEnhance
import numpy as np



telegram_url = 'https://api.telegram.org/bot'+soullabs

startmsg='''
🤖🎥 Bring Videos and Images Back To Life In Minutes (without the algo knowing)

Works on Facebook, TikTok, Snapchat and Google

Metadata Refresh Pro was created to keep ads running longer and making each clone seem “fresh” to an algorithm, so it works again and again.

🤔 What can the ad refresh bot do?

✅ Changes the source code of a video or image. Each creative will be unique for an advertising platform.
✅ The bot processes every frame of your video and applies invisible elements to the video.
✅ Changes the audio track
✅ Changes the soundtrack.
✅ Removes Metadata making your creative unique again.

 👉 How to use? It's easy!

1️⃣ Select tariffs and payment
2️⃣ Pay the fee
3️⃣ Upload your video or image
4️⃣ Get a ready-made unique video creative

'''

eopt = '''
The video is downloaded. Choose ways to edit.

1) Installing a transparent and invisible mesh
2) Small color correction for gamma, saturation and contrast
3) Replacing music with another, no copyright (joyful)
4) Replacing music with another, no copyright (disturbing)
5) Removing metadata
6) Reducing video fps by 10-15 frames
7) Crop the beginning of the video by 0.1-0.15s
8)Crop the end of the video by 0.1-0.15s
9) Acceleration of the audio track by 5-10%
'''
faq = '''
❔Can I upload multiple video creatives at once?
❕Video creatives are loaded and uniqueized one at a time, that is, 1 unique = 1 video creative.
❔How long does it take to unify?
❕On average, up to 5 minute
❔Are there any requirements for the downloaded files?
❕Format: mp4 / avi. File size: up to 500 MB.
Files up to 20 MB are uploaded without compression directly to the bot.
Files ranging in size from 20 to 500 MB must first be uploaded to Google Drive, then copy the link to
the file and upload it to the bot.
❔How to contact support?
❕You are welcome to ask questions about the bot and payment via Telegram @zefiagency
'''

notpaid = 'Unfortunately, your plan has expired! You can order a new tariff in the main menu!'

stripe_key = '284685063:TEST:Nzg4ODRhNGVkYzU3'

base = os.path.dirname(__file__)
db = os.path.join(base,'telegram.db')






def imageEdits():
    buttons = [ [InlineKeyboardButton("❌ Overlay invisible mesh",callback_data='Overlay invisible mesh')],
                [InlineKeyboardButton("❌ Flip the image",callback_data='Flip the image')],
                [InlineKeyboardButton("❌ Remove metadata",callback_data='Remove metadata')],
                [InlineKeyboardButton("❌ Color correction",callback_data='Color correction')],
                [InlineKeyboardButton("CONFIRM",callback_data="sendEdit")]          
             ]
    return buttons

def downloadFromDrive(glink,fmt):

    gauth = GoogleAuth()

    cred = os.path.join(base,'kevin.json')

    gauth.LoadCredentialsFile(cred)

    if gauth.access_token_expired:
        print("Expire, Refreshing token")

        # Refresh them if expired

        gauth.Refresh()
    else:
        print("good")
        gauth.Authorize()

    drive = GoogleDrive(gauth)

    glink = re.search('\/d\/(.*)\/view?',glink).groups()[0]
    file = drive.CreateFile({'id':glink})

    file.GetContentFile(glink+fmt)
    return glink+fmt



def uploadToDrive(path,id):
    gauth = GoogleAuth()

    cred = os.path.join(base,'kevin.json')

    gauth.LoadCredentialsFile(cred)

    if gauth.access_token_expired:
        print("Expire, Refreshing token")

        # Refresh them if expired

        gauth.Refresh()
    else:
        print("good")
        gauth.Authorize()


    drive = GoogleDrive(gauth)
    nfile = drive.CreateFile({'parents':[{'id':id}],'title':path})

    nfile.SetContentFile(path)
    nfile.Upload()

    nfile.InsertPermission({'type':'anyone',
                            'value':'anyone',
                            'role':'reader'
                            })
    return nfile['webContentLink']

def executeSql(query,type=None):
    try:
        con = psycopg2.connect(database='postgres',
                                host='31.220.17.29',
                                user='soul',
                                password='soul.1234',
                                port='5432'
                                )

        cur = con.cursor()
        
        if type == None:
            cur.execute(query)
            l = cur.fetchall()
            #con.commit()
            cur.close()
            con.close()
            return l
        else:
            print(query)
            cur.execute(query)
            con.commit()
            cur.close()
            con.close()
            print("commit")
    except:
        cur.close()
        con.close()
        print("Error Occured in database")
        return []

def checkPayment(chat_id):

    try:
        con = psycopg2.connect(database='postgres',
                                host='31.220.17.29',
                                user='soul',
                                password='soul.1234',
                                port='5432'
                                )

        cur = con.cursor()
        l = executeSql("select payment_status from users where chat_id={0}".format(chat_id))
        
        l = l[0][0]
        print(l)
        if l == 100:
            cur.close()
            con.close()
            return True
        else:
            cur.close()
            con.close()
            return False
    except:
        cur.close()
        con.close()
        return False



def editImage(path,chat_id,edits):
    
    with Image.open(path) as image:
        for _ in edits:
            if _ == 'Overlay invisible mesh':
                image = imageRemoveMetadata(image)
            elif _ == 'Flip the image':
                image = imageFlip(image)
            elif _ == 'Remove metadata':
                image = imageRemoveMetadata(image)
            elif _ == 'Color correction':
                image = imgColorCorrection(image)
        
        image.save('{0}.jpg'.format(chat_id))
    return '{0}.jpg'.format(chat_id)

def imgColorCorrection(image):
    filter = ImageEnhance.Color(image)
    img = filter.enhance(1.5)
    return img
    

def imageFlip(image):
    img_data = np.array(image)
    flip = np.flip(img_data,axis=1)
    img = Image.fromarray(flip)
    return img

def imageRemoveMetadata(image):
    img_data = np.array(image)
    return Image.fromarray(img_data)

def editVideo(path,chat_id,edits,fmt=None):
    l=None

    if fmt != None:
        path = downloadFromDrive(path,fmt)

    with VideoFileClip(path) as clip:
        for _ in edits:

            if _ == 'Installing mesh':
                pass
            elif _ == 'Color correction':
                clip = colorCorrection(clip)
                continue
            elif _ == 'Replacing music (joyful)':
                clip,l = replaceMusicJoyful(clip)
                continue
            elif _ == 'Replacing music (disturbing)':
                clip,l = replaceMusicJoyful(clip)
            elif _ == 'Removing metadata':
                clip = removeMetadata(clip)
            elif _ == 'Reducing video fps':
                clip = reduceFPS(clip)
                continue
            elif _ == 'Crop start of video':
                clip = cropStart(clip)
                continue
            elif _ == 'Crop end of video':
                clip = cropEnd(clip)
                continue
            elif _ == 'Speed up audio':
                clip = accelerateAudio(clip)
                continue

        final = clip.write_videofile('{0}.mp4'.format(chat_id))
        if l != None:
            l.close()
        return '{0}.mp4'.format(chat_id)            





def cropStart(clip):
    #crop video by 10%-30% at the beginning and at the end
    dur = clip.duration
    n = random.randrange(10,15)
    n = n/100
    clip1 = clip.subclip(n,)
    #clip2 = clip1.subclip(0,dur-(n*dur))
    #final = clip2.write_videofile('{0}.avi'.format(chat_id),fps=clip.fps,codec='libx264')
    return clip1

def cropEnd(clip):
    dur = clip.duration
    n = random.randrange(10,15)
    n = n/100
    #clip1 = clip.subclip(n*dur,)
    clip2 = clip.subclip(0,dur-n)
    #final = clip2.write_videofile('{0}.avi'.format(chat_id),fps=clip.fps,codec='libx264')
    return clip2




def replaceMusicJoyful(clip):
    gtc = os.path.dirname(__file__)
    au = os.path.join(gtc,'joy.mp3')
    l = AudioFileClip(au)
    m = afx.audio_loop(l,duration=clip.duration)
    clip = clip.set_audio(m)
    #final = clip.write_videofile('{0}.avi'.format(chat_id),fps=clip.fps,codec='libx264')
    return clip,l

def replaceMusicDisturbing(path):
    pass

def reduceFPS(clip):
    nfps = clip.fps
    n = random.randrange(10,15)
    nfps = abs(nfps-n)
    final = clip.set_fps(nfps)
    return final
    #final = clip.write_videofile('{0}.avi'.format(chat_id),fps=nfps,codec='libx264')
    #return '{0}.avi'.format(chat_id)
    
    #reduce fps by 10-15 frames

def accelerateAudio(clip):
    clip = clip.fx(vfx.speedx,1.5)
    return clip
    #accelerate audio track by 5-10%

def colorCorrection(clip):
    #small color correction for gamma saturation and contrast
    clip = clip.fx(vfx.lum_contrast)
    clip = clip.fx(vfx.colorx,1.05)
    return clip

def installMesh(path):
    #installing a trasparent and invisible meshpass
    pass
def removeMetadata(clip):
    clip = colorCorrection(clip)
    return clip
    




def mainBtn():
    buttons = [
        [KeyboardButton('Upload a video🎥'),KeyboardButton('Upload a image🖼️')],
        [KeyboardButton('Tariffs and payment💳'),KeyboardButton('FAQ ❓')],
        [KeyboardButton('Tech. Support💻'),KeyboardButton('About Bot 🤖')],
        [KeyboardButton('Referral Code🪙')]
    ]
    return buttons

def editBtns():
    buttons = [ [InlineKeyboardButton("1) ❌ Installing mesh",callback_data='Installing mesh')],
                [InlineKeyboardButton("2) ❌ Color correction",callback_data='Color correction')],
                [InlineKeyboardButton("3) ❌ Replacing music (joyful)",callback_data='Replacing music (joyful)')],
                [InlineKeyboardButton("4) ❌ Replacing music (disturbing)",callback_data='Replacing music (disturbing)')],
                [InlineKeyboardButton("5) ❌ Removing metadata",callback_data='Removing metadata')],
                [InlineKeyboardButton("6) ❌ Reducing video fps",callback_data='Reducing video fps')],
                [InlineKeyboardButton("7) ❌ Crop start of video",callback_data='Crop start of video')],
                [InlineKeyboardButton("8) ❌ Crop end of video",callback_data='Crop end of video')],
                [InlineKeyboardButton("9) ❌ Speed up audio",callback_data='Speed up audio')],
                [InlineKeyboardButton("CONFIRM",callback_data="sendEdit")]          
             ]
    return buttons

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    with open(os.path.join(base,'hello.jpg'),'rb') as f:
        await update.effective_chat.send_photo(f)
    
    l = await update.effective_chat.send_message(startmsg,reply_markup=ReplyKeyboardMarkup(mainBtn(),resize_keyboard=True))
    user = executeSql("select chat_id from users")
    user = [x[0] for x in user]
    if l.chat.id not in user:
        ran = random.randrange(2022,2100)
        reff = "ZEFI"+str(update.effective_chat.id)+str(ran)
        executeSql("insert into users (chat_id,referral_code) values ({0},'{1}')".format(l.chat.id,reff),'commit')
    return


async def msgHandler(update: Update, context:ContextTypes.DEFAULT_TYPE ):
    print(update)

    if 'mode' in context.user_data.keys():
        if 'googleVideo' in context.user_data['mode']:

            link = update.message.text

            if link == '❌ Cancel':
                context.user_data.clear()
                await context.bot.deleteMessage(update.effective_chat.id,update.message.id)
                await update.effective_chat.send_message("Action cancled.",reply_markup = ReplyKeyboardMarkup(mainBtn(),resize_keyboard=True))

            context.user_data['glink'] = link
            msg = eopt.split('\n\n')[1]
            msg = 'The link is saved. Choose ways to uniqueize\n\n'+msg
            await update.effective_chat.send_message(msg)
            m=await update.effective_chat.send_message('Set checkboxes on the options you like',reply_markup=InlineKeyboardMarkup(editBtns()))
            context.user_data['p_m'] = m.message_id
            return
        elif 'referral' in context.user_data['mode']:
            invite = update.message.text
            l = executeSql("select chat_id where referral_code='{0}'".format(invite))
            if len(l)==0:
                await update.effective_chat.send_message("Invalid invite code")
                context.user_data.clear()
            else:
                check = executeSql("select referred_by from users where chat_id={0}".format(update.effective_chat.id))

                if len(check)!= 0 or check[0][0] == None:
                    l = l[0][0]
                    executeSql("update users set referred_by={0} where chat_id={1}".format(l,update.effective_chat.id),"commit")
                    await update.effective_chat.send_message("Invite code received!")
                    context.user_data.clear()
                    return
                else:
                    await update.effective_chat.send_message("You already redeemed code!")
                    return

    if update.message.text == 'Upload a video🎥':
        #check userplan
        if checkPayment(update.effective_chat.id):
            context.user_data['type'] = 'video'

            msg = 'To switch to the mode of uploading video to the bot, click on the button below. The bot sees your file only in this mode.'
            inlinebtn = [[InlineKeyboardButton('Upload video mode',callback_data='videoMode')]]
            
            m = await update.effective_chat.send_message(msg,reply_markup=InlineKeyboardMarkup(inlinebtn))
            context.user_data['p_m'] = m.message_id
            return
        else:
            await update.effective_chat.send_message(notpaid)
            return
    
    elif update.message.text == '❌ Cancel':
        context.user_data.clear()

        print(update.message.id)
        await context.bot.deleteMessage(update.effective_chat.id,update.message.id)
        await start(update,context)
        return
    
    elif update.message.text == 'Tariffs and payment💳':
        # check if user is registered or not!

        if checkPayment(update.effective_chat.id) == False:
            btn = [[InlineKeyboardButton('Unlimited creative',callback_data='payment')],[InlineKeyboardButton('Back',callback_data='home')]]
            u = await update.effective_chat.send_message('List of our tariffs:\n\nUnlimited Creatives- $9 per month',reply_markup=InlineKeyboardMarkup(btn))

            print(u.message_id)
            return
        else:
            msg = 'You have already purchased a tariff:\nunlimited Creatives.\n\nNumber of remaining to be edited videos: 999'
            
            customer = executeSql("select customer_id from users where chat_id={0}".format(update.effective_chat.id))
            customer = customer[0][0]
            cus = stripe.billing_portal.Session.create(customer=customer)
            btn = [[InlineKeyboardButton('Customer portal',url=cus['url'])]]
            await update.effective_chat.send_message(msg,reply_markup=InlineKeyboardMarkup(btn))
    elif update.message.text == 'Tech. Support💻':
        with open(os.path.join(base,'support.jpg'),'rb') as f:
            await update.effective_chat.send_photo(f)
        await update.effective_chat.send_message("!?️ Ask your questions about the bot, operation and payment via Telegram @zefiagency")
        return
    elif update.message.text == 'FAQ ❓':
        with open(os.path.join(base,'faq.jpg'),'rb') as f:
            await update.effective_chat.send_photo(f)
        await update.effective_chat.send_message(faq)
        return
    elif update.message.text == 'About Bot 🤖':        
        await start(update,context)
    
    elif update.message.text == 'Upload a image🖼️':

        if checkPayment(update.effective_chat.id):
            context.user_data['type'] = 'image'
            msg = 'Upload an image WITHOUT COMPRESSION in PNG / JPG format up to 20 mb in size.\nYou can choose the following settings for editing\n1. Overlay invisible mesh\n2. Flip the image\n3. Minimum image zoom\n4. Remove metadata\n5. Color correctionThe bot sees your files only in this mode.'
            inlinebtn = [[InlineKeyboardButton('Image edit mode',callback_data='imageMode')]]
            
            m = await update.effective_chat.send_message(msg,reply_markup=InlineKeyboardMarkup(inlinebtn))
            context.user_data['p_m'] = m.message_id
            return
        else:
            await update.effective_chat.send_message(notpaid)
            return
    
    elif update.message.text=='Referral Code🪙':
        btn = [[InlineKeyboardButton("Enter Referral Code",callback_data="referral"),InlineKeyboardButton("No Referral",callback_data="No Referral")]]

        l = executeSql("select referral_code from users where chat_id={0}".format(update.effective_chat.id))
        
        l = l[0][0]
        if l == None:
            reff = "ZEFI"+str(update.effective_chat.id)+str(random.randrange(2022,2100))
            executeSql("update users set referral_code='{0}' where chat_id={1}".format(reff,update.effective_chat.id),"commit")
            await update.effective_chat.send_message("Your unique referral code is: {0}".format(reff),reply_markup=InlineKeyboardMarkup(btn))
        
        else:
            await update.effective_chat.send_message("Your unique referral code is: {0}".format(l),reply_markup=InlineKeyboardMarkup(btn))



async def fileHandler(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if 'mode' in context.user_data.keys():
            print("yes")    
            allowed = ['mp4','MP4','avi']

            if context.user_data['mode'] == 'imageUpload':
                v = update.message.document

                print(v)
                if 'png' not in v['mime_type'] and 'jpeg' not in v['mime_type']:
                    await update.effective_chat.send_message("Wrong format media!")
                    #context.user_data.clear()
                    await start(update,context)
                    return
                else:
    
                    #f = context.bot.getFile(v['file_id']).download()
                    #f = File(v['file_id'],v['file_unique_id'])
                    f = await context.bot.get_file(v['file_id'])
                    
                    await f.download_to_memory()
                    #await f.download_to_memory()
                    print(f)
                    print("\n\n",f.file_path)
                    #context.user_data.clear()
                    context.user_data['file'] = f.file_path.split('documents/')[1]
                    print(context.user_data['file'])

                    m= await update.effective_chat.send_message("Your image is uploaded, select the settings to edit",reply_markup=InlineKeyboardMarkup(imageEdits()))
                    
                    context.user_data['p_m'] = m.message_id
                    return                                        


            if context.user_data['mode'] == 'telegramVideo':

                v = update.message.video
                print(v)
                if 'mp4' not in v['mime_type'] and 'avi' not in v['mime_type']:
                    await update.effective_chat.send_message("Wrong format media!")
                    #context.user_data.clear()
                    start(update,context)
                    return
                else:
                    await update.effective_chat.send_message("We have received you video, it is now downloading!")
                    #f = context.bot.getFile(v['file_id']).download()
                    #f = File(v['file_id'],v['file_unique_id'])
                    f = await context.bot.get_file(v['file_id'])
                    
                    await f.download_to_memory()
                    #await f.download_to_memory()
                    print(f)
                    print("\n\n",f.file_path)
                    #context.user_data.clear()
                    context.user_data['file'] = f.file_path.split('videos/')[1]
                    print(context.user_data['file'])

                    await update.effective_chat.send_message(eopt)
                    m=await update.effective_chat.send_message('Set checkboxes on the options you like',reply_markup=InlineKeyboardMarkup(editBtns()))
                    context.user_data['p_m'] = m.message_id
                    return


async def queryHandler(update: Update,context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query.data

    editoptions = ['Installing mesh',
            'Color correction',
             'Replacing music (joyful)',
             'Replacing music (disturbing)',
             'Removing metadata',
             'Reducing video fps',
             'Crop start of video',
             'Crop end of video',
             'Speed up audio'
            ]
    imageoptions = ['Overlay invisible mesh',
                    'Flip the image',
                    'Remove metadata',
                    'Color correction',
    ]

    if query == 'imageMode':
        await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=context.user_data['p_m'])
        btn = [[KeyboardButton('❌ Cancel')]]
        m = await update.effective_chat.send_message("Upload an image WITHOUT COMPRESSION in PNG / JPG format up to 20 mb in size.",reply_markup=ReplyKeyboardMarkup(btn,resize_keyboard=True)) 
        context.user_data['p_m'] = m.message_id
        await update.callback_query.answer('image editing mode activated!')
        context.user_data['mode'] ='imageUpload'
        return

    if query == 'videoMode':
        # check tarrif!
        msg = 'Choose how you want to send your video in telegram chat or link to google Drive.'
        ibutton = [[InlineKeyboardButton('Telegram chat',callback_data='telegramUpload'),InlineKeyboardButton('Google Drive',callback_data='googleUpload')]]
        btn = [[KeyboardButton('❌ Cancel')]]
        await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=context.user_data['p_m'])
        await update.effective_chat.send_message('You have unlimited tariff.',reply_markup=ReplyKeyboardMarkup(btn,resize_keyboard=True))
        m = await update.effective_chat.send_message(msg,reply_markup=InlineKeyboardMarkup(ibutton))
        context.user_data['p_m'] = m.message_id
        await update.callback_query.answer('video editing mode activated!')
        return
    
    elif query == 'telegramUpload':
        await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=context.user_data['p_m'])
        m = await update.effective_chat.send_message("Upload a video to the chat (maximum 20MB) without compression ⚠️ Format: mp4 / avi")
        context.user_data['mode'] = 'telegramVideo'
        context.user_data['p_m'] = m.message_id
        await update.callback_query.answer('OK')
        return
    elif query == 'googleUpload':
        await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=context.user_data['p_m'])
        btn = [[InlineKeyboardButton("mp4",callback_data='mp4'),InlineKeyboardButton("avi",callback_data='avi')]]
        m = await update.effective_chat.send_message("Select the video format on your Google Drive",reply_markup=InlineKeyboardMarkup(btn))        
        context.user_data['p_m'] = m.message_id
        await update.callback_query.answer('google drive upload')
        return
    elif query == 'mp4' or query == 'avi':
        context.user_data['format'] = '.'+query
        await context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=context.user_data['p_m'])
        msg = 'Your video format is mp4. Send Google Drive link.\nBe sure to set access to the file for those who have the link.\nLink format: https://drive.google.com/file/d/1aBCDEF2GhIjK3lMnop4_QrsTUVwxYzAB/view?usp=sharing'
        m = await update.effective_chat.send_message(msg)
        with open(os.path.join(base,'drive.jpg'),'rb') as f:
            await update.effective_chat.send_photo(f)
        
        #await update.effective_chat.send_photo()
        context.user_data['mode'] = 'googleVideo'
        context.user_data['p_m'] = m.message_id
        await update.callback_query.answer(query)
        return    

    elif query in imageoptions and context.user_data['type']=='image':
        if 'edit' in context.user_data.keys():

            if query in context.user_data['edit']:
                context.user_data['edit'].remove(query)
                buttons = []
                #buttons.pop(idx)

                for i in range(len(imageoptions)):
                    if imageoptions[i] in context.user_data['edit']:
                        txt = "{0} {1}".format('✅',imageoptions[i])
                        buttons.append([InlineKeyboardButton(txt,callback_data=imageoptions[i])])
                    else:
                        txt = "{0} {1}".format('❌',imageoptions[i])
                        buttons.append([InlineKeyboardButton(txt,callback_data=imageoptions[i])])

                buttons.append([InlineKeyboardButton("CONFIRM",callback_data="sendEdit")])
                await context.bot.deleteMessage(update.effective_chat.id,context.user_data['p_m'])
                m = await update.effective_chat.send_message('set checkboxes on the options you like',reply_markup=InlineKeyboardMarkup(buttons))
                print(context.user_data['edit'])
                context.user_data['p_m'] = m.message_id
                return

            else:
                context.user_data['edit'].append(query)
                buttons = []
                for i in range(len(imageoptions)):
                    if imageoptions[i] in context.user_data['edit']:
                        txt = "{0} {1}".format('✅',imageoptions[i])
                        buttons.append([InlineKeyboardButton(txt,callback_data=imageoptions[i])])
                    else:
                        txt = "{0} {1}".format('❌',imageoptions[i])
                        buttons.append([InlineKeyboardButton(txt,callback_data=imageoptions[i])])
                buttons.append([InlineKeyboardButton("CONFIRM",callback_data="sendEdit")])
                await context.bot.deleteMessage(update.effective_chat.id,context.user_data['p_m'])

                m = await update.effective_chat.send_message('set checkboxes on the options you like',reply_markup=InlineKeyboardMarkup(buttons))
                context.user_data['p_m'] = m.message_id
                return
        else:
            context.user_data['edit'] = []
            context.user_data['edit'].append(query)
            print(context.user_data['edit'])
            buttons = []
            for i in range(len(imageoptions)):
                if imageoptions[i] in context.user_data['edit']:
                    txt = "{0} {1}".format('✅',imageoptions[i])
                    buttons.append([InlineKeyboardButton(txt,callback_data=imageoptions[i])])
                else:
                    txt = "{0} {1}".format('❌',imageoptions[i])
                    buttons.append([InlineKeyboardButton(txt,callback_data=imageoptions[i])])            
            buttons.append([InlineKeyboardButton("CONFIRM",callback_data="sendEdit")])
            await context.bot.deleteMessage(update.effective_chat.id,context.user_data['p_m'])

            m = await update.effective_chat.send_message('set checkboxes on the options you like',reply_markup=InlineKeyboardMarkup(buttons))
            context.user_data['p_m'] = m.message_id
            return

    
    elif query in editoptions:
        if 'edit' in context.user_data.keys():

            if query in context.user_data['edit']:
                context.user_data['edit'].remove(query)
                buttons = []
                #buttons.pop(idx)

                for i in range(1,len(editoptions)+1):
                    if editoptions[i-1] in context.user_data['edit']:
                        txt = str(i)+") {0} {1}".format('✅',editoptions[i-1])
                        buttons.append([InlineKeyboardButton(txt,callback_data=editoptions[i-1])])
                    else:
                        txt = str(i)+") {0} {1}".format('❌',editoptions[i-1])
                        buttons.append([InlineKeyboardButton(txt,callback_data=editoptions[i-1])])

                buttons.append([InlineKeyboardButton("CONFIRM",callback_data="sendEdit")])
                await context.bot.deleteMessage(update.effective_chat.id,context.user_data['p_m'])
                m = await update.effective_chat.send_message('set checkboxes on the options you like',reply_markup=InlineKeyboardMarkup(buttons))
                print(context.user_data['edit'])
                context.user_data['p_m'] = m.message_id
                return

            else:
                context.user_data['edit'].append(query)
                buttons = []
                for i in range(1,len(editoptions)+1):
                    if editoptions[i-1] in context.user_data['edit']:
                        txt = str(i)+") {0} {1}".format('✅',editoptions[i-1])
                        buttons.append([InlineKeyboardButton(txt,callback_data=editoptions[i-1])])
                    else:
                        txt = str(i)+") {0} {1}".format('❌',editoptions[i-1])
                        buttons.append([InlineKeyboardButton(txt,callback_data=editoptions[i-1])])
                buttons.append([InlineKeyboardButton("CONFIRM",callback_data="sendEdit")])
                await context.bot.deleteMessage(update.effective_chat.id,context.user_data['p_m'])

                m = await update.effective_chat.send_message('set checkboxes on the options you like',reply_markup=InlineKeyboardMarkup(buttons))
                context.user_data['p_m'] = m.message_id
                return
        else:
            context.user_data['edit'] = []
            context.user_data['edit'].append(query)
            print(context.user_data['edit'])
            buttons = []
            for i in range(1,len(editoptions)+1):
                if editoptions[i-1] in context.user_data['edit']:
                    txt = str(i)+") {0} {1}".format('✅',editoptions[i-1])
                    buttons.append([InlineKeyboardButton(txt,callback_data=editoptions[i-1])])
                else:
                    txt = str(i)+") {0} {1}".format('❌',editoptions[i-1])
                    buttons.append([InlineKeyboardButton(txt,callback_data=editoptions[i-1])])            
            buttons.append([InlineKeyboardButton("CONFIRM",callback_data="sendEdit")])
            await context.bot.deleteMessage(update.effective_chat.id,context.user_data['p_m'])

            m = await update.effective_chat.send_message('set checkboxes on the options you like',reply_markup=InlineKeyboardMarkup(buttons))
            context.user_data['p_m'] = m.message_id
            return
    elif query == 'sendEdit':
        await update.callback_query.answer('Confirm!')

        try:

            await context.bot.deleteMessage(update.effective_chat.id,context.user_data['p_m'])
            if context.user_data['type'] == 'image':
                m = await update.effective_chat.send_message('Image editing started.')
                context.user_data['p_m'] = m.message_id
                elist = context.user_data['edit']
                f = context.user_data['file']
                f = editImage(f,update.effective_chat.id,elist)
            else:
                m = await update.effective_chat.send_message('video editing process started! Please wait.')
                context.user_data['p_m'] = m.message_id
                elist = context.user_data['edit']
                
                if context.user_data['mode']=='googleVideo':
                    f = context.user_data['glink']
                    fmt = context.user_data['format']
                    f = editVideo(f,str(update.effective_chat.id),elist,fmt)
                
                else:
                    f = context.user_data['file']

                    f = editVideo(f,str(update.effective_chat.id),elist)
            
            f_link = uploadToDrive(f,drive_id)
            print("\n\n",f_link)
            msg = "<a href='{0}'>{1}</a>".format(f_link,f_link)
            await context.bot.send_message(update.effective_chat.id,msg,parse_mode=ParseMode.HTML,reply_markup=ReplyKeyboardMarkup(mainBtn(),resize_keyboard=True))        
            context.user_data.clear()
        except:
            await update.effective_chat.send_message("Sorry, something went wrong. You may send a broken link or format of the file wrong, be sure to set access to the file for those who have link.",reply_markup=ReplyKeyboardMarkup(mainBtn(),resize_keyboard=True))
            context.user_data.clear()   
    elif query == 'payment':
        await update.callback_query.answer('payment')
        btn = [[InlineKeyboardButton('Go to the payment',callback_data='stripe')],[InlineKeyboardButton('Cancel',callback_data='home')]]
        await update.effective_chat.send_message("You have choosed a Unlimited Creatives tariff- $9 per month.\n Is that correct",reply_markup=InlineKeyboardMarkup(btn))
        return
    elif query == 'stripe':
        await update.callback_query.answer('')
        
        msg = 'To go to the payment page, click on the "Pay" button.\n\nAfter successful payment, click on the button "Check my payment"'
        
        #btn = [[InlineKeyboardButton('Pay Now!',url='https://buy.stripe.com/test_fZe8z4d1T4wb4YocMM')],[InlineKeyboardButton("Check my payment",callback_data='checkPayment')]]
        #update.effective_chat.send_message("Pay Now",reply_markup=InlineKeyboardMarkup(btn))

        l = stripe.PaymentLink.create(
            line_items=[{'price':'price_1M7LROITV27aYUdhO9icaCAR','quantity':'1'}],
            metadata = {'chat_id':update.effective_chat.id}
        )
        btn = [[InlineKeyboardButton('Pay',url=str(l['url']))],[InlineKeyboardButton("Check my payment",callback_data='checkPayment')]]
        await update.effective_chat.send_message(msg,reply_markup=InlineKeyboardMarkup(btn))
        return
    elif query == 'home':
        await update.callback_query.answer('cancel')
        context.user_data.clear()
        await update.effective_chat.send_message("Payment cancel")

    elif query == 'checkPayment':
        await update.callback_query.answer('check payment')
        if checkPayment(update.effective_chat.id):
            msg = 'You have already purchased a tariff:\nunlimited Creatives.\n\nNumber of remaining to be edited videos: 999'
            
            customer = executeSql("select customer_id from users where chat_id={0}".format(update.effective_chat.id))
            customer = customer[0][0]
            cus = stripe.billing_portal.Session.create(customer=customer)
            btn = [[InlineKeyboardButton('Customer portal',url=cus['url'])]]
            await update.effective_chat.send_message(msg,reply_markup=InlineKeyboardMarkup(btn))
            return
        else:
            await update.effective_chat.send_message("Error! Your transaction was not found. if you really paid, then provide proof to technical support!")
            return
    
    elif query == 'referral':
        await update.effective_chat.send_message("Enter invite code")
        context.user_data['mode'] = 'referral'
        await update.callback_query.answer("refferal")
        return
    elif query == 'No Referral':
        await update.callback_query.answer("Okay")
        executeSql("update users set referred_by=0 where chat_id={0}".format(update.effective_chat.id),"commit")

if __name__ == '__main__':
    application = ApplicationBuilder().token(soullabs).concurrent_updates(True).build()
    
    start_handler = CommandHandler('start', start)
    file_handler = MessageHandler(filters.VIDEO | filters.PHOTO | filters.ATTACHMENT,fileHandler)
    msg_handler = MessageHandler(filters.TEXT,msgHandler)
    query_handler = CallbackQueryHandler(queryHandler)
    application.add_handler(start_handler)
    application.add_handler(file_handler)
    application.add_handler(msg_handler)
    application.add_handler(query_handler)
    
    application.run_polling()
