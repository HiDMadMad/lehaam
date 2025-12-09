ASCII_ART = """
  _         _                           
 | |    ___| |__   __ _  __ _ _ __ ___  
 | |   / _ \\ '_ \\ / _` |/ _` | '_ ` _ \\ 
 | |__|  __/ | | | (_| | (_| | | | | | |
 |_____\\___|_| |_|\\__,_|\\__,_|_| |_| |_|
 ================ 1.0.0 ================

"""  # \\ are for fix the warning

if __name__ == "__main__":
    print(ASCII_ART,"use this file as a module!\n")

MESSAGES = {
    "first welcome" : " hi {}, welcome to Lehaam!",

    # menus
    "main cli menu":"\n ==== main menu ====\n 0.how it works\n 1.sleep now\
                     \n 2.sleep at HH:MM\n 3.wake up at HH:MM\n 4.exit\n",


    #inputs
    "sleep at input":"\n you want to sleep at ..?",

    "wake up at input":"\n you want to wake up at ..?",

    "time input":"\n enter the time as HH:MM (or 'q' to return to menu)\n >> ",


    #outputs
    "current time":" current time :  {}:{}",

    "sleep now wake up":"\n if you go to sleep right now\
                         \n and fall asleep in 15 minutes (on average),\
                         \n you should aim to wake up at",

    "sleep at wake up":"\n if you go to sleep at {}:{}\
                        \n and fall asleep in 15 minutes (on average),\
                        \n you should aim to wake up at",

    "wake up at sleep" : "\n if you want wake up refresh at {}:{}\
                          \n and fall asleep in 15 minutes (on average),\
                          \n you should aim to sleep at",

    "about Lehaam":" sleep happens in cycles of about 90 minutes.\
                    \n waking up between these cycles helps you feel refreshed.\
                    \n Lehaam calculates optimal times to fall asleep and wake up for better rest.",


    #errors
    "wrong input" : "\n your input means you are a failure =)\
                     \n go to your room and think about your mistakes :)\n\n",

    "not sup os" : "\n OS \"{}\" is not supported.",

    "time input error":"\n enter time like \"10:26\" or \"10:00\" ...",
}
#MadMad_58