import sys,os,logging,traceback
from pathlib import Path
from PySide6.QtCore import QObject,Signal,Slot,Property,QUrl,QThread,Qt,qInstallMessageHandler
from PySide6.QtGui import QGuiApplication,QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication,QMessageBox,QSystemTrayIcon,QMenu
from PySide6.QtMultimedia import QMediaPlayer,QAudioOutput
from core.paths import app_root,user_data_dir
from core.database import Database
from core.settings import Settings
from core.scanner import discover,read_metadata,AUDIO,VIDEO
from core.player_controller import PlayerController
from core.mixer import Mixer

DATA=user_data_dir()
LOG=DATA/"lumina.log"
logging.basicConfig(filename=LOG,level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s")
def qt_log(kind,context,message): logging.info("Qt: %s",message)
qInstallMessageHandler(qt_log)
def exception_hook(t,v,tb):
    logging.critical("Exceção não tratada",exc_info=(t,v,tb))
    try:
        QMessageBox.critical(None,"Lumina Player","Ocorreu um erro inesperado.\n\nLog: "+str(LOG)+"\n\n"+str(v))
    except Exception: pass
sys.excepthook=exception_hook

class Worker(QObject):
    progress=Signal(int,int,str); done=Signal(int); failed=Signal(str)
    def __init__(self,db,folders,extensions): super().__init__(); self.db=db; self.folders=folders; self.extensions=extensions
    @Slot()
    def run(self):
        try:
            paths=list(discover(self.folders,self.extensions)); total=len(paths); count=0
            for i,p in enumerate(paths,1):
                try: self.db.upsert_track(read_metadata(p)); count+=1
                except Exception: logging.exception("Falha ao ler %s",p)
                self.progress.emit(i,total,str(p))
            self.done.emit(count)
        except Exception as e: self.failed.emit(str(e))

class Backend(QObject):
    tracksChanged=Signal(); videosChanged=Signal(); toast=Signal(str); scanProgress=Signal(int,int,str)
    pageChanged=Signal()
    def __init__(self):
        super().__init__()
        self.db=Database(DATA/"library.sqlite3"); self.settings=Settings(self.db)
        self.player=PlayerController(self.db,self.settings,self); self.mixer=Mixer(self.player.player,self.player.audio,self.db,self)
        self.player.toast.connect(self.toast.emit)
        self._tracks=[]; self._videos=[]; self._search=""; self._page="Explorar"; self._thread=None; self._worker=None
        self.refresh()
    @Property(QObject,constant=True)
    def playback(self): return self.player
    @Property(QObject,constant=True)
    def mixerObject(self): return self.mixer
    @Property("QVariantList",notify=tracksChanged)
    def tracks(self): return self._tracks
    @Property("QVariantList",notify=videosChanged)
    def videos(self): return self._videos
    @Property(str,notify=pageChanged)
    def page(self): return self._page
    @Slot(str)
    def setPage(self,p): self._page=p; self.pageChanged.emit()
    @Slot()
    def refresh(self): self._tracks=self.db.tracks(self._search); self.tracksChanged.emit()
    @Slot(str)
    def search(self,s): self._search=s; self.refresh()
    @Slot(str)
    def addFolder(self,url):
        p=QUrl(url).toLocalFile() if url.startswith("file:") else url
        if not Path(p).is_dir(): self.toast.emit("Selecione uma pasta válida."); return
        self.db.add_folder(p); self.scan()
    @Slot()
    def scan(self): self._start_scan(AUDIO)
    @Slot()
    def scanVideos(self): self._start_scan(VIDEO)
    def _start_scan(self,ext):
        if self._thread and self._thread.isRunning(): self.toast.emit("Já existe uma varredura em andamento."); return
        folders=self.db.folders()
        if not folders: self.toast.emit("Adicione uma pasta primeiro nas Configurações."); return
        self._thread=QThread(self); self._worker=Worker(self.db,folders,ext); self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run); self._worker.progress.connect(self.scanProgress)
        self._worker.done.connect(self._scan_done); self._worker.failed.connect(self.toast)
        self._worker.done.connect(self._thread.quit); self._worker.failed.connect(self._thread.quit)
        self._thread.finished.connect(self._worker.deleteLater); self._thread.start()
    @Slot(int)
    def _scan_done(self,n): self.refresh(); self.toast.emit(f"Varredura concluída: {n} arquivo(s) indexado(s).")
    @Slot(int)
    def setVolume(self,v): self.player.setVolume(v)
    @Slot()
    def togglePlay(self): self.player.togglePlay()
    @Slot()
    def skip(self): self.player.skip()
    @Slot()
    def previous(self): self.player.previous()
    @Slot(str)
    def openPath(self,path):
        p=Path(QUrl(path).toLocalFile() if path.startswith("file:") else path)
        if p.is_dir(): self.addFolder(str(p))
        elif p.is_file() and p.suffix.lower() in AUDIO:
            d=read_metadata(p); d["id"]=self.db.upsert_track(d); self.refresh(); self.player.playTrack(d)
        elif p.is_file() and p.suffix.lower() in VIDEO: self.toast.emit("Selecione o vídeo na aba Vídeos.")
    @Slot()
    def toggleFavorite(self,tid): self.db.toggle_favorite(int(tid)); self.refresh()
    @Slot()
    def shutdown(self): self.player.shutdown()

def main():
    app=QApplication(sys.argv); app.setApplicationName("Lumina Player"); app.setOrganizationName("Lumina")
    app.setQuitOnLastWindowClosed(False)
    backend=Backend()
    engine=QQmlApplicationEngine()
    engine.rootContext().setContextProperty("backend",backend)
    qml=app_root()/"qml"/"Main.qml"
    engine.load(QUrl.fromLocalFile(str(qml)))
    if not engine.rootObjects(): return 2
    app.aboutToQuit.connect(backend.shutdown)
    return app.exec()
if __name__=="__main__":
    try: sys.exit(main())
    except Exception:
        logging.exception("Falha ao iniciar")
        app=QApplication.instance() or QApplication(sys.argv)
        QMessageBox.critical(None,"Lumina Player",f"Não foi possível iniciar.\nLog: {LOG}")
        sys.exit(1)
