import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import "../components"
import ".."
Item{
 Column{anchors.fill:parent;spacing:12
  Row{width:parent.width
   Column{Text{text:"Sua biblioteca";color:Theme.foreground;font.pixelSize:26;font.bold:true}Text{text:"Músicas armazenadas no seu computador";color:Theme.muted;font.pixelSize:12}}
   Item{width:1}
   Button{text:"＋ Adicionar pasta";onClicked:folder.open()}
  }
  TextField{width:parent.width;placeholderText:"Buscar músicas, artistas ou álbuns";onTextChanged:backend.search(text)
   color:Theme.foreground;background:Rectangle{radius:9;color:Theme.surface;border.color:Theme.surface2}}
  Row{spacing:10;Text{text:backend.tracks.length+" faixas";color:Theme.muted}Button{text:"Reescanear";onClicked:backend.scan()}}
  ListView{id:list;width:parent.width;height:parent.height-125;clip:true;spacing:3;model:backend.tracks
   delegate:TrackRow{track:modelData;onActivated:function(t){backend.playback.playTrack(t)}}
   ScrollBar.vertical:ScrollBar{}
   Text{anchors.centerIn:parent;visible:list.count===0;text:"Biblioteca vazia\nAdicione uma pasta para começar.";color:Theme.muted;horizontalAlignment:Text.AlignHCenter}
  }
 }
 FolderDialog{id:folder;title:"Escolher pasta de músicas";onAccepted:backend.addFolder(selectedFolder.toString())}
}
