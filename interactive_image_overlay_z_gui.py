import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np

LANGUAGES = {
    "en": {
        "title": "Interactive Image Overlay Z",
        "preview": "Preview",
        "settings": "Settings",
        "credits": "Made by Ium101",
        "select_overlay": "Select Watermark",
        "select_targets": "Select Images",
        "position": "Position:",
        "size": "Size (%):",
        "opacity": "Opacity (%):",
        "padding": "Padding:",
        "top_bottom_padding": "Top/Bottom (px):",
        "left_right_padding": "Left/Right (px):",
        "color": "Color:",
        "auto_tone": "Auto-adjust tone",
        "no_color": "Original Color",
        "choose_color": "Choose Color",
        "apply": "Apply to This Image",
        "skip": "Skip This Image",
        "previous": "◀ Previous Image",
        "process_all": "Process All Images",
        "image": "Image",
        "of": "of",
        "select_output": "Select Output Folder",
        "success": "All images processed successfully!",
        "saved": "Saved:",
        "top_left": "Top Left",
        "top_center": "Top Center",
        "top_right": "Top Right",
        "middle_left": "Middle Left",
        "center": "Center",
        "middle_right": "Middle Right",
        "bottom_left": "Bottom Left",
        "bottom_center": "Bottom Center",
        "bottom_right": "Bottom Right",
        "no_images": "No images selected!",
        "no_watermark": "Please select a watermark first!",
        "all_configured": "All images configured! Click 'Process All' to save.",
        "no_more": "No more images.",
        "first_image": "This is the first image."
    },
    "pt": {
        "title": "Sobreposição Interativa Z",
        "preview": "Visualização",
        "settings": "Configurações",
        "credits": "Feito por Ium101",
        "select_overlay": "Selecionar Marca d'água",
        "select_targets": "Selecionar Imagens",
        "position": "Posição:",
        "size": "Tamanho (%):",
        "opacity": "Opacidade (%):",
        "padding": "Preenchimento:",
        "top_bottom_padding": "Topo/Base (px):",
        "left_right_padding": "Esq/Dir (px):",
        "color": "Cor:",
        "auto_tone": "Ajustar tom automaticamente",
        "no_color": "Cor Original",
        "choose_color": "Escolher Cor",
        "apply": "Aplicar a Esta Imagem",
        "skip": "Pular Esta Imagem",
        "previous": "◀ Imagem Anterior",
        "process_all": "Processar Todas as Imagens",
        "image": "Imagem",
        "of": "de",
        "select_output": "Selecionar Pasta de Saída",
        "success": "Todas as imagens processadas com sucesso!",
        "saved": "Salvo:",
        "top_left": "Superior Esquerdo",
        "top_center": "Topo Centro",
        "top_right": "Superior Direito",
        "middle_left": "Meio Esquerdo",
        "center": "Centro",
        "middle_right": "Meio Direito",
        "bottom_left": "Inferior Esquerdo",
        "bottom_center": "Base Centro",
        "bottom_right": "Inferior Direito",
        "no_images": "Nenhuma imagem selecionada!",
        "no_watermark": "Por favor, selecione uma marca d'água primeiro!",
        "all_configured": "Todas as imagens configuradas! Clique em 'Processar Todas' para salvar.",
        "no_more": "Não há mais imagens.",
        "first_image": "Esta é a primeira imagem."
    }
}

