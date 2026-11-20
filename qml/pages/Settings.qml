import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import ".."
Column{
 spacing:14
 Text{text:"Configurações";font.pixelSize:26;font.bold:true;color:Theme.foreground}
 Text{text:"Aparência";font.pixelSize:16;color:Theme.foreground}
 Row{spacing:8;Button{text:"Escuro";onClicked:Theme.dark=true}Button{text:"Claro";onClicked:Theme.dark=false}}
 Text{text:"Paleta";color:Theme.muted}
 Flow{width:parent.width;spacing:8
  Repeater{model:["Lumina","Ciano Elétrico","Magenta Neon","Laranja Choque","Azul Cobalto","Vermelho Carmesim"]
   delegate:Button{text:modelData;onClicked:Theme.palette=modelData}
  }
 }
 Text{text:"Biblioteca";font.pixelSize:16;color:Theme.foreground}
 Button{text:"Adicionar pasta";onClicked:folder.open()}
 Button{text:"Reescanear";onClicked:backend.scan()}
 Text{text:"Mixer";font.pixelSize:16;color:Theme.foreground}
 Row{spacing:8;Text{text:"Velocidade";color:Theme.muted;anchors.verticalCenter:parent.verticalCenter}
  Slider{from:.5;to:2;value:1;onMoved:backend.mixerObject.setSpeed(value)}Button{text:"Resetar";onClicked:backend.mixerObject.resetSpeed()}}
 Row{spacing:8;Text{text:"Balanço";color:Theme.muted;anchors.verticalCenter:parent.verticalCenter}
  Slider{from:-1;to:1;value:0;onMoved:backend.mixerObject.setBalance(value)}Button{text:"Resetar";onClicked:backend.mixerObject.resetBalance()}}
 Row{spacing:8;Text{text:"Ganho";color:Theme.muted;anchors.verticalCenter:parent.verticalCenter}
  Slider{from:.25;to:1.25;value:1;onMoved:backend.mixerObject.setGain(value)}Button{text:"Resetar";onClicked:backend.mixerObject.resetGain()}}
 Text{text:"O equalizador gráfico depende de DSP de áudio não exposto diretamente pelo QMediaPlayer; os presets são perfis salvos, não equalização efetiva nesta versão.";color:Theme.muted;wrapMode:Text.WordWrap}
 FolderDialog{id:folder;onAccepted:backend.addFolder(selectedFolder.toString())}
}
