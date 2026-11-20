import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "."
ApplicationWindow{
 id:win;visible:true;width:1366;height:768;minimumWidth:960;minimumHeight:600
 title:"Lumina Player";color:Theme.background
 onClosing:backend.shutdown()
 Shortcut{sequence:"Space";onActivated:backend.togglePlay()}
 Shortcut{sequence:"N";onActivated:backend.skip()}
 Shortcut{sequence:"P";onActivated:backend.previous()}
 Shortcut{sequence:"M";onActivated:backend.playback.toggleMute()}
 Shortcut{sequence:"Left";onActivated:backend.playback.seekRelative(-5000)}
 Shortcut{sequence:"Right";onActivated:backend.playback.seekRelative(5000)}
 Shortcut{sequence:"Up";onActivated:backend.setVolume(Math.min(100,backend.playback.volume+5))}
 Shortcut{sequence:"Down";onActivated:backend.setVolume(Math.max(0,backend.playback.volume-5))}
 Shortcut{sequence:"F11";onActivated:visibility=visibility===Window.FullScreen?Window.Windowed:Window.FullScreen}
 Shortcut{sequence:"Ctrl+F";onActivated:backend.setPage("Explorar")}
 RowLayout{anchors.fill:parent;anchors.bottomMargin:100;spacing:0
  Sidebar{Layout.fillHeight:true}
  Rectangle{Layout.fillWidth:true;Layout.fillHeight:true;color:Theme.background
   ColumnLayout{anchors.fill:parent;anchors.margins:26;spacing:16
    RowLayout{Layout.fillWidth:true
     Text{text:backend.page;color:Theme.foreground;font.pixelSize:13;font.bold:true}
     Item{Layout.fillWidth:true}
     Text{text:"● OFFLINE";color:Theme.highlight;font.pixelSize:10}
    }
    StackLayout{Layout.fillWidth:true;Layout.fillHeight:true;currentIndex:backend.page==="Explorar"?0:backend.page==="Vídeos"?1:backend.page==="Configurações"?2:backend.page==="Playlists"?3:4
     Explore{} Video{} Settings{} Playlists{} Artists{}
    }
   }
  }
 }
 PlayerBar{anchors.left:parent.left;anchors.right:parent.right;anchors.bottom:parent.bottom}
 Rectangle{id:toast;anchors.horizontalCenter:parent.horizontalCenter;anchors.bottom:parent.bottom;anchors.bottomMargin:112
  width:toastLabel.implicitWidth+34;height:42;radius:12;color:Theme.surface2;border.color:Theme.accent;opacity:0;visible:opacity>0
  Text{id:toastLabel;anchors.centerIn:parent;color:Theme.foreground;font.pixelSize:12}
  Behavior on opacity{NumberAnimation{duration:180}}
  Timer{id:hideTimer;interval:2500;onTriggered:toast.opacity=0}
 }
 Connections{target:backend;function onToast(msg){toastLabel.text=msg;toast.opacity=1;hideTimer.restart()}}
}
