import sys
from pathlib import Path

# add project root to path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import datetime as dt
import telebot
from telebot import types

import libs.lehaam_pieces as lp
from libs.bot_messages import get_message, format_time_result

# bot token from BotFather
TOKEN = "8468679708:AAGPUvGLfxILId7aHPxY8QWBG-g1FJWgKZc"

bot = telebot.TeleBot(TOKEN)

# default timezone offset
DEFAULT_TIMEZONE_OFFSET = '+03:30'  # Tehran

# user data storage (language preferences)
user_data = {}

# conversation states
WAITING_SLEEP_TIME = 'waiting_sleep_time'
WAITING_WAKE_TIME = 'waiting_wake_time'
WAITING_TIMEZONE = 'waiting_timezone'
user_states = {}


def get_user_lang(user_id:int) -> str:
    """get user's selected language, default to english"""
    return user_data.get(user_id, {}).get('lang', 'en')


def set_user_lang(user_id:int, lang:str):
    """set user's language preference"""
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]['lang'] = lang


def get_user_timezone_offset(user_id:int) -> str:
    """get user's timezone offset, default to Tehran (+03:30)"""
    return user_data.get(user_id, {}).get('timezone_offset', DEFAULT_TIMEZONE_OFFSET)


def set_user_timezone_offset(user_id:int, offset:str):
    """set user's timezone offset preference"""
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]['timezone_offset'] = offset


def parse_timezone_offset(offset_str:str):
    """parse timezone offset string like +03:30 or -05:00"""
    try:
        # remove spaces
        offset_str = offset_str.strip()
        
        # handle UTC/0
        if offset_str == '0' or offset_str.upper() == 'UTC':
            return dt.timedelta(0)
        
        # check format
        if offset_str[0] not in ['+', '-']:
            raise ValueError("must start with + or -")
        
        sign = 1 if offset_str[0] == '+' else -1
        time_part = offset_str[1:]
        
        if ':' in time_part:
            hours, minutes = map(int, time_part.split(':'))
        else:
            hours = int(time_part)
            minutes = 0
        
        return sign * dt.timedelta(hours=hours, minutes=minutes)
    except:
        return None


def get_current_time_with_offset(offset_str:str) -> dt.datetime:
    """get current UTC time adjusted by offset"""
    try:
        offset = parse_timezone_offset(offset_str)
        if offset is None:
            # fallback to default
            offset = parse_timezone_offset(DEFAULT_TIMEZONE_OFFSET)
        
        utc_now = dt.datetime.utcnow()
        return utc_now + offset
    except:
        # ultimate fallback
        return dt.datetime.now()


def validate_timezone_offset(offset_str:str) -> bool:
    """validate timezone offset format"""
    return parse_timezone_offset(offset_str) is not None


def set_user_state(user_id:int, state:str):
    """set user's conversation state"""
    user_states[user_id] = state


def get_user_state(user_id:int) -> str:
    """get user's conversation state"""
    return user_states.get(user_id, None)


def clear_user_state(user_id:int):
    """clear user's conversation state"""
    if user_id in user_states:
        del user_states[user_id]


def get_language_keyboard():
    """create language selection keyboard"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_en = types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
    btn_fa = types.InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa")
    markup.add(btn_en, btn_fa)
    return markup


def get_main_menu_keyboard(lang:str):
    """create main menu keyboard"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn_sleep_now = types.InlineKeyboardButton(
        get_message(lang, "btn_sleep_now"), 
        callback_data="sleep_now"
    )
    btn_sleep_at = types.InlineKeyboardButton(
        get_message(lang, "btn_sleep_at"), 
        callback_data="sleep_at"
    )
    btn_wake_at = types.InlineKeyboardButton(
        get_message(lang, "btn_wake_at"), 
        callback_data="wake_at"
    )
    btn_about = types.InlineKeyboardButton(
        get_message(lang, "btn_about"), 
        callback_data="about"
    )
    btn_settings = types.InlineKeyboardButton(
        get_message(lang, "btn_settings"), 
        callback_data="settings"
    )
    btn_change_lang = types.InlineKeyboardButton(
        get_message(lang, "btn_change_lang"), 
        callback_data="change_lang"
    )
    
    markup.add(btn_sleep_now, btn_sleep_at, btn_wake_at, btn_about, btn_settings, btn_change_lang)
    return markup


