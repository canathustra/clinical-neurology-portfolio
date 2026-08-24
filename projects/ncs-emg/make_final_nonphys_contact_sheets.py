from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


SOURCE = Path(r"C:\Users\uugur\OneDrive\Desktop\animations_ncs_emg\qa_final_nonphys_pages")
OUTPUT = Path(r"C:\Users\uugur\OneDrive\Desktop\animations_ncs_emg\qa_final_nonphys_contact_sheets")
COLS = 4
ROWS = 4
THUMB = (400, 225)
LABEL_H = 24


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    files = sorted(SOURCE.glob("*.png"))
    font = ImageFont.load_default()
    per_sheet = COLS * ROWS
    for sheet_index, start in enumerate(range(0, len(files), per_sheet), 1):
        batch = files[start:start + per_sheet]
        sheet = Image.new("RGB", (COLS * THUMB[0], ROWS * (THUMB[1] + LABEL_H)), "white")
        draw = ImageDraw.Draw(sheet)
        for index, file in enumerate(batch):
            image = Image.open(file).convert("RGB")
            image.thumbnail(THUMB, Image.Resampling.LANCZOS)
            col, row = index % COLS, index // COLS
            x, y = col * THUMB[0], row * (THUMB[1] + LABEL_H)
            sheet.paste(image, (x, y))
            draw.text((x + 6, y + THUMB[1] + 5), file.stem, fill="#111", font=font)
        sheet.save(OUTPUT / f"contact-{sheet_index:02d}.png")
    print({"pages": len(files), "sheets": (len(files) + per_sheet - 1) // per_sheet, "output": str(OUTPUT)})


if __name__ == "__main__":
    main()
