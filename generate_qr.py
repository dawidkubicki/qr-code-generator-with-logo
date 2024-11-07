import qrcode
import qrcode.image.svg
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode import qr
from PIL import Image, ImageDraw
import os

def generate_png_qr():
    # Create QR code instance with larger size and error correction
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=50,  # Increased from 20 to 50 for much larger QR code
        border=4,
    )
    
    # Add the data
    qr.add_data('https://fhtrade.eu')
    qr.make(fit=True)
    
    # Create QR image
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to PIL Image and add rounded corners
    # Convert to RGBA to support transparency
    qr_image = qr_image.convert("RGBA")
    
    # Create a white box in the center of the QR code
    qr_width, qr_height = qr_image.size
    logo_size = 150  # Size of the logo and white box
    box_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
    
    # Create a white box
    for x in range(box_position[0], box_position[0] + logo_size):
        for y in range(box_position[1], box_position[1] + logo_size):
            qr_image.putpixel((x, y), (255, 255, 255, 255))  # White color with full opacity
    
    # Create a mask with rounded corners
    mask = Image.new("L", qr_image.size, 0)
    draw = ImageDraw.Draw(mask)
    radius = 30  # Adjust this value to change how rounded the corners are
    draw.rounded_rectangle([(0, 0), qr_image.size], radius=radius, fill=255)
    
    # Apply the mask
    output = Image.new("RGBA", qr_image.size, (255, 255, 255, 0))
    output.paste(qr_image, mask=mask)
    
    # Open the logo image from the logo folder
    logo_path = os.path.join('logo', 'logo.png')
    
    try:
        logo = Image.open(logo_path)
        # Resize logo to desired size while maintaining aspect ratio
        logo = logo.resize((logo_size, logo_size))
        
        # Calculate position to place logo in center (same as white box)
        logo_pos = box_position
        
        # Paste the logo onto the QR code
        output.paste(logo, logo_pos, logo)
    except FileNotFoundError:
        print("Warning: Logo file not found in 'logo' folder. QR code generated without logo.")
    except Exception as e:
        print(f"Warning: Could not add logo to QR code: {str(e)}")
    
    # Save the final image
    output.save('fhtrade_qr.png')

def generate_svg_qr():
    # Create QR code instance for SVG
    factory = qrcode.image.svg.SvgImage
    qr_svg = qrcode.make('https://fhtrade.eu', image_factory=factory)
    
    # Save SVG file
    with open('fhtrade_qr.svg', 'wb') as f:
        qr_svg.save(f)

def generate_pdf_qr():
    # Create QR code for PDF
    qr_code = qr.QrCodeWidget('https://fhtrade.eu')
    bounds = qr_code.getBounds()
    
    # Create drawing with larger size
    width = 400
    height = 400
    drawing = Drawing(width, height, transform=[width/bounds[2], 0, 0, height/bounds[3], 0, 0])
    drawing.add(qr_code)
    
    # Save PDF file
    renderPDF.drawToFile(drawing, 'fhtrade_qr.pdf')

if __name__ == "__main__":
    print("Generating QR codes...")
    # Generate all formats
    generate_png_qr()
    generate_svg_qr()
    generate_pdf_qr()
    print("QR codes generated successfully in PNG, SVG, and PDF formats!")
