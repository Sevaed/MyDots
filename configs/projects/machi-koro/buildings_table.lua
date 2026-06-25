require("copy")

Base = {
  blue = {
    wheat_field = {
      cost = 1,
      activation_numbers = { 1 },
      income = { type = "simple", amount = 1 },
      symbol = "grain",
      amount = 6
    },

    ranch = {
      cost = 1,
      activation_numbers = { 2 },
      income = { type = "simple", amount = 1 },
      symbol = "cow",
      amount = 6
    },

    forest = {
      cost = 3,
      activation_numbers = { 5 },
      income = { type = "simple", amount = 1 },
      symbol = "gear",
      amount = 6
    },

    mine = {
      cost = 6,
      activation_numbers = { 9 },
      income = { type = "simple", amount = 5 },
      symbol = "gear",
      amount = 6
    },

    apple_orchard = {
      cost = 3,
      activation_numbers = { 10 },
      income = { type = "simple", amount = 3 },
      symbol = "grain",
      amount = 6
    },
  },

  green = {
    bakery = {
      activation_numbers = { 2, 3 },
      cost = 1,
      income = { type = "simple", amount = 1 },
      symbol = "box",
      amount = 6
    },

    convenience_store = {
      activation_numbers = { 4 },
      cost = 2,
      income = { type = "simple", amount = 3 },
      symbol = "box",
      amount = 6
    },

    cheese_factory = {
      activation_numbers = { 7 },
      cost = 5,
      income = { type = "symbol", symbol = "cow", amount = 3 },
      symbol = "factory",
      amount = 6
    },

    furniture_factory = {
      activation_numbers = { 8 },
      cost = 3,
      income = { type = "symbol", symbol = "gear", amount = 3 },
      symbol = "factory",
      amount = 6
    },

    fruit_and_vegetable_market = {
      activation_numbers = { 11, 12 },
      cost = 2,
      income = { type = "symbol", symbol = "grain", amount = 2 },
      symbol = "market",
      amount = 6
    },
  },

  red = {
    cafe = {
      activation_numbers = { 3 },
      cost = 2,
      income = { type = "rob", victim = "active_player", amount = 1 },
      symbol = "cup",
      amount = 6
    },

    restaurant = {
      activation_numbers = { 9, 10 },
      cost = 3,
      income = { type = "rob", victim = "active_player", amount = 2 },
      symbol = "cup",
      amount = 6
    },
  },

  violet = {
    stadium = {
      activation_numbers = { 6 },
      cost = 6,
      income = { type = "rob", victim = "all", amount = 2 },
      symbol = "tower",
      amount = 5
    },

    tv_station = {
      activation_numbers = { 6 },
      cost = 7,
      income = { type = "rob", victim = "any", amount = 5 },
      symbol = "tower",
      amount = 5
    },

    business_center = {
      activation_numbers = { 6 },
      cost = 8,
      income = { type = "custom_action", action = "TODO" },
      symbol = "tower",
      amount = 5
    },
  },

  special = {
    train_station = {
      cost = 4,
      desc = "можно бросать 2 кубика",
      amount = 0
    },

    shopping_mall = {
      cost = 10,
      desc = "каждое предприятие с символом коробки/чашки приносит на 1 монету больше",
      amount = 0
    },

    amusement_park = {
      cost = 16,
      desc = "если на кубиках выпал дубль сделайте ещё 1 ход",
      amount = 0
    },

    radio_tower = {
      cost = 22,
      desc = "один раз за ход можно перепросить кубики",
      amount = 0
    },
  }
}

Starter_pack = {
  blue = {
    wheat_field = {
      activation_numbers = { 1 },
      income = { type = "simple", amount = 1 },
      symbol = "grain",
      amount = 1
    }
  },

  green = {
    bakery = {
      activation_numbers = { 2, 3 },
      income = { type = "simple", amount = 1 },
      symbol = "box",
      amount = 1,
    }
  }
}

Types = {
  wheat_field = "blue",
  ranch = "blue",
  forest = "blue",
  mine = "blue",
  apple_orchard = "blue",

  bakery = "green",
  convenience_store = "green",
  cheese_factory = "green",
  furniture_factory = "green",
  fruit_and_vegetable_market = "green",

  cafe = "red",
  restaurant = "red",

  stadium = "violet",
  tv_station = "violet",
  business_center = "violet",

  train_station = "special",
  shopping_mall = "special",
  amusement_park = "special",
  radio_tower = "special",
}
function Move_building(building_name, inventory)
  local type = Types[building_name]
  local building = Base[type][building_name]
  if not inventory[type] then
    inventory[type] = {}
  end
  if inventory[type][building_name] then
    inventory[type][building_name].amount = inventory[type][building_name].amount + 1
  else
    local to_insert = table.copy(building)
    to_insert.amount = 1
    inventory[type][building_name] = to_insert
  end
  building.amount = building.amount - 1
end

return {
  Base = Base,
  Starter_pack = Starter_pack,
  Types = Types,
  Move_building = Move_building
}
