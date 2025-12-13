import sys
from pathlib import Path

# add project root to path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import datetime as dt
import logging
import telebot
from telebot import types

import libs.lehaam_pieces as lp
from libs.bot_messages import get_message, format_time_result
from libs.user_storage import load_user_data, get_user_data, set_user_data
from libs.bot_handlers import BotHandlers

# setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# bot token from BotFather
TOKEN = "8468679708:AAEbDAcd3GnuCPtFYiw-crr1IkDvRaVvsIY"

bot = telebot.TeleBot(TOKEN)

# default timezone offset
DEFAULT_TIMEZONE_OFFSET = '+03:30'  # Tehran

# load user data from file
user_data = load_user_data()
logger.info(f"loaded data for {len(user_data)} users")

# conversation states
WAITING_SLEEP_TIME = 'waiting_sleep_time'
WAITING_WAKE_TIME = 'waiting_wake_time'
WAITING_TIMEZONE = 'waiting_timezone'
user_states = {}


def get_user_lang(user_id:int) -> str:
    """get user's selected language, default to english"""
    return get_user_data(user_data, user_id, 'lang', 'en')


def set_user_lang(user_id:int, lang:str):
    """set user's language preference"""
    set_user_data(user_data, user_id, 'lang', lang)
    logger.info(f"user {user_id} language set to {lang}")


def get_user_timezone_offset(user_id:int) -> str:
    """get user's timezone offset, default to Tehran (+03:30)"""
    return get_user_data(user_data, user_id, 'timezone_offset', DEFAULT_TIMEZONE_OFFSET)


def set_user_timezone_offset(user_id:int, offset:str):
    """set user's timezone offset preference"""
    set_user_data(user_data, user_id, 'timezone_offset', offset)
    logger.info(f"user {user_id} timezone set to {offset}")


def parse_timezone_offset(offset_str:str):
    """parse timezone offset string like +03:30 or -05:00"""
    try:
        offset_str = offset_str.strip()
        
        if offset_str == '0' or offset_str.upper() == 'UTC':
            return dt.timedelta(0)
        
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
    except Exception as e:
        logger.warning(f"failed to parse timezone offset '{offset_str}': {e}")
        return None


def get_current_time_with_offset(offset_str:str) -> dt.datetime:
    """get current UTC time adjusted by offset"""
    try:
        offset = parse_timezone_offset(offset_str)
        if offset is None:
            offset = parse_timezone_offset(DEFAULT_TIMEZONE_OFFSET)
        
        utc_now = dt.datetime.utcnow()
        return utc_now + offset
    except Exception as e:
        logger.error(f"error getting time with offset: {e}")
        return dt.datetime.now()


def validate_timezone_offset(offset_str:str) -> bool:
    """validate timezone offset format"""
    return parse_timezone_offset(offset_str) is not None


def set_user_state(user_id:int, state:str):
    """set user's conversation state"""
    user_states[user_id] = state
    logger.debug(f"user {user_id} state set to {state}")


def get_user_state(user_id:int) -> str:
    """get user's conversation state"""
    return user_states.get(user_id, None)


def clear_user_state(user_id:int):
    """clear user's conversation state"""
    if user_id in user_states:
        del user_states[user_id]
        logger.debug(f"user {user_id} state cleared")


# keyboard generators
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
    
    buttons = [
        types.InlineKeyboardButton(get_message(lang, "btn_sleep_now"), callback_data="sleep_now"),
        types.InlineKeyboardButton(get_message(lang, "btn_sleep_at"), callback_data="sleep_at"),
        types.InlineKeyboardButton(get_message(lang, "btn_wake_at"), callback_data="wake_at"),
        types.InlineKeyboardButton(get_message(lang, "btn_about"), callback_data="about"),
        types.InlineKeyboardButton(get_message(lang, "btn_settings"), callback_data="settings"),
        types.InlineKeyboardButton(get_message(lang, "btn_change_lang"), callback_data="change_lang"),
    ]
    
    markup.add(*buttons)
    return markup


def get_about_keyboard(lang:str):
    """create about menu keyboard"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    buttons = [
        types.InlineKeyboardButton(get_message(lang, "btn_about_cycles"), callback_data="about_cycles"),
        types.InlineKeyboardButton(get_message(lang, "btn_about_timing"), callback_data="about_timing"),
        types.InlineKeyboardButton(get_message(lang, "btn_about_calc"), callback_data="about_calc"),
        types.InlineKeyboardButton(get_message(lang, "btn_about_tips"), callback_data="about_tips"),
        types.InlineKeyboardButton(get_message(lang, "btn_back"), callback_data="back"),
    ]
    
    markup.add(*buttons)
    return markup


def get_back_keyboard(lang:str):
    """create simple back button keyboard"""
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton(get_message(lang, "btn_back"), callback_data="back")
    markup.add(btn_back)
    return markup


def get_settings_keyboard(lang:str):
    """create settings menu keyboard"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn_timezone = types.InlineKeyboardButton(get_message(lang, "btn_timezone"), callback_data="settings_timezone")
    btn_back = types.InlineKeyboardButton(get_message(lang, "btn_back"), callback_data="back")
    
    markup.add(btn_timezone, btn_back)
    return markup


