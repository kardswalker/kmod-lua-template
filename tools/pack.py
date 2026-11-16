#!/usr/bin/env python3
"""Check a mod folder and pack it into dist/<id>-<version>.kmod (a zip with the files at its root).

    python tools/pack.py my_mod
"""
import json, os, re, sys, zipfile


def fail(msg):
    print("error:", msg)
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        fail("usage: python tools/pack.py <mod folder>")
    folder = os.path.normpath(sys.argv[1])
    if not os.path.isdir(folder):
        fail(f"{folder} is not a folder")
    try:
        with open(os.path.join(folder, "mod.json"), encoding="utf-8-sig") as f:
            mod = json.load(f)
    except (OSError, ValueError) as e:
        fail(f"mod.json: {e}")

    mod_id, version = mod.get("id"), mod.get("version")
    if mod.get("format") != 1:
        fail('mod.json: "format" must be 1')
    if not isinstance(mod_id, str) or not re.fullmatch(r"[a-z0-9_]+", mod_id):
        fail('mod.json: "id" must match [a-z0-9_]+')
    if mod_id != os.path.basename(folder):
        fail(f'mod.json: "id" ({mod_id}) must equal the folder name ({os.path.basename(folder)})')
    if version is None:
        fail('mod.json: "version" is required')
    if not os.path.isfile(os.path.join(folder, "main.lua")):
        fail("main.lua is missing")
    for s in mod.get("settings", []):
        if s.get("type") not in ("bool", "number", "choice", "string"):
            fail(f'setting "{s.get("id")}": unknown type {s.get("type")!r}')

    os.makedirs("dist", exist_ok=True)
    out = os.path.join("dist", f"{mod_id}-{version}.kmod")
    n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(folder):
            for name in sorted(files):
                path = os.path.join(root, name)
                z.write(path, os.path.relpath(path, folder).replace(os.sep, "/"))
                n += 1
    print(f"packed {n} file(s) -> {out}")


if __name__ == "__main__":
    main()
