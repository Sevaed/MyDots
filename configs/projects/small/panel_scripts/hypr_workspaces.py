#!/usr/bin/python
import subprocess
import json


def debug_print(text):
    if __name__ == "__main__":
        print(text)


def get_current_workspace() -> str:
    result = subprocess.run(["hyprctl", "activewindow", "-j"], capture_output=True)
    raw_data = json.loads(result.stdout.strip())
    if raw_data == {}:
        answer = json.loads(
            subprocess.run(
                ["hyprctl", "activeworkspace", "-j"], capture_output=True
            ).stdout.strip()
        )["id"]
    else:
        if raw_data["workspace"]["id"] == -98:
            answer = "󰥺"
        else:
            answer = raw_data["workspace"]["id"]
    return str(answer)


def get_current_non_magical_workspace() -> str:
    result = subprocess.run(["hyprctl", "activeworkspace", "-j"], capture_output=True)
    raw_data = json.loads(result.stdout.strip())
    return str(raw_data["id"])


def get_existing_workspaces() -> list[str]:
    result = subprocess.run(["hyprctl", "workspaces", "-j"], capture_output=True)
    raw_data = json.loads(result.stdout.strip())
    answer = []
    for i in raw_data:
        if i["id"] != -98:
            answer.append(str(i["id"]))
    answer.sort(key=int)
    answer.reverse()
    for i in raw_data:
        if i["id"] == -98:
            answer.append("󰥺")
    answer.reverse()
    return answer


def parse_workspaces(current_workspace: str, all_workspaces: list[str]) -> list[str]:
    if current_workspace not in all_workspaces:
        exit(
            f"Your code is ass, take debug info and fix it:\n{current_workspace}\n{all_workspaces}"
        )
    else:
        for number, workspace in enumerate(all_workspaces):
            if workspace == current_workspace:
                all_workspaces[number] = f" {current_workspace}"
            elif (
                current_workspace == "󰥺"
                and workspace == get_current_non_magical_workspace()
            ):
                all_workspaces[number] = f" {workspace}"
            else:
                all_workspaces[number] = f" {workspace}"
    return all_workspaces


thing = parse_workspaces(get_current_workspace(), get_existing_workspaces())
sas = ""
for i in thing:
    if len(sas) == 0:
        sas += i
    else:
        sas += " " + i
print(sas)
