import libs.messages as msg
import libs.lehaam_pieces as lp

lp.clear_command_line()
print(msg.ASCII_ART, end='')
lp.first_welcome()
lp.display_main_menu()

while(True):
    main_menu_user_req = input(" >> ").strip().lower()
    lp.clear_command_line()

    match(main_menu_user_req):
        case '0'|'how it works':
            lp.display_ascii()

            lp.about_Lehaam()

            lp.display_main_menu()


        case '1'|'sleep now':
            lp.display_ascii()

            now = lp.disp_and_ret_current_time()
            wake_times = lp.calculate_wake_times(now)
            lp.display_calculated_times(wake_times, "sleep now wake up")

            lp.display_main_menu()


        case '2'|'sleep at HH:MM':
            lp.display_ascii()

            now = lp.disp_and_ret_current_time()
            user_time = lp.get_user_time("sleep at input", "time input")
            if(user_time == None):
                lp.display_main_menu()
                continue
            wake_hour, wake_minute = user_time
            wake_times = lp.calculate_wake_times_from_sleep_at(now, wake_hour, wake_minute)
            lp.display_calculated_times(wake_times, "sleep at wake up", wake_hour, wake_minute)

            lp.display_main_menu()


        case '3'|'wake up at HH:MM':
            lp.display_ascii()

            now = lp.disp_and_ret_current_time()
            user_time = lp.get_user_time("wake up at input", "time input")
            if(user_time == None):
                lp.display_main_menu()
                continue
            sleep_hour, sleep_minute = user_time
            sleep_times = lp.calculate_sleep_times_from_wake_at(now, sleep_hour, sleep_minute)
            lp.display_calculated_times(sleep_times, "wake up at sleep", sleep_hour, sleep_minute)

            lp.display_main_menu()


        case '4'|'exit':
            break

        case _:
            lp.display_ascii()
            print(msg.MESSAGES["wrong input"])
            lp.display_main_menu()
#MadMad_69