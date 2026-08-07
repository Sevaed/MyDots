local config_directory_name = "config_files/"

local files_list = { "variables", "autostart", "keybindings", "windowrules", "looks", "plugins", "input" }
for _, v in pairs(files_list) do
  require(config_directory_name .. v)
end

hl.monitor({
  output   = "desc: Philips Consumer Electronics Company PHL 243V5 ZV01543018798",
  mode     = "prefered",
  position = "auto",
  scale    = "1",
})
hl.monitor({
  output   = "desc: Dell Inc. DELL P2418D MY3ND9C304DT",
  mode     = "2560x1440@59.95",
  position = "0x0",
  scale    = "1.25",
})



hl.env("XCURSOR_SIZE", "24")
hl.env("HYPRCURSOR_SIZE", "24")
hl.env("QT_QPA_PLATFORMTHEME", "qt6ct")
