#!/usr/bin/env python3
"""Copy a mod folder to the phone (adb) and reload the mods.

    python tools/push.py my_mod            # copy + reload + enable (dev build only for the reload part)
    python tools/push.py my_mod --no-reload

Needs adb on PATH and the kmod DEV build on the phone. The reload works by writing kmod/dev/console.lua, which the dev
build runs whenever the file changes; its output is printed here.
"""
import os, subprocess, sys, tempfile, time

ROOT = "/sdcard/Android/media/com.android1939.kardsapk/kmod"


def adb(*args, check=True):
    r = subprocess.run(["adb", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        print(r.stdout + r.stderr)
        sys.exit(1)
    return r.stdout


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        sys.exit(1)
    folder = os.path.normpath(args[0])
    mod_id = os.path.basename(folder)
    if not os.path.isfile(os.path.join(folder, "mod.json")):
        print(f"{folder} has no mod.json")
        sys.exit(1)

    adb("shell", f"rm -rf {ROOT}/mods/{mod_id}")
    adb("push", folder, f"{ROOT}/mods/")
    print(f"copied {mod_id} to {ROOT}/mods/")
    if "--no-reload" in sys.argv:
        return

    adb("shell", f"rm -f {ROOT}/dev/console.out")
    # the dev build runs console.lua at every start, so the script deletes itself first
    script = f'os.remove(kmod.paths.dev .. "/console.lua")\nkmod.console_exec("enable {mod_id}")\nkmod.console_exec("mods")\nprint("--done--")\n'
    with tempfile.NamedTemporaryFile("w", suffix=".lua", delete=False, encoding="utf-8") as f:
        f.write(script)
        local = f.name
    adb("push", local, f"{ROOT}/dev/console.lua")
    os.unlink(local)
    for _ in range(40):
        time.sleep(0.5)
        out = adb("shell", f"cat {ROOT}/dev/console.out", check=False)
        if "--done--" in out:
            print(out.replace("--done--", "").rstrip())
            return
    print("no answer from the game: is the DEV build running? (the copy itself worked; reload from the Mods page or restart)")


if __name__ == "__main__":
    main()
