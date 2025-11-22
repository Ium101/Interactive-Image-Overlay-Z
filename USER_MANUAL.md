# User Manual / Manual do Usuário - Image Overlay Z

<h3 align="center">
  <a href="#english">English</a> • <a href="#português-brasil">Português (Brasil)</a>
</h3>

---

## English

Welcome to the user manual for **Image Overlay Z**! This guide provides a step-by-step walkthrough of how to use the graphical application to apply overlays to your images efficiently.

### Table of Contents

1.  [Introduction](#1-introduction)
2.  [System Requirements](#2-system-requirements)
3.  [Step-by-Step Guide](#3-step-by-step-guide)
    -   [Step 1: Language Selection](#step-1-language-selection)
    -   [Step 2: Select the Overlay Image](#step-2-select-the-overlay-image)
    -   [Step 3: Select the Target Images](#step-3-select-the-target-images)
    -   [Step 4: Select the Output Folder](#step-4-select-the-output-folder)
    -   [Step 5: Configure Options](#step-5-configure-options)
    -   [Step 6: Processing](#step-6-processing)
4.  [Explanation of Options](#4-explanation-of-options)
    -   [Auto-Recolor for Contrast](#auto-recolor-for-contrast)
    -   [Overlay Size](#overlay-size)
    -   [Opacity](#opacity)
    -   [Position](#position)
5.  [Troubleshooting](#5-troubleshooting)

---

### 1. Introduction

**Image Overlay Z** is a graphical tool designed to apply an image overlay to multiple images at once. It simplifies the process with a user-friendly interface, eliminating the need for command-line operations. Its standout feature is the ability to intelligently adjust the overlay's tone to ensure it is always visible, whether the background is light or dark.

### 2. System Requirements

To run the application, you will need:
-   **Python 3.8 or higher**.
-   The following Python libraries: **pillow** and **Numpy**. You can install them with this command:
    ```bash
    pip install pillow numpy
    ```

### 3. Step-by-Step Guide

#### Step 1: Language Selection
When you first run the script, a window will appear asking you to choose your preferred language. Click **"Continue in English"** or **"Continuar em Português Brasileiro"** to proceed.

#### Step 2: Select the Overlay Image
A file dialog will open. Navigate to and select the image file you want to use as your overlay (e.g., your logo). This image should ideally have a transparent background for the best results.

#### Step 3: Select the Target Images
Next, another file dialog will open. Here, you can select one or more images that you want to apply the overlay to. You can select multiple files at once by holding down **Ctrl** (Windows/Linux) or **Cmd** (Mac) while clicking.

#### Step 4: Select the Output Folder
After selecting your images, you will be prompted to choose a folder where the new, processed images will be saved.

#### Step 5: Configure Options
A graphical interface will appear with real-time preview. You can:
1.  **Choose Position:** Select from 9 positions (corners, edges, and center) using buttons in a 3×3 grid.
2.  **Set Size:** Use a slider to adjust the overlay size as a percentage of the image height.
3.  **Set Opacity:** Use a slider to control transparency (0-100%).
4.  **Set Padding:** Adjust top/bottom and left/right padding (in pixels) for precise positioning.
5.  **Auto-adjust Tone:** Enable/disable automatic tone adjustment based on the background brightness.
6.  **Choose Color Mode:** Select between original color, auto-tone, or custom color.

You have two workflows:
- **Quick Mode:** Skip the "Apply" step and go straight to "Process All Images" to apply the current settings to all selected images at once.
- **Detailed Mode:** Click "Apply to This Image" for each image to customize them individually, then click "Process All Images" to process only the images you applied settings to.

You can also skip specific images by clicking "Skip This Image" - they won't be processed.

#### Step 6: Processing
Click "Process All Images" to begin. A success message will show how many images were processed. Your new images will be in the output folder you selected.

### 4. Explanation of Options

#### Auto-Recolor for Contrast
This is the application's most powerful feature. When enabled, it analyzes the area behind the overlay on each image and automatically adjusts the tone:
-   If the area is **dark**, the overlay is automatically made **lighter**.
-   If the area is **light**, the overlay is automatically made **darker**.
This ensures your overlay is always easy to see.

#### Position
You can place the overlay in 9 different positions: all four corners, the four edges (top, bottom, left, right centers), and the center of the image.

#### Size
The overlay size is set as a percentage of the target image's height. For example, `10%` means the overlay will be 10% of the image's height. This maintains consistent sizing across images of different dimensions.

#### Opacity
Controls how transparent the overlay is. A value of `100` means it's fully visible, while `50` is semi-transparent.

#### Padding
Allows you to fine-tune the position by adding extra space from the edges:
-   **Top/Bottom Padding:** Distance from top or bottom edge.
-   **Left/Right Padding:** Distance from left or right edge.

### 5. Troubleshooting

-   **Error: "File or directory not found"**
    -   **Solution:** Ensure that the file paths selected for the overlay and target images are correct and that you have permission to save files in the chosen output folder.

-   **Application closes unexpectedly:**
    -   **Solution:** If you close any of the initial file or option dialogs, the application will exit by design. To complete the process, you must provide input for all steps.

For other issues, please open an *issue* on our GitHub repository.

---

## Português (Brasil)

Bem-vindo ao manual do usuário do **Image Overlay Z**! Este guia oferece um passo a passo detalhado de como usar a aplicação gráfica para aplicar sobreposições em suas imagens de forma eficiente.

### Índice

1.  [Introdução](#1-introdução-1)
2.  [Requisitos do Sistema](#2-requisitos-do-sistema-1)
3.  [Guia Passo a Passo](#3-guia-passo-a-passo)
    -   [Passo 1: Seleção de Idioma](#passo-1-seleção-de-idioma)
    -   [Passo 2: Selecione a Imagem de Sobreposição](#passo-2-selecione-a-imagem-de-sobreposição)
    -   [Passo 3: Selecione as Imagens de Destino](#passo-3-selecione-as-imagens-de-destino)
    -   [Passo 4: Selecione a Pasta de Saída](#passo-4-selecione-a-pasta-de-saída)
    -   [Passo 5: Configure as Opções](#passo-5-configure-as-opções)
    -   [Passo 6: Processamento](#passo-6-processamento)
4.  [Explicação das Opções](#4-explicação-das-opções)
    -   [Ajuste de Cor Automático para Contraste](#ajuste-de-cor-automático-para-contraste)
    -   [Tamanho da Sobreposição](#tamanho-da-sobreposição)
    -   [Opacidade](#opacidade)
    -   [Posição](#posição)
5.  [Solução de Problemas](#5-solução-de-problemas)

---

### 1. Introdução

O **Image Overlay Z** é uma ferramenta gráfica projetada para aplicar uma sobreposição de imagem em múltiplos arquivos de uma só vez. Ele simplifica o processo com uma interface amigável, eliminando a necessidade de operações de linha de comando. Sua principal funcionalidade é a capacidade de ajustar inteligentemente o tom da sobreposição para garantir que ela esteja sempre visível, seja o fundo claro ou escuro.

### 2. Requisitos do Sistema

Para executar a aplicação, você precisará de:
-   **Python 3.8 ou superior**.
-   As seguintes bibliotecas Python: **pillow** e **Numpy**. Você pode instalá-las com este comando:
    ```bash
    pip install pillow numpy
    ```

### 3. Guia Passo a Passo

#### Passo 1: Seleção de Idioma
Ao executar o script pela primeira vez, uma janela aparecerá pedindo para você escolher seu idioma de preferência. Clique em **"Continuar em Português Brasileiro"** ou **"Continue in English"** para prosseguir.

#### Passo 2: Selecione a Imagem de Sobreposição
Uma janela de seleção de arquivo será aberta. Navegue e selecione o arquivo de imagem que você deseja usar como sua sobreposição (por exemplo, seu logo). Para melhores resultados, essa imagem deve ter um fundo transparente.

#### Passo 3: Selecione as Imagens de Destino
Em seguida, outra janela de seleção de arquivo será aberta. Aqui, você pode selecionar uma ou mais imagens nas quais deseja aplicar a sobreposição. Você pode selecionar vários arquivos de uma vez segurando **Ctrl** (Windows/Linux) ou **Cmd** (Mac) enquanto clica.

#### Passo 4: Selecione a Pasta de Saída
Após selecionar suas imagens, você será solicitado a escolher uma pasta onde as novas imagens processadas serão salvas.

#### Passo 5: Configure as Opções
Uma interface gráfica aparecerá com visualização em tempo real. Você pode:
1.  **Escolher Posição:** Selecione entre 9 posições (cantos, bordas e centro) usando botões em uma grade 3×3.
2.  **Definir Tamanho:** Use um controle deslizante para ajustar o tamanho da sobreposição como uma porcentagem da altura da imagem.
3.  **Definir Opacidade:** Use um controle deslizante para controlar a transparência (0-100%).
4.  **Definir Preenchimento:** Ajuste o preenchimento superior/inferior e esquerdo/direito (em pixels) para posicionamento preciso.
5.  **Ajustar Tom Automaticamente:** Ativar/desativar o ajuste automático de tom com base no brilho do fundo.
6.  **Escolher Modo de Cor:** Selecione entre cor original, tom automático ou cor personalizada.

Você tem dois fluxos de trabalho:
- **Modo Rápido:** Pule a etapa "Aplicar" e vá direto para "Processar Todas as Imagens" para aplicar as configurações atuais a todas as imagens selecionadas de uma só vez.
- **Modo Detalhado:** Clique em "Aplicar a Esta Imagem" para cada imagem a fim de personalizá-las individualmente, então clique em "Processar Todas as Imagens" para processar apenas as imagens às quais você aplicou as configurações.

Você também pode pular imagens específicas clicando em "Pular Esta Imagem" - elas não serão processadas.

#### Passo 6: Processamento
Clique em "Processar Todas as Imagens" para começar. Uma mensagem de sucesso mostrará quantas imagens foram processadas. Suas novas imagens estarão na pasta de saída que você selecionou.

### 4. Explicação das Opções

#### Ajuste de Cor Automático para Contraste
Esta é a funcionalidade mais poderosa da aplicação. Quando ativada, ela analisa a área atrás da sobreposição em cada imagem e ajusta automaticamente o tom:
-   Se a área for **escura**, a sobreposição é automaticamente tornada mais **clara**.
-   Se a área for **clara**, a sobreposição é automaticamente tornada mais **escura**.
Isso garante que sua sobreposição seja sempre fácil de ver.

#### Posição
Você pode posicionar a sobreposição em 9 posições diferentes: todos os quatro cantos, as quatro bordas (centros superior, inferior, esquerdo e direito) e o centro da imagem.

#### Tamanho
O tamanho da sobreposição é definido como uma porcentagem da altura da imagem de destino. Por exemplo, `10%` significa que a sobreposição será 10% da altura da imagem. Isso mantém o dimensionamento consistente em imagens de diferentes dimensões.

#### Opacidade
Controla o quão transparente a sobreposição é. Um valor de `100` significa que está totalmente visível, enquanto `50` é semitransparente.

#### Preenchimento
Permite que você ajuste melhor a posição adicionando espaço extra nas bordas:
-   **Preenchimento Superior/Inferior:** Distância da borda superior ou inferior.
-   **Preenchimento Esquerdo/Direito:** Distância da borda esquerda ou direita.

### 5. Solução de Problemas

-   **Erro: "Arquivo ou diretório não encontrado"**
    -   **Solução:** Certifique-se de que os caminhos dos arquivos selecionados para a sobreposição e as imagens de destino estão corretos e que você tem permissão para salvar arquivos na pasta de saída escolhida.

-   **A aplicação fecha inesperadamente:**
    -   **Solution:** Se você fechar qualquer uma das janelas de seleção de arquivo ou de opções, a aplicação será encerrada. Para concluir o processo, você deve fornecer as informações em todos os passos.

For other issues, please open an *issue* on our GitHub repository.
```
