table.unpack = unpack
XPadding = 50
YPadding = 20
BlockXPadding = 2
BlockYPadding = 2
BlockHeight = 10
BlockWidth = 40


PlatformHeight = BlockHeight
PlatformWidth = 50
PlatformPadding = 20
PlatformSpeed = 600
function love.load()
  if love.window.setFullscreen(true) then
    Rectangles = {}
    width, height = love.graphics.getDimensions()
    PlatformX = width / 2 - PlatformWidth / 2
    XPadding = XPadding +
        (width - math.floor((width - XPadding * 2) / (BlockWidth + BlockXPadding) - BlockXPadding) * (BlockWidth + BlockXPadding)) /
        2
    local x = XPadding
    local y = YPadding
    repeat
      repeat
        local color = { 255, 255, 255 }
        if #Rectangles % 3 == 0 then color = { 0, 0, 255 } end
        table.insert(Rectangles, {
          x = x,
          y = y,
          color = color
        })
        y = y + BlockHeight + BlockYPadding
      until y + BlockHeight >= height / 2
      x = x + BlockWidth + BlockXPadding
      y = YPadding
    until x + BlockWidth + XPadding >= width
  else
    os.exit("NoFullScreen")
  end
end

function love.update(dt)
  local touches = love.touch.getTouches()

  for _, id in ipairs(touches) do
    local x, y = love.touch.getPosition(id)
    if x > width / 2 then
      PlatformX = PlatformX + PlatformSpeed * dt
    else
      PlatformX = PlatformX - PlatformSpeed * dt
    end
  end
  if PlatformX < 0 then
    PlatformX = 0
  elseif PlatformX + PlatformWidth > width then
    PlatformX = width - PlatformWidth
  end
end

function love.draw()
  -- (width - math.floor((width - 50* 2) / (BlockWidth + BlockXPadding) - BlockXPadding) * (BlockWidth + BlockXPadding)) /2
  local sas = string.format("widthP: %i\n", width - 100)
  --   width -
  --   math.floor((width - 50 * 2) / (BlockWidth + BlockXPadding) - BlockXPadding) * (BlockWidth + BlockXPadding)) /
  -- 2
  love.graphics.setColor(love.math.colorFromBytes(255, 255, 255))
  love.graphics.print(sas, 10, 10)
  for _, rectangle in ipairs(Rectangles) do
    love.graphics.setColor(love.math.colorFromBytes(table.unpack(rectangle.color)))
    love.graphics.rectangle("fill", rectangle.x, rectangle.y, BlockWidth, BlockHeight)
    love.graphics.setColor(love.math.colorFromBytes(255, 255, 255))
  end

  love.graphics.setColor(love.math.colorFromBytes(255, 0, 0))
  love.graphics.rectangle("fill", PlatformX, height - PlatformPadding - PlatformHeight, PlatformWidth,
    PlatformHeight)
end
