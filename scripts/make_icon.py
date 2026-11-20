from PIL import Image, ImageDraw
from pathlib import Path
out=Path("assets/icon.ico")
size=256
im=Image.new("RGBA",(size,size),(10,10,15,255))
d=ImageDraw.Draw(im)
d.rounded_rectangle((12,12,244,244),radius=54,outline=(139,43,226,255),width=16)
d.polygon([(104,70),(104,186),(194,128)],fill=(57,255,20,255))
im.save(out,format="ICO",sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
print(out)
