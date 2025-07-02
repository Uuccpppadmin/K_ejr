#!/usr/bin/env python3
# Developer: Abraham
# Telegram: @K_ejr

import os
import re
import sys
from pathlib import Path

def print_intro():
    intro = """
+---------------------------------------------+
|              K_ejr Tool v1.0                |
|       Developed by: Abraham                 |
|       Telegram: @K_ejr                      |
|                                             |
|  A tool to convert XLSX to TXT and sort     |
|  numbers based on prefixes.                 |
+---------------------------------------------+
"""
    print(intro)

if "--help" in sys.argv:
    print("""
Usage: K_ejr or hhhh (no arguments needed)

Steps:
  1. Enter file path (.txt/.csv/.xlsx)
  2. Choose whether to remove prefix
  3. Enter filter prefixes (comma-separated)
  4. View sorted file in /sdcard/Download/egypt_numbers/
""")
    sys.exit()

def convert_xlsx_to_txt(filepath):
    import zipfile
    import xml.etree.ElementTree as ET

    if not zipfile.is_zipfile(filepath):
        print("❌ Not a valid XLSX file.")
        return None

    txt_path = Path(filepath).with_suffix(".txt")

    try:
        with zipfile.ZipFile(filepath) as archive:
            print("🔍 Opened XLSX archive successfully.")
            sheet_xml = archive.read("xl/worksheets/sheet1.xml")
            print("✅ Read sheet1.xml")

        root = ET.fromstring(sheet_xml)
        ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

        numbers = []
        for cell in root.findall(".//main:c", ns):
            v = cell.find("main:v", ns)
            if v is not None:
                val = v.text
                if val.isdigit() and len(val) >= 10:
                    numbers.append(val)

        print(f"📊 Found {len(numbers)} valid numbers.")

        with open(txt_path, "w") as out:
            for num in numbers:
                out.write(num + "\n")

        print(f"✅ Numbers saved to: {txt_path}")
        return str(txt_path)

    except Exception as e:
        print("❌ Failed to process XLSX file:", e)
        return None

def sort_numbers_from_txt(input_path, remove_prefix="", filter_prefixes=[]):
    with open(input_path, "r") as f:
        raw_lines = [line.strip().replace('"', '').replace("'", "") for line in f if line.strip()]

    if remove_prefix:
        cleaned = [line[len(remove_prefix):] for line in raw_lines if line.startswith(remove_prefix)]
    else:
        cleaned = raw_lines

    groups = {p: [] for p in filter_prefixes}
    for num in cleaned:
        for p in filter_prefixes:
            if num.startswith(p):
                groups[p].append(num)
                break

    base = Path(input_path).stem
    output_dir = Path("/sdcard/Download/egypt_numbers")
    output_dir.mkdir(parents=True, exist_ok=True)

    index = 1
    while True:
        out_name = f"{base}_{index}.txt"
        output_path = output_dir / out_name
        if not output_path.exists():
            break
        index += 1

    with open(output_path, "w") as out:
        for p in filter_prefixes:
            out.write(f"--- Numbers starting with {p} ---\n")
            for num in groups[p]:
                out.write(num + "\n")
            out.write("\n")

    print("✅ Sorting complete. File saved at:", output_path)

def ask_path():
    while True:
        filepath = input("Enter file path (.txt/.csv/.xlsx): ").strip()
        if os.path.isfile(filepath):
            return filepath
        else:
            print("❌ File not found. Please try again.")

def ask_yes_no(prompt):
    while True:
        ans = input(prompt).strip().lower()
        if ans in ['y', 'n']:
            return ans
        print("❌ Invalid input. Enter 'y' or 'n'.")

def ask_prefixes():
    while True:
        raw = input("Enter filter prefixes (comma-separated): ").strip()
        if raw:
            prefixes = [p.strip() for p in raw.split(",") if p.strip()]
            if prefixes:
                return prefixes
        print("❌ Invalid prefixes. Please enter at least one.")

def main_loop():
    while True:
        filepath = ask_path()

        if filepath.endswith(".xlsx"):
            print("🔄 Converting Excel to TXT...")
            filepath = convert_xlsx_to_txt(filepath)
            if not filepath:
                continue

        remove_prefix = ""
        if ask_yes_no("Do you want to remove a prefix? (y/n): ") == "y":
            remove_prefix = input("Enter prefix to remove: ").strip()

        prefixes = ask_prefixes()
        sort_numbers_from_txt(filepath, remove_prefix, prefixes)

        again = ask_yes_no("Do you want to sort another file? (y/n): ")
        if again == "n":
            print("👋 Exiting. Goodbye!")
            break

if __name__ == "__main__":
    print_intro()
    main_loop()
