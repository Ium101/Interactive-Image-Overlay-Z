import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image
import numpy as np

LANGUAGES = {
    "en": {
        "title": "Interactive Image Overlay Z",
        "select_overlay": "Select Watermark",
        "select_targets": "Select Images",
        "position": "Position:",
        "size": "Size (%):",
        "opacity": "Opacity (%):",
        "top_bottom_padding": "Top/Bottom (px):",
        "left_right_padding": "Left/Right (px):",
        "auto_tone": "Auto-adjust tone",
        "no_color": "Original Color",
        "choose_color": "Choose Color",
        "apply": "Apply to This Image",
        "skip": "Skip This Image",
        "process_all": "Process All Images",
        "select_output": "Select Output Folder",
        "success": "All images processed successfully!",
        "no_images": "No images selected!",
        "no_watermark": "Please select a watermark first!",
        "top_left": "Top Left",
        "top_center": "Top Center",
        "top_right": "Top Right",
        "middle_left": "Middle Left",
        "center": "Center",
        "middle_right": "Middle Right",
        "bottom_left": "Bottom Left",
        "bottom_center": "Bottom Center",
        "bottom_right": "Bottom Right",
    },
    "pt": {
        "title": "Sobreposição Interativa Z",
        "select_overlay": "Selecionar Marca d'água",
        "select_targets": "Selecionar Imagens",
        "position": "Posição:",
        "size": "Tamanho (%):",
        "opacity": "Opacidade (%):",
        "top_bottom_padding": "Topo/Base (px):",
        "left_right_padding": "Esq/Dir (px):",
        "auto_tone": "Ajustar tom automaticamente",
        "no_color": "Cor Original",
        "choose_color": "Escolher Cor",
        "apply": "Aplicar a Esta Imagem",
        "skip": "Pular Esta Imagem",
        "process_all": "Processar Todas as Imagens",
        "select_output": "Selecionar Pasta de Saída",
        "success": "Todas as imagens processadas com sucesso!",
        "no_images": "Nenhuma imagem selecionada!",
        "no_watermark": "Por favor, selecione uma marca d'água primeiro!",
        "top_left": "Canto Superior Esquerdo",
        "top_center": "Topo Centro",
        "top_right": "Canto Superior Direito",
        "middle_left": "Meio Esquerdo",
        "center": "Centro",
        "middle_right": "Meio Direito",
        "bottom_left": "Canto Inferior Esquerdo",
        "bottom_center": "Base Centro",
        "bottom_right": "Canto Inferior Direito",
    }
}

def analyze_brightness(image, bbox):
    """Analyze brightness of the region where watermark will be placed"""
    region = image.crop(bbox)
    gray_region = region.convert('L')
    pixels = list(gray_region.getdata())
    return sum(pixels) / len(pixels) if pixels else 128

def adjust_overlay_tone(overlay, brightness):
    """Adjust overlay tone based on background brightness"""
    if brightness > 128:
        # Light background - make overlay darker
        overlay = Image.new('RGBA', overlay.size, (0, 0, 0, 0))
    else:
        # Dark background - make overlay lighter
        overlay = Image.new('RGBA', overlay.size, (255, 255, 255, 0))
    return overlay

def process_images(overlay_path, target_paths, output_folder, position, size_percent, opacity, tb_padding, lr_padding, auto_tone):
    """Process all images with watermark overlay"""
    overlay = Image.open(overlay_path).convert("RGBA")
    
    for target_path in target_paths:
        try:
            base = Image.open(target_path).convert("RGBA")
            base_w, base_h = base.size
            overlay_w, overlay_h = overlay.size
            
            # Resize overlay
            new_h = int(base_h * size_percent / 100.0)
            new_w = int(new_h * (overlay_w / overlay_h))
            overlay_resized = overlay.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # Calculate position with padding
            if position == "top_left":
                pos_x, pos_y = lr_padding, tb_padding
            elif position == "top_center":
                pos_x, pos_y = (base_w - new_w) // 2, tb_padding
            elif position == "top_right":
                pos_x, pos_y = base_w - new_w - lr_padding, tb_padding
            elif position == "middle_left":
                pos_x, pos_y = lr_padding, (base_h - new_h) // 2
            elif position == "center":
                pos_x, pos_y = (base_w - new_w) // 2, (base_h - new_h) // 2
            elif position == "middle_right":
                pos_x, pos_y = base_w - new_w - lr_padding, (base_h - new_h) // 2
            elif position == "bottom_left":
                pos_x, pos_y = lr_padding, base_h - new_h - tb_padding
            elif position == "bottom_center":
                pos_x, pos_y = (base_w - new_w) // 2, base_h - new_h - tb_padding
            else:  # bottom_right
                pos_x, pos_y = base_w - new_w - lr_padding, base_h - new_h - tb_padding
            
            # Apply auto-tone adjustment if enabled
            if auto_tone:
                bbox = (pos_x, pos_y, pos_x + new_w, pos_y + new_h)
                brightness = analyze_brightness(base, bbox)
                overlay_resized = adjust_overlay_tone(overlay_resized, brightness)
            
            # Apply opacity
            opacity_val = opacity / 100.0
            if opacity_val < 1.0:
                channels = overlay_resized.split()
                if len(channels) == 4:
                    r, g, b, a = channels
                    a = a.point(lambda p: int(p * opacity_val))
                    overlay_resized = Image.merge('RGBA', (r, g, b, a))
            
            # Composite images
            combined = base.copy()
            combined.paste(overlay_resized, (pos_x, pos_y), overlay_resized)
            
            # Save output
            basename = os.path.splitext(os.path.basename(target_path))[0]
            out_path = os.path.join(output_folder, basename + ".png")
            combined.save(out_path, format="PNG", compress_level=0, optimize=False)
            
        except Exception as e:
            return str(e)
    
    return None

def run_cli(lang_code):
    """Run the CLI version for batch processing"""
    L = LANGUAGES[lang_code]
    
    root = tk.Tk()
    root.withdraw()
    
    # Select overlay
    overlay_path = filedialog.askopenfilename(
        title=L["select_overlay"],
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
    )
    if not overlay_path:
        return
    
    # Select target images
    target_paths = filedialog.askopenfilenames(
        title=L["select_targets"],
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
    )
    if not target_paths:
        return
    
    # Select output folder
    output_folder = filedialog.askdirectory(title=L["select_output"])
    if not output_folder:
        return
    
    # Get settings
    position = "bottom_right"  # Default position
    size_percent = 10  # Default 10% of image height
    opacity = 100  # Default full opacity
    tb_padding = 10  # Default top/bottom padding
    lr_padding = 10  # Default left/right padding
    auto_tone = True  # Default auto-tone enabled
    
    # Process all images
    error = process_images(overlay_path, target_paths, output_folder, position, size_percent, opacity, tb_padding, lr_padding, auto_tone)
    
    if error:
        messagebox.showerror(L["title"], f"Error: {error}")
    else:
        messagebox.showinfo(L["title"], L["success"])
    
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    # Language selection
    lang_choice = simpledialog.askstring(
        "Language / Idioma",
        "Select language / Selecione o idioma:\n1. Português Brasileiro\n2. English\nEnter 1 or 2:"
    )
    
    lang_code = "pt" if lang_choice == "1" else "en"
    run_cli(lang_code)