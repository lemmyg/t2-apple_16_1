#!/usr/bin/env python3
import re
import subprocess
import traceback

SECONDARY_MONITOR = 'eDP'
SECONDARY_X = 1920
SECONDARY_Y = 1200

try:

    # Run the xrandr command and capture its output
    p = subprocess.Popen('xrandr --listmonitors', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()

    #print (output)
    # Decode the output as a string
    output_str = output.decode('utf-8')

    connected_displays = output_str.splitlines()[1:]

    # If there are only one or zero connected displays, exit
    if len(connected_displays) > 2:
        print("Less than 2 displays are connected. Exiting.")
        exit()

    primary_display = ""
    secondary_display = ""

    # Set the secondary display to the first non-eDP display in the list
    for display in connected_displays:
        if SECONDARY_MONITOR in display:
            secondary_display = display
        else:
            primary_display = display


    regex = r'(\d+)\/\d+x(\d+).*  ([a-zA-Z0-9_-]+)'

    print("primary: ", primary_display)
    print("secondary: ", secondary_display)
    if primary_display:
        primary_x, primary_y, primary = re.search(regex, primary_display).groups()
    if secondary_display:
        secondary_x, secondary_y, secondary = re.search(regex, secondary_display).groups()


    # Set the secondary display (non-eDP) to the left of the primary display (eDP)
    command = f'xrandr --output {secondary} --mode {SECONDARY_X}x{SECONDARY_Y} --rotate normal'
    if primary_display:
        command += f' --right-of {primary} --output {primary} --mode {primary_x}x{primary_y} --rotate normal'
    print(command)

    # Run the xrandr command
    p = subprocess.Popen(command, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if error:
        print (error.decode('utf-8'))

except Exception:
    print(traceback.format_exc())
