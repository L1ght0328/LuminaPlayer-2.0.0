# Lumina Player — build na nuvem (Windows 10/11)

O usuário final **não precisa instalar Python, pip ou qualquer ferramenta de desenvolvimento**. O GitHub Actions prepara o programa em um computador Windows na nuvem e publica dois downloads: versão portátil e instalador.

## 1. Criar uma conta e um repositório
1. Acesse https://github.com e crie uma conta gratuita, se ainda não tiver.
2. Clique em **New repository**.
3. Dê o nome `lumina-player`.
4. Escolha Public ou Private e clique em **Create repository**.

## 2. Enviar os arquivos pelo navegador
1. Baixe e extraia o ZIP do projeto.
2. Abra o repositório no GitHub.
3. Clique em **Add file > Upload files**.
4. Arraste para a página **todo o conteúdo que está dentro da pasta `lumina_player_cloud`**, não a pasta externa em si.
5. Aguarde o envio e clique em **Commit changes**.

### Atenção à pasta oculta .github
Alguns sistemas escondem pastas que começam com ponto. Confirme que o arquivo `.github/workflows/build.yml` foi enviado.
Se não aparecer:
1. No repositório, clique em **Add file > Create new file**.
2. No campo do nome, digite exatamente `.github/workflows/build.yml`.
3. Abra o arquivo `build.yml` que veio no ZIP, copie todo o conteúdo e cole no editor do GitHub.
4. Clique em **Commit changes**.

## 3. Acompanhar o build e baixar
1. Abra a aba **Actions** do repositório.
2. Clique na execução mais recente chamada **Build Lumina Player**.
3. Aguarde o processo terminar com o ícone verde. O primeiro build pode levar alguns minutos.
4. No fim da página da execução, procure **Artifacts**.
5. Baixe:
   - `LuminaPlayer-Portable`: ZIP com a pasta do programa. Extraia e abra `LuminaPlayer.exe`.
   - `LuminaPlayer-Installer`: ZIP do artefato contendo `LuminaPlayer_Setup.exe`. Extraia e execute o instalador.

## 4. Se o build falhar
1. Na aba Actions, clique na execução com ícone vermelho.
2. Abra a etapa que falhou.
3. Copie as últimas linhas do erro e envie ao assistente para corrigir os arquivos necessários.

## 5. Se o programa fechar ou travar
1. Pressione `Win + R`.
2. Cole `%APPDATA%\\LuminaPlayer` e pressione Enter.
3. Abra `lumina.log`.
4. Copie o conteúdo e envie ao assistente. O aplicativo não envia logs nem dados para a internet.

## 6. Aviso do Windows SmartScreen
O executável não tem assinatura digital comercial. O Windows pode exibir **O Windows protegeu seu computador**.
Só se você baixou o instalador do seu próprio repositório GitHub e confia nele: clique em **Mais informações > Executar assim mesmo**. Se o antivírus indicar uma ameaça real, não ignore o alerta; envie o log para análise.

## 7. Atualizar o aplicativo
Substitua os arquivos alterados no repositório usando **Add file > Upload files**, ou abra um arquivo e use o lápis para editá-lo no navegador. Faça **Commit changes**. O workflow será executado novamente em cada push para a branch `main`.

## Recursos e limitações desta compilação
- Biblioteca de áudio local, leitura de tags e banco SQLite.
- Controles básicos de reprodução, volume, shuffle, repeat, busca e favoritos no banco.
- Tema escuro/claro e seis paletas.
- Aba de vídeo com seleção local e controles básicos; suporte efetivo a contêineres/codecs varia conforme a distribuição do Qt e o backend multimídia.
- O mixer expõe balanço/velocidade/ganho; o equalizador DSP de três bandas não é aplicado nesta versão. Os presets armazenam perfis, não alteram o espectro.
- Gestão visual completa de playlists, miniaturas de vídeo lazy, legendas SRT, tray icon, sleep timer, fila editável, teclas de mídia, drag-and-drop, espectro reativo, transições completas e persistência total da janela ainda não estão implementados.
- A versão não pode prometer RAM inferior a 350 MB, CPU inferior a 3% ou abertura abaixo de 3 segundos sem medições no Windows de destino.
- A CI executa testes em modo offscreen, cria o ícone e tenta fazer smoke test do executável. O smoke test é indicativo e não substitui testes manuais em Windows 10/11.

## Teste inicial após baixar
- Adicionar uma pasta com MP3/FLAC e verificar se as faixas aparecem.
- Reproduzir, pausar e retomar.
- Testar anterior/próxima, incluindo fim da fila.
- Testar volume 0, 50 e 100, mute e seek.
- Alterar velocidade e balanço no mixer.
- Abrir um vídeo MP4 conhecido e testar tela cheia.
- Reiniciar o app e confirmar que o banco e configurações continuam na pasta `%APPDATA%\\LuminaPlayer`.
