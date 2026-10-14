local mainMod = "ALT"
local function notify(text)
  hl.exec_cmd("notify-send " .. text)
end

function Better_move_to_special()
  if hl.get_active_workspace().id == hl.get_active_window().workspace.id then
    hl.dispatch(hl.dsp.window.move({ workspace = "special:magic" }))
  else
    hl.dispatch(hl.dsp.window.move({ workspace = hl.get_active_workspace() }))
  end
end

function Swap_workspace_and_special()
  local function get_widows()
    local special_windows = {}
    local pre_special_windows = hl.get_windows({ workspace = hl.get_active_special_workspace() })
    local workspace_windows = hl.get_windows({ workspace = hl.get_active_workspace() })
    if pre_special_windows then
      for _, window in ipairs(pre_special_windows) do
        if window.workspace.special then
          table.insert(special_windows, window)
        end
      end
    end
    return special_windows, workspace_windows
  end
  local special_windows, workspace_windows = get_widows()
  for index, value in ipairs(workspace_windows) do
    hl.dispatch(hl.dsp.window.move({ workspace = "special:magic", window = value }))
  end
  for index, value in ipairs(special_windows) do
    hl.dispatch(hl.dsp.window.move({ workspace = hl.get_active_workspace(), window = value }))
  end
end

Execute = hl.dsp.exec_cmd

local app_binds = {
  ["Q"] = terminal,
  ["E"] = fileManager,
  ["V"] = "copyq show",
  ["R"] = menu,
  ["W"] = browser
}

local scrips = {
  ["M"] = "kitty --app-id MSH ~/.config/projects/git/MouseSwitcherHyprland/mouse-switch.py",
  ["space"] = "~/.config/scripts/sound.py UwU",
}

local others = {
  ["SHIFT + K"] = "kill -9 $(hyprctl -j activewindow | jq '.pid')",
}

local macroces = {
  -- ["ALT + SHIFT + F1"] = "flameshot gui -c",
  -- ["ALT + F1"] =
  -- "sh -c 'lockfile=/tmp/screenshot.lock; [ -e $lockfile ] && exit; touch $lockfile; grim -g \"$(slurp)\" - | wl-copy; rm -f $lockfile'",
  -- ["ALT + F2"] =
  -- "sh -c 'lockfile=/tmp/boomer.lock; [ -e $lockfile ] && exit; touch $lockfile; grim - | wayland-boomer; rm -f $lockfile'",
  -- ["ALT+F3"] = "",
}

local executable = { app_binds, scrips, others, macroces }


local miscellaneous = {
  -- ["escape"] = hl.dsp.window.close(),
  ["escape"] = hl.dsp.window.close(),
  ["SHIFT + L"] = hl.dsp.exec_cmd("hyprshutdown"),
  ["C"] = hl.dsp.window.float({ action = "toggle" }),
  ["F"] = hl.dsp.window.fullscreen({ action = "toggle" }),
  ["TAB"] = Better_move_to_special,
  -- ["ALT + END"] = hl.dsp.pass({ window = "class:^(com\\.obsproject\\.Studio)$" }),
  ["T"] = Swap_workspace_and_special,
}


-- LOOPS
for _, group in pairs(executable) do
  for bind, command in pairs(group) do
    hl.bind(mainMod .. " + " .. bind, Execute(command))
  end
end


for bind, command in pairs(miscellaneous) do
  hl.bind(mainMod .. " + " .. bind, command)
end



-- MANUAL_BINDS

hl.bind("CTRL+ TAB", hl.dsp.workspace.toggle_special("magic"))
hl.bind("CTRL+ F1", Execute("grim -c - | wl-copy"))

-- HYPRSLOP

hl.bind(mainMod .. " + left", hl.dsp.focus({ direction = "left" }))
hl.bind(mainMod .. " + right", hl.dsp.focus({ direction = "right" }))
hl.bind(mainMod .. " + up", hl.dsp.focus({ direction = "up" }))
hl.bind(mainMod .. " + down", hl.dsp.focus({ direction = "down" }))

hl.bind(mainMod .. " + SHIFT + left", hl.dsp.window.move({ direction = "left" }))
hl.bind(mainMod .. " + SHIFT + right", hl.dsp.window.move({ direction = "right" }))
hl.bind(mainMod .. " + SHIFT + up", hl.dsp.window.move({ direction = "up" }))
hl.bind(mainMod .. " + SHIFT + down", hl.dsp.window.move({ direction = "down" }))

-- Switch workspaces with mainMod + [0-9]
-- Move active window to a workspace with mainMod + SHIFT + [0-9]
for i = 1, 10 do
  local key = i % 10 -- 10 maps to key 0
  hl.bind(mainMod .. " + " .. key, hl.dsp.focus({ workspace = i, on_current_monitor = true }))
  hl.bind(mainMod .. " + SHIFT + " .. key, hl.dsp.window.move({ workspace = i }))
end



hl.bind(mainMod .. " + mouse:272", hl.dsp.window.drag(), { mouse = true })
hl.bind(mainMod .. " + mouse:273", hl.dsp.window.resize(), { mouse = true })

-- Laptop multimedia keys for volume and LCD brightness
hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+"),
  { locked = true, repeating = true })
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"),
  { locked = true, repeating = true })
hl.bind("XF86AudioMute", hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"),
  { locked = true, repeating = true })
hl.bind("XF86AudioMicMute", hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle"),
  { locked = true, repeating = true })
hl.bind("XF86MonBrightnessUp", hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%+"), { locked = true, repeating = true })
hl.bind("XF86MonBrightnessDown", hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%-"), { locked = true, repeating = true })

-- Requires playerctl
hl.bind("XF86AudioNext", hl.dsp.exec_cmd("playerctl next"), { locked = true })
hl.bind("XF86AudioPause", hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioPlay", hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioPrev", hl.dsp.exec_cmd("playerctl previous"), { locked = true })
