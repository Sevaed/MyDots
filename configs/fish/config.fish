if status is-interactive
    # Commands to run in interactive sessions can go here
end
# ASDF configuration code
if test -z $ASDF_DATA_DIR
    set _asdf_shims "$HOME/.asdf/shims"
else
    set _asdf_shims "$ASDF_DATA_DIR/shims"
end
luarocks path --bin | source

# Do not use fish_add_path (added in Fish 3.2) because it
# potentially changes the order of items in PATH
if not contains $_asdf_shims $PATH
    set -gx --prepend PATH $_asdf_shims
end
set --erase _asdf_shims
# Инициализация Starship
starship init fish | source

cod init $fish_pid fish | source

# Убираем стандартное приветствие
set -U fish_greeting ""

# Устанавливаем редактор по умолчанию
set -x EDITOR helix
set SUDO_EDITOR $EDITOR
set -x XDG_CONFIG_HOME ~/.config

set -Ux FZF_DEFAULT_COMMAND 'fd --hidden --follow'

set AUR "sudo pacman"

# Добавляем пути в переменную PATH
export PATH="/home/sevaed/.local/xonsh-env/xbin:/opt/android-sdk/platform-tools/:$HOME/.cargo/bin:/home/sevaed/.local/bin:/home/sevaed/go/bin:$PATH"
# Алиасы
alias ls="eza --tree -L=1 --icons=always --group-directories-first"
alias copy="wl-copy"
alias tint="tint -d -n -l 1"
alias rp="realpath"
alias po="dualsensectl power-off;sudo pkill -9 AmneziaVPN; $AUR -Syu --noconfirm | lolcat; syncr | lolcat; hyprshutdown -t 'Shutting down...' --post-cmd 'shutdown -P 0'"
alias syncr="/home/sevaed/git/backup/my_configs/main.py"
alias mpv="mpv --vo=kitty --image-display-duration=inf --keep-open=always"
alias mkdir="mkdir -p"
alias PYstarter="~/.config/projects/git/PYstarter/PYstarter"
alias dualsense_statistic="/home/sevaed/.config/projects/git/controller_battery_statistic/statistic_viewer.py"
alias pipes="pipes.sh -r 0 -RK -p10"
alias bat="bat -P --style header,header-filesize"
alias cat="bat -P --style plain"
alias rofi="rofi -show drun -show-icons -theme /home/sevaed/.config/rofi/mytheme-normal.rasi -normal-window"
alias razer_shit="echo -ne '\x03\x00' | sudo tee /sys/bus/hid/drivers/razermouse/*/device_mode"
alias hx="helix"

function crp
    realpath $argv | wl-copy
end

function runB
    nohup $argv >/dev/null 2>&1 &
end

function vv
    set -l D (pwd)
    set -l FILE "venv/bin/activate.fish"

    while test "$PWD" != /
        if test -f $FILE
            source $FILE
            echo "Activated: "(pwd)/$FILE
            cd $D
            return
        end
        cd ..
    end
    cd $D
    read -l -P "$FILE not found, do you want to create venv? [Y/n] " ans
    switch $ans
        case '' y Y
            if python3 -m venv venv
                source $FILE
                echo "$FILE was created and activated"
                return 0
            else
                echo "Not sucsecfully"
                return 1
            end
        case '*'
            return 1
    end
end

# Created by `pipx` on 2026-01-15 18:46:08
set PATH $PATH /home/sevaed/.local/bin