class InteractiveOverlayApp:
    def __init__(self, lang_code):
        self.L = LANGUAGES[lang_code]
        self.lang_code = lang_code
        self.root = tk.Tk()
        self.root.title(self.L["title"])
        self.root.geometry("1200x800")
        
        self.overlay_path = None
        self.target_paths = []
        self.current_index = 0
        self.output_folder = None
        self.settings = {}
        
        self.overlay_original = None
        self.base_original = None
        self.preview_image = None
        
        self.setup_ui()
        
        # Automatically start the selection process
        self.root.after(100, self.start_selection_process)
        
    def setup_ui(self):
        # REMOVE ALL PADDING FROM ROOT WINDOW
        self.root.config(padx=0, pady=0)
        
        # Top controls - MINIMAL padding
        control_frame = ttk.Frame(self.root, padding="2")
        control_frame.pack(fill=tk.X, padx=0, pady=0)
        
        self.image_label = ttk.Label(control_frame, text="", font=("Arial", 10, "bold"))
        self.image_label.pack(side=tk.LEFT, padx=5)
        
        # Main content area with ABSOLUTE ZERO padding/margin on ALL SIDES
        content_frame = ttk.Frame(self.root, padding="0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Left side - Preview (ZERO PADDING, ZERO MARGIN)
        preview_frame = ttk.Frame(content_frame, padding="0", relief=tk.FLAT, borderwidth=0)
        preview_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        self.canvas = tk.Canvas(preview_frame, bg='#2b2b2b', highlightthickness=0, relief=tk.FLAT, bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Right side - Controls (NO BLACK BORDERS, COMPACT, BIGGER TEXT)
        settings_frame = ttk.Frame(content_frame, padding="8", relief=tk.FLAT, borderwidth=0)
        settings_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=0, pady=0)
        settings_frame.config(width=300)
        
        # Settings label
        ttk.Label(settings_frame, text=self.L["settings"], font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        # Position
        ttk.Label(settings_frame, text=self.L["position"], font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 3))
        self.position_var = tk.StringVar(value="bottom_right")
        
        # 3x3 grid layout for positions (more compact)
        position_grid = ttk.Frame(settings_frame)
        position_grid.pack(anchor=tk.W, padx=5, pady=3)
        
        positions = [
            ("top_left", self.L["top_left"], 0, 0),
            ("top_center", self.L["top_center"], 0, 1),
            ("top_right", self.L["top_right"], 0, 2),
            ("middle_left", self.L["middle_left"], 1, 0),
            ("center", self.L["center"], 1, 1),
            ("middle_right", self.L["middle_right"], 1, 2),
            ("bottom_left", self.L["bottom_left"], 2, 0),
            ("bottom_center", self.L["bottom_center"], 2, 1),
            ("bottom_right", self.L["bottom_right"], 2, 2)
        ]
        for val, text, row, col in positions:
            ttk.Radiobutton(position_grid, text=text, variable=self.position_var, 
                          value=val, command=self.update_preview).grid(row=row, column=col, sticky=tk.W, padx=2, pady=1)
        
        # Size
        ttk.Separator(settings_frame, orient='horizontal').pack(fill=tk.X, pady=6)
        ttk.Label(settings_frame, text=self.L["size"], font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 3))
        self.size_var = tk.IntVar(value=10)
        size_frame = ttk.Frame(settings_frame)
        size_frame.pack(fill=tk.X, padx=5)
        ttk.Scale(size_frame, from_=1, to=50, variable=self.size_var, 
                 orient=tk.HORIZONTAL, command=lambda x: self.update_preview()).pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.size_label = ttk.Label(size_frame, text="10%", width=6, font=("Arial", 9))
        self.size_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Opacity
        ttk.Separator(settings_frame, orient='horizontal').pack(fill=tk.X, pady=6)
        ttk.Label(settings_frame, text=self.L["opacity"], font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 3))
        self.opacity_var = tk.IntVar(value=100)
        opacity_frame = ttk.Frame(settings_frame)
        opacity_frame.pack(fill=tk.X, padx=5)
        ttk.Scale(opacity_frame, from_=1, to=100, variable=self.opacity_var, 
                 orient=tk.HORIZONTAL, command=lambda x: self.update_preview()).pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.opacity_label = ttk.Label(opacity_frame, text="100%", width=6, font=("Arial", 9))
        self.opacity_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Padding
        ttk.Separator(settings_frame, orient='horizontal').pack(fill=tk.X, pady=6)
        ttk.Label(settings_frame, text=self.L["padding"], font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 3))
        
        ttk.Label(settings_frame, text=self.L["top_bottom_padding"], font=("Arial", 9)).pack(anchor=tk.W, padx=5, pady=(3, 0))
        self.top_bottom_padding_var = tk.IntVar(value=0)
        tb_frame = ttk.Frame(settings_frame)
        tb_frame.pack(fill=tk.X, padx=5)
        ttk.Scale(tb_frame, from_=0, to=100, variable=self.top_bottom_padding_var, 
                 orient=tk.HORIZONTAL, command=lambda x: self.update_preview()).pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.top_bottom_padding_label = ttk.Label(tb_frame, text="0px", width=6, font=("Arial", 9))
        self.top_bottom_padding_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Label(settings_frame, text=self.L["left_right_padding"], font=("Arial", 9)).pack(anchor=tk.W, padx=5, pady=(3, 0))
        self.left_right_padding_var = tk.IntVar(value=0)
        lr_frame = ttk.Frame(settings_frame)
        lr_frame.pack(fill=tk.X, padx=5, pady=(0, 3))
        ttk.Scale(lr_frame, from_=0, to=100, variable=self.left_right_padding_var, 
                 orient=tk.HORIZONTAL, command=lambda x: self.update_preview()).pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.left_right_padding_label = ttk.Label(lr_frame, text="0px", width=6, font=("Arial", 9))
        self.left_right_padding_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Color
        ttk.Separator(settings_frame, orient='horizontal').pack(fill=tk.X, pady=6)
        ttk.Label(settings_frame, text=self.L["color"], font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 3))
        self.color_mode = tk.StringVar(value="auto_tone")
        
        ttk.Radiobutton(settings_frame, text=self.L["auto_tone"], variable=self.color_mode, 
                       value="auto_tone", command=self.update_preview).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Radiobutton(settings_frame, text=self.L["no_color"], variable=self.color_mode, 
                       value="original", command=self.update_preview).pack(anchor=tk.W, padx=5, pady=2)
        
        color_frame = ttk.Frame(settings_frame)
        color_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Radiobutton(color_frame, text=self.L["choose_color"], variable=self.color_mode, 
                       value="custom", command=self.update_preview).pack(side=tk.LEFT)
        self.color_button = tk.Button(color_frame, text="■", font=("Arial", 14), 
                                      command=self.choose_color, width=2, bg="white")
        self.color_button.pack(side=tk.LEFT, padx=5)
        self.selected_color = (255, 255, 255)
        
        # Action buttons (LARGER BUTTONS, CLOSER TOGETHER)
        ttk.Separator(settings_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Navigation buttons frame - LARGER BUTTONS WITH MINIMAL SPACING
        nav_frame = ttk.Frame(settings_frame)
        nav_frame.pack(fill=tk.X, pady=2)
        
        # Style for larger buttons
        style = ttk.Style()
        style.configure("Large.TButton", font=("Arial", 10), padding=8)
        style.configure("Accent.TButton", font=("Arial", 11, "bold"), padding=10)
        
        ttk.Button(nav_frame, text=self.L["previous"], 
                  command=self.previous_image, style="Large.TButton").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 1))
        ttk.Button(nav_frame, text=self.L["apply"], 
                  command=self.apply_current, style="Large.TButton").pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(1, 0))
        
        ttk.Button(settings_frame, text=self.L["skip"], 
                  command=self.skip_current, style="Large.TButton").pack(fill=tk.X, pady=2)
        ttk.Button(settings_frame, text=self.L["process_all"], 
                  command=self.process_all, style="Accent.TButton").pack(fill=tk.X, pady=10)
        
        # Credits with translation
        credits = ttk.Label(settings_frame, text=self.L["credits"] + "\nGitHub", 
                          font=("Arial", 8), justify=tk.CENTER)
        credits.pack(side=tk.BOTTOM, pady=5)
        
        # Style
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 10, "bold"))
    
    def start_selection_process(self):
        """Automatically start watermark and images selection"""
        # Select watermark first
        overlay_path = filedialog.askopenfilename(
            title=self.L["select_overlay"],
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if not overlay_path:
            self.root.destroy()
            return
            
        self.overlay_path = overlay_path
        self.overlay_original = Image.open(overlay_path).convert("RGBA")
        
        # Then automatically select target images
        paths = filedialog.askopenfilenames(
            title=self.L["select_targets"],
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if not paths:
            self.root.destroy()
            return
            
        self.target_paths = list(paths)
        self.current_index = 0
        self.settings = {}
        self.load_current_image()
        
    def analyze_brightness(self, image, bbox):
        """Analyze brightness of the region where watermark will be placed"""
        region = image.crop(bbox)
        gray_region = region.convert('L')
        pixels = list(gray_region.getdata())
        avg_brightness = sum(pixels) / len(pixels)
        return avg_brightness / 255.0
    
    def adjust_overlay_tone(self, overlay, brightness):
        """Adjust overlay tone based on background brightness"""
        overlay = overlay.convert('RGBA')
        channels = overlay.split()
        
        if len(channels) == 4:
            r, g, b, a = channels
        else:
            return overlay
        
        r_array = np.array(r, dtype=np.float32)
        g_array = np.array(g, dtype=np.float32)
        b_array = np.array(b, dtype=np.float32)
        
        if brightness > 0.5:  # Light background - make watermark DARKER
            darken_factor = max(0.02, (1.0 - brightness) ** 2.5)
            r_array = r_array * darken_factor
            g_array = g_array * darken_factor
            b_array = b_array * darken_factor
        else:  # Dark background - make watermark LIGHTER
            lighten_strength = (1.0 - brightness) ** 0.5
            r_array = r_array + (255.0 - r_array) * lighten_strength * 0.95
            g_array = g_array + (255.0 - g_array) * lighten_strength * 0.95
            b_array = b_array + (255.0 - b_array) * lighten_strength * 0.95
        
        r_array = np.clip(r_array, 0, 255).astype(np.uint8)
        g_array = np.clip(g_array, 0, 255).astype(np.uint8)
        b_array = np.clip(b_array, 0, 255).astype(np.uint8)
        
        new_r = Image.fromarray(r_array, mode='L')
        new_g = Image.fromarray(g_array, mode='L')
        new_b = Image.fromarray(b_array, mode='L')
        
        size = a.size
        new_r = new_r.resize(size, Image.Resampling.LANCZOS) if new_r.size != size else new_r
        new_g = new_g.resize(size, Image.Resampling.LANCZOS) if new_g.size != size else new_g
        new_b = new_b.resize(size, Image.Resampling.LANCZOS) if new_b.size != size else new_b
        
        return Image.merge('RGBA', (new_r, new_g, new_b, a))
        
    def load_current_image(self):
        if not self.target_paths:
            return
            
        self.base_original = Image.open(self.target_paths[self.current_index]).convert("RGBA")
        self.image_label.config(text=f"{self.L['image']} {self.current_index + 1} {self.L['of']} {len(self.target_paths)}")
        
        # Load saved settings if any
        if self.current_index in self.settings:
            s = self.settings[self.current_index]
            self.position_var.set(s['position'])
            self.size_var.set(s['size'])
            self.opacity_var.set(s['opacity'])
            self.top_bottom_padding_var.set(s.get('top_bottom_padding', 0))
            self.left_right_padding_var.set(s.get('left_right_padding', 0))
            self.color_mode.set(s['color_mode'])
            if s['color']:
                self.selected_color = s['color']
                self.color_button.config(bg=self.rgb_to_hex(s['color']))
        else:
            # Reset to defaults
            self.position_var.set("bottom_right")
            self.size_var.set(10)
            self.opacity_var.set(100)
            self.top_bottom_padding_var.set(0)
            self.left_right_padding_var.set(0)
            self.color_mode.set("auto_tone")
            self.selected_color = (255, 255, 255)
            self.color_button.config(bg="white")
        
        self.update_preview()
        
    def update_preview(self):
        if not self.overlay_original or not self.base_original:
            return
            
        # Update labels
        self.size_label.config(text=f"{self.size_var.get()}%")
        self.opacity_label.config(text=f"{self.opacity_var.get()}%")
        self.top_bottom_padding_label.config(text=f"{self.top_bottom_padding_var.get()}px")
        self.left_right_padding_label.config(text=f"{self.left_right_padding_var.get()}px")
        
        # Create preview
        base = self.base_original.copy()
        overlay = self.overlay_original.copy()
        
        base_w, base_h = base.size
        overlay_w, overlay_h = overlay.size
        
        # Resize overlay
        size_percent = self.size_var.get() / 100.0
        new_h = int(base_h * size_percent)
        new_w = int(new_h * (overlay_w / overlay_h))
        overlay_resized = overlay.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Get padding values
        tb_padding = self.top_bottom_padding_var.get()
        lr_padding = self.left_right_padding_var.get()
        
        # Calculate position with padding (9 positions)
        position = self.position_var.get()
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
        
        # Apply color mode
        color_mode = self.color_mode.get()
        if color_mode == "auto_tone":
            # Auto-adjust tone based on background brightness
            bbox = (pos_x, pos_y, pos_x + new_w, pos_y + new_h)
            brightness = self.analyze_brightness(base, bbox)
            overlay_resized = self.adjust_overlay_tone(overlay_resized, brightness)
        elif color_mode == "custom":
            # Apply custom color
            overlay_resized = self.recolor_overlay(overlay_resized, self.selected_color)
        
        # Apply opacity by adjusting alpha channel
        opacity = self.opacity_var.get() / 100.0
        if opacity < 1.0:
            # Get alpha channel and multiply by opacity
            channels = overlay_resized.split()
            if len(channels) == 4:
                r, g, b, a = channels
                a = a.point(lambda p: int(p * opacity))
                overlay_resized = Image.merge('RGBA', (r, g, b, a))
        
        # Combine using alpha compositing to preserve transparency
        combined = base.copy()
        combined.paste(overlay_resized, (pos_x, pos_y), overlay_resized)
        
        # Display in canvas
        self.display_image(combined)
        
    def display_image(self, image):
        # Resize to fit canvas
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        
        if canvas_w <= 1 or canvas_h <= 1:
            canvas_w, canvas_h = 800, 600
        
        img_w, img_h = image.size
        scale = min(canvas_w / img_w, canvas_h / img_h) * 0.95  # 95% to add padding
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
        
        display_img = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        self.preview_image = ImageTk.PhotoImage(display_img)
        
        self.canvas.delete("all")
        x = canvas_w // 2
        y = canvas_h // 2
        self.canvas.create_image(x, y, anchor=tk.CENTER, image=self.preview_image)
        
    def recolor_overlay(self, overlay, target_color):
        overlay = overlay.convert('RGBA')
        channels = overlay.split()
        
        if len(channels) == 4:
            r, g, b, a = channels
        else:
            return overlay
        
        r_array = np.array(r, dtype=np.float32)
        g_array = np.array(g, dtype=np.float32)
        b_array = np.array(b, dtype=np.float32)
        
        luminance = 0.299 * r_array + 0.587 * g_array + 0.114 * b_array
        luminance_normalized = luminance / 255.0
        
        target_r, target_g, target_b = target_color
        new_r_array = np.clip(luminance_normalized * target_r, 0, 255).astype(np.uint8)
        new_g_array = np.clip(luminance_normalized * target_g, 0, 255).astype(np.uint8)
        new_b_array = np.clip(luminance_normalized * target_b, 0, 255).astype(np.uint8)
        
        new_r = Image.fromarray(new_r_array, mode='L')
        new_g = Image.fromarray(new_g_array, mode='L')
        new_b = Image.fromarray(new_b_array, mode='L')
        
        return Image.merge('RGBA', (new_r, new_g, new_b, a))
        
    def choose_color(self):
        from tkinter.colorchooser import askcolor
        color = askcolor(title=self.L["choose_color"])
        if color[0]:
            self.selected_color = tuple(int(c) for c in color[0])
            self.color_button.config(bg=color[1])
            self.color_mode.set("custom")
            self.update_preview()
            
    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb
        
    def apply_current(self):
        if not self.target_paths:
            return
            
        # Save settings for current image
        self.settings[self.current_index] = {
            'position': self.position_var.get(),
            'size': self.size_var.get(),
            'opacity': self.opacity_var.get(),
            'top_bottom_padding': self.top_bottom_padding_var.get(),
            'left_right_padding': self.left_right_padding_var.get(),
            'color_mode': self.color_mode.get(),
            'color': self.selected_color if self.color_mode.get() == "custom" else None
        }
        
        # Move to next image
        if self.current_index < len(self.target_paths) - 1:
            self.current_index += 1
            self.load_current_image()
        else:
            messagebox.showinfo(self.L["title"], self.L["all_configured"])
            
    def skip_current(self):
        if not self.target_paths:
            return
            
        if self.current_index < len(self.target_paths) - 1:
            self.current_index += 1
            self.load_current_image()
        else:
            messagebox.showinfo(self.L["title"], self.L["no_more"])
    
    def previous_image(self):
        if not self.target_paths:
            return
            
        if self.current_index > 0:
            self.current_index -= 1
            self.load_current_image()
        else:
            messagebox.showinfo(self.L["title"], self.L["first_image"])
            
    def process_all(self):
        if not self.target_paths:
            messagebox.showwarning(self.L["title"], self.L["no_images"])
            return
            
        if not self.settings:
            messagebox.showwarning(self.L["title"], "No images configured! Use 'Apply' to configure images.")
            return
            
        output_folder = filedialog.askdirectory(title=self.L["select_output"])
        if not output_folder:
            return
            
        # Process each image
        processed_count = 0
        for idx, target_path in enumerate(self.target_paths):
            if idx not in self.settings:
                continue  # Skip images without settings
                
            s = self.settings[idx]
            
            try:
                # Load images
                base = Image.open(target_path).convert("RGBA")
                overlay = self.overlay_original.copy()
                
                base_w, base_h = base.size
                overlay_w, overlay_h = overlay.size
                
                # Resize
                size_percent = s['size'] / 100.0
                new_h = int(base_h * size_percent)
                new_w = int(new_h * (overlay_w / overlay_h))
                overlay_resized = overlay.resize((new_w, new_h), Image.Resampling.LANCZOS)
                
                # Position with padding
                position = s['position']
                tb_padding = s.get('top_bottom_padding', 0)
                lr_padding = s.get('left_right_padding', 0)
                
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
                
                # Apply color mode
                color_mode = s['color_mode']
                if color_mode == "auto_tone":
                    # Auto-adjust tone based on background brightness
                    bbox = (pos_x, pos_y, pos_x + new_w, pos_y + new_h)
                    brightness = self.analyze_brightness(base, bbox)
                    overlay_resized = self.adjust_overlay_tone(overlay_resized, brightness)
                elif color_mode == "custom" and s['color']:
                    # Apply custom color
                    overlay_resized = self.recolor_overlay(overlay_resized, s['color'])
                
                # Apply opacity by adjusting alpha channel
                opacity = s['opacity'] / 100.0
                if opacity < 1.0:
                    channels = overlay_resized.split()
                    if len(channels) == 4:
                        r, g, b, a = channels
                        a = a.point(lambda p: int(p * opacity))
                        overlay_resized = Image.merge('RGBA', (r, g, b, a))
                
                # Combine using alpha compositing to preserve transparency
                combined = base.copy()
                combined.paste(overlay_resized, (pos_x, pos_y), overlay_resized)
                
                # Save as PNG with highest quality (no compression, no grey dots)
                basename = os.path.splitext(os.path.basename(target_path))[0]
                out_path = os.path.join(output_folder, basename + ".png")
                
                # Save with no compression to avoid artifacts
                combined.save(out_path, format="PNG", compress_level=0, optimize=False)
                    
                processed_count += 1
                
            except Exception as e:
                messagebox.showerror(self.L["title"], f"Error processing {os.path.basename(target_path)}: {str(e)}")
                continue
        
        messagebox.showinfo(self.L["title"], f"{self.L['success']}\n{processed_count} images processed.")
        
    def run(self):
        self.root.mainloop()

def show_language_selection():
    root = tk.Tk()
    root.title("Interactive Image Overlay Z")
    root.geometry("600x500")
    root.resizable(False, False)
    root.configure(bg='#f0f0f0')
    
    # REMOVE ALL PADDING FROM ROOT WINDOW
    root.config(padx=0, pady=0)

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    
    # Main frame with NO padding - fill entire window
    main_frame = tk.Frame(root, bg='#ffffff', relief=tk.FLAT, borderwidth=0)
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=0, pady=0)
    main_frame.grid_columnconfigure(0, weight=1)
    
    # Header section with gradient-like colored background - FULL WIDTH
    header_frame = tk.Frame(main_frame, bg='#4a90e2', height=140)
    header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
    header_frame.grid_columnconfigure(0, weight=1)
    header_frame.grid_propagate(False)

    # Title with icon
    title_frame = tk.Frame(header_frame, bg='#4a90e2')
    title_frame.pack(expand=True)
    
    title = tk.Label(title_frame, text="🖼️ Interactive Image Overlay Z", 
                    font=("Arial", 24, "bold"), fg='white', bg='#4a90e2')
    title.pack(pady=(20, 5))
    
    subtitle = tk.Label(title_frame, text="Sobreposição Interativa Z", 
                       font=("Arial", 20, "bold"), fg='#e8f4ff', bg='#4a90e2')
    subtitle.pack(pady=(0, 20))
    
    # Content section
    content_frame = tk.Frame(main_frame, bg='#ffffff')
    content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=30, pady=30)
    content_frame.grid_columnconfigure(0, weight=1)
    
    # Info text
    info_text = tk.Label(content_frame, 
                        text="Choose your language to begin\nEscolha seu idioma para começar",
                        font=("Arial", 11), fg='#666666', bg='#ffffff', justify=tk.CENTER)
    info_text.grid(row=0, column=0, pady=(0, 25))
    
    # Custom button style
    def create_button(parent, text, command, row):
        btn_frame = tk.Frame(parent, bg='#ffffff')
        btn_frame.grid(row=row, column=0, pady=8, sticky=tk.EW)
        
        btn = tk.Button(btn_frame, text=text, command=command,
                       font=("Arial", 12, "bold"),
                       bg='#4a90e2', fg='white',
                       activebackground='#357abd',
                       activeforeground='white',
                       relief=tk.FLAT,
                       padx=20, pady=15,
                       cursor='hand2',
                       borderwidth=0)
        btn.pack(fill=tk.X, padx=40)
        
        # Hover effect
        def on_enter(e):
            btn.config(bg='#357abd')
        def on_leave(e):
            btn.config(bg='#4a90e2')
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def start_with_language(lang):
        root.destroy()
        app = InteractiveOverlayApp(lang)
        app.run()
    
    create_button(content_frame, "EN/US", 
                 lambda: start_with_language("en"), 1)
    create_button(content_frame, "PT/BR", 
                 lambda: start_with_language("pt"), 2)
    
    # Separator
    separator = tk.Frame(content_frame, height=2, bg='#e0e0e0')
    separator.grid(row=3, column=0, sticky=tk.EW, pady=20, padx=40)
    
    # Credits
    credits = tk.Label(content_frame, 
                      text="Made by Ium101 from GitHub\nFeito por Ium101 do GitHub",
                      font=("Arial", 9), fg='#999999', bg='#ffffff', justify=tk.CENTER)
    credits.grid(row=4, column=0, pady=(5, 0))
    
    root.mainloop()

if __name__ == "__main__":
    show_language_selection()