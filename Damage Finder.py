
import re
import os
import sys
import platform

# OS Detection
is_windows = platform.system() == "Windows"
is_linux = platform.system() == "Linux"

# Resize terminal (Windows only)
if is_windows:
    os.system('mode con: cols=200 lines=80')

if is_windows:
    local_appdata = os.environ.get('LOCALAPPDATA')
    log_file = os.path.join(local_appdata, "Warframe", "EE.log")
else:
    # Adjust path for Proton/Steam on Linux
    log_file = os.path.expanduser("~/.local/share/Steam/steamapps/compatdata/230410/pfx/drive_c/users/steamuser/AppData/Local/Warframe/EE.log")

try:
    with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
        loglist = f.read().split('\n')
except FileNotFoundError:
    print(f"Log File not found at: {log_file}")
    exit(1)

substring = "Damage too high:"
pattern = re.escape(substring) + r'\s*([\d,]+)'

# Function to extract the damage number from each string
def extract_damage(s):
    match = re.search(pattern, s)
    if match:
        return int(match.group(1).replace(',', ''))
    else:
        return float('-inf')

# Find the string with the highest damage value
max_string = max(loglist, key=extract_damage)

# Find the line number where max_string appears
def find_line_number(target_string, log_list):
    for i, line in enumerate(log_list, start=1):
        if line == target_string:
            return i
    return -1 # Not found

# Index things
line_number = find_line_number(max_string, loglist)
max_line_index = loglist.index(max_string)

# Extract damage number for final display
match = re.search(pattern, max_string)
damage_number = match.group(1) if match else "0"

# --- REWORKED CLOSEST VICTIM SEARCH & CONTEXT ENGINE ---
detected_enemy = "Unknown Enemy"
enemy_pattern = re.compile(r'Victim:\s*([^,\s]+)')

context_lines = []
# Walk backward up to 50 lines from the max damage index to find the closest victim
max_lookback = min(50, max_line_index)
victim_found = False

for i in range(max_line_index - 1, max_line_index - 1 - max_lookback, -1):
    line = loglist[i]
    context_lines.insert(0, line) # Maintain correct ascending log chronology
    
    # Check for the victim if we haven't found one yet
    if not victim_found:
        enemy_match = enemy_pattern.search(line)
        if enemy_match:
            raw_enemy = enemy_match.group(1).replace("Avatar", "")
            detected_enemy = re.sub(r'\d+$', '', raw_enemy)
            victim_found = True  # Break target search loop step but keep gathering context lines if needed

# Append the final maximum damage row to the bottom of context printout
context_lines.append(max_string)

# --- OUTPUT SECTION ---
print("=" * 60)
print("Context lines from log:")
print("=" * 60)
for line in context_lines:
    print(line)

print('\n' + "=" * 60)
print(f"You dealt: {int(damage_number.replace(',', '')):,} damage.")
print(f"Enemy Target Hit: {detected_enemy}")
print(f"Found on line {line_number} of log.")
print("=" * 60 + '\n')

# Cross-platform wait for user input
if is_windows:
    import msvcrt
    print("Press any key to exit...")
    msvcrt.getch()
else:
    input("Press Enter to exit...")
