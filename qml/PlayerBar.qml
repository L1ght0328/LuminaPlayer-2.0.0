import QtQuick
import QtQuick.Controls
import "."
Rectangle {
 height:100;color:Theme.surface;border.color:Theme.surface2
 Column{anchors.fill:parent;anchors.margins:12;spacing:4
  Row{width:parent.width;height:42;spacing:8
   Column{width:230;anchors.verticalCenter:parent.verticalCenter
    Text{text:backend.playback.title;color:Theme.foreground;font.bold:true;font.pixelSize:13;elide:Text.ElideRight;width:230}
    Text{text:backend.playback.artist;color:Theme.muted;font.pixelSize:11;elide:Text.ElideRight;width:230}
   }
   Item{width:10}
   ToolButton{text:"⇄";onClicked:backend.playback.toggleShuffle();contentItem:Text{text:parent.text;color:backend.playback.shuffle?Theme.highlight:Theme.muted}}
   ToolButton{text:"|◀";onClicked:backend.previous()}
   ToolButton{width:42;height:42;background:Rectangle{radius:21;color:Theme.accent}
    contentItem:Text{text:backend.playback.state==="playing"?"Ⅱ":"▶";color:"white";font.pixelSize:18;horizontalAlignment:Text.AlignHCenter;verticalAlignment:Text.AlignVCenter}
    onClicked:backend.togglePlay()
   }
   ToolButton{text:"▶|";onClicked:backend.skip()}
   ToolButton{text:backend.playback.repeat==="one"?"↻¹":"↻";onClicked:backend.playback.cycleRepeat();contentItem:Text{text:parent.text;color:backend.playback.repeat==="off"?Theme.muted:Theme.highlight}}
   Item{width:10}
   ToolButton{text:backend.playback.volume===0?"🔇":"🔊";onClicked:backend.playback.toggleMute()}
   Slider{width:100;from:0;to:100;value:backend.playback.volume;onMoved:backend.setVolume(Math.round(value))}
   Text{text:backend.playback.volume+"%";color:Theme.muted;font.pixelSize:10;anchors.verticalCenter:parent.verticalCenter}
  }
  Row{width:parent.width;spacing:8
   Text{text:fmt(backend.playback.position);color:Theme.muted;font.pixelSize:10;anchors.verticalCenter:parent.verticalCenter}
   Slider{id:seek;width:parent.width-100;from:0;to:Math.max(1,backend.playback.duration);value:backend.playback.position;onMoved:backend.playback.seek(Math.round(value))}
   Text{text:fmt(backend.playback.duration);color:Theme.muted;font.pixelSize:10;anchors.verticalCenter:parent.verticalCenter}
  }
 }
 function fmt(ms){let s=Math.floor(ms/1000);return Math.floor(s/60)+":"+String(s%60).padStart(2,"0")}
}
