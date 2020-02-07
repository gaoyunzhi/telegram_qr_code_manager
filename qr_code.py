#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, MessageHandler, Filters
import time
import os
import traceback as tb
from telegram_util import getDisplayUser, log_on_fail, getTmpFile, autoDestroy, matchKey
import yaml
import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image

with open('credential') as f:
    credential = yaml.load(f, Loader=yaml.FullLoader)

updater = Updater(credential['token'], use_context=True)
tele = updater.bot
debug_group = tele.get_chat(-1001198682178)
this_bot = tele.id


@log_on_fail(debug_group)
def handlePrivate(update, context):
    msg = update.effective_message
    msg.forward(debug_group.id)
    usr = update.effective_user.username 
    if not msg.photo:
    	return
    photo = msg.photo
    os.system('mkdir photo > /dev/null 2>&1')
    filename = 'photo/%s_%d' % (usr, msg.message_id)
    photo[0].get_file().download(filename)
    msg.reply_text('received')
    

@log_on_fail(debug_group)
def handleCommand(update, context):
    msg = update.effective_message
    msg.forward(debug_group.id)
    usr = update.effective_user.username
    for filename in os.listdir('photo/'):
    	if not filename.startswith(usr):
    		continue
    	msg.reply_text(pytesseract.image_to_string(Image.open('photo/' + filename)))
    

dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.private and (~Filters.command), handlePrivate))
dp.add_handler(MessageHandler(Filters.private and Filters.command, handleCommand))

updater.start_polling()
updater.idle()