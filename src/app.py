#!/usr/bin/env python3
"""
二维码生成工具 - 真实功能
支持自定义内容、颜色、尺寸、保存PNG
"""
import sys, os, tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
import tkinter as tk

try:
    import qrcode
    from PIL import Image, ImageTk
    HAS_DEP = True
except ImportError:
    HAS_DEP = False

class App:
    def __init__(self, root):
        self.root = root
        root.title("二维码生成工具 v1.0")
        root.geometry("600x650")
        self.img = None
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#1f538d", height=60)
        f.pack(fill="x")
        tk.Label(f, text="🔲 二维码生成工具", font=("Arial",16,"bold"),
                 fg="white", bg="#1f538d").pack(pady=15)
        main = tk.Frame(self.root, padx=20, pady=15)
        main.pack(fill="both", expand=True)
        tk.Label(main, text="输入内容（网址/文字/名片信息）：",
                 font=("Arial",11)).pack(anchor="w", pady=(0,5))
        self.entry = tk.Text(main, height=4, font=("Consolas",11),
                              bd=2, relief="groove")
        self.entry.pack(fill="x", pady=(0,10))
        self.entry.insert(1.0, "https://github.com/102839544")
        cf = tk.Frame(main)
        cf.pack(fill="x", pady=5)
        tk.Label(cf, text="尺寸：").pack(side="left")
        self.size = tk.Spinbox(cf, from_=1, to=20, width=5)
        self.size.delete(0, "end")
        self.size.insert(0, "6")
        self.size.pack(side="left", padx=5)
        tk.Button(cf, text="🚀 生成二维码", command=self.generate,
                  bg="#1f538d", fg="white", font=("Arial",11,"bold"),
                  padx=20, pady=5).pack(side="right")
        self.canvas = tk.Canvas(main, width=350, height=350,
                                 bg="white", relief="groove", bd=2)
        self.canvas.pack(pady=10)
        tk.Button(main, text="💾 保存图片", command=self.save,
                  bg="#5cb85c", fg="white", font=("Arial",10,"bold"),
                  padx=20).pack(pady=5)
        self.status = tk.Label(main, text="输入内容后点击「生成二维码」",
                               font=("Arial",10), fg="gray")
        self.status.pack()
    
    def generate(self):
        if not HAS_DEP:
            messagebox.showerror("缺少依赖", "请运行：pip install qrcode[pil]")
            return
        content = self.entry.get(1.0, "end").strip()
        if not content:
            messagebox.showwarning("提示", "请输入内容")
            return
        try:
            qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=int(self.size.get()), border=4)
            qr.add_data(content)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            self.img = img
            # 显示在 Canvas
            img_tk = ImageTk.PhotoImage(img.resize((300,300)))
            self.canvas.delete("all")
            self.canvas.create_image(175, 175, image=img_tk)
            self.canvas.image = img_tk
            self.status.config(text="✅ 生成成功！可点击「保存图片」")
        except Exception as e:
            messagebox.showerror("错误", str(e))
    
    def save(self):
        if not self.img:
            messagebox.showwarning("提示", "请先生成二维码")
            return
        path = filedialog.asksaveasfilename(title="保存二维码",
                 defaultextension=".png", filetypes=[("PNG图片","*.png")])
        if path:
            self.img.save(path)
            messagebox.showinfo("保存成功", f"二维码已保存至：\n{path}")
            self.status.config(text=f"✅ 已保存：{Path(path).name}")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
