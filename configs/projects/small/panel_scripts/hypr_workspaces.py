#!/usr/bin/env python
import subprocess
import json
import sys

SPECIAL_WORKSPACE_NAME = "󰥺"

ACTIVE_WORKSPACE_SYMBOL = " "
INACTIVE_WORKSPACE_SYMBOL = " "
BACKGROUND_WORKSPACE_SYMBOL = " "
SECOND_MONITOR_WORKSPACE_SYMBOL = "󰺕 "


ready = True

if len(sys.argv) > 1 and sys.argv[1] == "-d":
    ready = True


workspaces = json.loads(
    subprocess.run(["hyprctl", "workspaces", "-j"], capture_output=True).stdout.strip()
)

monitors = json.loads(
    subprocess.run(["hyprctl", "monitors", "-j"], capture_output=True).stdout.strip()
)

for monitor in monitors:
    if monitor["specialWorkspace"]["id"]:
        monitor["specialWorkspace"]["name"] = SPECIAL_WORKSPACE_NAME
    if monitor["focused"]:
        active_monitor = monitor
    else:
        inactive_monitor = monitor

# text = {
#     active_workspace_id: active_workspace_entry,
# }

# if background_workspace_id:
#     text[background_workspace_id] = background_workspace_entry
# if second_monitor_workspace_id:
#     text[second_monitor_workspace_id] = second_monitor_workspace_entry
# if inactive_workspaces_ids:
#     for it, id in enumerate(inactive_workspaces_ids):
#         text[id] = inactive_workspaces_entryes[it]

for workspace in workspaces:
    if workspace["id"] < 0:
        workspace["name"] = SPECIAL_WORKSPACE_NAME

unsorted_answer = {}
if active_monitor["specialWorkspace"]["id"]:
    unsorted_answer[active_monitor["specialWorkspace"]["id"]] = (
        ACTIVE_WORKSPACE_SYMBOL + active_monitor["specialWorkspace"]["name"]
    )
    unsorted_answer[active_monitor["activeWorkspace"]["id"]] = (
        BACKGROUND_WORKSPACE_SYMBOL + active_monitor["activeWorkspace"]["name"]
    )
else:
    unsorted_answer[active_monitor["activeWorkspace"]["id"]] = (
        ACTIVE_WORKSPACE_SYMBOL + active_monitor["activeWorkspace"]["name"]
    )


if inactive_monitor["specialWorkspace"]["id"]:
    unsorted_answer[inactive_monitor["specialWorkspace"]["id"]] = (
        SECOND_MONITOR_WORKSPACE_SYMBOL + inactive_monitor["specialWorkspace"]["name"]
    )
    unsorted_answer[inactive_monitor["activeWorkspace"]["id"]] = (
        ACTIVE_WORKSPACE_SYMBOL + inactive_monitor["activeWorkspace"]["name"]
    )
else:
    unsorted_answer[inactive_monitor["activeWorkspace"]["id"]] = (
        SECOND_MONITOR_WORKSPACE_SYMBOL + inactive_monitor["activeWorkspace"]["name"]
    )


for workspace in workspaces:
    if workspace["id"] not in unsorted_answer:
        unsorted_answer[workspace["id"]] = INACTIVE_WORKSPACE_SYMBOL + workspace["name"]

order = sorted(unsorted_answer, key=lambda el: el)
if ready:
    answer = ""
    for i in order:
        answer += unsorted_answer[i] + " "
    print(answer)
