#!/usr/bin/env bash

SWIFTPOINT="swiftpoint-limited-swiftpoint-creator"
RAZER_1="razer-razer-basilisk-v3-x-hyperspeed-2"
RAZER_2="razer-razer-basilisk-v3-x-hyperspeed-3"

get_enabled() {
    hyprctl getoption "device[$1]:enabled" 2>/dev/null | awk '/int:/ {print $2}'
}

SWIFT_ENABLED="$(get_enabled "$SWIFTPOINT")"
RAZER1_ENABLED="$(get_enabled "$RAZER_1")"
RAZER2_ENABLED="$(get_enabled "$RAZER_2")"

OPTIONS=()

# Swiftpoint only
if [[ "$SWIFT_ENABLED" != "1" || "$RAZER1_ENABLED" != "0" || "$RAZER2_ENABLED" != "0" ]]; then
    OPTIONS+=("Swiftpoint")
fi

# Razer only
if [[ "$SWIFT_ENABLED" != "0" || "$RAZER1_ENABLED" != "1" || "$RAZER2_ENABLED" != "1" ]]; then
    OPTIONS+=("Razer")
fi

# Both
if [[ "$SWIFT_ENABLED" != "1" || "$RAZER1_ENABLED" != "1" || "$RAZER2_ENABLED" != "1" ]]; then
    OPTIONS+=("Both")
fi

OPTIONS+=("Cancel")

CHOICE="$(
    printf "%s\n" "${OPTIONS[@]}" |
    rofi -dmenu -theme /home/sevaed/.config/rofi/mytheme-normal.rasi -p "Select mouse"
)"

case "$CHOICE" in
    "Swiftpoint")
        hyprctl --batch "\
keyword device[$SWIFTPOINT]:enabled true ; \
keyword device[$RAZER_1]:enabled false ; \
keyword device[$RAZER_2]:enabled false"
        ;;
    "Razer")
        hyprctl --batch "\
keyword device[$SWIFTPOINT]:enabled false ; \
keyword device[$RAZER_1]:enabled true ; \
keyword device[$RAZER_2]:enabled true"
        ;;
    "Both")
        hyprctl --batch "\
keyword device[$SWIFTPOINT]:enabled true ; \
keyword device[$RAZER_1]:enabled true ; \
keyword device[$RAZER_2]:enabled true"
        ;;
    "Cancel" | "")
        exit 0
        ;;
esac
