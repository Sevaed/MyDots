import os
import sys
import json

# TODO w*ndows shit
# dev
file = os.path.abspath("desktop.spcf.json")

hid_keys = {
    "4": "a",
    "5": "b",
    "6": "c",
    "7": "d",
    "8": "e",
    "9": "f",
    "10": "g",
    "11": "h",
    "12": "i",
    "13": "j",
    "14": "k",
    "15": "l",
    "16": "m",
    "17": "n",
    "18": "o",
    "19": "p",
    "20": "q",
    "21": "r",
    "22": "s",
    "23": "t",
    "24": "u",
    "25": "v",
    "26": "w",
    "27": "x",
    "28": "y",
    "29": "z",
    "30": "1",
    "31": "2",
    "32": "3",
    "33": "4",
    "34": "5",
    "35": "6",
    "36": "7",
    "37": "8",
    "38": "9",
    "39": "0",
    "40": "Enter",
    "41": "Esc",
    "42": "Backspace",
    "43": "Tab",
    "44": "Space",
    "45": "-",
    "46": "=",
    "47": "[",
    "48": "]",
    "49": "\\",
    "51": ";",
    "52": "'",
    "53": "`",
    "54": ",",
    "55": ".",
    "56": "/",
    "57": "CapsLock",
    "58": "F1",
    "59": "F2",
    "60": "F3",
    "61": "F4",
    "62": "F5",
    "63": "F6",
    "64": "F7",
    "65": "F8",
    "66": "F9",
    "67": "F10",
    "68": "F11",
    "69": "F12",
    "79": "Right",
    "80": "Left",
    "81": "Down",
    "82": "Up",
    "224": "LeftCtrl",
    "225": "LeftShift",
    "226": "LeftAlt",
    "227": "LeftMeta",
    "228": "RightCtrl",
    "229": "RightShift",
    "230": "RightAlt",
    "231": "RightMeta",
}
button_id = {
    "left": "left",
    "scroll_up": "scroll_up",
    "middle": "middle",
    "scroll_down": "scroll_down",
    "right": "right",
    "fingertipLeft": "fingertip_left",
    "fingertipRight": "fingertip_right",
    "triggerLeftPush": "trigger_left_push",
    "triggerRightPush": "trigger_right_push",
    "triggerLeftPull": "trigger_left_pull",
    "maxButtonValue": "trigger_right_pull",
    "edgeFront": "edge_front",
    "edgeRear": "edge_rear",
    "thumbTop": "thumb_top",
    "thumbBottom": "thumb_bottom",
}

output_action_ids = [
    "dpiConfigure",
    "reportInterval",
    "liftOffSelect",
    "gameDeviceSelect",
    "ledSet",
    "oledSet",
    "autoReleaseInputs",
    "tiltAutoZeroing",
    "doNothing",
    "keyboardKey",
    "wait",
    "hapticFeedback",
    "keyboardKeyString",
    "mouseButton",
    "mouseScroll",
    "keyboardMedia",
    "alternateOutputActions",
    "gotoOutputAction",
    "stopLooping",
    "joystickButton",
    "profileJump",
]


def evaluate_keyboard_key(output_item):
    HidPageValue = str(output_item["KeyCode"]["HidPageValue"])
    ButtonState = output_item["ButtonState"]
    if ButtonState == "downOn":
        answer = "↓"
    elif ButtonState == "upOff":
        answer = "↑"
    elif ButtonState == "tap":
        answer = "•"
    else:
        exit("line 143")
    if HidPageValue in hid_keys:
        answer += hid_keys[HidPageValue]
    return answer


def evaluate_haptic_feedback(output_item):
    StrengthPercentage = output_item["StrengthPercentage"]
    Time_ms = output_item["Time10ms"]
    return (StrengthPercentage, Time_ms)


def evaluate_dpi_configure(output_item):
    levels = []
    for level in output_item["Levels"]:
        levels.append({"XDpi": level["XDpiRaw"], "YDpi": level["YDpiRaw"]})
    return levels


def evaluate_led(output_item):
    # TODO find more data
    return "NotImplementedYet"


def evaluate_oled(output_item):
    # TODO find more data
    return "NotImplementedYet"


