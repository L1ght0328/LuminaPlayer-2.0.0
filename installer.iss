#define AppName "Lumina Player"
#define AppVersion "1.0.0"
#define AppExe "LuminaPlayer.exe"
[Setup]
AppId={{7A32E8D0-1B72-4A87-92F4-2E63B7AFC410}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=Lumina
DefaultDirName={autopf}\Lumina Player
DefaultGroupName=Lumina Player
OutputDir=installer_output
OutputBaseFilename=LuminaPlayer_Setup
ArchitecturesInstallIn64BitMode=x64
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
SetupIconFile=assets\icon.ico
[Files]
Source: "dist\LuminaPlayer\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion
[Icons]
Name: "{group}\Lumina Player"; Filename: "{app}\{#AppExe}"
Name: "{autodesktop}\Lumina Player"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon
[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Atalhos:"
[Run]
Filename: "{app}\{#AppExe}"; Description: "Abrir Lumina Player"; Flags: postinstall nowait skipifsilent