def get_about_keyboard(lang:str):
    """create about menu keyboard"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn_cycles = types.InlineKeyboardButton(
        get_message(lang, "btn_about_cycles"), 
        callback_data="about_cycles"
    )
    btn_timing = types.InlineKeyboardButton(
        get_message(lang, "btn_about_timing"), 
        callback_data="about_timing"
    )
    btn_calc = types.InlineKeyboardButton(
        get_message(lang, "btn_about_calc"), 
        callback_data="about_calc"
    )
    btn_tips = types.InlineKeyboardButton(
        get_message(lang, "btn_about_tips"), 
        callback_data="about_tips"
    )
    btn_back = types.InlineKeyboardButton(
        get_message(lang, "btn_back"), 
        callback_data="back"
    )
    
    markup.add(btn_cycles, btn_timing, btn_calc, btn_tips, btn_back)
    return markup


def get_back_keyboard(lang:str):
    """create simple back button keyboard"""
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton(
        get_message(lang, "btn_back"), 
        callback_data="back"
    )
    markup.add(btn_back)
    return markup


def get_settings_keyboard(lang:str):
    """create settings menu keyboard"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn_timezone = types.InlineKeyboardButton(
        get_message(lang, "btn_timezone"),
        callback_data="settings_timezone"
    )
    btn_back = types.InlineKeyboardButton(
        get_message(lang, "btn_back"),
        callback_data="back"
    )
    
    markup.add(btn_timezone, btn_back)
    return markup


def get_timezone_back_keyboard(lang:str):
    """simple back button for timezone setting"""
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton(
        get_message(lang, "btn_back"),
        callback_data="settings"
    )
    markup.add(btn_back)
    return markup


@bot.message_handler(commands=['start'])
def start_command(message):
    """handle /start command - show language selection"""
    user_id = message.from_user.id
    clear_user_state(user_id)
    
    bot.send_message(
        message.chat.id,
        get_message('en', 'welcome'),
        reply_markup=get_language_keyboard()
    )


@bot.message_handler(commands=['cancel'])
def cancel_command(message):
    """cancel current operation"""
    user_id = message.from_user.id
    lang = get_user_lang(user_id)
    clear_user_state(user_id)
    
    bot.send_message(
        message.chat.id,
        get_message(lang, 'cancel'),
        reply_markup=get_main_menu_keyboard(lang),
        parse_mode='Markdown'
    )


def handle_settings(call, user_id, lang):
    """handle settings menu"""
    if call.data == "settings":
        clear_user_state(user_id)
        bot.edit_message_text(
            get_message(lang, 'settings_menu'),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_settings_keyboard(lang),
            parse_mode='Markdown'
        )
        return True
    
    elif call.data == "settings_timezone":
        current_offset = get_user_timezone_offset(user_id)
        set_user_state(user_id, WAITING_TIMEZONE)
        bot.edit_message_text(
            get_message(lang, 'timezone_prompt').format(current_offset),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_timezone_back_keyboard(lang),
            parse_mode='Markdown'
        )
        return True
    
    return False


@bot.callback_query_handler(func=lambda call:True)
def callback_handler(call):
    """handle button presses"""
    user_id = call.from_user.id
    lang = get_user_lang(user_id)
    
    try:
        # language selection
        if call.data == "lang_en":
            set_user_lang(user_id, 'en')
            clear_user_state(user_id)
            bot.edit_message_text(
                get_message('en', 'language_selected'),
                call.message.chat.id,
                call.message.message_id
            )
            bot.send_message(
                call.message.chat.id,
                get_message('en', 'main_menu'),
                reply_markup=get_main_menu_keyboard('en'),
                parse_mode='Markdown'
            )
        
        elif call.data == "lang_fa":
            set_user_lang(user_id, 'fa')
            clear_user_state(user_id)
            bot.edit_message_text(
                get_message('fa', 'language_selected'),
                call.message.chat.id,
                call.message.message_id
            )
            bot.send_message(
                call.message.chat.id,
                get_message('fa', 'main_menu'),
                reply_markup=get_main_menu_keyboard('fa'),
                parse_mode='Markdown'
            )
        
        # change language
        elif call.data == "change_lang":
            clear_user_state(user_id)
            bot.edit_message_text(
                get_message('en', 'welcome'),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_language_keyboard()
            )
        # back to main menu
        elif call.data == "back":
            clear_user_state(user_id)
            bot.edit_message_text(
                get_message(lang, 'main_menu'),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_main_menu_keyboard(lang),
                parse_mode='Markdown'
            )
        
        # sleep now
        elif call.data == "sleep_now":
            clear_user_state(user_id)
            user_offset = get_user_timezone_offset(user_id)
            now = get_current_time_with_offset(user_offset)
            wake_times = lp.calculate_wake_times(now)
            
            result = format_time_result(
                lang, wake_times, "sleep_now_result",
                f"{now.hour:02d}", f"{now.minute:02d}"
            )
            
            bot.edit_message_text(
                result,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard(lang),
                parse_mode='Markdown'
            )
        
        # sleep at
        elif call.data == "sleep_at":
            set_user_state(user_id, WAITING_SLEEP_TIME)
            bot.edit_message_text(
                get_message(lang, 'sleep_at_prompt'),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard(lang),
                parse_mode='Markdown'
            )
        
        # wake at
        elif call.data == "wake_at":
            set_user_state(user_id, WAITING_WAKE_TIME)
            bot.edit_message_text(
                get_message(lang, 'wake_at_prompt'),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_back_keyboard(lang),
                parse_mode='Markdown'
            )
        
        # about menu
        elif call.data == "about":
            clear_user_state(user_id)
            bot.edit_message_text(
                get_message(lang, 'about_title'),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_about_keyboard(lang),
                parse_mode='Markdown'
            )
        
        # about sections
        elif call.data == "about_cycles":
            bot.edit_message_text(
                get_message(lang, 'about_cycles'),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_about_keyboard(lang),
                parse_mode='Markdown'
            )
        
        elif call.data == "about_timing":
            bot.edit_message_text(
                get_message(lang, 'about_timing'),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_about_keyboard(lang),
                parse_mode='Markdown'
            )
        
        elif call.data == "about_calc":
            bot.edit_message_text(
                get_message(lang, 'about_calculation'),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_about_keyboard(lang),
                parse_mode='Markdown'
            )
        
        elif call.data == "about_tips":
            bot.edit_message_text(
                get_message(lang, 'about_tips'),
                call.message.chat.id,
                call.message.message_id,
                reply_markup=get_about_keyboard(lang),
                parse_mode='Markdown'
            )
        
        # settings
        if handle_settings(call, user_id, lang):
            bot.answer_callback_query(call.id)
            return
        
        # answer callback to remove loading state
        bot.answer_callback_query(call.id)
        
    except Exception as e:
        print(f"error in callback handler : {e}")
        bot.answer_callback_query(call.id, "error occurred!")

