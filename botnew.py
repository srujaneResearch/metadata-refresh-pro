from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler,filters
from telegram import *

import pandas as pd
#from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext
import json
soullabs = "5855809302:AAGaZX7__rCZsbb_pqu0VAm2r76HO1pcqhU"
#updater = Updater(soullabs,use_context=True)
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

from moviepy.editor import VideoFileClip,AudioFileClip,CompositeAudioClip,afx,vfx
import urllib
import time
import pyodbc
import locale
#import util
from datetime import datetime, timedelta
from urllib.parse import quote
import socket
import requests
import random
telegram_url = 'https://api.telegram.org/bot'+soullabs
from dateutil import relativedelta
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
stripe_key = '284685063:TEST:Nzg4ODRhNGVkYzU3'
def editVideo(path,chat_id,edits):
    l=None
    with VideoFileClip(path) as clip:
        for _ in edits:

            if _ == 'Installing mesh':
                pass
            elif _ == 'Color correction':
                clip = colorCorrection(clip)
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
            elif _ == 'Crop video':
                clip = crop(clip)
                continue
            elif _ == 'Speed up audio':
                clip = accelerateAudio(clip)
                continue

        final = clip.write_videofile('{0}.mp4'.format(chat_id))
        if l != None:
            l.close()
        return '{0}.mp4'.format(chat_id)            





def crop(clip):
    #crop video by 10%-30% at the beginning and at the end
    dur = clip.duration
    n = random.randrange(10,30)
    n = n/100
    clip1 = clip.subclip(n*dur,)
    clip2 = clip1.subclip(0,dur-(n*dur))
    #final = clip2.write_videofile('{0}.avi'.format(chat_id),fps=clip.fps,codec='libx264')
    return clip2



def replaceMusicJoyful(clip):
    l = AudioFileClip('joy.mp3')
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
    #clip = clip.fx(vfx.colorx,1.05)
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
        [KeyboardButton('Tech. Support💻'),KeyboardButton('About Bot 🤖')]
    ]
    return buttons

def editBtns():
    buttons = [ [InlineKeyboardButton("1) ❌ Installing mesh",callback_data='Installing mesh')],
                [InlineKeyboardButton("2) ❌ Color correction",callback_data='Color correction')],
                [InlineKeyboardButton("3) ❌ Replacing music (joyful)",callback_data='Replacing music (joyful)')],
                [InlineKeyboardButton("4) ❌ Replacing music (disturbing)",callback_data='Replacing music (disturbing)')],
                [InlineKeyboardButton("5) ❌ Removing metadata",callback_data='Removing metadata')],
                [InlineKeyboardButton("6) ❌ Reducing video fps",callback_data='Reducing video fps')],
                [InlineKeyboardButton("7) ❌ Crop video",callback_data='Crop video')],
                [InlineKeyboardButton("8) ❌ Speed up audio",callback_data='Speed up audio')],
                [InlineKeyboardButton("CONFIRM",callback_data="sendEdit")]          
             ]
    return buttons

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_message(startmsg,reply_markup=ReplyKeyboardMarkup(mainBtn(),resize_keyboard=True))
    return


async def msgHandler(update: Update, context:ContextTypes.DEFAULT_TYPE ):
    
    if update.message.text == 'Upload a video🎥':
        #check userplan
        msg = 'To switch to the mode of uploading video to the bot, click on the button below. The bot sees your file only in this mode.'
        inlinebtn = [[InlineKeyboardButton('Upload video mode',callback_data='videoMode')]]
        
        await update.effective_chat.send_message(msg,reply_markup=InlineKeyboardMarkup(inlinebtn))
        return
    
    elif update.message.text == '❌ Cancel':
        context.user_data.clear()
        await start(update,context)
        return
    
    elif update.message.text == 'Tariffs and payment💳':
        # check if user is registered or not!
        btn = [[InlineKeyboardButton('Unlimited creative',callback_data='payment')],[InlineKeyboardButton('back',callback_data='home')]]
        await update.effective_chat.send_message('List of our tariffs:\n\nUnlimited Creatives- $9 per month',reply_markup=InlineKeyboardMarkup(btn))
        return

