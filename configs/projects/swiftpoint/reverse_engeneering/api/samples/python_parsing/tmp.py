sas = [
    [
        {"Trigger": {"system_event": "profileChanged"}},
        {
            "Activation": [
                {
                    "dpi_levels": [
                        {"XDpi": 1500, "YDpi": 1500},
                        {"XDpi": 100, "YDpi": 12000},
                    ]
                },
                {"report_interval": "rI_1000_Hz"},
                {"liftOffSelect": "two"},
                {"gamepad_emulation": "none"},
                {"led": "NotImplementedYet"},
                {"oled": "NotImplementedYet"},
                {"autoReleaseInputs": True},
                {"tiltAutoZeroing": True},
            ],
            "Deactivation": [],
        },
    ],
    [
        {"Trigger": {"button_toggle": "trigger_left_push"}},
        {
            "Activation": [
                {"keyboard_key": "↓LeftAlt"},
                {"keyboard_key": "•F1"},
                {"keyboard_key": "↑LeftAlt"},
                {"hapticFeedback": (83, 7)},
            ],
            "Deactivation": [],
        },
    ],
    [
        {"Trigger": {"button_toggle": "fingertip_left"}},
        {
            "Activation": [
                {"keyboard_key": "↓LeftMeta"},
                {"keyboard_key": "↓LeftAlt"},
                {"keyboard_key": "•F1"},
                {"keyboard_key": "↑LeftMeta"},
                {"keyboard_key": "↑LeftAlt"},
            ],
            "Deactivation": [],
        },
    ],
    [
        {
            "Trigger": {"button_toggle": "fingertip_left"},
            "modificator": {"activation_force": 30.0},
        },
        {
            "Activation": [
                {"wait": 300},
                {"keyboard_key": "•Esc"},
                {"hapticFeedback": (42, 30)},
                {"wait": 100},
                {"keyboard_key": "↓LeftMeta"},
                {"keyboard_key": "↓LeftAlt"},
                {"keyboard_key": "↓LeftShift"},
                {"keyboard_key": "•F1"},
                {"keyboard_key": "↑LeftMeta"},
                {"keyboard_key": "↑LeftAlt"},
                {"keyboard_key": "↑LeftShift"},
            ],
            "Deactivation": [],
        },
    ],
    [
        {"Trigger": {"button_toggle": "edge_front"}},
        {
            "Activation": [
                {"keyboard_key": "↓LeftMeta"},
                {"keyboard_key": "•r"},
                {"keyboard_key": "↑LeftMeta"},
                {"wait": 500},
                {"string": "gimp"},
                {"keyboard_key": "•Enter"},
            ],
            "Deactivation": [{"keyboard_key": "↑y"}, {"keyboard_key": "↑LeftCtrl"}],
        },
    ],
    [
        {"Trigger": {"button_toggle": "trigger_left_pull"}},
        {
            "Activation": [
                {"keyboard_key": "↓LeftMeta"},
                {"keyboard_key": "•r"},
                {"keyboard_key": "↑LeftMeta"},
                {"wait": 500},
                {"string": "freecad"},
                {"keyboard_key": "•Enter"},
                {"wait": 500},
                {"keyboard_key": "•Tab"},
                {"keyboard_key": "•Space"},
            ],
            "Deactivation": [{"hapticFeedback": (83, 7)}],
        },
    ],
    [
        {"Trigger": {"button_toggle": "edge_rear"}},
        {
            "Activation": [
                {"keyboard_key": "↓LeftMeta"},
                {"keyboard_key": "•Esc"},
                {"keyboard_key": "↑LeftMeta"},
            ],
            "Deactivation": [],
        },
    ],
    [
        {"Trigger": {"button_toggle": "trigger_right_push"}},
        {
            "Activation": [
                {"keyboard_key": "↓LeftMeta"},
                {"keyboard_key": "•r"},
                {"keyboard_key": "↑LeftMeta"},
                {"wait": 300},
                {"string": "zoom"},
                {"keyboard_key": "•Enter"},
            ],
            "Deactivation": [],
        },
    ],
    [
        {"Trigger": {"button_toggle": "trigger_right_pull"}},
        {
            "Activation": [
                {"keyboard_key": "↓LeftMeta"},
                {"keyboard_key": "•q"},
                {"keyboard_key": "↑LeftMeta"},
                {"wait": 500},
                {"string": "fastfetch"},
                {"keyboard_key": "•Enter"},
            ],
            "Deactivation": [{"keyboard_key": "↑LeftMeta"}],
        },
    ],
    [
        {"Trigger": {"button_toggle": "left"}},
        {
            "Activation": [{"mouse_button": 0, "button_state": "downOn"}],
            "Deactivation": [{"mouse_button": 0, "button_state": "upOff"}],
        },
    ],
    [
        {
            "Trigger": {"button_toggle": "left"},
            "modificator": {"activation_force": 50.0},
        },
        {"Activation": [{"hapticFeedback": (0, 7)}], "Deactivation": []},
    ],
    [
        {"Trigger": {"button_toggle": "fingertip_right"}},
        {
            "Activation": [
                {"keyboard_key": "↓LeftMeta"},
                {"keyboard_key": "↓LeftShift"},
                {"keyboard_key": "•t"},
                {"keyboard_key": "↑LeftShift"},
                {"keyboard_key": "↑LeftMeta"},
            ],
            "Deactivation": [],
        },
    ],
    [
        {"Trigger": {"button_toggle": "middle"}},
        {
            "Activation": [{"mouse_button": 2, "button_state": "downOn"}],
            "Deactivation": [{"mouse_button": 2, "button_state": "upOff"}],
        },
    ],
    [
        {"Trigger": {"scroll_wheel_direction": "forward"}},
        {"Activation": [{"mouse_scroll": "up"}], "Deactivation": []},
    ],
    [
        {"Trigger": {"scroll_wheel_direction": "back"}},
        {"Activation": [{"mouse_scroll": "down"}], "Deactivation": []},
    ],
    [
        {"Trigger": {"button_toggle": "right"}},
        {
            "Activation": [{"mouse_button": 1, "button_state": "downOn"}],
            "Deactivation": [{"mouse_button": 1, "button_state": "upOff"}],
        },
    ],
    [
        {"Trigger": {"button_toggle": "trigger_left_push"}},
        {"Activation": [{"hapticFeedback": (83, 7)}], "Deactivation": []},
    ],
    [
        {"Trigger": {"button_toggle": "thumb_bottom"}},
        {
            "Activation": [{"mouse_button": 3, "button_state": "downOn"}],
            "Deactivation": [{"mouse_button": 3, "button_state": "upOff"}],
        },
    ],
    [
        {"Trigger": {"button_toggle": "thumb_top"}},
        {
            "Activation": [{"mouse_button": 4, "button_state": "downOn"}],
            "Deactivation": [{"mouse_button": 4, "button_state": "upOff"}],
        },
    ],
]
