import PyPDF2
import os
import logging


source_folder = r"C:\Users\zjin6\Xiaohuan\OrigionFiles"
combined_folder = r"C:\Users\zjin6\Xiaohuan"
# logging.disable(logging.CRITICAL)
# logging.basicConfig(filename='myProgramLog.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(filename=combined_folder + '\\' + 'combine_Log.txt', level=logging.DEBUG, format='%(message)s')
logging.debug('Start of program')
pdfFiles = []
pdfWriter = PyPDF2.PdfFileWriter()


for filename in os.listdir(source_folder):
    if filename.endswith('.pdf'):
        pdfFiles.append(filename)
pdfFiles.sort(key=str.lower)
logging.debug('Find PDF files: \n %s' % pdfFiles)


pageOrder = 1
for filename in pdfFiles:
    pdfFileObj = open(source_folder + '\\' + filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    logging.info(filename.split('.')[0][3:] + ' ...... ' + str(pageOrder))
    pageOrder += pdfReader.numPages

    for pageNum in range(0, pdfReader.numPages):
        pageObj = pdfReader.getPage(pageNum)
        pdfWriter.addPage(pageObj)


pdfOutput = open(combined_folder + '\\' + 'combined_PDF.pdf', 'wb')
pdfWriter.write(pdfOutput)
pdfOutput.close()


logging.debug('End of program')
# logging.debug('Some debugging details.')
# logging.info('The logging module is working.')
# logging.warning('An error message is about to be logged.')
