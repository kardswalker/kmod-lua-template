kmod_api.lua (already here) declares kmod's own API: Mod, Log, Settings, Lang, Console, kmod, FindFirstOf, RegisterHook ...
It does not depend on the game version. zz_fallback.lua is a one-line placeholder so the example works before you run typegen.

For autocomplete of the GAME's classes, add the output of the `typegen` console command next to it:

  adb pull /sdcard/Android/media/com.android1939.kardsapk/kmod/types .

(or copy the types folder off the phone over USB). You should end up with files like types/Script_Engine.lua.
They are generated from your own game install; do not commit or share them. Running typegen also rewrites
kmod_api.lua, which is fine.
