import os
from bs4 import BeautifulSoup

# Folder where you saved the web pages
save_folder = r'C:\Users\zjin6\Downloads\Salttiger_Books'

# Loop through each saved HTML file and extract the required text
for filename in os.listdir(save_folder):
    file_path = os.path.join(save_folder, filename)
    if filename.endswith('.html'):  # Ensuring it's an HTML file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            soup = BeautifulSoup(content, 'html.parser')

            # Extract text from <h1 class="entry-title"> within <header class="entry-header">
            entry_header = soup.find('header', class_='entry-header')
            if entry_header:
                entry_title = entry_header.find('h1', class_='entry-title')
                if entry_title:
                    print(f"Title: {entry_title.get_text(strip=True)}")

            # Extract text in <strong> after <p>内容简介：</p> within <div class="entry-content">
            entry_content = soup.find('div', class_='entry-content')
            if entry_content:
                intro_paragraph = entry_content.find('p', string="内容简介：")
                if intro_paragraph and intro_paragraph.next_sibling:
                    strong_tag = intro_paragraph.find_next('strong')
                    if strong_tag:
                        print(f"Intro: {strong_tag.get_text(strip=True)}")
                        print()
                    else:
                        print()
