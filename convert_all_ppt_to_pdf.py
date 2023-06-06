import os
import glob
import win32com.client
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Total time used: {total_time:.0f} seconds")
        return result
    return wrapper

def ppt_to_pdf(ppt_path, pdf_path):
    powerpoint = win32com.client.Dispatch("Powerpoint.Application")
    powerpoint.Visible = 1
    deck = powerpoint.Presentations.Open(ppt_path)
    deck.SaveAs(pdf_path, 32)
    deck.Close()
    powerpoint.Quit()

@timer
def main():
    folder_path = input("Enter the path to the folder containing the PowerPoint files: ")
    ppt_files = glob.glob(os.path.join(folder_path, "*.pptx"))

    count = 0
    for i, ppt_file in enumerate(ppt_files):
        pdf_file = os.path.splitext(ppt_file)[0] + ".pdf"
        ppt_to_pdf(ppt_file, pdf_file)
        count += 1
        print(f"{i + 1}. {os.path.basename(pdf_file)}")

    print(f"Total number of files converted: {count}")

if __name__ == '__main__':
    main()
