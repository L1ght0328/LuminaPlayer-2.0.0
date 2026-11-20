import QtQuick
import QtQuick.Controls
import QtMultimedia
import ".."
Column{
 spacing:10
 Text{text:"Vídeos";font.pixelSize:26;font.bold:true;color:Theme.foreground}
 Text{text:"Selecione um arquivo de vídeo local para reproduzir.";color:Theme.muted}
 Button{text:"Abrir vídeo";onClicked:videoDialog.open()}
 VideoOutput{id:videoOutput;width:parent.width;height:parent.height-120;visible:video.source!==""}
 Row{spacing:8
  Button{text:video.playbackState===MediaPlayer.PlayingState?"Pausar":"Reproduzir";onClicked:video.playbackState===MediaPlayer.PlayingState?video.pause():video.play()}
  Button{text:"-10s";onClicked:video.position=Math.max(0,video.position-10000)}
  Button{text:"+10s";onClicked:video.position=Math.min(video.duration,video.position+10000)}
  Button{text:"Tela cheia";onClicked:videoWindow.showFullScreen()}
 }
 MediaPlayer{id:video;videoOutput:videoOutput;audioOutput:AudioOutput{}}
 FileDialog{id:videoDialog;nameFilters:["Vídeos (*.mp4 *.mkv *.avi *.mov *.webm *.wmv)"];onAccepted:{video.source=selectedFile;video.play()}}
 Window{id:videoWindow;visible:false;width:1280;height:720;color:"black";VideoOutput{anchors.fill:parent;source:video}}
}
