import datetime as dt
import os
import platform

try:
    from . import messages as msg
except Exception:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # add project root
    import messages as msg


"""
====================== Lehaam Pieces ======================
this module's name is inspired by "Puzzle Pieces",
because each function and constant here is like
a piece of the Lehaam's app puzzle. together, they form the
core of the Lehaam program.
===========================================================
"""

if __name__ == "__main__":
    print(msg.ASCII_ART,"use this file as a module!\n")

#==================== constants ====================#
TO_FALL_ASLEEP = 15  # 15min
SLEEP_CYCLE = 90  # 90min
SUGGESTED_CYCLES = [4, 5, 6]

USER_PLATFORM = platform.system()
USER_NAME = os.getlogin()


#==================== display functions ====================#
def first_welcome():
    """displays welcome message with the user's name"""
    print(msg.MESSAGES["first welcome"].format(USER_NAME))

def display_ascii():
    """displays ASCII art"""
    print(msg.ASCII_ART)

def display_main_menu():
    """displays main CLI menu"""
    print(msg.MESSAGES["main cli menu"])

def about_Lehaam():
    """displays information about Lehaam app"""
    print(msg.MESSAGES["about Lehaam"])

def disp_and_ret_current_time() -> dt.datetime:
    """
    displays and returns current time

    returns:
        datetime.datetime : current system time
    """
    now = dt.datetime.now()
    print(msg.MESSAGES["current time"].format(f"{now.hour:02d}", f"{now.minute:02d}"))
    return now

def display_calculated_times(cal_times:list[tuple[dt.datetime, bool]], message_key:str, *message_args:any):
    """
    prints calculated wake-up or sleep times

    args:
        wake_times : list of tuples (datetime, is_suggested)
        message_key : key in msg.MESSAGES for header message
        *message_args : optional arguments for formatting message
    """
    if(message_key):
        print(msg.MESSAGES[message_key].format(*message_args))
    for time, suggested in cal_times:
        print(f"                           -> {time.hour:02d}:{time.minute:02d}", end='')
        if(suggested):
            print(" (suggested)")
        else:
            print('')


#==================== OS functions ====================#
def clear_command_line():
    if(USER_PLATFORM == 'Windows'):
        os.system("cls")
    elif(USER_PLATFORM == 'Linux' or USER_PLATFORM == 'Darwin'):
        os.system("clear")
    else:
        print(msg.MESSAGES["not sup os"].format(USER_PLATFORM))


#==================== calculate functions ====================#
def calculate_wake_times(now:dt.datetime) -> list[tuple[dt.datetime, bool]]:
    """calculates suggested wake-up times based on sleep cycles"""
    wake_times = []
    for i in range(1, 8):
        wake_time = now + dt.timedelta(minutes=i * SLEEP_CYCLE + TO_FALL_ASLEEP)
        wake_times.append((wake_time, i in SUGGESTED_CYCLES))
    return wake_times

def calculate_wake_times_from_sleep_at(now:dt.datetime, hour:int, minute:int) -> list[tuple[dt.datetime, bool]]:
    """calculates wake-up times if user wants to sleep at a specific time"""
    wake_times = []
    target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    for i in range(1, 8):
        sleep_time = target_time + dt.timedelta(minutes=i * SLEEP_CYCLE + TO_FALL_ASLEEP)
        wake_times.append((sleep_time, i in SUGGESTED_CYCLES))
    return wake_times

def calculate_sleep_times_from_wake_at(now:dt.datetime, hour:int, minute:int) -> list[tuple[dt.datetime, bool]]:
    """calculates suggested sleep times if user wants to wake up at a specific time"""
    sleep_times = []
    target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    for i in range(7, 0, -1):
        sleep_time = target_time - dt.timedelta(minutes=i * SLEEP_CYCLE + TO_FALL_ASLEEP)
        sleep_times.append((sleep_time, i in SUGGESTED_CYCLES))
    return sleep_times


#==================== UI functions ====================#
def get_user_time(message_key:str, prompt_key:str) -> tuple[int, int] | None:
    """
    prompts user for a time input in HH:MM format and validates it

    args:
        message_key : key in msg.MESSAGES for message 
        prompt_key : key in msg.MESSAGES for prompt message

    returns:
        (hour, minute) tuple if valid, None if user quits by typing 'q'
    """
    if(message_key):
        print(msg.MESSAGES[message_key], end='')
    while True:
        user_time = input(msg.MESSAGES[prompt_key])
        if user_time.lower() == 'q':
            return None
        try:
            hour, minute = map(int, user_time.split(':'))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError()
            return hour, minute
        except ValueError:
            print(msg.MESSAGES["time input error"])

#MadMad_146