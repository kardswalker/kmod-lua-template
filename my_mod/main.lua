-- main.lua runs once when the mod is loaded (game start, or after `reload`).
-- Everything registered here (hooks, timers, console commands) is removed automatically when the mod is reloaded or disabled.

Log.info(Lang.t("loaded", { id = Mod.id, version = Mod.version }))

-- Settings declared in mod.json. Read them once and keep them up to date.
local verbose = Settings.get("verbose")
Settings.on_change(function(id, value)
  if id == "verbose" then verbose = value end
  Log.info("setting " .. id .. " = " .. tostring(value))
end)

-- Find a game object. Not found = an INVALID object (not nil), so always check IsValid().
local pc = FindFirstOf("PlayerController")
if pc:IsValid() then
  Log.info("player controller: " .. pc:GetPathName())
end

-- A console command (type `my_mod.hello Bob` in the dev console).
Console.register("my_mod.hello", function(args)
  local who = args[1] or Settings.get("nick")
  return Lang.t("hello", { name = who })
end, { help = "say hello", usage = "my_mod.hello [name]" })

-- A repeating task: every 5 seconds, 3 times. Return true to stop.
local ticks = 0
LoopAsync(5000, function()
  ticks = ticks + 1
  if verbose then Log.info("tick " .. ticks) end
  return ticks >= 3
end)

-- Hook a game function (the function must already exist in memory).
-- Find paths with the console: `search PlayerController clientrestart function`,
-- watch calls with: `hook /Script/Engine.PlayerController:ClientRestart 5`.
--
-- RegisterHook("/Script/Engine.PlayerController:ClientRestart", function(self, params)
--   Log.info("restart: " .. self:GetName())
-- end)