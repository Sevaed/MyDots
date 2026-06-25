local buildings_table_lib = require("buildings_table")
require("copy")

local function ask(answer)
  answer = string.lower(answer)
  if answer == "y" or answer == "yes" then
    return true, true
  elseif answer == "n" or answer == "no" then
    return true, false
  else
    return false
  end
end



local function get_players_amount()
  local answer
  print("Input players amount from 2 to 5")
  repeat
    answer = tonumber(io.read())
  until type(answer) == "number" and (answer > 1 and answer < 6)
  return answer
end

local function finish(player)
  print("Player number " .. player .. "have won!")
end

local function choose_victim(active_player_id, players_data, income_amount)
  local answer
  local avalible_victims = {}
  for id, player in pairs(players_data) do
    if id ~= active_player_id and player.money > 0 then
      avalible_victims[tostring(id)] = player.money
    end
    if avalible_victims == {} then
      return false
    end
  end
  local options = ""
  for id, money in pairs(avalible_victims) do
    options = options .. id .. ": " .. tostring(money) .. "."
  end
  print("From who you want to steal " .. income_amount .. "?\n" .. options)
  repeat
    answer = tonumber(io.read())
  until type(answer) == "number" and answer > 1 and answer <= #avalible_victims
  return tonumber(answer)
end
local function ask_about_dices()
  local answer
  print("Do you want to roll 2 dices? Y/N")
  repeat
    answer = io.read()
    is_correct, to_return = ask(answer)
  until type(answer) == "string" and is_correct
  return to_return
end

local function ask_about_reroll()
  local answer
  print("Do you want to reroll dices? Y/N")
  repeat
    answer = io.read()
    is_correct, to_return = ask(answer)
  until type(answer) == "string" and is_correct
  return to_return
end

local function ask_about_second_move()
  local answer
  print("Do you want to make second move? Y/N")
  repeat
    answer = io.read()
    is_correct, to_return = ask(answer)
  until type(answer) == "string" and is_correct
  return to_return
end


local function shop(active_player)
  local function generate_description(building)
    local type_of_income = building.income.type
    local income_amount = building.income.amount
    local answer = ""
    if type_of_income == "simple" then
      answer = "Get " .. income_amount .. " from bank."
    elseif type_of_income == "rob" then
      local victim = building.income.victim
      if victim == "active_player" then
        answer = "Take " .. income_amount .. " from active player."
      elseif victim == "all" then
        answer = "Take " .. income_amount .. " from all players."
      elseif victim == "any" then
        answer = "Take " .. income_amount .. " from any choosen player."
      else
        print(victim .. "- was written as victim")
      end
    elseif type_of_income == "symbol" then
      local symbol = building.income.symbol
      answer = "Get " .. income_amount .. " from bank for each oif yours buildings with \"" .. symbol .. "\" symbol"
    elseif type_of_income == "custom_action" then
      print("TODO")
    else
      print(type_of_income .. "- was type_of_income")
    end
    local color = building.color
    if color == "blue" then
      answer = answer .. "\nOn any players move."
    elseif color == "red" then
      answer = answer .. "\nOn other players move."
    elseif color == "green" or color == "violet" then
      answer = answer .. "\nOn yours move."
    end
    return answer
  end
  local buildings_table = table.copy(buildings_table_lib.Base)
  local function prepare_buildings_table(buildings_table)
    local new_buildings_table = {}
    for color, buildings in pairs(buildings_table) do
      for smth, building in pairs(buildings) do
        building.color = color
        if color ~= "special" then
          building.desc = generate_description(building)
        end
        table.insert(new_buildings_table, building)
      end
    end
    return new_buildings_table
  end
  buildings_table = prepare_buildings_table(buildings_table)
  local page_size = 3
  local pages = {}
  for i = 1, math.ceil(#buildings_table / page_size), 1 do
    pages[i] = {}
  end
  for building_id = 1, #buildings_table, 1 do
    for page_number = 1, #pages do
      if #pages[page_number] < page_size then
        table.insert(pages[page_number], buildings_table[building_id])
        break
      end
    end
  end
  for index, page in ipairs(pages) do
    local spacer = "  |  "
    local text = ""
    local function evaluate_thing(thing)
      local answer = ""
      if thing.activation_numbers then
        local thing = thing.activation_numbers
        for i, value in ipairs(thing) do
          if #thing > 1 and i < #thing then
            answer = answer .. value .. ", "
          else
            answer = answer .. value
          end
        end
      end
      return answer
    end
    for bi, building in ipairs(page) do
      text = text .. evaluate_thing(building) .. "\n" .. building.desc
      if bi < 3 then
        text = text .. spacer
      end
      print(text)
    end
  end
  os.exit()
end



return {
  get_players_amount = get_players_amount,
  finish = finish,
  choose_victim = choose_victim,
  shop = shop,
  ask_about_dices = ask_about_dices,
  ask_about_reroll = ask_about_reroll,
  ask_about_second_move = ask_about_second_move,
}
