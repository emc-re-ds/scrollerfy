# Scrollerfy 

## Table Of Contents
* [General Info](#general-info)
* [Prerequisites](#prerequisites)
* [Module Example](#prerequisites)
* [Custom Arguments](#prerequisites)
* [License](#license)

### General Info
This module shows the information of the song that is currently playing on Spotify and scrolls it if the characters are longer that a certain number configured or if the user does not want any scroll.

![sample screenshot](https://shor.at/KV7H3cnO)

### Prerequisites
- Python (2.x or 3.x)
- Python `dbus` module

### Module Example
```
[module/spotify]
type = custom/script
tail = true
format = <label>
label = %output%
click-left = playerctl play-pause spotify
;exec = python -u /path/to/spotify/script -s -t 35 -f '{artist}: {song}' -p '[playing],[paused]'
exec-if = pgrep -x spotify
exec = ~/bin/init_polySpotify.sh
format-foreground = #1db954
interval = 1
```

### Custom Arguments

##### Truncate

The argument "-t" is optional and sets the `trunlen`. It specifies the maximum length of the printed string, so that it gets truncated when the specified length is exceeded. Defaults to 35.

Override example:

``` ini
exec = python /path/to/spotify/script -t 42
```

##### Format

The argument "-f" is optional and sets the format. You can specify how to display the song and the artist's name, as well as where (or whether) to print the play-pause indicator. 

Override example:

``` ini
exec = python /path/to/spotify/script -f '{play_pause} {song} - {artist} - {album}'
```

This would output "Lone Digger - Caravan Palace - <I°_°I>" in your polybar, instead of what is shown in the screenshot.

##### Status indicator

The argument "-p" is optional, and sets which unicode symbols to use for the status indicator. These should be given as a comma-separated string, with the play indicator as the first value and the pause indicator as the second.

Override example:

``` ini
exec = python /path/to/spotify/script -p '[playing],[paused]'
```

##### Fonts

The argument "--font" is optional, and allow to specify which font from your Polybar config to use to display the main label.

Override example:
```ini
exec = python /path/to/spotify/script --font=1
```

The argument "--playpause-font" is optional, and allow to specify which font from your Polybar config to use to display the "play/pause" indicator.

Override example:
``` ini
exec = python /path/to/spotify/script -p '[playing],[paused]' --playpause-font=2
```

##### Quiet

The argument "-q" or "--quiet" is optional and specifies whether to display the output when the current song is paused.
This will make polybar only show a song title and artist (or whatever your custom format is) when the song is actually playing and not when it's paused.
Simply setting the flag on the comand line will enable this option.

Override example:
```ini
exec = python /path/to/spotify/script -q
```

##### Scroll

The argument "-s" or "--scroll" is optional, allows scrolling of the text when the specified length is exceeded.

Override example:
```ini
exec = python /path/to/spotify/script -s
```

### License
SRCompiler is Free Software: You can use, study share and improve it at your will. Specifically you can redistribute and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

