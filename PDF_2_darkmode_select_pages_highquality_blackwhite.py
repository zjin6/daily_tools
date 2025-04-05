import fitz  # PyMuPDF
import os
import tempfile
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

def convert_pdf_to_dark_mode(
    input_pdf, 
    output_pdf, 
    pages_to_convert=None, 
    dpi=600,
    contrast_factor=2.0,        # How much to enhance contrast (higher = more contrast)
    threshold_value=190,        # Threshold for text detection (higher = more text)
    sharpness_factor=2.0,       # How much to sharpen (higher = sharper text)
    use_binary_mode=True,       # Whether to use binary thresholding for crisp text
    jpeg_quality=95             # Quality of JPEG compression (higher = better quality)
):
    """
    Convert selected pages of a PDF to dark mode with high quality and enhanced font clarity.
    
    Args:
        input_pdf: Path to input PDF
        output_pdf: Path for output PDF
        pages_to_convert: List of page numbers to convert (0-based index)
                         If None, converts all pages
        dpi: Resolution (higher = better quality)
        contrast_factor: How much to enhance contrast
        threshold_value: Threshold for text detection (0-255)
        sharpness_factor: How much to sharpen the text
        use_binary_mode: Whether to use binary thresholding for crisp text edges
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
    print(f"Using high-quality settings: DPI={dpi}, Contrast={contrast_factor}, Threshold={threshold_value}")
    
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
            
            # Draw a black background
            out_page.draw_rect(out_page.rect, color=(0, 0, 0), fill=(0, 0, 0))
            
            # Calculate matrix scale based on DPI
            scale = dpi / 72
            matrix = fitz.Matrix(scale, scale)
            
            # Render the page as a high-resolution image
            pix = page.get_pixmap(matrix=matrix)
            
            # Convert the pixmap to a PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Apply high-quality text enhancement
            
            # 1. Enhance contrast first for better text definition
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast_factor)
            
            # 2. Sharpen the image to make text edges crisper
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(sharpness_factor)
            
            # 3. Convert to grayscale for better text processing
            img = img.convert('L')
            
            # 4. Apply thresholding for sharper text edges
            if use_binary_mode:
                # Binary mode for very crisp text edges
                img = img.point(lambda x: 0 if x < threshold_value else 255, '1')
            else:
                # Standard thresholding but maintain grayscale
                img = img.point(lambda x: min(255, max(0, (x - threshold_value) * 255 / (255 - threshold_value) if x > threshold_value else 0)))
            
            # 5. Invert colors (black to white, white to black)
            img = ImageOps.invert(img.convert('RGB'))
            
            # 6. Save temporarily with high quality
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

# Example usage - convert specific pages
input_pdf_path = r"C:\Users\zjin6\Downloads\Generative.AI.in.Action.2024.9.pdf"
output_pdf_path = r"C:\Users\zjin6\Downloads\Generative.AI.in.Action.2024.9_dark_mode_hq.pdf"

# Specify which pages you want to convert (0-based index)
#selected_pages = [9, 14, 15, 16, 17, 18, 19, 24]  # 0-based (so 9 is page 10 in the PDF)
selected_pages = list(range(20,30))  # 0-based (so 9 is page 10 in the PDF)

# Convert with high-quality settings
convert_pdf_to_dark_mode(
    input_pdf_path, 
    output_pdf_path, 
    pages_to_convert=selected_pages, 
    dpi=600,
    contrast_factor=2.0,
    threshold_value=190,
    sharpness_factor=2.0,
    use_binary_mode=True,
    jpeg_quality=95
)
