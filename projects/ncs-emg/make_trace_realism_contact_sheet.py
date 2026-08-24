from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).parent / ".qa-trace-realism"
files = sorted(root.glob("*.png"))
font = ImageFont.load_default(size=15)
cols, rows = 2, 3
thumb_w, thumb_h, label_h = 800, 450, 28
for sheet_no in range((len(files) + cols * rows - 1) // (cols * rows)):
    subset = files[sheet_no * cols * rows : (sheet_no + 1) * cols * rows]
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), "#101820")
    draw = ImageDraw.Draw(sheet)
    for i, file in enumerate(subset):
        image = Image.open(file).convert("RGB")
        image.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = (i % cols) * thumb_w
        y = (i // cols) * (thumb_h + label_h)
        sheet.paste(image, (x, y))
        draw.rectangle((x, y + thumb_h, x + thumb_w, y + thumb_h + label_h), fill="#071118")
        draw.text((x + 8, y + thumb_h + 6), file.stem[:86], fill="#e9f4f6", font=font)
    sheet.save(root / f"contact-sheet-{sheet_no + 1:02d}.jpg", quality=91)
