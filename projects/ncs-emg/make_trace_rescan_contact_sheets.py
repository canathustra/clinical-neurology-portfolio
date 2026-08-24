from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).parent / ".qa-trace-realism-rescan"
files = sorted(path for path in ROOT.glob("*.png") if not path.name.startswith("contact-"))
font = ImageFont.load_default(size=14)
cols, rows = 3, 3
thumb_w, thumb_h, label_h = 533, 300, 26
per_sheet = cols * rows

for sheet_no in range((len(files) + per_sheet - 1) // per_sheet):
    subset = files[sheet_no * per_sheet:(sheet_no + 1) * per_sheet]
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), "#101820")
    draw = ImageDraw.Draw(sheet)
    for index, file in enumerate(subset):
        image = Image.open(file).convert("RGB")
        image.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = (index % cols) * thumb_w
        y = (index // cols) * (thumb_h + label_h)
        sheet.paste(image, (x, y))
        draw.rectangle((x, y + thumb_h, x + thumb_w, y + thumb_h + label_h), fill="#071118")
        draw.text((x + 6, y + thumb_h + 5), file.stem[:64], fill="#e9f4f6", font=font)
    sheet.save(ROOT / f"contact-rescan-{sheet_no + 1:02d}.png")

print({"images": len(files), "sheets": (len(files) + per_sheet - 1) // per_sheet, "root": str(ROOT)})
