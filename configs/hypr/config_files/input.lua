local languages = require("config_files/languages")
local mouses = require("config_files/mouses")
hl.config({
  input = {
    kb_layout    = languages,
    kb_variant   = "",
    kb_model     = "pc104",
    kb_options   = "grp:win_space_toggle",
    kb_rules     = "",

    follow_mouse = 1,

    sensitivity  = 0, -- -1.0 - 1.0, 0 means no modification.

    touchpad     = {
      natural_scroll = false,
    },
  },
  misc = {
    middle_click_paste = false
  }
})


hl.device({
  name = "swiftpoint-limited-swiftpoint-creator",
  enabled = mouses.swiftpoint
})
hl.device({
  name = "razer-razer-basilisk-v3-x-hyperspeed-3",
  enabled = mouses.razer
})