@bot.message_handler(func=lambda message:True)
def handle_text_messages(message):
    """handle text messages (time inputs)"""
    user_id = message.from_user.id
    lang = get_user_lang(user_id)
    state = get_user_state(user_id)

    # handle timezone offset input
    if state == WAITING_TIMEZONE:
        offset_str = message.text.strip()
        
        if validate_timezone_offset(offset_str):
            # normalize format
            if offset_str == '0':
                offset_str = '+00:00'
            
            set_user_timezone_offset(user_id, offset_str)
            clear_user_state(user_id)
            
            bot.send_message(
                message.chat.id,
                get_message(lang, 'timezone_changed').format(offset_str),
                parse_mode='Markdown'
            )
            
            # show main menu
            import time
            time.sleep(1)
            
            bot.send_message(
                message.chat.id,
                get_message(lang, 'main_menu'),
                reply_markup=get_main_menu_keyboard(lang),
                parse_mode='Markdown'
            )
            return
        else:
            bot.send_message(
                message.chat.id,
                get_message(lang, 'invalid_timezone'),
                parse_mode='Markdown'
            )
            return

    # handle sleep at time input
    if state == WAITING_SLEEP_TIME:
        try:
            hour, minute = map(int, message.text.strip().split(':'))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError()
            
            user_offset = get_user_timezone_offset(user_id)
            now = get_current_time_with_offset(user_offset)
            wake_times = lp.calculate_wake_times_from_sleep_at(now, hour, minute)
            
            result = format_time_result(
                lang, wake_times, "sleep_at_result",
                f"{hour:02d}", f"{minute:02d}", f"{hour:02d}", f"{minute:02d}"
            )
            
            clear_user_state(user_id)
            bot.send_message(
                message.chat.id,
                result,
                reply_markup=get_back_keyboard(lang),
                parse_mode='Markdown'
            )
            
        except (ValueError, AttributeError):
            bot.send_message(
                message.chat.id,
                get_message(lang, 'invalid_time'),
                parse_mode='Markdown'
            )

    # handle wake at time input
    elif state == WAITING_WAKE_TIME:
        try:
            hour, minute = map(int, message.text.strip().split(':'))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError()
            
            user_offset = get_user_timezone_offset(user_id)
            now = get_current_time_with_offset(user_offset)
            sleep_times = lp.calculate_sleep_times_from_wake_at(now, hour, minute)
            
            result = format_time_result(
                lang, sleep_times, "wake_at_result",
                f"{hour:02d}", f"{minute:02d}", f"{hour:02d}", f"{minute:02d}"
            )
            
            clear_user_state(user_id)
            bot.send_message(
                message.chat.id,
                result,
                reply_markup=get_back_keyboard(lang),
                parse_mode='Markdown'
            )
            
        except (ValueError, AttributeError):
            bot.send_message(
                message.chat.id,
                get_message(lang, 'invalid_time'),
                parse_mode='Markdown'
            )

    # no active state - show main menu
    else:
        bot.send_message(
            message.chat.id,
            get_message(lang, 'main_menu'),
            reply_markup=get_main_menu_keyboard(lang),
            parse_mode='Markdown'
        )


def main():
    """Start the bot"""
    print("🤖 Lehaam bot is running...")
    print("press Ctrl+C to stop")
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\n👋 bot stopped!")

if __name__ == '__main__':
    main()
#MadMad_575