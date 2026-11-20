import QtQuick
import QtQuick.Controls
import "components"
import "."
Rectangle {
 width:220;color:Theme.surface
 Column {
  anchors.fill:parent;anchors.margins:18;spacing:10
  Row{spacing:10
   Rectangle{width:34;height:34;radius:10;color:Theme.accent;Text{anchors.centerIn:parent;text:"L";font.bold:true;font.pixelSize:22;color:"white"}}
   Column{Text{text:"LUMINA";color:Theme.foreground;font.bold:true;font.pixelSize:17;letterSpacing:2}Text{text:"PLAYER";color:Theme.muted;font.pixelSize:9;letterSpacing:3}}
  }
  Rectangle{width:parent.width;height:1;color:Theme.surface2}
  Text{text:"BIBLIOTECA";color:Theme.muted;font.pixelSize:10;font.bold:true}
  Repeater{model:["Explorar","Playlists","Cantores","Vídeos"]
   delegate:Button{width:parent.width;height:42;text:modelData;flat:true
    contentItem:Text{text:parent.text;color:backend.page===parent.text?Theme.highlight:Theme.foreground;font.pixelSize:14;verticalAlignment:Text.AlignVCenter}
    background:Rectangle{radius:8;color:backend.page===modelData?Theme.surface2:"transparent"}
    onClicked:backend.setPage(modelData)
   }
  }
  Item{Layout.fillHeight:true}
  Button{text:"Configurações";width:parent.width;onClicked:backend.setPage("Configurações")}
  Text{text:"OFFLINE • LOCAL";color:Theme.muted;font.pixelSize:9}
 }
}
