from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter

pages = Path(r"C:\Users\uugur\OneDrive\Desktop\animations_ncs_emg\book_pages")
out = Path(r"C:\Users\uugur\OneDrive\Desktop\animations_ncs_emg\textbook_figures_v3")
out.mkdir(parents=True, exist_ok=True)

# Coordinates are from 144-dpi renders of the user-provided Chapter 8 PDF.
# Captions and surrounding prose are intentionally excluded.
crops = {
    "fig_8_4_differential.png": (5, (95, 750, 590, 1425)),
    "fig_8_5_impedance_noise.png": (5, (620, 195, 1055, 790)),
    "fig_8_6_frayed_cable.png": (6, (690, 205, 980, 690)),
    "fig_8_7_passband.png": (6, (610, 845, 1080, 1250)),
    "fig_8_8_filter_stack.png": (7, (125, 185, 580, 785)),
    "fig_8_9_filter_tradeoff.png": (7, (610, 185, 1080, 690)),
    "fig_8_11_stimulus_measurement.png": (8, (120, 190, 570, 760)),
    "fig_8_12_cables.png": (8, (620, 190, 1065, 660)),
    "fig_8_13_walking_anode.png": (9, (215, 205, 1005, 590)),
    "fig_8_14_15_cathode_anode.png": (9, (115, 710, 565, 1485)),
    "fig_8_17_supramaximal.png": (10, (610, 205, 1065, 610)),
    "fig_8_19_costimulation.png": (11, (610, 195, 1075, 535)),
    "fig_8_20_block_patterns.png": (12, (130, 205, 730, 640)),
    "fig_8_24_g1_g2.png": (14, (130, 790, 1060, 1425)),
    "fig_8_26_anti_ortho.png": (15, (120, 820, 580, 1410)),
    "fig_8_27_electrode_search.png": (16, (120, 175, 690, 660)),
    "fig_8_28_depth_edema.png": (16, (110, 685, 710, 1120)),
    "fig_8_29_false_speed.png": (17, (115, 185, 575, 640)),
    "fig_8_31_g1_g2_distance.png": (19, (500, 175, 1085, 650)),
    "fig_8_32_elbow_distance.png": (19, (120, 730, 1060, 1275)),
    "fig_8_33_34_display_settings.png": (20, (145, 190, 1025, 900)),
}

for name, (page_number, box) in crops.items():
    image = Image.open(pages / f"page-{page_number:02d}.png").convert("RGB")
    cropped = image.crop(box)
    cropped = ImageEnhance.Contrast(cropped).enhance(1.05)
    cropped = cropped.filter(ImageFilter.UnsharpMask(radius=1.2, percent=115, threshold=3))
    cropped.save(out / name, optimize=True)

print(f"cropped={len(crops)} output={out}")
