local UI = require("UI")
local buildings_table = require("buildings_table")

local players_amount = UI.get_players_amount()
local players_data = {}
local function initialize_game(players_amount)
  for player = 1, players_amount, 1 do
    players_data[player] = { active = false, money = 3, inventory = table.copy(buildings_table.Starter_pack) }
  end
end

local function roll_the_dice(amount)
  if amount == 1 then
    return { math.random(1, 6), 0 }
  else
    return { math.random(1, 6), math.random(1, 6) }
  end
end

local function check_for_finish()
  for player, data in pairs(players_data) do
    local count = 0
    for _ in pairs(data.inventory.special or {}) do
      count = count + 1
    end
    if count == 4 then
      UI.finish(player)
      return true
    end
  end
  return false
end

local function evaluate_result(result, active_player_id)
  result = result[1] + result[2]
  local function deal_with_income_type(building, inventory, to_double)
    local income_type = building.income.type
    local income_amount = building.income.amount
    if to_double then income_amount = income_amount + 1 end
    if income_type == "simple" then
      return income_amount
    elseif income_type == "symbol" then
      local symbol = building.income.symbol
      local counter = 0
      for _, i in pairs(inventory.blue) do
        if i.symbol == symbol then
          counter = counter + i.amount
        end
      end
      return income_amount * counter
    elseif income_type == "rob" then
      local victim = building.income.victim
      if victim == "active_player" then
        local active_player_money = players_data[active_player_id].money
        if active_player_money >= income_amount then
          players_data[active_player_id].money = active_player_money - income_amount
          return income_amount
        elseif active_player_money > 0 then
          players_data[active_player_id].money = 0
          return active_player_money
        else
          return 0
        end
      elseif victim == "all" then
        local bank = 0
        for _, player in pairs(players_data) do
          local player_money = player.money
          if player_money >= income_amount then
            bank = bank + income_amount
            player.money = player_money - income_amount
          elseif player_money > 0 then
            bank = bank + player_money
            player.money = 0
          end
        end
        return bank
      elseif victim == "any" then
        local victim_id = UI.choose_victim(active_player_id, players_data, income_amount)
        if victim_id == false then
          return 0
        end
        local victim_money = players_data[victim_id].money
        if victim_money >= income_amount then
          players_data[victim_id].money = victim_money - income_amount
          return income_amount
        elseif victim_money > 0 then
          players_data[victim_id].money = 0
          return victim_money
        else
          return 0
        end
      end
    else
      print("TODO")
    end
  end
  local to_check = { "red", "blue", "green", "violet" }
  for _, color in ipairs(to_check) do
    for player_id = 1, players_amount do
      local inventory = players_data[player_id].inventory
      local to_double = false
      if inventory.special and inventory.special.shopping_mall then
        to_double = true
      end
      if player_id == active_player_id and color == "red" then
        goto continue
      end
      if player_id ~= active_player_id and (color == "green" or color == "violet") then
        goto continue
      end
      local income = 0
      for _, building in pairs(inventory[color] or {}) do
        for _, number in ipairs(building.activation_numbers) do
          if result == number then
            if to_double and (building.symbol == "cup" or building.symbol == "box") then
              income = income + deal_with_income_type(building, inventory, true)
            else
              income = income + deal_with_income_type(building, inventory)
            end
          end
        end
      end
      players_data[player_id].money = players_data[player_id].money + income
      ::continue::
    end
  end
end
local function purchase_phase(active_player)
  local choice = UI.shop(active_player.money)
  if choice then
    buildings_table.Move_building(choice, active_player.inventory)
  end
end
local function move(active_player_id)
  print("Yours move "..active_player_id)
  local active_player = players_data[active_player_id]
  local amount_of_dices = 1
  if active_player.inventory.special and players_data[active_player_id].inventory.special.train_station then
    amount_of_dices = UI.ask_about_dices()
  end
  local result = roll_the_dice(amount_of_dices)
  if active_player.inventory.special and active_player.inventory.special.radio_tower and UI.ask_about_reroll() then
    if active_player.inventory.special.train_station then
      amount_of_dices = UI.ask_about_dices()
    end
    result = roll_the_dice(amount_of_dices)
  end
  if amount_of_dices == 1 then
    print("Dice rolls on: " .. result[1])
  else
    print("Dices rolls on: " .. result[1] .. ", " .. result[2])
  end
  evaluate_result(result, active_player_id)
  for id, player in pairs(players_data) do
    print(id..": "..player.money)
  end
  if active_player.money > 0 then
    purchase_phase(active_player)
  end
  if (active_player.inventory.special and active_player.inventory.special.amusement_park) and result[1] == result[2] then
    if UI.ask_about_second_move() then
      move(active_player_id)
    end
  end
end



initialize_game(players_amount)
local active_player_id = 1
while true do
  move(active_player_id)
  if check_for_finish() then
    break
  end
  active_player_id = active_player_id % players_amount + 1
end
