local windowrule = hl.window_rule

local function notify(text)
  hl.exec_cmd("notify-send " .. text)
end


windowrule({
  -- Fix some dragging issues with XWayland
  name     = "fix-xwayland-drags",
  match    = {
    class      = "^$",
    title      = "^$",
    xwayland   = true,
    float      = true,
    fullscreen = false,
    pin        = false,
  },

  no_focus = true,
})
windowrule({
  name = "rofi",
  match = {
    class = "^(Rofi)$"
  },
  stay_focused = true,
  focus_on_activate = true,
  dim_around = true,
  pin = true,
})
windowrule({
  name = "copyq",
  match = { class = "com.github.hluk.copyq" },
  float = true,
  stay_focused = true,
  dim_around = true,
  -- pin = true,
  focus_on_activate = true
})
windowrule({
  name = "flameshot",
  match = { class = "flameshot" },
  animation = "fade",
  rounding = false,
  border_size = 0,
  fullscreen = true,
  float = true,
  -- pin = true,
  monitor = 1,
  move = { 0, 0 },
  size = { "(monitor_w*2)", "(monitor_h)" },
})
windowrule({
  name = "wayland-boomer",
  match = { title = "^wayland-boomer$" },
  float = true,
  fullscreen = true,
  no_anim = true,
  monitor = 1,
  move = { 0, 0 },
})
windowrule({
  decorate = false,focus_on_activate=true
})
