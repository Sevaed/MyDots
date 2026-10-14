if status is-interactive
    # Инициализация Starship
    starship init fish | source

    cod init $fish_pid fish | source

    # Убираем стандартное приветствие
    set -U fish_greeting ""

    fastfetch
    # luarocks path --bin | source
end

# Устанавливаем редактор по умолчанию
set -x EDITOR helix
set SUDO_EDITOR $EDITOR
set -x XDG_CONFIG_HOME ~/.config

set -Ux FZF_DEFAULT_COMMAND 'fd --hidden --follow'

set AUR yay
set -Ux QMK_HOME "/home/sevaed/.config/qmk/qmk_firmware"

set -x GOPATH ~/go

fish_add_path --global /opt/android-sdk/platform-tools ~/.local/bin $GOPATH/bin

# Алиасы
alias ls="eza --tree -L=1 --icons=always --group-directories-first"
alias copy="wl-copy"
alias tint="tint -d -n -l 1"
alias rp="realpath"
alias po="dualsensectl power-off; $AUR -Syu --noconfirm | lolcat; syncr | lolcat; shutdown -P 0"
alias syncr="/home/sevaed/.config/backup/MyDots/backup.py -b"
alias mpv="mpv --image-display-duration=inf --keep-open=always"
alias mkdir="mkdir -p"
alias PYstarter="~/.config/projects/git/PYstarter/PYstarter"
alias dualsense_statistic="/home/sevaed/.config/projects/git/controller_battery_statistic/statistic_viewer.py"
alias pipes="pipes.sh -r 0 -RK -p10"
# alias bat="bat -P --style header,header-filesize"
alias cat="bat -P --style plain"
alias razer_shit="echo -ne '\x03\x00' | sudo tee /sys/bus/hid/drivers/razermouse/*/device_mode"
alias hx="helix"
alias py="python"
alias I_am_femboy_UwU="fastfetch && ~/.config/scripts/sound.py UwU"

function crp
    if test $argv
        realpath $argv | wl-copy
    else
        realpath "." | wl-copy
    end
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
