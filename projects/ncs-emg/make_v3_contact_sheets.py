from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(r"C:\Users\uugur\OneDrive\Desktop\animations_ncs_emg\qa_nonphys_v4_69")
files = sorted(root.glob("*.png"))
font = ImageFont.load_default(size=15)
cols, rows = 3, 3
thumb_w, thumb_h, label_h = 500, 281, 28
for sheet_no in range((len(files) + cols * rows - 1) // (cols * rows)):
    subset = files[sheet_no * cols * rows : (sheet_no + 1) * cols * rows]
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), "#d5dde4")
    draw = ImageDraw.Draw(sheet)
    for i, file in enumerate(subset):
        image = Image.open(file).convert("RGB")
        image.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = (i % cols) * thumb_w
        y = (i // cols) * (thumb_h + label_h)
        sheet.paste(image, (x, y))
        draw.rectangle((x, y + thumb_h, x + thumb_w, y + thumb_h + label_h), fill="#e7edf3")
        draw.text((x + 8, y + thumb_h + 6), file.stem[:62], fill="#16232c", font=font)
    sheet.save(root / f"contact-sheet-{sheet_no + 1:02d}.jpg", quality=92)
