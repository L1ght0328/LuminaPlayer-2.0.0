from __future__ import annotations
import sqlite3
from pathlib import Path

SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS tracks(
 id INTEGER PRIMARY KEY, path TEXT UNIQUE NOT NULL, title TEXT NOT NULL,
 artist TEXT NOT NULL DEFAULT 'Desconhecido', album TEXT NOT NULL DEFAULT 'Desconhecido',
 year TEXT DEFAULT '', genre TEXT DEFAULT '', duration REAL DEFAULT 0,
 format TEXT DEFAULT '', bitrate INTEGER DEFAULT 0, sample_rate INTEGER DEFAULT 0,
 channels INTEGER DEFAULT 0, size INTEGER DEFAULT 0, mtime REAL DEFAULT 0,
 cover BLOB, play_count INTEGER DEFAULT 0, last_played TEXT
);
CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS folders(path TEXT PRIMARY KEY);
CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY, track_id INTEGER, path TEXT NOT NULL,
 played_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS playlists(id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL);
CREATE TABLE IF NOT EXISTS playlist_tracks(
 playlist_id INTEGER REFERENCES playlists(id) ON DELETE CASCADE,
 track_id INTEGER REFERENCES tracks(id) ON DELETE CASCADE, position INTEGER DEFAULT 0,
 PRIMARY KEY(playlist_id,track_id)
);
CREATE TABLE IF NOT EXISTS favorites(track_id INTEGER PRIMARY KEY REFERENCES tracks(id) ON DELETE CASCADE);
CREATE INDEX IF NOT EXISTS idx_tracks_title ON tracks(title COLLATE NOCASE);
CREATE INDEX IF NOT EXISTS idx_tracks_artist ON tracks(artist COLLATE NOCASE);
"""
class Database:
    def __init__(self, path: str | Path):
        self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
        with self.connect() as c:
            c.execute("PRAGMA journal_mode=WAL"); c.executescript(SCHEMA)
    def connect(self):
        c=sqlite3.connect(str(self.path),timeout=20)
        c.row_factory=sqlite3.Row
        c.execute("PRAGMA foreign_keys=ON"); c.execute("PRAGMA busy_timeout=20000")
        return c
    def setting(self,key,default=None):
        with self.connect() as c: r=c.execute("SELECT value FROM settings WHERE key=?",(key,)).fetchone()
        return r["value"] if r else default
    def set_setting(self,key,value):
        with self.connect() as c:
            c.execute("INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",(key,str(value)))
    def upsert_track(self,d):
        cols=["path","title","artist","album","year","genre","duration","format","bitrate","sample_rate","channels","size","mtime","cover"]
        with self.connect() as c:
            c.execute(f"INSERT INTO tracks({','.join(cols)}) VALUES({','.join('?' for _ in cols)}) ON CONFLICT(path) DO UPDATE SET "+
                      ",".join(f"{x}=excluded.{x}" for x in cols if x!="path"),[d.get(x) for x in cols])
            return int(c.execute("SELECT id FROM tracks WHERE path=?",(d["path"],)).fetchone()["id"])
    def tracks(self,search="",order="title"):
        allowed={"title","artist","album","duration","mtime","play_count"}
        order=order if order in allowed else "title"; p=f"%{search}%"
        with self.connect() as c:
            rows=c.execute(f"""SELECT t.id,t.path,t.title,t.artist,t.album,t.year,t.genre,t.duration,t.format,
                t.bitrate,t.sample_rate,t.channels,t.size,t.play_count,t.last_played,
                EXISTS(SELECT 1 FROM favorites f WHERE f.track_id=t.id) AS favorite
                FROM tracks t WHERE ?='' OR t.title LIKE ? OR t.artist LIKE ? OR t.album LIKE ? OR t.path LIKE ?
                ORDER BY t.{order} COLLATE NOCASE""",(search,p,p,p,p)).fetchall()
        return [dict(x) for x in rows]
    def folders(self):
        with self.connect() as c: return [r[0] for r in c.execute("SELECT path FROM folders ORDER BY path")]
    def add_folder(self,path):
        with self.connect() as c: c.execute("INSERT OR IGNORE INTO folders(path) VALUES(?)",(str(Path(path).resolve()),))
    def record_play(self,t):
        with self.connect() as c:
            c.execute("UPDATE tracks SET play_count=play_count+1,last_played=CURRENT_TIMESTAMP WHERE id=?",(t.get("id"),))
            c.execute("INSERT INTO history(track_id,path) VALUES(?,?)",(t.get("id"),t["path"]))
    def recent(self,limit=30):
        with self.connect() as c:
            rows=c.execute("""SELECT t.id,t.path,t.title,t.artist,t.album,t.duration,t.format FROM history h
                JOIN tracks t ON t.id=h.track_id ORDER BY h.id DESC LIMIT ?""",(limit,)).fetchall()
        return [dict(x) for x in rows]
    def most_played(self,limit=30):
        with self.connect() as c:
            rows=c.execute("SELECT id,path,title,artist,album,duration,format FROM tracks ORDER BY play_count DESC LIMIT ?",(limit,)).fetchall()
        return [dict(x) for x in rows]
    def toggle_favorite(self,track_id):
        with self.connect() as c:
            exists=c.execute("SELECT 1 FROM favorites WHERE track_id=?",(track_id,)).fetchone()
            if exists: c.execute("DELETE FROM favorites WHERE track_id=?",(track_id,)); return False
            c.execute("INSERT OR IGNORE INTO favorites(track_id) VALUES(?)",(track_id,)); return True
    def create_playlist(self,name):
        with self.connect() as c: c.execute("INSERT INTO playlists(name) VALUES(?)",(name.strip(),))
    def playlists(self):
        with self.connect() as c: return [dict(r) for r in c.execute("SELECT id,name FROM playlists ORDER BY name")]
    def add_to_playlist(self,pid,tid):
        with self.connect() as c:
            n=c.execute("SELECT COUNT(*) FROM playlist_tracks WHERE playlist_id=?",(pid,)).fetchone()[0]
            c.execute("INSERT OR IGNORE INTO playlist_tracks(playlist_id,track_id,position) VALUES(?,?,?)",(pid,tid,n))
