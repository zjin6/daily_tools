
filepath = input('filepath: ')

with open(filepath, 'r') as f:
    lines = f.readlines()

subtitles = []
subtitle_text = ""

for line in lines:
    if not line.strip():  # If the line is empty, skip it
        continue
    elif line.strip().isdigit():
        # If the line contains only digits, it's the subtitle index
        # Append the previous subtitle text to the list and reset the variable
        if subtitle_text:
            subtitles.append(subtitle_text.strip())
            subtitle_text = ""
    else:
        # If the line is not empty or a digit, it's either a time code or part of the subtitle text
        try:
            # If the line can be parsed as a time code, skip it
            start, end = line.strip().split(" --> ")
        except ValueError:
            # If the line is not a time code, it's part of the subtitle text
            subtitle_text += line.strip() + " "

# Append the last subtitle text to the list
subtitles.append(subtitle_text.strip())

# Print the extracted subtitle text
for subtitle in subtitles:
    print(subtitle)

text = " ".join(subtitles)