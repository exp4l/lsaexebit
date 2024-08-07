import time
import sys

def display_analyzing_message(stop_event):
    """
    Display an animated analyzing message while processing the query.
    """
    message = "Analyzing Database to find answers"
    animation_chars = ["-", "\\", "|", "/", "//", "-"]
    animation_index = 0

    while not stop_event.is_set():
        sys.stdout.write(f"\r{message} {animation_chars[animation_index]}")
        sys.stdout.flush()
        time.sleep(0.1)
        animation_index = (animation_index + 1) % len(animation_chars)

        # Add some extra flair
        if animation_index == 0:
            sys.stdout.write("\r" + " " * (len(message) + 4) + "\r")
            sys.stdout.write(f"\r{message} ")
            sys.stdout.write("   (Looking for answers...)")
            sys.stdout.flush()
            time.sleep(0.2)
            sys.stdout.write("\r" + " " * (len(message) + 4) + "\r")
            sys.stdout.write(f"\r{message} ")
            sys.stdout.flush()

    sys.stdout.write("\n")
    sys.stdout.flush()
