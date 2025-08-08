import qrcode
from fpdf import FPDF

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data('https://www.junia.com')
qr.make(fit=True)

img = qr.make_image(fill='black', back_color='white')

# Save QR code as an image
img.save('qrcode.png')

# Create PDF and add QR code image
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)  
pdf.cell(40, 10, 'QR Code Example')
pdf.ln(10)
pdf.set_font('Arial', '', 12)
pdf.cell(40, 10, 'QR code for https://www.junia.com')   
pdf.image('qrcode.png', x=10, y=80, w=100)
pdf.output('qrcode.pdf', 'F')