def get_timezone_back_keyboard(lang:str):
    """simple back button for timezone setting"""
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton(get_message(lang, "btn_back"), callback_data="settings")
    markup.add(btn_back)
    return markup


# initialize handlers
keyboards = {
    'language': get_language_keyboard,
    'main_menu': get_main_menu_keyboard,
    'about': get_about_keyboard,
    'back': get_back_keyboard,
    'settings': get_settings_keyboard,
    'timezone_back': get_timezone_back_keyboard,
}

handlers = BotHandlers(bot, user_states, keyboards)


@bot.message_handler(commands=['start'])
def start_command(message):
    """handle /start command - show language selection or main menu"""
    user_id = message.from_user.id
    clear_user_state(user_id)
    
    # check if user already has a language set
    user_lang = get_user_lang(user_id)
    
    logger.info(f"user {user_id} started bot (lang: {user_lang})")
    
    # if user already has language, show main menu
    if user_lang and user_lang in ['en', 'fa']:
        bot.send_message(
            message.chat.id,
            get_message(user_lang, 'main_menu'),
            reply_markup=get_main_menu_keyboard(user_lang),
            parse_mode='Markdown'
        )
    else:
        # new user, show language selection
        bot.send_message(
            message.chat.id,
            get_message('en', 'welcome'),
            reply_markup=get_language_keyboard()
        )


@bot.message_handler(commands=['cancel'])
def cancel_command(message):
    """cancel current operation"""
    user_id = message.from_user.id
    lang = get_user_lang(user_id) or 'en'  # fallback to english if None
    clear_user_state(user_id)
    
    logger.info(f"user {user_id} cancelled operation")
    
    bot.send_message(
        message.chat.id,
        get_message(lang, 'cancel'),
        reply_markup=get_main_menu_keyboard(lang),
        parse_mode='Markdown'
    )


@bot.callback_query_handler(func=lambda call:True)
def callback_handler(call):
    """handle button presses"""
    user_id = call.from_user.id
    lang = get_user_lang(user_id) or 'en'  # fallback to english if None
    
    try:
        # handle different callback types using handlers
        if handlers.handle_language_selection(call, user_id, set_user_lang, get_main_menu_keyboard):
            bot.answer_callback_query(call.id)
            return
        
        if handlers.handle_navigation(call, user_id, lang):
            bot.answer_callback_query(call.id)
            return
        
        if handlers.handle_sleep_calculations(call, user_id, lang, get_user_timezone_offset):
            bot.answer_callback_query(call.id)
            return
        
        if handlers.handle_about_section(call, user_id, lang):
            bot.answer_callback_query(call.id)
            return
        
        if handlers.handle_settings(call, user_id, lang, get_user_timezone_offset, set_user_state):
            bot.answer_callback_query(call.id)
            return
        
        bot.answer_callback_query(call.id)
        
    except Exception as e:
        logger.error(f"error in callback handler: {e}", exc_info=True)
        bot.answer_callback_query(call.id, "error occurred!")


@bot.message_handler(func=lambda message:True)
def handle_text_messages(message):
    """handle text messages (time inputs)"""
    user_id = message.from_user.id
    lang = get_user_lang(user_id)
    state = get_user_state(user_id)

    try:
        # handle timezone offset input
        if state == WAITING_TIMEZONE:
            offset_str = message.text.strip()
            
            if validate_timezone_offset(offset_str):
                if offset_str == '0':
                    offset_str = '+00:00'
                
                set_user_timezone_offset(user_id, offset_str)
                clear_user_state(user_id)
                
                bot.send_message(
                    message.chat.id,
                    get_message(lang, 'timezone_changed').format(offset_str),
                    parse_mode='Markdown'
                )
                
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
                logger.info(f"user {user_id} calculated sleep at {hour:02d}:{minute:02d}")
                
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
                logger.info(f"user {user_id} calculated wake at {hour:02d}:{minute:02d}")
                
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
            
    except Exception as e:
        logger.error(f"error handling text message: {e}", exc_info=True)
        bot.send_message(
            message.chat.id,
            get_message(lang, 'error_occurred'),
            parse_mode='Markdown'
        )


def main():
    """start the bot"""
    logger.info("🤖 Lehaam bot v1.1.0 starting...")
    logger.info(f"loaded {len(user_data)} users from storage")
    
    print("🤖 Lehaam bot is running...")
    print("press Ctrl+C to stop")
    
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        logger.info("bot stopped by user")
        print("\n👋 bot stopped!")
    except Exception as e:
        logger.error(f"bot crashed: {e}", exc_info=True)


if __name__ == '__main__':
    main()
#MadMad_441