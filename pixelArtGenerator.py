import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk


class PixelArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Générateur de Pixel Art")

        self.style = ttk.Style()
        self.style.configure('My.TFrame', background='#333333')

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.create_color_average_tab()
        self.create_8bit_tab()

    def create_color_average_tab(self):
        color_average_tab = ttk.Frame(self.notebook, style='My.TFrame')  # Utilisez le style 'My.TFrame'
        self.notebook.add(color_average_tab, text="Couleurs normales")

        load_button = tk.Button(color_average_tab, text="Charger une image", command=self.load_file_color_average)
        load_button.pack(pady=10)

        self.fig_color_average, self.ax_color_average = plt.subplots()
        self.ax_color_average.axis("off")
        self.canvas_color_average = FigureCanvasTkAgg(self.fig_color_average, master=color_average_tab)
        self.canvas_color_average.get_tk_widget().pack()

        pixel_entry_label = tk.Label(color_average_tab, text="Pixels Par Ligne:")
        pixel_entry_label.pack()
        self.pixel_entry_color_average = tk.Entry(color_average_tab, textvariable=tk.IntVar(value=10))
        self.pixel_entry_color_average.pack()

        convert_button = tk.Button(color_average_tab, text="Convertir", command=self.update_image_color_average)
        convert_button.pack(pady=10)

        download_button = tk.Button(color_average_tab, text="Télécharger", command=self.save_image_color_average)
        download_button.pack(pady=10)

        self.root.configure(bg='#333333')
        load_button.configure(bg='#555555', fg='white')
        pixel_entry_label.configure(bg='#333333', fg='white')
        self.pixel_entry_color_average.configure(bg='#555555', fg='white')
        convert_button.configure(bg='#555555', fg='white')
        download_button.configure(bg='#555555', fg='white')

    def create_8bit_tab(self):
        bit8_tab = ttk.Frame(self.notebook, style='My.TFrame')
        self.notebook.add(bit8_tab, text="8-bit")

        load_button = tk.Button(bit8_tab, text="Charger une image", command=self.load_file_8bit)
        load_button.pack(pady=10)

        self.fig_8bit, self.ax_8bit = plt.subplots()
        self.ax_8bit.axis("off")
        self.canvas_8bit = FigureCanvasTkAgg(self.fig_8bit, master=bit8_tab)
        self.canvas_8bit.get_tk_widget().pack()

        pixel_entry_label = tk.Label(bit8_tab, text="Pixels Par Ligne:")
        pixel_entry_label.pack()
        self.pixel_entry_8bit = tk.Entry(bit8_tab, textvariable=tk.IntVar(value=10))
        self.pixel_entry_8bit.pack()

        convert_button = tk.Button(bit8_tab, text="Convertir", command=self.convert_image_8bit)
        convert_button.pack(pady=10)

        reset_button = tk.Button(bit8_tab, text="Réinitialiser", command=self.reset_image_8bit)
        reset_button.pack(pady=10)

        download_button = tk.Button(bit8_tab, text="Télécharger", command=self.save_image_8bit)
        download_button.pack(pady=10)

        self.root.configure(bg='#333333')
        load_button.configure(bg='#555555', fg='white')
        pixel_entry_label.configure(bg='#333333', fg='white')
        self.pixel_entry_8bit.configure(bg='#555555', fg='white')
        convert_button.configure(bg='#555555', fg='white')
        reset_button.configure(bg='#555555', fg='white')
        download_button.configure(bg='#555555', fg='white')

    def load_file_color_average(self):
        file_path = filedialog.askopenfilename(title="Sélectionner une image",
                                               filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_color_average = plt.imread(file_path)
            self.show_image_color_average()

    def show_image_color_average(self):
        if hasattr(self, 'image_color_average'):
            self.ax_color_average.clear()
            self.ax_color_average.imshow(self.image_color_average)
            self.ax_color_average.axis("off")
            self.canvas_color_average.draw()

    def update_image_color_average(self):
        if hasattr(self, 'image_color_average'):
            height, width, _ = self.image_color_average.shape

            max_pixel_size = min(height, width)

            pixel_per_line = int(self.pixel_entry_color_average.get())

            if pixel_per_line == 0:
                messagebox.showerror("Erreur",
                                     "Veuillez entrer une valeur supérieure à zéro pour les pixels par ligne.")
                return

            if pixel_per_line > max_pixel_size:
                messagebox.showerror("Erreur",
                                     "Le nombre de pixels par ligne ne peut pas dépasser les dimensions de l'image.")
                return

            pixel_size_x = width // pixel_per_line
            pixel_size_y = height // pixel_per_line

            pixelated_image = np.zeros_like(self.image_color_average)
            for i in range(0, height, pixel_size_y):
                for j in range(0, width, pixel_size_x):
                    block = self.image_color_average[i:i + pixel_size_y, j:j + pixel_size_x, :]
                    average_color = np.mean(block, axis=(0, 1))
                    pixelated_image[i:i + pixel_size_y, j:j + pixel_size_x, :] = average_color

            self.ax_color_average.clear()
            self.ax_color_average.imshow(pixelated_image)
            self.ax_color_average.axis("off")
            self.canvas_color_average.draw()

    def save_image_color_average(self):
        if hasattr(self, 'image_color_average'):
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                plt.imsave(file_path, self.ax_color_average.images[0].get_array())

    def load_file_8bit(self):
        file_path = filedialog.askopenfilename(title="Sélectionner une image",
                                               filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.original_image_8bit = Image.open(file_path)
            self.image_8bit = self.original_image_8bit.copy()
            self.show_image_8bit()

    def show_image_8bit(self):
        if hasattr(self, 'image_8bit'):
            img = ImageTk.PhotoImage(self.image_8bit)
            self.ax_8bit.clear()
            self.canvas_8bit.image = img
            self.ax_8bit.imshow(self.image_8bit)
            self.ax_8bit.axis("off")

            self.canvas_8bit.draw()

    def convert_image_8bit(self):
        if hasattr(self, 'original_image_8bit'):
            pixel_per_line = int(self.pixel_entry_8bit.get())

            if pixel_per_line == 0:
                messagebox.showerror("Erreur",
                                     "Veuillez entrer une valeur supérieure à zéro pour les pixels par ligne.")
                return

            width, height = self.original_image_8bit.size

            pixel_size_x = width // pixel_per_line
            pixel_size_y = height // pixel_per_line

            original_array = np.array(self.original_image_8bit)

            pixelated_array = np.zeros_like(original_array)
            for i in range(0, height, pixel_size_y):
                for j in range(0, width, pixel_size_x):
                    block = original_array[i:i + pixel_size_y, j:j + pixel_size_x, :]

                    average_color = np.median(block, axis=(0, 1))
                    pixelated_array[i:i + pixel_size_y, j:j + pixel_size_x, :] = average_color

                    quantized_array = (block // 32) * 32
                    pixelated_array[i:i + pixel_size_y, j:j + pixel_size_x, :] = np.median(quantized_array, axis=(0, 1))

            pixelated_image = Image.fromarray(pixelated_array.astype('uint8'))

            self.image_8bit = pixelated_image
            self.show_image_8bit()

    def reset_image_8bit(self):
        if hasattr(self, 'original_image_8bit'):
            self.image_8bit = self.original_image_8bit.copy()
            self.show_image_8bit()

    def save_image_8bit(self):
        if hasattr(self, 'image_8bit'):
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.image_8bit.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = PixelArtApp(root)
    root.mainloop()
