#!/bin/sh
to_translate=$(wl-paste --primary)
translated=$(~/.config/scripts/translator.py $to_translate)
notify-send $translated
wl-copy $translated
