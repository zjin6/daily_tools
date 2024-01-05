from bs4 import BeautifulSoup

# The path to the saved HTML file on your computer
file_path = r"C:\Users\zjin6\Downloads\Salttiger_Books\Learn AI-Assisted Python Programming_ With GitHub Copilot and ChatGPT _ SaltTiger.html"

# Open the saved HTML file
with open(file_path, 'r', encoding='utf-8') as file:
    # Read the content of the file
    content = file.read()
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')  # or 'html5lib' if it's an MHTML file
    
    # Find the <header> element with the class 'entry-header'
    entry_header = soup.find('header', class_='entry-header')
    if entry_header:
        entry_title = entry_header.find('h1', class_='entry-title')
        if entry_title:
            print(entry_title.get_text(strip=True))
        else:
            print("The <h1> element with class 'entry-title' was not found.")
    else:
        print("The <header> element with class 'entry-header' was not found.")
    
    # Find the <div> element with the class 'entry-content'
    entry_content = soup.find('div', class_='entry-content')
    if entry_content:
        # Find the <p> element with the exact text "内容简介："
        intro_paragraph = entry_content.find('p', string="内容简介：")
        if intro_paragraph:
            # Find the next <strong> element after the <p>
            strong_tag = intro_paragraph.find_next('strong')
            if strong_tag:
                print(strong_tag.get_text(strip=True))
            else:
                print("The <strong> element after the <p> with '内容简介：' was not found.")
        else:
            print("The <p> element with '内容简介：' was not found.")
    else:
        print("The <div> element with class 'entry-content' was not found.")
