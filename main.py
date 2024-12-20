import os
import sys
import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
from ttkbootstrap import Style
import qrcode
from PIL import Image, ImageTk

# Función para manejar rutas de recursos
def resource_path(relative_path):
    """Obtiene la ruta absoluta para los recursos, compatible con PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class QRCodeGeneratorApp:
    def __init__(self, root):
        # Estilo con ttkbootstrap
        self.style = Style(theme="darkly")
        self.root = root
        self.root.title("Generador de código QR | by @marichu_kt | © 2024")

        # Cambiar el icono de la ventana
        logo_path = resource_path("logo.ico")  # Ruta al archivo de icono
        self.root.iconbitmap(logo_path)

        # Configurar tamaño y posición de la ventana
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 500
        window_height = 600
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.resizable(False, False)

        # Colores predeterminados del QR
        self.qr_color = "black"
        self.bg_color = "white"

        self.setup_ui()

    def setup_ui(self):
        # Título
        self.title_label = tk.Label(
            self.root, 
            text="Generador QR", 
            font=("Courier new", 24, "bold"), 
            bg=self.style.colors.bg, 
            fg=self.style.colors.primary
        )
        self.title_label.pack(pady=10)

        # Frame para texto/URL
        text_frame = tk.Frame(self.root, bg=self.style.colors.bg)
        text_frame.pack(pady=5)
        self.text_label = tk.Label(
            text_frame, 
            text="Texto/URL:", 
            font=("Courier new", 16, "bold"), 
            bg=self.style.colors.bg, 
            fg=self.style.colors.light
        )
        self.text_label.grid(row=0, column=0, padx=5)
        self.text_entry = tk.Entry(
            text_frame, 
            font=("Helvetica", 14), 
            width=30, 
            relief="solid"
        )
        self.text_entry.grid(row=0, column=1, padx=5)

        # Frame para botones
        button_frame = tk.Frame(self.root, bg=self.style.colors.bg)
        button_frame.pack(pady=10)

        # Botón con imagen para cambiar tema
        theme_icon_path = resource_path("theme.ico")  # Ruta al archivo .ico
        theme_image = ImageTk.PhotoImage(Image.open(theme_icon_path).resize((27, 27)))
        self.theme_button = tk.Button(
            button_frame, 
            image=theme_image, 
            command=self.toggle_theme, 
            bg=self.style.colors.bg, 
            borderwidth=0, 
            activebackground=self.style.colors.bg
        )
        self.theme_button.image = theme_image  # Necesario para evitar que la imagen sea recolectada por el garbage collector
        self.theme_button.pack(side=tk.LEFT, padx=5)

        # Color del QR
        self.color_button = tk.Button(
            button_frame, 
            text="Color del QR", 
            command=self.choose_qr_color, 
            font=("Helvetica", 12, "bold"), 
            bg=self.style.colors.primary, 
            fg="white", 
            activebackground=self.style.colors.info, 
            relief="solid"
        )
        self.color_button.pack(side=tk.LEFT, padx=5)
        self.bg_button = tk.Button(
            button_frame, 
            text="Color de fondo", 
            command=self.choose_bg_color, 
            font=("Helvetica", 12, "bold"), 
            bg=self.style.colors.primary, 
            fg="white", 
            activebackground=self.style.colors.info, 
            relief="solid"
        )
        self.bg_button.pack(side=tk.LEFT, padx=5)
        self.generate_button = tk.Button(
            button_frame, 
            text="Generar QR", 
            command=self.generate_qr, 
            font=("Helvetica", 12, "bold"), 
            bg=self.style.colors.primary, 
            fg="white", 
            activebackground=self.style.colors.info, 
            relief="solid"
        )
        self.generate_button.pack(side=tk.LEFT, padx=5)

        # Canvas para mostrar el QR
        self.qr_canvas = tk.Canvas(
            self.root, 
            width=300, 
            height=300, 
            bg=self.style.colors.dark, 
            highlightthickness=0
        )
        self.qr_canvas.pack(pady=15)

        # Botón Guardar
        self.save_button = tk.Button(
            self.root, 
            text="Guardar Código QR", 
            command=self.save_qr, 
            font=("Helvetica", 12, "bold"), 
            bg=self.style.colors.success, 
            fg="white", 
            activebackground=self.style.colors.info, 
            relief="solid"
        )
        self.save_button.pack(pady=2)

        # Créditos
        self.credit_label = tk.Label(
            self.root, 
            text="by @marichu_kt | © 2024", 
            font=("Helvetica", 10), 
            bg=self.style.colors.bg, 
            fg=self.style.colors.light
        )
        self.credit_label.pack(side=tk.BOTTOM, pady=2)

    def toggle_theme(self):
        current_theme = self.style.theme_use()
        if current_theme == "darkly":
            self.style.theme_use("flatly")
        else:
            self.style.theme_use("darkly")

    def choose_qr_color(self):
        color = colorchooser.askcolor(title="Seleccionar color del código QR")
        if color[1]:
            self.qr_color = color[1]

    def choose_bg_color(self):
        color = colorchooser.askcolor(title="Seleccionar color de fondo del QR")
        if color[1]:
            self.bg_color = color[1]

    def generate_qr(self):
        content = self.text_entry.get()
        if not content:
            messagebox.showwarning("Advertencia", "Por favor, introduce un texto o URL.")
            return
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(content)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color=self.qr_color, back_color=self.bg_color)
            qr_img = qr_img.resize((300, 300))
            self.qr_image = ImageTk.PhotoImage(qr_img)
            self.qr_canvas.create_image(150, 150, image=self.qr_image)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el código QR. {e}")

    def save_qr(self):
        if not hasattr(self, "qr_image"):
            messagebox.showwarning("Advertencia", "Por favor, genera un código QR primero.")
            return
        try:
            content = self.text_entry.get()
            filetypes = [("PNG", "*.png"), ("JPEG", "*.jpeg"), ("JPEG", "*.jpg")]
            filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=filetypes)
            if filename:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=10,
                    border=4,
                )
                qr.add_data(content)
                qr.make(fit=True)
                qr_img = qr.make_image(fill_color=self.qr_color, back_color=self.bg_color)
                qr_img.save(filename)
                messagebox.showinfo("Éxito", f"Código QR guardado como '{filename}'.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el código QR. {e}")

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGeneratorApp(root)
    root.mainloop()
