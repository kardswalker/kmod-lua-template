# kmod mod template

A starting point for a [kmod loader](https://ccb-team.github.io/KMod-Loader-Android/) mod (Lua).

```
my_mod/            the mod itself: rename the folder AND the "id" in mod.json (they must match)
  mod.json         manifest: id, version, dependencies, settings
  main.lua         the script (comments explain each part)
  lang/            optional translations (en.json, zh-CN.json ...)
tools/pack.py      check the mod and pack it into dist/<id>-<version>.kmod
tools/push.py      copy the mod to the phone with adb and reload it (dev build)
types/             type declarations for VS Code: kmod_api.lua is included, the game classes come from `typegen` (see below)
.luarc.json        language server settings (points at ./types)
```

## Set up VS Code (autocomplete for the whole game)

1. Install VS Code and the **Lua** extension by sumneko (this folder recommends it). `types/kmod_api.lua` already gives
   completion for the kmod API (`Mod`, `Log`, `Settings`, `FindFirstOf`, `RegisterHook` ...).
2. For the game's own classes: in the game (dev build) open the console and run `typegen`. Then copy the result here:
   `adb pull /sdcard/Android/media/com.android1939.kardsapk/kmod/types .`
   (or copy the `types` folder off the phone over USB). Blueprint UI classes only appear if their screen was open
   when you ran `typegen`.
3. Open this folder in VS Code. Typing `FindFirstOf("PlayerController")` now gives completion and type info, and typos
   in property or function names are underlined.

## Work cycle

1. Edit `my_mod/main.lua` on the PC.
2. `python tools/push.py my_mod` copies it to the phone, enables it and reloads (dev build must be running).
3. Look at the output of `kmod/logs/kmod.log` on the phone, or `adb logcat -s KModCore KModLoader`.
4. Explore the game from the dev console: `search`, `find`, `props`, `funcs`, `hook`.

Without adb: copy the `my_mod` folder into `Android/media/com.android1939.kardsapk/kmod/mods/` by any means (file manager,
USB), then press **Mods** in the game settings (or type `reload` in the dev console) and tick the mod.

## Share it

`python tools/pack.py my_mod` writes `dist/my_mod-0.1.0.kmod`. Players put that file into
`Android/media/com.android1939.kardsapk/kmod/inbox/`; it installs on the next start or when the Mods page opens.

Docs: https://ccb-team.github.io/KMod-Loader-Android/
