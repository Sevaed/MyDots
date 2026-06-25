#!/bin/bash

main_menu() {
    chosen=$(echo -e "Выключить\nПерезагрузить\nВыбрать ОС для следующей загрузки\nВыйти из сессии\nОтмена" | rofi -dmenu -p "Действие:")

    case $chosen in
        "Выключить")
            systemctl poweroff
            ;;
        "Перезагрузить")
            systemctl reboot
            ;;
        "Выбрать ОС для следующей загрузки")
            if DISPLAY="$DISPLAY" XAUTHORITY="$XAUTHORITY" sudo -E /home/seva/scripts/grub-reboot.sh; then
                rofi -e "ОС выбрана. Перезагрузите вручную."
            else
                main_menu
            fi
            ;;
        "Выйти из сессии")
            systemctl restart display-manager
            ;;
        "Отмена" | "")
            exit 0
            ;;
        *)
            main_menu
            ;;
    esac
}

main_menu