async def fileHandler(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if 'mode' in context.user_data.keys():
            print("yes")    
            allowed = ['mp4','MP4','avi']
            if context.user_data['mode'] == 'telegramVideo':
                v = update.message.video
                print(v)
                if 'mp4' not in v['mime_type']:
                    await update.effective_chat.send_message("Wrong format media!")
                    context.user_data.clear()
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
                    context.user_data.clear()
                    context.user_data['file'] = f.file_path.split('videos/')[1]
                    print(context.user_data['file'])
                    msg = 'The video is downloaded. Choose ways to edit.\n\
                            1) Installing a transparent and invisible mesh\n\
                            2) Small color correction for gamma, saturation and contrast\n\
                            3) Replacing music with another, no copyright (joyful)\n\
                            4) Replacing music with another, no copyright (disturbing)\n\
                            5) Removing metadata\n\
                            6) Reducing video fps by 10-15 frames\n\
                            7) Crop video by 10-30% at the beginning and at the end\n\
                            8) Acceleration of the audio track by 5-10%'
                    await update.effective_chat.send_message(msg)
                    await update.effective_chat.send_message('Set checkboxes on the options you like',reply_markup=InlineKeyboardMarkup(editBtns()))
                    return


async def queryHandler(update: Update,context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query.data

    editoptions = ['Installing mesh',
            'Color correction',
             'Replacing music (joyful)',
             'Replacing music (disturbing)',
             'Removing metadata',
             'Reducing video fps',
             'Crop video',
             'Speed up audio'
            ]

    if query == 'videoMode':
        # check tarrif!
        msg = 'Choose how you want to send your video in telegram chat or link to google Drive.'
        ibutton = [[InlineKeyboardButton('Telegram chat',callback_data='telegramUpload'),InlineKeyboardButton('Google Drive',callback_data='googleUpload')]]
        btn = [[KeyboardButton('❌ Cancel')]]
        await update.effective_chat.send_message('You have unlimited tariff.',reply_markup=ReplyKeyboardMarkup(btn,resize_keyboard=True))
        await update.effective_chat.send_message(msg,reply_markup=InlineKeyboardMarkup(ibutton))
        await update.callback_query.answer('video editing mode activated!')
        return
    
    elif query == 'telegramUpload':
        await update.effective_chat.send_message("Upload a video to the chat (maximum 20MB) without compression ⚠️ Format: mp4 / avi")
        context.user_data['mode'] = 'telegramVideo'
        return
    
    elif query in editoptions:
        if 'edit' in context.user_data.keys():

            if query in context.user_data['edit']:
                context.user_data['edit'].remove(query)
                buttons = []
                #buttons.pop(idx)

                for i in range(len(editoptions)):
                    if editoptions[i] in context.user_data['edit']:
                        txt = str(i)+") {0} {1}".format('✅',editoptions[i])
                        buttons.append([InlineKeyboardButton(txt,callback_data=editoptions[i])])
                    else:
                        txt = str(i)+") {0} {1}".format('❌',editoptions[i])
                        buttons.append([InlineKeyboardButton(txt,callback_data=editoptions[i])])

                buttons.append([InlineKeyboardButton("CONFIRM",callback_data="sendEdit")])
                await update.effective_chat.send_message('set checkboxes on the options you like',reply_markup=InlineKeyboardMarkup(buttons))
                print(context.user_data['edit'])
                return

            else:
                context.user_data['edit'].append(query)
                buttons = []
                for i in range(len(editoptions)):
                    if editoptions[i] in context.user_data['edit']:
                        txt = str(i)+") {0} {1}".format('✅',editoptions[i])
                        buttons.append([InlineKeyboardButton(txt,callback_data=editoptions[i])])
                    else:
                        txt = str(i)+") {0} {1}".format('❌',editoptions[i])
                        buttons.append([InlineKeyboardButton(txt,callback_data=editoptions[i])])
                buttons.append([InlineKeyboardButton("CONFIRM",callback_data="sendEdit")])
                await update.effective_chat.send_message('set checkboxes on the options you like',reply_markup=InlineKeyboardMarkup(buttons))
                return
        else:
            context.user_data['edit'] = []
            context.user_data['edit'].append(query)
            print(context.user_data['edit'])
            buttons = []
            for i in range(len(editoptions)):
                if editoptions[i] in context.user_data['edit']:
                    txt = str(i)+") {0} {1}".format('✅',editoptions[i])
                    buttons.append([InlineKeyboardButton(txt,callback_data=editoptions[i])])
                else:
                    txt = str(i)+") {0} {1}".format('❌',editoptions[i])
                    buttons.append([InlineKeyboardButton(txt,callback_data=editoptions[i])])            
            buttons.append([InlineKeyboardButton("CONFIRM",callback_data="sendEdit")])
            await update.effective_chat.send_message('set checkboxes on the options you like',reply_markup=InlineKeyboardMarkup(buttons))
            return
    elif query == 'sendEdit':
        await update.effective_chat.send_message('video editing process started! Please wait.')
        elist = context.user_data['edit']
        f = context.user_data['file']

        f = editVideo(f,str(update.effective_chat.id),elist)
        with open(f,'rb') as sfile:
            await update.effective_chat.send_video(sfile)
        
        context.user_data.clear()
    
    elif query == 'payment':
        btn = [[InlineKeyboardButton('Go to the payment',callback_data='stripe')],[InlineKeyboardButton('Cancel',callback_data='home')]]
        update.effective_chat.send_message("You have choosed a Unlimited Creatives tariff- $9 per month.\n Is that correct",reply_markup=InlineKeyboardMarkup(btn))
        return
    elif query == 'stripe':
        expiry = datetime.now()-relativedelta.relativedelta(month=1)
        expiry = expiry.strftime("%y/%m/%d")
        description = 'Unlimited Tarrif Plan\nRenews at {0}'.format(expiry)
        btn = [[InlineKeyboardButton('Pay Now!',url='https://buy.stripe.com/test_fZe8z4d1T4wb4YocMM')]]
        #update.effective_chat.send_message("Pay Now",reply_markup=InlineKeyboardMarkup(btn))
        '''
        update.effective_chat.send_invoice(title='Metadata Refresh Pro\nUnlimited',
                                            description='Unlimited Tarrif plan\n',
                                            payload='subscription',
                                            photo_url='https://img.freepik.com/premium-vector/bot-chat-say-hi-robots-that-are-programmed-talk-customers-online_68708-622.jpg?w=2000',
                                            provider_token=stripe_key,
                                            currency='USD',
                                            prices=[LabeledPrice('Unlimited Tarrif',amount=9*100)]
                                            )
        '''
        return



def preCheckout(update:Update,context:ContextTypes.DEFAULT_TYPE):
    """Answers the PreQecheckoutQuery, important to handel payment"""
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != "subscription": #same string used in sendInvoice method, refer elif context.user_data['point'] == 'Payment' section and observe the parameters
        # answer False pre_checkout_query
        query.answer(ok=False, error_message="Something went wrong..")
    else:
        query.answer(ok=True)

def paymentSuccess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirms the successful payment. this method is invoked after a successful payment"""
    
    update.message.reply_text("We have received your payment, Thank you!")
    #k = datetime.now() #get the accurate time
    #k=k.strftime("Ref:D%d/%m/%yT%H:%M:%S") #format the datetime
    #create the summary as per the format
    #summary = context.user_data['msg']+"\n\n"+"Payment Received\n"+ k+str(update.effective_chat.id)+"\n----------------------------------\n"+"From User : {0}".format(update.effective_chat.username)
    context.user_data.clear() #clear the user_data after process completes.









if __name__ == '__main__':
    application = ApplicationBuilder().token(soullabs).concurrent_updates(True).build()
    
    start_handler = CommandHandler('start', start)
    file_handler = MessageHandler(filters.VIDEO,fileHandler)
    msg_handler = MessageHandler(filters.TEXT,msgHandler)
    query_handler = CallbackQueryHandler(queryHandler)
    application.add_handler(start_handler)
    application.add_handler(file_handler)
    application.add_handler(msg_handler)
    application.add_handler(query_handler)
    
    application.run_polling()
