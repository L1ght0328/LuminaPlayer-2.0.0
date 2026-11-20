import QtQuick
import QtQuick.Controls
import ".."
Rectangle {
 property var track
 signal activated(var item)
 width:ListView.view?ListView.view.width:600; height:58; radius:9
 color:mouse.containsMouse?Theme.surface2:"transparent"
 Row {
  anchors.fill:parent; anchors.margins:10; spacing:12
  Rectangle { width:38;height:38;radius:8;anchors.verticalCenter:parent.verticalCenter
   gradient:Gradient{GradientStop{position:0;color:Theme.accent}GradientStop{position:1;color:"#24143A"}}
   Text{anchors.centerIn:parent;text:(track.title||"?").charAt(0).toUpperCase();color:"white";font.bold:true}
  }
  Column { width:parent.width-150;anchors.verticalCenter:parent.verticalCenter;spacing:3
   Text{text:track.title||"Sem título";color:Theme.foreground;font.pixelSize:13;elide:Text.ElideRight;width:parent.width}
   Text{text:(track.artist||"Desconhecido")+" • "+(track.album||"");color:Theme.muted;font.pixelSize:11;elide:Text.ElideRight;width:parent.width}
  }
  Text{text:track.format||"";color:Theme.muted;font.pixelSize:10;anchors.verticalCenter:parent.verticalCenter}
  Text{text:rootTime(track.duration);color:Theme.muted;font.pixelSize:10;anchors.verticalCenter:parent.verticalCenter}
 }
 MouseArea{id:mouse;anchors.fill:parent;hoverEnabled:true;onClicked:activated(track)}
 function rootTime(v){let s=Math.floor(v||0);return Math.floor(s/60)+":"+String(s%60).padStart(2,"0")}
}
