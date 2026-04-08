from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs('assets', exist_ok=True)

def make_frame(filename, c1, c2, c3, text):
    size = 500
    img = Image.new('RGBA', (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0,0,size-1,size-1], outline=c1, width=6)
    draw.rectangle([6,6,size-7,size-7], outline=c2, width=6)
    draw.rectangle([12,12,size-13,size-13], outline=c3, width=6)
    r = 130
    draw.polygon([(0,0),(r,0),(0,r)], fill=c1)
    draw.polygon([(0,0),(r-15,0),(0,r-15)], fill=c2)
    draw.polygon([(0,0),(r-30,0),(0,r-30)], fill=c3)
    draw.polygon([(size,size),(size-r,size),(size,size-r)], fill=c1)
    draw.polygon([(size,size),(size-r+15,size),(size,size-r+15)], fill=c2)
    draw.polygon([(size,size),(size-r+30,size),(size,size-r+30)], fill=c3)
    draw.rectangle([0,size-55,size,size], fill=(*c1[:3],220))
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0,0), text, font=font)
    tw = bbox[2]-bbox[0]
    draw.text(((size-tw)/2, size-42), text, fill='white', font=font)
    img.save(f'assets/{filename}')
    print(f"Created: {filename}")

make_frame('frame_iran.png',      (0,166,81),   (255,255,255), (206,17,38),  'Stand With Iran')
make_frame('frame_palestine.png', (0,0,0),      (255,255,255), (0,150,57),   'Stand With Palestine')
make_frame('frame_kashmir.png',   (1,94,52),    (255,255,255), (1,94,52),    'Stand With Kashmir')
make_frame('frame_pakistan.png',  (1,94,52),    (255,255,255), (1,94,52),    'I Love Pakistan')
make_frame('frame_peace.png',     (30,144,255), (255,255,255), (30,144,255), 'Peace For All')
print("All frames created!")
