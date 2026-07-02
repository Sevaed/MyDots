User_apps = {
  browser, telegram .. " -startintray", discord .. " -m", SwiftPoint_X1, "qpwgraph -m",
  "copyq --start-server",
  "kdeconnect-indicator", "steam -silent", "obs --collection Base --minimize-to-tray" }
Background_services = { bar, "AmneziaVPN", "wl-clipdord-history -t", "wl-paste --watch cliphist store",
  "wl-clip-persist --clipbord regulr --disply wayland-1",
  "dbus-update-activation-environment --systemd --all", "ydotoold", "hyprpm reload",
  "systemctl --user start hyprpolkitagent", "hyprpaper", "niri-screen-time -daemon", "hyprpm update" ,"sunshine", "hypridle"}
Python_scripts = {
  "python ~/projects/small/controller_battery_statistic/log_writer.py 2>> ~/projects/small/controller_battery_statistic/err_log.txt" }
Lua_scripts = { "python ~/projects/small/recordings_move.lua" }
Commands = { User_apps, Background_services, Python_scripts, Lua_scripts }




hl.on("hyprland.start", function()
  for _, group in ipairs(Commands) do
    for _, command in ipairs(group) do
      hl.exec_cmd(command)
    end
  end
end)
