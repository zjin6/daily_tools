import fitz  # PyMuPDF
import os
import tempfile
from PIL import Image, ImageOps, ImageEnhance

def convert_pdf_to_dark_mode_simple(
    input_pdf, 
    output_pdf, 
    pages_to_convert=None, 
    dpi=600,
    sharpness_factor=2.0,     # How much to sharpen text
    jpeg_quality=95           # Quality of JPEG compression
):
    """
    Convert selected pages of a PDF to dark mode by simply inverting colors and enhancing sharpness.
    
    Args:
        input_pdf: Path to input PDF
        output_pdf: Path for output PDF
        pages_to_convert: List of page numbers to convert (0-based index)
                         If None, converts all pages
        dpi: Resolution (higher = better quality)
        sharpness_factor: How much to sharpen the text
        jpeg_quality: Quality of JPEG compression
    """
    # Open the input PDF
    doc = fitz.open(input_pdf)
    
    # Determine which pages to process
    total_doc_pages = len(doc)
    
    if pages_to_convert is None:
        # Process all pages if not specified
        pages_to_convert = list(range(total_doc_pages))
    else:
        # Filter out invalid page numbers
        pages_to_convert = [p for p in pages_to_convert if 0 <= p < total_doc_pages]
    
    if not pages_to_convert:
        print("No valid pages to convert!")
        return
    
    print(f"Processing {len(pages_to_convert)} selected pages out of {total_doc_pages} total pages")
    print(f"Using simplified approach: DPI={dpi}, Sharpness={sharpness_factor}")
    
    # Create a new output PDF
    out_doc = fitz.open()
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Process only selected pages
        for i, page_num in enumerate(pages_to_convert):
            print(f"Processing page {page_num+1} ({i+1}/{len(pages_to_convert)})...")
            
            # Get the current page
            page = doc[page_num]
            
            # Create a new page in the output PDF with the same dimensions
            out_page = out_doc.new_page(width=page.rect.width, height=page.rect.height)
            
            # Calculate matrix scale based on DPI
            scale = dpi / 72
            matrix = fitz.Matrix(scale, scale)
            
            # Render the page as a high-resolution image
            pix = page.get_pixmap(matrix=matrix)
            
            # Convert the pixmap to a PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # 1. Enhance sharpness for better text clarity
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(sharpness_factor)
            
            # 2. Simply invert the colors
            img = ImageOps.invert(img)
            
            # 3. Save temporarily with high quality
            temp_img_path = os.path.join(temp_dir, f"temp_page_{i}.jpg")
            img.save(temp_img_path, "JPEG", quality=jpeg_quality)
            
            # Insert the processed image into the output page
            out_page.insert_image(out_page.rect, filename=temp_img_path)
    
    # Save the output PDF with compression
    out_doc.save(output_pdf, garbage=4, deflate=True, clean=True)
    doc.close()
    out_doc.close()
    
    print(f"Dark mode PDF saved to {output_pdf}")
    print(f"Original full document size: {os.path.getsize(input_pdf) / (1024*1024):.2f} MB")
    print(f"New size (selected pages only): {os.path.getsize(output_pdf) / (1024*1024):.2f} MB")

# Example usage
input_pdf_path = r"C:\Users\zjin6\Downloads\Generative.AI.in.Action.2024.9.pdf"
output_pdf_path = r"C:\Users\zjin6\Downloads\Generative.AI.in.Action.2024.9_dark_mode_simple.pdf"

# Specify which pages you want to convert (0-based index)
#selected_pages = [9, 14, 15, 16, 17, 18, 19, 24]  # 0-based (so 9 is page 10 in the PDF)
selected_pages = list(range(20,30))  # 0-based (so 9 is page 10 in the PDF)

# Convert with simplified approach
convert_pdf_to_dark_mode_simple(
    input_pdf_path, 
    output_pdf_path, 
    pages_to_convert=selected_pages, 
    dpi=600,
    sharpness_factor=2.0,
    jpeg_quality=95
)
