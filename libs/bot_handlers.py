"""
telegram bot callback handlers
separated handlers for better code organization
"""
import datetime as dt
import logging
from libs.bot_messages import get_message, format_time_result
import libs.lehaam_pieces as lp

logger = logging.getLogger(__name__)


class BotHandlers:
    """class to organize bot callback handlers"""
    
    def __init__(self, bot, user_states, get_keyboards):
        """
        initialize handlers
        
        args:
            bot : telebot instance
            user_states : dict of user conversation states
            get_keyboards : dict of keyboard generator functions
        """
        self.bot = bot
        self.user_states = user_states
        self.keyboards = get_keyboards
    
    def clear_state(self, user_id: int):
        """clear user conversation state"""
        if user_id in self.user_states:
            del self.user_states[user_id]
    
    def handle_language_selection(self, call, user_id:int, set_lang_func, get_main_menu_kb) -> bool:
        """
        handle language selection callbacks
        
        returns:
            bool : True if handled, False otherwise
        """
        try:
            if call.data == "lang_en":
                set_lang_func(user_id, 'en')
                self.clear_state(user_id)
                
                self.bot.edit_message_text(
                    get_message('en', 'language_selected'),
                    call.message.chat.id,
                    call.message.message_id
                )
                
                self.bot.send_message(
                    call.message.chat.id,
                    get_message('en', 'main_menu'),
                    reply_markup=get_main_menu_kb('en'),
                    parse_mode='Markdown'
                )
                logger.info(f"user {user_id} selected English")
                return True
            
            elif call.data == "lang_fa":
                set_lang_func(user_id, 'fa')
                self.clear_state(user_id)
                
                self.bot.edit_message_text(
                    get_message('fa', 'language_selected'),
                    call.message.chat.id,
                    call.message.message_id
                )
                
                self.bot.send_message(
                    call.message.chat.id,
                    get_message('fa', 'main_menu'),
                    reply_markup=get_main_menu_kb('fa'),
                    parse_mode='Markdown'
                )
                logger.info(f"user {user_id} selected Persian")
                return True
                
        except Exception as e:
            logger.error(f"error in language selection: {e}", exc_info=True)
            
        return False
    
    def handle_navigation(self, call, user_id:int, lang:str) -> bool:
        """
        handle navigation callbacks (back, change language)
        
        returns:
            bool : True if handled
        """
        try:
            if call.data == "change_lang":
                self.clear_state(user_id)
                self.bot.edit_message_text(
                    get_message('en', 'welcome'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=self.keyboards['language']()
                )
                logger.info(f"user {user_id} changing language")
                return True
            
            elif call.data == "back":
                self.clear_state(user_id)
                self.bot.edit_message_text(
                    get_message(lang, 'main_menu'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=self.keyboards['main_menu'](lang),
                    parse_mode='Markdown'
                )
                logger.debug(f"user {user_id} returned to main menu")
                return True
                
        except Exception as e:
            logger.error(f"error in navigation: {e}", exc_info=True)
            
        return False
    
    def handle_sleep_calculations(self, call, user_id:int, lang:str, get_offset_func) -> bool:
        """
        handle sleep calculation callbacks
        
        returns:
            bool : True if handled
        """
        try:
            if call.data == "sleep_now":
                self.clear_state(user_id)
                
                user_offset = get_offset_func(user_id)
                now = self._get_time_with_offset(user_offset)
                wake_times = lp.calculate_wake_times(now)
                
                result = format_time_result(
                    lang, wake_times, "sleep_now_result",
                    f"{now.hour:02d}", f"{now.minute:02d}"
                )
                
                self.bot.edit_message_text(
                    result,
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=self.keyboards['back'](lang),
                    parse_mode='Markdown'
                )
                logger.info(f"user {user_id} calculated sleep now")
                return True
            
            elif call.data == "sleep_at":
                from apps.telegram_bot import WAITING_SLEEP_TIME
                self.user_states[user_id] = WAITING_SLEEP_TIME
                
                self.bot.edit_message_text(
                    get_message(lang, 'sleep_at_prompt'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=self.keyboards['back'](lang),
                    parse_mode='Markdown'
                )
                logger.debug(f"user {user_id} entering sleep at mode")
                return True
            
            elif call.data == "wake_at":
                from apps.telegram_bot import WAITING_WAKE_TIME
                self.user_states[user_id] = WAITING_WAKE_TIME
                
                self.bot.edit_message_text(
                    get_message(lang, 'wake_at_prompt'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=self.keyboards['back'](lang),
                    parse_mode='Markdown'
                )
                logger.debug(f"user {user_id} entering wake at mode")
                return True
                
        except Exception as e:
            logger.error(f"error in sleep calculations: {e}", exc_info=True)
            
        return False
    
    def handle_about_section(self, call, user_id:int, lang:str) -> bool:
        """
        handle about section callbacks
        
        returns:
            bool : True if handled
        """
        try:
            about_pages = {
                "about": "about_title",
                "about_cycles": "about_cycles",
                "about_timing": "about_timing",
                "about_calc": "about_calculation",
                "about_tips": "about_tips"
            }
            
            if call.data in about_pages:
                if call.data == "about":
                    self.clear_state(user_id)
                
                self.bot.edit_message_text(
                    get_message(lang, about_pages[call.data]),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=self.keyboards['about'](lang),
                    parse_mode='Markdown'
                )
                logger.debug(f"user {user_id} viewing {call.data}")
                return True
                
        except Exception as e:
            logger.error(f"error in about section: {e}", exc_info=True)
            
        return False
    
    def handle_settings(self, call, user_id:int, lang:str, get_offset_func, set_state_func) -> bool:
        """
        handle settings callbacks
        
        returns:
            bool : True if handled
        """
        try:
            if call.data == "settings":
                self.clear_state(user_id)
                self.bot.edit_message_text(
                    get_message(lang, 'settings_menu'),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=self.keyboards['settings'](lang),
                    parse_mode='Markdown'
                )
                logger.debug(f"user {user_id} opened settings")
                return True
            
            elif call.data == "settings_timezone":
                from apps.telegram_bot import WAITING_TIMEZONE
                
                current_offset = get_offset_func(user_id)
                set_state_func(user_id, WAITING_TIMEZONE)
                
                self.bot.edit_message_text(
                    get_message(lang, 'timezone_prompt').format(current_offset),
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=self.keyboards['timezone_back'](lang),
                    parse_mode='Markdown'
                )
                logger.debug(f"user {user_id} changing timezone")
                return True
                
        except Exception as e:
            logger.error(f"error in settings: {e}", exc_info=True)
            
        return False
    
    @staticmethod
    def _get_time_with_offset(offset_str:str) -> dt.datetime:
        """helper to get current time with offset"""
        from apps.telegram_bot import get_current_time_with_offset
        return get_current_time_with_offset(offset_str)
#MadMad_265