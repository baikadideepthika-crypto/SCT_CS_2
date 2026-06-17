import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

def xor_pixels(image, key):
    img = image.convert("RGB")
    pixels = list(img.getdata())
    new_pixels = [(r ^ key, g ^ key, b ^ key) for r, g, b in pixels]
    new_img = Image.new("RGB", img.size)
    new_img.putdata(new_pixels)
    return new_img

def swap_pixels(image):
    img = image.convert("RGB")
    pixels = list(img.getdata())
    for i in range(0, len(pixels) - 1, 2):
        pixels[i], pixels[i + 1] = pixels[i + 1], pixels[i]
    new_img = Image.new("RGB", img.size)
    new_img.putdata(pixels)
    return new_img

class ImageEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption Tool - SkillCraft Technology")
        self.root.state("zoomed")
        self.root.configure(bg="#1e1e2e")

        self.original_image = None
        self.processed_image = None
        self.input_path = None
        self.PREVIEW_SIZE = (500, 400)

        self._build_ui()

    def _build_ui(self):
        # Title
        tk.Label(self.root, text="🔐 Image Encryption Tool",
                 font=("Courier New", 20, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(pady=10)

        tk.Label(self.root, text="SkillCraft Technology — Cyber Security Internship",
                 font=("Courier New", 10), bg="#1e1e2e", fg="#6c7086").pack()

        # Preview frame
        preview_frame = tk.Frame(self.root, bg="#1e1e2e")
        preview_frame.pack(pady=15)

        # Original canvas
        orig_frame = tk.Frame(preview_frame, bg="#313244", bd=2, relief="ridge")
        orig_frame.grid(row=0, column=0, padx=30)
        tk.Label(orig_frame, text="Original Image", font=("Courier New", 11, "bold"),
                 bg="#313244", fg="#a6e3a1").pack(pady=6)
        self.orig_canvas = tk.Canvas(orig_frame, width=500, height=400,
                                     bg="#1e1e2e", highlightthickness=0)
        self.orig_canvas.pack(padx=10, pady=8)

        # Arrow
        tk.Label(preview_frame, text="→", font=("Courier New", 30, "bold"),
                 bg="#1e1e2e", fg="#f38ba8").grid(row=0, column=1, padx=20)

        # Processed canvas
        proc_frame = tk.Frame(preview_frame, bg="#313244", bd=2, relief="ridge")
        proc_frame.grid(row=0, column=2, padx=30)
        tk.Label(proc_frame, text="Processed Image", font=("Courier New", 11, "bold"),
                 bg="#313244", fg="#f38ba8").pack(pady=6)
        self.proc_canvas = tk.Canvas(proc_frame, width=500, height=400,
                                     bg="#1e1e2e", highlightthickness=0)
        self.proc_canvas.pack(padx=10, pady=8)

        # Controls
        ctrl_frame = tk.Frame(self.root, bg="#1e1e2e")
        ctrl_frame.pack(pady=10)

        tk.Label(ctrl_frame, text="Encryption Key (0–255):",
                 font=("Courier New", 12), bg="#1e1e2e", fg="#cdd6f4").grid(
            row=0, column=0, padx=10, sticky="e")
        self.key_entry = tk.Entry(ctrl_frame, font=("Courier New", 12),
                                  bg="#313244", fg="#cdd6f4",
                                  insertbackground="#cdd6f4", width=6, justify="center")
        self.key_entry.insert(0, "42")
        self.key_entry.grid(row=0, column=1, padx=10)

        tk.Label(ctrl_frame, text="Operation:",
                 font=("Courier New", 12), bg="#1e1e2e", fg="#cdd6f4").grid(
            row=0, column=2, padx=10, sticky="e")
        self.op_var = tk.StringVar(value="XOR")
        op_menu = tk.OptionMenu(ctrl_frame, self.op_var, "XOR", "Swap Pixels", "XOR + Swap")
        op_menu.config(font=("Courier New", 11), bg="#313244", fg="#cdd6f4",
                       activebackground="#45475a", width=14)
        op_menu["menu"].config(bg="#313244", fg="#cdd6f4")
        op_menu.grid(row=0, column=3, padx=10)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(pady=12)

        buttons = [
            ("📂 Open Image",  "#89b4fa", self.open_image),
            ("🔒 Encrypt",     "#a6e3a1", self.encrypt_image),
            ("🔓 Decrypt",     "#fab387", self.decrypt_image),
            ("💾 Save Result", "#cba6f7", self.save_image),
        ]
        for text, color, cmd in buttons:
            tk.Button(btn_frame, text=text, command=cmd,
                      font=("Courier New", 12, "bold"),
                      bg=color, fg="#1e1e2e", activebackground=color,
                      relief="flat", padx=18, pady=8, cursor="hand2").pack(side="left", padx=10)

        # Status
        self.status_var = tk.StringVar(value="Ready — Open an image to begin.")
        tk.Label(self.root, textvariable=self.status_var,
                 font=("Courier New", 10), bg="#181825", fg="#a6adc8",
                 anchor="w", padx=10).pack(fill="x", side="bottom", ipady=5)

    def _get_key(self):
        try:
            key = int(self.key_entry.get())
            if not (0 <= key <= 255):
                raise ValueError
            return key
        except ValueError:
            messagebox.showerror("Invalid Key", "Enter a number between 0 and 255.")
            return None

    def _show_on_canvas(self, image, canvas):
        preview = image.copy()
        preview.thumbnail(self.PREVIEW_SIZE, Image.LANCZOS)
        photo = ImageTk.PhotoImage(preview)
        canvas.image = photo
        # Center on canvas
        x = self.PREVIEW_SIZE[0] // 2
        y = self.PREVIEW_SIZE[1] // 2
        canvas.delete("all")
        canvas.create_image(x, y, anchor="center", image=photo)

    def _apply_operation(self, image, key):
        op = self.op_var.get()
        if op == "XOR":
            return xor_pixels(image, key)
        elif op == "Swap Pixels":
            return swap_pixels(image)
        else:
            return swap_pixels(xor_pixels(image, key))

    def open_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp"), ("All Files", "*.*")])
        if not path:
            return
        self.input_path = path
        self.original_image = Image.open(path)
        self.processed_image = None
        self._show_on_canvas(self.original_image, self.orig_canvas)
        self.proc_canvas.delete("all")
        self.status_var.set(f"Loaded: {os.path.basename(path)}  |  Size: {self.original_image.size}")

    def encrypt_image(self):
        if not self.original_image:
            messagebox.showwarning("No Image", "Please open an image first.")
            return
        key = self._get_key()
        if key is None:
            return
        self.processed_image = self._apply_operation(self.original_image, key)
        self._show_on_canvas(self.processed_image, self.proc_canvas)
        self.status_var.set(f"✅ Encrypted using {self.op_var.get()} with key={key}. Save the result!")

    def decrypt_image(self):
        if not self.processed_image:
            messagebox.showwarning("No Image", "Please encrypt an image first.")
            return
        key = self._get_key()
        if key is None:
            return
        decrypted = self._apply_operation(self.processed_image, key)
        self._show_on_canvas(decrypted, self.proc_canvas)
        self.processed_image = decrypted
        self.status_var.set(f"✅ Decrypted using {self.op_var.get()} with key={key}.")

    def save_image(self):
        if not self.processed_image:
            messagebox.showwarning("Nothing to Save", "No processed image to save.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All Files", "*.*")])
        if path:
            self.processed_image.save(path)
            self.status_var.set(f"💾 Saved to: {os.path.basename(path)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptionApp(root)
    root.mainloop()
