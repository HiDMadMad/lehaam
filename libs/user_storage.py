"""
user data storage management
handles saving and loading user preferences to/from JSON file
"""
import json
import os
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

USER_DATA_FILE = "user_data.json"


def load_user_data() -> Dict[int, Dict[str, Any]]:
    """
    load user data from JSON file
    
    returns:
        dict: user data with user_id as key
    """
    try:
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # convert string keys to int
                return {int(k): v for k, v in data.items()}
        logger.info("no existing user data file found, starting fresh")

    except Exception as e:
        logger.error(f"error loading user data: {e}", exc_info=True)
    
    return {}


def save_user_data(data:Dict[int, Dict[str, Any]]) -> bool:
    """
    save user data to JSON file
    
    args:
        data : user data dictionary
        
    returns:
        bool : True if successful, False otherwise
    """
    try:
        # convert int keys to string for JSON
        data_to_save = {str(k): v for k, v in data.items()}
        
        with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
        logger.debug(f"saved data for {len(data)} users")
        return True
        
    except Exception as e:
        logger.error(f"error saving user data: {e}", exc_info=True)
        return False


def get_user_data(data:Dict[int, Dict[str, Any]], user_id:int, key:str, default:Any=None) -> Any:
    """
    get specific user data value
    
    args:
        data : user data dictionary
        user_id : telegram user id
        key : data key to retrieve
        default : default value if not found
        
    returns:
        the value or default
    """
    return data.get(user_id, {}).get(key, default)


def set_user_data(data:Dict[int, Dict[str, Any]], user_id:int, key:str, value:Any) -> bool:
    """
    set specific user data value and save to file
    
    args:
        data : user data dictionary
        user_id : telegram user id
        key : data key to set
        value : value to set
        
    returns:
        bool : True if successful
    """
    if user_id not in data:
        data[user_id] = {}
    
    data[user_id][key] = value
    
    return save_user_data(data)


def delete_user_data(data:Dict[int, Dict[str, Any]], user_id:int) -> bool:
    """
    delete all data for a specific user
    
    args:
        data : user data dictionary
        user_id : telegram user id
        
    returns:
        bool : True if successful
    """
    if user_id in data:
        del data[user_id]
        logger.info(f"deleted data for user {user_id}")
        return save_user_data(data)
    
    return True


def get_stats() -> Dict[str, int]:
    """
    get statistics about stored data
    
    returns:
        dict : statistics
    """
    data = load_user_data()
    
    return {
        'total_users': len(data),
        'users_with_lang': sum(1 for u in data.values() if 'lang' in u),
        'users_with_timezone': sum(1 for u in data.values() if 'timezone_offset' in u),
    }
#MadMad_131