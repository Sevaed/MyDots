table.copy = function(orig, copies)
  copies = copies or {}
  local copy = {}
  if type(orig) == 'table' then
    if copies[orig] then
      copy = copies[orig]
    else
      copies[orig] = copy
      for orig_key, orig_value in next, orig, nil do
        copy[table.copy(orig_key, copies)] = table.copy(orig_value, copies)
      end
      setmetatable(copy, table.copy(getmetatable(orig), copies))
    end
  else
    copy = orig
  end
  return copy
end
