import fitz  # PyMuPDF
import os
import tempfile

def convert_pdf_to_dark_mode(input_pdf, output_pdf, dpi=300, max_pages=20):
    """
    Convert a PDF to dark mode with high quality but limited to specified number of pages.
    
    Args:
        input_pdf: Path to input PDF
        output_pdf: Path for output PDF
        dpi: Resolution (higher = better quality)
        max_pages: Maximum number of pages to process
    """
    # Open the input PDF
    doc = fitz.open(input_pdf)
    
    # Limit pages to process
    total_pages = min(len(doc), max_pages)
    print(f"Processing first {total_pages} pages out of {len(doc)} total pages")
    
    # Create a new output PDF
    out_doc = fitz.open()
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Process limited number of pages
        for page_num in range(total_pages):
            print(f"Processing page {page_num + 1}/{total_pages}...")
            
            # Get the current page
            page = doc[page_num]
            
            # Create a new page in the output PDF with the same dimensions
            out_page = out_doc.new_page(width=page.rect.width, height=page.rect.height)
            
            # Draw a black background
            out_page.draw_rect(out_page.rect, color=(0, 0, 0), fill=(0, 0, 0))
            
            # Calculate matrix scale based on DPI (300 DPI / 72 = 4.17)
            scale = dpi / 72
            matrix = fitz.Matrix(scale, scale)
            
            # Render the page as a high-resolution image
            pix = page.get_pixmap(matrix=matrix)
            
            # Convert the pixmap to a PIL Image
            import PIL.Image
            img = PIL.Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Process the image - invert colors and enhance text
            from PIL import ImageOps, ImageEnhance
            
            # Enhance contrast first
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.5)  # Increase contrast for better readability
            
            # Convert to grayscale for better text clarity
            img = img.convert('L')
            
            # Apply thresholding for sharper text
            threshold = 180  # Adjust as needed
            img = img.point(lambda x: 0 if x < threshold else 255, '1')
            
            # Invert colors (black to white, white to black)
            img = ImageOps.invert(img.convert('RGB'))
            
            # Save temporarily with better quality
            temp_img_path = os.path.join(temp_dir, f"temp_page_{page_num}.jpg")
            img.save(temp_img_path, "JPEG", quality=90)  # Higher quality for test
            
            # Insert the processed image into the output page
            out_page.insert_image(out_page.rect, filename=temp_img_path)
    
    # Save the output PDF with compression
    out_doc.save(output_pdf, garbage=4, deflate=True, clean=True)
    doc.close()
    out_doc.close()
    
    print(f"Dark mode PDF saved to {output_pdf}")
    print(f"Original size: {os.path.getsize(input_pdf) / (1024*1024):.2f} MB")
    print(f"New size: {os.path.getsize(output_pdf) / (1024*1024):.2f} MB")

# Example usage
input_pdf_path = r"C:\Users\zjin6\Downloads\Generative.AI.in.Action.2024.9.pdf"
output_pdf_path = r"C:\Users\zjin6\Downloads\Generative.AI.in.Action.2024.9_dark_mode_20pages.pdf"
convert_pdf_to_dark_mode(input_pdf_path, output_pdf_path, dpi=600, max_pages=20)
