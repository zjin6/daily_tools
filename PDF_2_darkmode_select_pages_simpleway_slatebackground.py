import fitz  # PyMuPDF
import os
import tempfile
import numpy as np
from PIL import Image, ImageEnhance

def convert_pdf_to_dark_mode(
    input_pdf, 
    output_pdf, 
    pages_to_convert=None, 
    dpi=600,
    sharpness_factor=2.0,     # How much to sharpen text
    jpeg_quality=95,          # Quality of JPEG compression
    slate_color=(30, 30, 48)  # Deep slate color (RGB) - can be adjusted
):
    """
    Convert selected pages of a PDF to dark mode with deep slate background and white text.
    
    Args:
        input_pdf: Path to input PDF
        output_pdf: Path for output PDF
        pages_to_convert: List of page numbers to convert (0-based index)
                         If None, converts all pages
        dpi: Resolution (higher = better quality)
        sharpness_factor: How much to sharpen the text
        jpeg_quality: Quality of JPEG compression
        slate_color: The RGB tuple for deep slate color
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
    print(f"Creating dark mode with deep slate background: DPI={dpi}, Slate color={slate_color}")
    
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
            
            # 2. Convert the image to a numpy array for pixel manipulation
            img_array = np.array(img)
            
            # 3. Invert colors (will make black text white and white background black)
            img_array = 255 - img_array
            
            # 4. Replace black background (formerly white) with deep slate
            # Find pixels that are very dark (former white areas, now black after inversion)
            black_threshold = 20  # Pixels with all RGB values below this are considered black
            black_mask = np.all(img_array < black_threshold, axis=2)
            
            # Set those pixels to our deep slate color
            slate_array = np.array(slate_color, dtype=np.uint8)
            img_array[black_mask] = slate_array
            
            # 5. Make other colors more visible on dark background (optional)
            # This step adjusts mid-tone colors to be more visible against dark background
            # Increase brightness of mid-tone colors (not already white or slate)
            mid_mask = ~black_mask & ~np.all(img_array > 230, axis=2)  # Not black and not white
            img_array[mid_mask] = np.minimum(img_array[mid_mask] * 1.3, 255).astype(np.uint8)
            
            # Convert back to PIL Image
            img = Image.fromarray(img_array)
            
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

# Example usage
input_pdf_path = r"C:\Users\zjin6\Downloads\Generative.AI.in.Action.2024.9.pdf"
output_pdf_path = r"C:\Users\zjin6\Downloads\Generative.AI.in.Action.2024.9_dark_mode_slate.pdf"

# Specify which pages you want to convert (0-based index)
selected_pages = list(range(25,30))  # Convert pages 20-29

# Convert to dark mode with deep slate background and white text
convert_pdf_to_dark_mode(
    input_pdf_path, 
    output_pdf_path, 
    pages_to_convert=selected_pages, 
    dpi=600,
    sharpness_factor=2.0,
    jpeg_quality=95,
    slate_color=(40, 40, 45)  # Deep slate blue-gray color (adjust to your preference)
)


# You can adjust this to your preference - here are some options:
# Darker slate: (20, 20, 35)
# Bluer slate: (25, 35, 50)
# Grayer slate: (40, 40, 45)
