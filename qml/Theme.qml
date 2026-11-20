pragma Singleton
import QtQuick
QtObject {
 property bool dark:true
 property string palette:"Lumina"
 property color background:dark?"#0A0A0F":"#F4F2F8"
 property color surface:dark?"#14121F":"#FFFFFF"
 property color surface2:dark?"#201B2D":"#EAE6F2"
 property color foreground:dark?"#F2F2F7":"#191522"
 property color muted:dark?"#A09CB5":"#706A80"
 property color accent:palette==="Ciano Elétrico"?"#00E5FF":palette==="Magenta Neon"?"#FF2BD6":palette==="Laranja Choque"?"#FF7A18":palette==="Azul Cobalto"?"#356BFF":palette==="Vermelho Carmesim"?"#F02D4E":"#8B2BE2"
 property color highlight:palette==="Lumina"?"#39FF14":accent
}
