import os
from PyPDF2 import PdfFileMerger

# ask the user to input the folder containing the PDF files to merge
folder_path = input("Enter the path to the folder containing the PDF files to merge: ")

# create a list of all the PDF files in the folder
pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]

# create a PdfFileMerger object
merger = PdfFileMerger()

# loop through each PDF file and add it to the merger object
for pdf_file in pdf_files:
    file_path = os.path.join(folder_path, pdf_file)
    merger.append(file_path)

# set the output file path to "Merged All.pdf"
output_file_path = os.path.join(folder_path, "zzz Merged All.pdf")

# write the merged PDF to a file
merger.write(output_file_path)

# close the merger object
merger.close()
