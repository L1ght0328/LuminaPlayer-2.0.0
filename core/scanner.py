from pathlib import Path
import os
from mutagen import File as MutagenFile
AUDIO={".mp3",".flac",".wav",".ogg",".m4a",".aac",".wma",".opus"}
VIDEO={".mp4",".mkv",".avi",".mov",".webm",".wmv"}
def read_metadata(path):
    p=Path(path).resolve(); st=p.stat()
    d={"path":str(p),"title":p.stem,"artist":"Desconhecido","album":"Desconhecido","year":"","genre":"",
       "duration":0.0,"format":p.suffix[1:].upper(),"bitrate":0,"sample_rate":0,"channels":0,
       "size":st.st_size,"mtime":st.st_mtime,"cover":None}
    try:
        a=MutagenFile(str(p),easy=False)
        if a is None: return d
        info=getattr(a,"info",None)
        if info:
            d["duration"]=float(getattr(info,"length",0) or 0)
            d["bitrate"]=int(getattr(info,"bitrate",0) or 0)
            d["sample_rate"]=int(getattr(info,"sample_rate",0) or 0)
            d["channels"]=int(getattr(info,"channels",0) or 0)
        tags=getattr(a,"tags",None)
        def value(keys,default):
            for k in keys:
                try:
                    v=tags.get(k)
                    if v is None: continue
                    if hasattr(v,"text"): v=v.text[0]
                    elif isinstance(v,(list,tuple)): v=v[0]
                    if str(v).strip(): return str(v).strip()
                except Exception: pass
            return default
        d["title"]=value(["TIT2","title"],d["title"]); d["artist"]=value(["TPE1","artist"],d["artist"])
        d["album"]=value(["TALB","album"],d["album"]); d["year"]=value(["TDRC","TYER","date"],"")
        d["genre"]=value(["TCON","genre"],"")
        pics=getattr(a,"pictures",None)
        if pics: d["cover"]=pics[0].data
        elif tags:
            for key in ("APIC:","covr"):
                try:
                    pic=tags.get(key)
                    if pic:
                        pic=pic[0] if isinstance(pic,list) else pic
                        d["cover"]=getattr(pic,"data",pic); break
                except Exception: pass
    except Exception: pass
    return d
def discover(folders,extensions=AUDIO):
    seen=set()
    for folder in folders:
        root=Path(folder)
        if not root.is_dir(): continue
        for base,dirs,names in os.walk(root):
            dirs[:]=[d for d in dirs if d not in {"$RECYCLE.BIN","System Volume Information"}]
            for name in names:
                p=Path(base)/name
                if p.suffix.lower() in extensions:
                    try:
                        k=str(p.resolve()).casefold()
                        if k not in seen: seen.add(k); yield p.resolve()
                    except OSError: pass
