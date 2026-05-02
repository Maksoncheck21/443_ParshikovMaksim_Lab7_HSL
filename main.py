import os
import math
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk

def rgb_to_hsl(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin

    l = (cmax + cmin) / 2

    if delta == 0:
        s = 0
        h = 0
    else:
        s = delta / (1 - abs(2 * l - 1))
        if cmax == r:
            h = 60 * (((g - b) / delta) % 6)
        elif cmax == g:
            h = 60 * (((b - r) / delta) + 2)
        else:
            h = 60 * (((r - g) / delta) + 4)

    return h, s, l


def hsl_to_rgb(h, s, l):
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2

    if 0 <= h < 60:
        r_prime, g_prime, b_prime = c, x, 0
    elif 60 <= h < 120:
        r_prime, g_prime, b_prime = x, c, 0
    elif 120 <= h < 180:
        r_prime, g_prime, b_prime = 0, c, x
    elif 180 <= h < 240:
        r_prime, g_prime, b_prime = 0, x, c
    elif 240 <= h < 300:
        r_prime, g_prime, b_prime = x, 0, c
    else:
        r_prime, g_prime, b_prime = c, 0, x

    r = round((r_prime + m) * 255)
    g = round((g_prime + m) * 255)
    b = round((b_prime + m) * 255)
    return r, g, b


def process_folder(input_folder, output_folder, h_adj, s_adj, l_adj):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

    for filename in files:
        img = Image.open(os.path.join(input_folder, filename)).convert("RGB")
        pixels = img.load()
        width, height = img.size

        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                h, s, l = rgb_to_hsl(r, g, b)

                new_h = (h + h_adj) % 360
                new_s = max(0, min(1, s * (s_adj / 100)))
                new_l = max(0, min(1, l * (l_adj / 100)))

                pixels[x, y] = hsl_to_rgb(new_h, new_s, new_l)

        img.save(os.path.join(output_folder, f"processed_{filename}"))
    print(f"Обработка завершена. Файлов: {len(files)}")


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("HSL Batch Processor - Variant 16")

        self.h_slider = self.create_slider("Hue (0-360)", 0, 360)
        self.s_slider = self.create_slider("Saturation %", 0, 200, 100)
        self.l_slider = self.create_slider("Lightness %", 0, 200, 100)

        tk.Button(root, text="Выбрать папку и запустить", command=self.run).pack(pady=20)

    def create_slider(self, label, min_v, max_v, default=0):
        tk.Label(self.root, text=label).pack()
        s = tk.Scale(self.root, from_=min_v, to=max_v, orient=tk.HORIZONTAL, length=300)
        s.set(default)
        s.pack()
        return s

    def run(self):
        folder = filedialog.askdirectory(title="Выберите папку с изображениями")
        if folder:
            out_folder = os.path.join(folder, "output_hsl")
            process_folder(folder, out_folder, self.h_slider.get(), self.s_slider.get(), self.l_slider.get())
            tk.messagebox.showinfo("Готово", f"Изображения сохранены в:\n{out_folder}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()