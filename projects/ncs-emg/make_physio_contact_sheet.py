from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root=Path(r"C:\Users\uugur\OneDrive\Desktop\animations_ncs_emg\qa_physio_audit")
files=sorted(root.glob("*.png"))
font=ImageFont.load_default(size=15)
cols,rows=2,4
thumb_w,thumb_h,label_h=800,450,28
for page in range((len(files)+cols*rows-1)//(cols*rows)):
    subset=files[page*cols*rows:(page+1)*cols*rows]
    sheet=Image.new("RGB",(cols*thumb_w,rows*(thumb_h+label_h)),"#101820")
    draw=ImageDraw.Draw(sheet)
    for i,file in enumerate(subset):
        image=Image.open(file).convert("RGB")
        image.thumbnail((thumb_w,thumb_h),Image.Resampling.LANCZOS)
        x=(i%cols)*thumb_w
        y=(i//cols)*(thumb_h+label_h)
        sheet.paste(image,(x,y))
        draw.rectangle((x,y+thumb_h,x+thumb_w,y+thumb_h+label_h),fill="#071118")
        draw.text((x+8,y+thumb_h+6),file.stem,fill="#e9f4f6",font=font)
    sheet.save(root/f"contact-{page+1}.jpg",quality=92)
