local lfs = require "lfs"
local sleep = require "sleep"
local initial_path = "/home/sevaed/Videos/obs/Recordings"
local destination_path = "/home/sevaed/Videos/obs/Replays"
while true do
for iter, dir_obj in lfs.dir(initial_path) do
  if iter then
    if string.find(iter, "Replay") then
      local filename = "/" .. iter
      os.rename(initial_path .. filename, destination_path .. filename)
      print("Moved \"" .. initial_path .. filename .. "\" to \"" .. destination_path .. filename .. "\"")
    end
  end
end
sleep(10*60*1000)
end
