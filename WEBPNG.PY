#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convertidor PNG ↔ WEBP
Desarrollado por Nicolás Aguirre nicolas-at-aguirrecastillo.com
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image

class ConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PNG ↔ WEBP Converter")
        self.geometry("620x450")
        self.resizable(False, False)

        # Variables
        self.files = []  # lista de rutas seleccionadas
        self.output_dir = tk.StringVar()
        self.quality = tk.IntVar(value=80)

        # --- FRAME PRINCIPAL ---
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill="both", expand=True)

        # --- Row 0: Agregar archivos & Listbox ---
        btn_add = ttk.Button(frm, text="Agregar archivos", command=self.choose_files)
        btn_add.grid(row=0, column=0, sticky="nw")

        self.lst_files = tk.Listbox(frm, height=10, width=60, selectmode=tk.EXTENDED)
        self.lst_files.grid(row=0, column=1, sticky="nsew", padx=(5,0))
        scrollbar = ttk.Scrollbar(frm, orient="vertical", command=self.lst_files.yview)
        scrollbar.grid(row=0, column=2, sticky="ns")
        self.lst_files.config(yscrollcommand=scrollbar.set)

        frm.columnconfigure(1, weight=1)
        frm.rowconfigure(0, weight=1)

        # --- Row 1: Eliminar seleccionados ---
        btn_remove = ttk.Button(frm, text="Eliminar seleccionados", command=self.remove_selected)
        btn_remove.grid(row=1, column=1, sticky="w", pady=(5,10))

        # --- Row 2: Carpeta de salida ---
        btn_out = ttk.Button(frm, text="Carpeta de salida", command=self.choose_output_dir)
        btn_out.grid(row=2, column=0, sticky="w")
        self.ent_out = ttk.Entry(frm, textvariable=self.output_dir, width=50)
        self.ent_out.grid(row=2, column=1, columnspan=2, sticky="we", padx=5, pady=5)

        # --- Row 3: Calidad WebP ---
        ttk.Label(frm, text="Calidad WebP:").grid(row=3, column=0, sticky="w")
        sld = ttk.Scale(frm, from_=0, to=100, orient="horizontal", variable=self.quality)
        sld.grid(row=3, column=1, sticky="we", padx=5)
        ttk.Label(frm, textvariable=self.quality).grid(row=3, column=2, sticky="w")

        # --- Row 4: Botones de conversión ---
        btn_to_webp = ttk.Button(frm, text="Convertir a .webp", command=self.convert_to_webp)
        btn_to_webp.grid(row=4, column=0, pady=15)
        btn_to_png  = ttk.Button(frm, text="Convertir a .png",  command=self.convert_to_png)
        btn_to_png.grid(row=4, column=1, sticky="w", pady=15)

        # --- Status bar & Copyright ---
        self.status = ttk.Label(self, text="", anchor="w")
        self.status.pack(side="bottom", fill="x", pady=5, padx=10)
        lbl_copy = ttk.Label(self,
            text="Desarrollado por Nicolás Aguirre nicolas-at-aguirrecastillo.com",
            font=("Arial", 8), foreground="gray")
        lbl_copy.pack(side="bottom", pady=2)

    def choose_files(self):
        """Permite agregar múltiples archivos PNG o WEBP a la lista, sin duplicados."""
        paths = filedialog.askopenfilenames(
            title="Selecciona imágenes PNG o WebP",
            filetypes=[
                ("Imágenes (PNG, WebP)", ("*.png", "*.webp")),
                ("Solo PNG", "*.png"),
                ("Solo WebP", "*.webp"),
                ("Todos los archivos", "*.*"),
            ]
        )
        if not paths:
            return
        added = 0
        for p in paths:
            if p not in self.files:
                self.files.append(p)
                self.lst_files.insert(tk.END, p)
                added += 1
        if added:
            self.status.config(text=f"Se agregaron {added} archivo(s).")
        else:
            self.status.config(text="No se agregaron archivos nuevos.")

    def remove_selected(self):
        """Elimina de la lista los archivos seleccionados en el Listbox."""
        sel = list(self.lst_files.curselection())
        if not sel:
            return
        for idx in reversed(sel):
            path = self.lst_files.get(idx)
            if path in self.files:
                self.files.remove(path)
            self.lst_files.delete(idx)
        self.status.config(text=f"Eliminados {len(sel)} archivo(s).")

    def choose_output_dir(self):
        d = filedialog.askdirectory(title="Selecciona carpeta de salida")
        if d:
            self.output_dir.set(d)

    def convert_to_webp(self):
        if not self._check_params(".png"):
            return
        self._batch_convert(".webp", {"format": "WEBP", "quality": self.quality.get()})

    def convert_to_png(self):
        if not self._check_params(".webp"):
            return
        self._batch_convert(".png", {"format": "PNG", "optimize": True, "compress_level": 6})

    def _check_params(self, required_ext):
        if not self.files:
            messagebox.showwarning("Atención", "No has seleccionado archivos.")
            return False
        if not self.output_dir.get():
            messagebox.showwarning("Atención", "No has definido carpeta de salida.")
            return False
        bad = [f for f in self.files if not f.lower().endswith(required_ext)]
        if bad:
            messagebox.showerror("Error", f"Estos no son {required_ext}: {bad}")
            return False
        return True

    def _batch_convert(self, target_ext, save_kwargs):
        outdir = self.output_dir.get()
        total = len(self.files)
        for idx, filepath in enumerate(self.files, start=1):
            try:
                img = Image.open(filepath)
                base = os.path.splitext(os.path.basename(filepath))[0]
                outpath = os.path.join(outdir, base + target_ext)
                img.save(outpath, **save_kwargs)
                self.status.config(text=f"Convertido {idx}/{total}: {outpath}")
                self.update_idletasks()
            except Exception as e:
                messagebox.showerror("Error",
                    f"No se pudo convertir:\n{filepath}\n{e}")
                break
        else:
            messagebox.showinfo("Listo", "¡Todas las conversiones han terminado!")

if __name__ == "__main__":
    try:
        from PIL import Image
    except ImportError:
        messagebox.showerror("Dependencia faltante",
            "Necesitas instalar Pillow:\n\npip install pillow")
        sys.exit(1)

    app = ConverterApp()
    app.mainloop()
