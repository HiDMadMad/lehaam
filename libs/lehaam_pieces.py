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

USER_PLATFORM = platform.system()
USER_NAME = os.getlogin()

#==================== functions ====================#
## displays :
def first_welcome():
    print(msg.MESSAGES["first welcome"].format(USER_NAME))

def display_ascii():
    print(msg.ASCII_ART)
def display_main_menu():
    print(msg.MESSAGES["main cli menu"])

def about_Lehaam():
    print(msg.MESSAGES["about Lehaam"])

def display_current_time():
    now = dt.datetime.now()
    print(msg.MESSAGES["current time"].format(now.hour, now.minute))

# def display_wake_up_times(times:list[(int, int)]):
#     print(msg.MESSAGES["sleep now wake up"])
#     for i in range(len(times)):
#         print(f"                           -> {times[i][0]:02d}:{times[i][1]:02d}", end='')
#         if(i == 4 or i == 6):
#             print(" (suggested)")
#         else:
#             print('')
#     print()
            

## os :
def clear_command_line():
    if(USER_PLATFORM == 'Windows'):
        os.system("cls")
    elif(USER_PLATFORM == 'Linux' or USER_PLATFORM == 'Darwin'):
        os.system("clear")
    else:
        print(msg.MESSAGES["not sup os"].format(USER_PLATFORM))


# calculates :
def add_minutes_to_time(hour:int, minute:int, add_min:int) -> tuple[int, int]:
    total = hour * 60 + minute + add_min
    total %= 24 * 60
    return total // 60, total % 60


# ui :
def get_time():
    pass

#MadMad_82