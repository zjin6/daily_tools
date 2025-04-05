import PyPDF2
import pyttsx3
import keyboard

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        num_pages = reader.getNumPages()

        text = ""
        for page_number in range(num_pages):
            page = reader.getPage(page_number)
            text += page.extractText()

        return text

# Provide the path to your PDF file
pdf_file_path = r"C:\Users\zjin6\Documents\tst.pdf"

# Call the function to read the PDF and get the extracted text
extracted_text = read_pdf(pdf_file_path)

# Split the extracted text into lines
lines = extracted_text.splitlines()

# Initialize pyttsx3 text-to-speech engine
engine = pyttsx3.init()

# Read the text line by line
for line in lines:
    # Check if the space button is pressed
    if keyboard.is_pressed('space'):
        # Pause the speech synthesis if space is pressed
        engine.stop()
        # Wait until space is released
        while keyboard.is_pressed('space'):
            pass
    # Print the line
    print(line)
    # Speak the line
    engine.say(line)
    engine.runAndWait()



# "C:\Users\zjin6\Downloads\tuesdays with morrie.pdf"