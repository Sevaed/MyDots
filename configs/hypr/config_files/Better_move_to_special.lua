function Better_move_to_special()
  local active_window_addres = hl.get_active_window().address
  local active_workspace_id = hl.get_active_workspace().id
  if active_window_addres and active_workspace_id then
    local window_workspace_id = hl.get_active_window().workspace.id
    if window_workspace_id == active_workspace_id then
      hl.dsp.window.move({ workspace = "special:magic" })
    else
      hl.dsp.window.move({ workspace = active_workspace_id })
    end
  end
end
