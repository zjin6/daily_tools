from pdf2image import convert_from_path


folder = r"C:\Users\zjin6\Chunyan"
images = convert_from_path(r"C:\Users\zjin6\Chunyan\Automotive Air Conditioning Training Manual.pdf", dpi=300)


for i in range(len(images)):
    images[i].save(folder + '\\' + 'page' + str(i) + '.jpg', 'JPEG')
