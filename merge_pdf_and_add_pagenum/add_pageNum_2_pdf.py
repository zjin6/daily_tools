import PyPDF2


sourcefile_path = r"C:\Users\zjin6\Xiaohuan\combined_PDF.pdf"
pageNum_A4Portfile_path = r"C:\Users\zjin6\Xiaohuan\pageNum_A4Port.pdf"
pageNum_A4Landfile_path = r"C:\Users\zjin6\Xiaohuan\pageNum_A4Land.pdf"
pageNum_A3Portfile_path = r"C:\Users\zjin6\Xiaohuan\pageNum_A3Port.pdf"
pageNum_A3Landfile_path = r"C:\Users\zjin6\Xiaohuan\pageNum_A3Land.pdf"

sourcefile = open(sourcefile_path, 'rb')
pageNum_A4Portfile = open(pageNum_A4Portfile_path, 'rb')
pageNum_A4Landfile = open(pageNum_A4Landfile_path, 'rb')
pageNum_A3Portfile = open(pageNum_A3Portfile_path, 'rb')
pageNum_A3Landfile = open(pageNum_A3Landfile_path, 'rb')

pdfReader_source = PyPDF2.PdfFileReader(sourcefile)
pdfReader_pageNum_A4Port = PyPDF2.PdfFileReader(pageNum_A4Portfile)
pdfReader_pageNum_A4Land = PyPDF2.PdfFileReader(pageNum_A4Landfile)
pdfReader_pageNum_A3Port = PyPDF2.PdfFileReader(pageNum_A3Portfile)
pdfReader_pageNum_A3Land = PyPDF2.PdfFileReader(pageNum_A3Landfile)

pdfWriter = PyPDF2.PdfFileWriter()


for pageNum in range(0, pdfReader_source.numPages):
    sourcePage = pdfReader_source.getPage(pageNum)
    page = sourcePage.mediaBox
    page_width = page.getUpperRight_x() - page.getUpperLeft_x()
    page_height = page.getUpperRight_y() - page.getLowerRight_y()
    if max(page_height, page_width) < 1000:
        if page_width < page_height:
            print(pageNum+1, 'A4 Portrait')
            sourcePage.mergePage(pdfReader_pageNum_A4Port.getPage(pageNum))
        else:
            print(pageNum+1, 'A4 Landscape')
            sourcePage.mergePage(pdfReader_pageNum_A4Land.getPage(pageNum))
    else:
        if page_width < page_height:
            print(pageNum+1, 'A3 Portrait')
            sourcePage.mergePage(pdfReader_pageNum_A3Port.getPage(pageNum))
        else:
            print(pageNum+1, 'A3 Landscape')
            sourcePage.mergePage(pdfReader_pageNum_A3Land.getPage(pageNum))
    pdfWriter.addPage(sourcePage)


pageNum_addedFile = open(r"C:\Users\zjin6\Xiaohuan\pageNum_added.pdf", 'wb')
pdfWriter.write(pageNum_addedFile)
pageNum_addedFile.close()
sourcefile.close()
pageNum_A4Portfile.close()
pageNum_A4Landfile.close()
pageNum_A3Portfile.close()
pageNum_A3Landfile.close()

















