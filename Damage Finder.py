import re
import os
import msvcrt

os.system('mode con: cols=200 lines=80')

local_appdata = os.environ['LOCALAPPDATA']
log_file = os.path.join(local_appdata, "Warframe", "EE.log")

loglist = open(log_file, "r", encoding="ansi").read().split('\n')
substring = "Damage too high:"
substring2 = "Damaging dead avatar"

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
    return -1  # Not found

# Index things
line_number = find_line_number(max_string, loglist)

max_line_index = loglist.index(max_string)

#Previous Line to show in-game damage number
if max_line_index > 0:
    previous_line = loglist[max_line_index - 1]

# Walk backwards to find "Damaging dead avatar"
def get_context_before_damage(logs, start_index):
    context_lines = []
    for i in range(start_index - 1, -1, -1):  # walk backward
        line = logs[i]
        context_lines.insert(0, line)  # maintain original order
        if substring2 in line:
            break
    context_lines.append(logs[start_index])    
    return context_lines

context = get_context_before_damage(loglist, max_line_index)
match = re.search(pattern, max_string)
if match:
    damage_number = match.group(1)
match = re.search(pattern, previous_line)
if match:
    display_number = match.group(1)


print("Context before damage:")
for line in context:
    print(line)
print('\n')
print("The in-game number says you dealt", display_number, "damage")
print("You actually dealt:", damage_number, "damage.")
print(f"Found on line {line_number} of log.")
print('\n')
print("Press any key to exit")
msvcrt.getch()