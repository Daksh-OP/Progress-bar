import sys
import time
import threading
import itertools
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

SPINNER = ['|', '/', '-', '\\']
BAR_LENGTH = 40
SLEEP_INTERVAL = 0.04

def colored_bar(percent):
    fill_length = int(BAR_LENGTH * percent // 100)
    bar = ''
    for i in range(BAR_LENGTH):
        if i < fill_length:
            # Gradient coloring (blue to green)
            color = Fore.CYAN if i < BAR_LENGTH // 2 else Fore.GREEN
            bar += color + '█'
        else:
            bar += Fore.BLACK + '░'
    return bar

def spinner_animation(stop_event, spinner_pos):
    for frame in itertools.cycle(SPINNER):
        if stop_event.is_set():
            break
        spinner_pos[0] = frame
        time.sleep(0.1)

def fake_progress_bar():
    percent = 0
    stop_spinner = threading.Event()
    spinner_pos = ['|']

    # Start spinner in a thread
    spinner_thread = threading.Thread(target=spinner_animation, args=(stop_spinner, spinner_pos))
    spinner_thread.start()

    try:
        while percent < 99:
            bar = colored_bar(percent)
            sys.stdout.write(
                f'\r{Fore.LIGHTWHITE_EX}Loading {spinner_pos[0]} |{bar}{Style.RESET_ALL}| {Fore.YELLOW}{percent+1}%{Style.RESET_ALL}'
            )
            sys.stdout.flush()
            time.sleep(SLEEP_INTERVAL + 0.01 * (percent % 5))
            percent += 1

        # Stuck at 99% forever with blinking "Almost done..." message
        blink = True
        bar = colored_bar(99)
        while True:
            msg = f"{Fore.GREEN if blink else Fore.LIGHTBLACK_EX}Almost done...{Style.RESET_ALL}" if blink else "             "
            sys.stdout.write(
                f'\r{Fore.LIGHTWHITE_EX}Loading {spinner_pos[0]} |{bar}{Style.RESET_ALL}| {Fore.YELLOW}99%{Style.RESET_ALL}   {msg}'
            )
            sys.stdout.flush()
            time.sleep(0.5)
            blink = not blink

    except KeyboardInterrupt:
        stop_spinner.set()
        spinner_thread.join()
        print(f'\n{Fore.RED}Progress interrupted by user. Goodbye!{Style.RESET_ALL}')

if __name__ == "__main__":
    print(f"{Fore.CYAN}Welcome to the Serious Progress Bar!{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}This may take a while...{Style.RESET_ALL}")
    time.sleep(1.2)
    fake_progress_bar()