def get_action(value):
    # TODO add all actions
    answer = {"Activation": [], "Deactivation": []}
    parsers = {
        # "":lambda action: {"":},
        "keyboardKey": lambda action: {"keyboard_key": evaluate_keyboard_key(action)},
        "hapticFeedback": lambda action: {
            "hapticFeedback": evaluate_haptic_feedback(action)
        },
        "keyboardKeyString": lambda action: {"string": action["KeyString"]},
        "wait": lambda action: {"wait": action["TimeToWaitms"]},
        "mouseButton": lambda action: {
            "mouse_button": action["ButtonId"],
            "button_state": action["ButtonState"],
        },
        "mouseScroll": lambda action: {"mouse_scroll": action["ScrollDirection"]},
        "dpiConfigure": lambda action: {"dpi_levels": evaluate_dpi_configure(action)},
        "reportInterval": lambda action: {"report_interval": action["ReportInterval"]},
        "liftOffSelect": lambda action: {"liftOffSelect": action["Level"]},
        "gameDeviceSelect": lambda action: {"gamepad_emulation": action["GameDevice"]},
        "ledSet": lambda action: {"led": evaluate_led(action)},
        "oledSet": lambda action: {"oled": evaluate_oled(action)},
        "autoReleaseInputs": lambda action: {
            "autoReleaseInputs": True if action["State"] == "enabled" else False
        },
        "tiltAutoZeroing": lambda action: {
            "tiltAutoZeroing": True if action["State"] == "enabled" else False
        },
    }

    for Output in ["ActivationOutputActionItems", "DeactivationOutputActionItems"]:
        if Output == "ActivationOutputActionItems":
            for action in value[Output]:
                if action["TypeId"] != "doNothing":
                    if action["TypeId"] not in parsers:
                        exit(f"{value[Output]['TypeId']} not implemented yet")
                    answer["Activation"].append(parsers[action["TypeId"]](action))
        if Output == "DeactivationOutputActionItems":
            for action in value[Output]:
                if action["TypeId"] != "doNothing":
                    if action["TypeId"] not in parsers:
                        exit(f"{value[Output]['TypeId']} not implemented yet")
                    answer["Deactivation"].append(parsers[action["TypeId"]](action))
    return answer


def evaluate_force(output_action, type_of_force):
    if type_of_force == "toggle":
        region = output_action["Region"]
        return region["EntryStartPercentageTenths"] / 10
    elif type_of_force == "range":
        force_range = output_action["Range"]
        return (
            force_range["StartPercentageTenths"] / 10,
            force_range["EndPercentageTenths"] / 10,
        )


def get_trigger(value):
    # TODO add different triggers
    answer = {}
    InputActionType = value["InputActionType"]
    Id = InputActionType["Id"]
    parses = {
        # "":lambda action: {"":},
        "systemEvent": lambda action: {"system_event": action["Code"]},
        "buttonToggle": lambda action: {
            "button_toggle": button_id[action["Button"]["Id"]]
        },
        "forceRegionToggle": lambda action: {
            "button_toggle": button_id[action["Button"]["Id"]],
            "activation_force": evaluate_force(action, "toggle"),
        },
        "forceRange": lambda action: {
            "button_toggle": button_id[action["Button"]["Id"]],
            "activation_range": evaluate_force(action, "range"),
        },
        "scroll": lambda action: {
            "scroll_wheel_direction": action["ScrollWheelDirection"]
        },
    }
    if Id not in parses:
        print(f"{Id} is not implemented yet")
    else:
        tmp = parses[Id](InputActionType)
        answer["Trigger"] = {list(tmp.keys())[0]: tmp[list(tmp.keys())[0]]}
        if len(tmp) == 2:
            answer["modificator"] = {list(tmp.keys())[1]: tmp[list(tmp.keys())[1]]}
    # if InputActionType["Id"] == "buttonToggle":
    #     answer["Trigger"] = f"{button_id[InputActionType["Button"]["Id"]]}"
    # elif InputActionType["Id"] == "forceRegionToggle":
    #     answer["Trigger"] = button_id[InputActionType["Button"]["Id"]]
    #     answer["modificator"] = "NotImplementedYet"
    # elif InputActionType["Id"] == "scroll":
    #     if InputActionType["ScrollWheelDirection"] == "forward":
    #         answer["Trigger"] = "button_mouse_2"
    #     else:
    #         answer["Trigger"] = "button_mouse_4"
    # if answer["Trigger"] == "":
    #     answer["Trigger"] = "NotImplementedYet"
    return answer


def parse_file(file):
    answer = []
    with open(file, "r") as file:
        data = json.load(file)

    values = data["RootProfile"]["Groups"][0]["ActionMappings"]["$values"]
    for value in values:
        answer.append([get_trigger(value), get_action(value)])
    return answer


print(parse_file(file))
