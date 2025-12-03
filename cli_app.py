import datetime as dt
import libs.messages as msg
import libs.lehaam_pieces as lp

lp.clear_command_line()
print(msg.ASCII_ART, end='')
lp.first_welcome()
lp.display_main_menu()

while(True):
    main_menu_user_req = input(" >> ")
    lp.clear_command_line()

    match(main_menu_user_req):
        case '1'|'how it works':
            lp.display_ascii()

            lp.about_Lehaam()

            lp.display_main_menu()

        case '2'|'sleep now':
            lp.display_ascii()
            
            # wake_up_suggests = []
            lp.display_current_time()
            print(msg.MESSAGES["sleep now wake up"])
            for i in range(1, 8):
                wake_h, wake_m = lp.add_minutes_to_time(
                    dt.datetime.now().hour,
                    dt.datetime.now().minute,
                    i * lp.SLEEP_CYCLE + lp.TO_FALL_ASLEEP
                )
                print(f"                           -> {wake_h:02d}:{wake_m:02d}", end='')
                if(i == 4 or i == 6):
                    print(" (suggested)")
                else:
                    print('')
                # wake_up_suggests.append([wake_h, wake_m])
            #lp.display_wake_up_times(wake_up_suggests)

            lp.display_main_menu()
            
        case '3'|'sleep at HH:MM':
            lp.display_ascii()

            lp.display_current_time()
            time = input(msg.MESSAGES["time input"])
            print(msg.MESSAGES["sleep at wake up"].format(time))
            #code
            
            lp.display_main_menu()

        case '4'|'wake up at HH:MM':
            lp.display_ascii()

            lp.display_current_time()
            time = input(msg.MESSAGES["time input"])
            print(msg.MESSAGES["wake up at"].format(time))
            #code
            
            lp.display_main_menu()
                        
        case '0'|'exit':
            break

        case _:
            lp.display_ascii()
            print(msg.MESSAGES["wrong input"])
            lp.display_main_menu()
#MadMad_71