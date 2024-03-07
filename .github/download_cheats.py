#!/usr/bin/env python3
# Copyright (c) 2022 José Manuel Barroso Galindo <theypsilon@gmail.com>

import time
import requests
import zipfile
import sys
import shutil
import traceback
from pathlib import Path

def main():
    start = time.time()

    target_dir = 'delme'
    if len(sys.argv) > 1:
        target_dir = sys.argv[1].strip()

    if 'delme' in target_dir.lower():
        shutil.rmtree(target_dir, ignore_errors=True)
        Path(target_dir).mkdir(parents=True, exist_ok=True)

    for i in range(8):
        try:
            install_cheats(target_dir)
            break
        except Exception as e:
            if i == 7:
                raise e
            print(e, flush=True)
            traceback.print_exc()
            print(f'Attempting again in 15 minutes... [{i}]', flush=True)
            time.sleep(60 * 15)

    print()
    print("Time:")
    end = time.time()
    print(end - start)
    print()

cheats_mapping = {
    "fds":"NES",
    "gb":"GameBoy",
    "gba":"GBA",
    "gbc":"GameBoy",
    "gen":"MegaDrive",
    "gg":"SMS",
    "lnx":"AtariLynx",
    "n64": "N64",
    "nes":"NES",
    "pce":"TGFX16",
    "pcd":"TGFX16-CD",
    "psx":"PSX",
    "scd":"MegaCD",
    "sms":"SMS",
    "snes":"SNES",
}

def install_cheats(target_dir):
    page_url = "https://gamehacking.org/mister"
    cheat_zips = collect_cheat_zips(page_url + '/?script=fetchcheats')

    for cheat_key, cheat_platform in cheats_mapping.items():
        cheat_zip = next(cheat_zip for cheat_zip in cheat_zips if cheat_key in cheat_zip)
        install_cheats_platform(target_dir, cheat_key, cheat_platform, page_url, cheat_zip)
        if cheat_key == 'sms':
            install_cheats_platform(target_dir, cheat_key, 'MegaDrive', page_url, cheat_zip)

def install_cheats_platform(target_dir, cheat_key, cheat_platform, page_url, cheat_zip):
    cheat_url = f'{page_url}/{cheat_zip}?script=fetchcheats'
    tmp_zip = f'/tmp/{cheat_key}{cheat_platform}.zip'
    cheat_folder = f'{target_dir}/Cheats/{cheat_platform}'

    print(f'cheat_keys: {cheat_key}, cheat_platform: {cheat_platform}, cheat_zip: {cheat_zip}, cheat_url: {cheat_url}', flush=True)

    download_file(cheat_url, tmp_zip)
    unzip(tmp_zip, cheat_folder)

def collect_cheat_zips(url):
    text = fetch_text(url)
    return [f[f.find('mister_'):f.find('.zip') + 4] for f in text.splitlines() if 'mister_' in f and '.zip' in f]

def fetch_text(url, cookies=None):
    r = requests.get(url, allow_redirects=True, cookies=cookies)
    if r.status_code != 200:
        raise Exception(f'Request to {url} failed: {r.status_code}')
    
    return r.text

def download_file(url, target):
    Path(target).parent.mkdir(parents=True, exist_ok=True)
    
    r = requests.get(url, allow_redirects=True)
    if r.status_code != 200:
        raise Exception(f'Request to {url} failed')
    
    with open(target, 'wb') as f:
        f.write(r.content)

def unzip(zip_file, target_dir):
    Path(target_dir).mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(target_dir)

if __name__ == '__main__':
    main()
