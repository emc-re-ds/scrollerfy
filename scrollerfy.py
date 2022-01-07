"""
    This file is part of Scrollerfy.
    Scrollerfy is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    Scrollerfy is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with Scrollerfy.  If not, see <https://www.gnu.org/licenses/>.
"""

#!/usr/bin/env python

import time

import sys
import dbus
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '-t',
    '--trunclen',
    type=int,
    metavar='trunclen'
)
parser.add_argument(
    '-f',
    '--format',
    type=str,
    metavar='custom format',
    dest='custom_format'
)
parser.add_argument(
    '-p',
    '--playpause',
    type=str,
    metavar='play-pause indicator',
    dest='play_pause'
)
parser.add_argument(
    '--font',
    type=str,
    metavar='the index of the font to use for the main label',
    dest='font'
)
parser.add_argument(
    '--playpause-font',
    type=str,
    metavar='the index of the font to use to display the playpause indicator',
    dest='play_pause_font'
)
parser.add_argument(
    '-q',
    '--quiet',
    action='store_true',
    help="if set, don't show any output when the current song is paused",
    dest='quiet',
)
parser.add_argument(
    '-s',
    '--scroll',
    action='store_true',
    help="if set, scrolls the text",
    dest='scroll_text',
)


args = parser.parse_args()


def fix_string(string):
    # corrects encoding for the python version used
    if sys.version_info.major == 3:
        return string
    else:
        return string.encode('utf-8')

def truncate(name, trunclen):
    if len(name) > trunclen:
        scroll = 1
        name = name[:trunclen]
        name += '...'
        if ('(' in name) and (')' not in name):
            name += ')'
    return name

def play_pause_icon(status, play_pause):
    if status == 'Playing':
        play_pause_ = play_pause[0]
    elif status == 'Paused':
        play_pause_ = play_pause[1]
    else:
        play_pause_ = str()

    if play_pause[2]:
        play_pause_ = label_with_font.format(font=play_pause[2], label=play_pause)

    return play_pause_

def scroller(name, song, play_pause, scroll_text, trunclen):
    current_state = spotify_properties.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')

    if (scroll_text == False or
            len(name) <= trunclen or
            current_state == 'Paused'):
        while(True):
            metadata = spotify_properties.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
            song_actual = fix_string(metadata['xesam:title']) if metadata['xesam:title'] else ''

            # call again the script if the song changes
            if (song != song_actual):
                return False

            # If the song is playing again and scrolling is activated, then change
            if (current_state != spotify_properties.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')):
                return False

            # If the scroll is desactivated
            if (len(name) > trunclen):
                name = name[:trunclen]
                name += '...'
                if ('(' in name) and (')' not in name):
                    name += ')'

            play_pause_ic = play_pause_icon(current_state, play_pause)
            print(play_pause_ic, name, sep=' ')
            time.sleep(0.25)
    else:
        marker = 0
        marker_tc = 0
        current_state = 'Playing'
        print_text = ''
        while(True):
            metadata = spotify_properties.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
            song_actual = fix_string(metadata['xesam:title']) if metadata['xesam:title'] else ''

            if (song != song_actual):
                return False

            play_pause_ic = play_pause_icon(current_state, play_pause)
            transition_char = " " + marker_tc*"<" + " "

            if (marker >= len(name)):
                text_tail = name[0:trunclen-len(transition_char)]
                if (current_state != 'Paused'):
                    marker_tc = marker_tc-1

                print_text = play_pause_ic + transition_char + text_tail
            else:
                if (marker+trunclen < len(name)):
                    text_head = name[marker:trunclen+marker]
                else:
                    text_head = name[marker:len(name)]

                if (abs(marker-len(name)) < trunclen):
                    if (current_state != 'Paused'):
                        tail_chars_num = trunclen-abs(marker-len(name))-len(transition_char)

                    if (tail_chars_num <= 0):
                        text_tail = ''
                    else:
                        text_tail = name[0:tail_chars_num]

                    print_text = play_pause_ic + text_head + transition_char + text_tail

                    if (marker_tc < 2 and current_state != 'Paused'):
                        marker_tc = marker_tc+1
                else:
                    text_tail = ''

                    print_text = play_pause_ic + text_head + transition_char

            if (current_state != 'Paused'):
                marker = marker+1

            print(print_text)

            if (marker == len(name)+3):
                marker = 0
                marker_tc = 0

            current_state = spotify_properties.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')
            time.sleep(0.25)

# Default parameters
output = fix_string(u'{play_pause} {artist}: {song}')
trunclen = 35
play_pause = fix_string(u'\u25B6,\u23F8') # first character is play, second is paused

label_with_font = '%{{T{font}}}{label}%{{T-}}'
font = args.font
play_pause_font = args.play_pause_font

quiet = args.quiet
scroll_text = args.scroll_text

# parameters can be overwritten by args
if args.trunclen is not None:
    trunclen = args.trunclen
if args.custom_format is not None:
    output = args.custom_format
if args.play_pause is not None:
    play_pause = args.play_pause

try:
    session_bus = dbus.SessionBus()
    spotify_bus = session_bus.get_object(
        'org.mpris.MediaPlayer2.spotify',
        '/org/mpris/MediaPlayer2'
    )

    spotify_properties = dbus.Interface(
        spotify_bus,
        'org.freedesktop.DBus.Properties'
    )

    metadata = spotify_properties.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
    status = spotify_properties.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')

    # Handle play/pause

    play_pause = play_pause.split(',')
    play_pause.append(play_pause_font)

    # Handle main label

    artist = fix_string(metadata['xesam:artist'][0]) if metadata['xesam:artist'] else ''
    song = fix_string(metadata['xesam:title']) if metadata['xesam:title'] else ''
    album = fix_string(metadata['xesam:album']) if metadata['xesam:album'] else ''

    if (quiet and status == 'Paused') or (not artist and not song and not album):
        print('')
    else:
        if font:
            artist = label_with_font.format(font=font, label=artist)
            song = label_with_font.format(font=font, label=song)
            album = label_with_font.format(font=font, label=album)

        name = output.format(artist=artist,
                song=song,
                album=album)

        scroller(name, song, play_pause, scroll_text, trunclen + 4)

except Exception as e:
    if isinstance(e, dbus.exceptions.DBusException):
        print('')
    else:
        print(e)

