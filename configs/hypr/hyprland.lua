local config_directory_name = "config_files/"

local files_list = { "variables", "autostart", "keybindings", "windowrules", "looks", "plugins" ,"input"}
for _, v in pairs(files_list) do
  require(config_directory_name .. v)
end

hl.monitor({
  output   = "",
  mode     = "preferred",
  position = "auto",
  scale    = "auto",
})



hl.env("XCURSOR_SIZE", "24")
hl.env("HYPRCURSOR_SIZE", "24")
hl.env("QT_QPA_PLATFORMTHEME","qt6ct")
