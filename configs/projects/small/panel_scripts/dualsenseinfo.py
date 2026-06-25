#!/usr/bin/python
import subprocess

check_battery_command = ["dualsensectl", "battery"]

result = subprocess.run(check_battery_command, capture_output=True, text=True)

if result.returncode == 0:
    dualsensctl_answer = result.stdout.strip()

    battery_procentage, battery_status = dualsensctl_answer.split(maxsplit=1)
else:
    exit(result.stderr.strip())
if not battery_procentage.isalnum:
    exit()
battery_procentage = int(battery_procentage)

if battery_status == "full":
    battery_status = "charging"

if battery_procentage < 33:
    if battery_status == "discharging":
        battery_icon = "󱊡"
    elif battery_status == "charging":
        battery_icon = "󱊤 "
elif battery_procentage < 66:
    if battery_status == "discharging":
        battery_icon = "󱊢"
    else:
        battery_icon = "󱊥 󱊥"
elif battery_procentage < 100:
    if battery_status == "discharging":
        battery_icon = "󱊣"
    else:
        battery_icon = "󱊦 "
else:
    battery_icon = "󰁹"

to_print = (
    f'"text":"󰊴 {battery_procentage}%{battery_icon}","tooltip":"Turn off controller"'
)
print("{" + to_print + "}")
