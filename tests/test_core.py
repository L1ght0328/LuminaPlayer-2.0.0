from pathlib import Path
from core.database import Database
from core.scanner import read_metadata

def test_db_and_fallback(tmp_path):
    db=Database(tmp_path/"db.sqlite")
    f=tmp_path/"sample.mp3"; f.write_bytes(b"not a real mp3")
    data=read_metadata(f)
    assert data["title"]=="sample"
    db.upsert_track(data)
    assert db.tracks()[0]["title"]=="sample"
