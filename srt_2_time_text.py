

filepath = input('filepath: ')

with open(filepath, 'r') as f:
    lines = f.readlines()

subtitles = []
subtitle_text = ""

for line in lines:
    if line.strip().isdigit():
        # If the line contains only digits, it's the subtitle index
        # Append the previous subtitle text to the list and reset the variable
        if subtitle_text:
            subtitles.append(subtitle_text)
            subtitle_text = ""
    elif line.strip():
        # If the line is not empty, it's part of the subtitle text
        subtitle_text += line.strip() + " "

# Append the last subtitle text to the list
subtitles.append(subtitle_text)

# Print the extracted subtitle text
for subtitle in subtitles:
    print(subtitle)
