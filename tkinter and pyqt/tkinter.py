import math
import tkinter as tk
from tkinter import messagebox, ttk


class App:
    U = ["celsius", "fahrenheit", "kelvin"]

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("temperature converter (tkinter)")
        self.root.geometry("350x250")

        tk.Label(self.root, text="enter temperature:", font=("Arial", 12)).grid(
            row=0, column=0, columnspan=2, pady=10)

        self.e = tk.Entry(self.root, width=15)
        self.e.grid(row=1, column=0, columnspan=2, pady=5)
        self.e.bind("<Return>", lambda ev: self.go())

        self.a = ttk.Combobox(self.root, values=self.U, state="readonly", width=12)
        self.a.set("celsius")
        self.a.grid(row=2, column=0, pady=10, padx=10)

        self.b = ttk.Combobox(self.root, values=self.U, state="readonly", width=12)
        self.b.set("fahrenheit")
        self.b.grid(row=2, column=1, pady=10, padx=10)

        tk.Button(self.root, text="convert", command=self.go, bg="#4CAF50", fg="white").grid(
            row=3, column=0, pady=15)
        tk.Button(self.root, text="swap", command=self.swap).grid(row=3, column=1, pady=15)

        self.r = tk.Label(self.root, text="result: ", font=("Arial", 12, "bold"))
        self.r.grid(row=4, column=0, columnspan=2)

    def to_c(self, v, u):
        if u == "fahrenheit":
            return (v - 32) * 5 / 9
        if u == "kelvin":
            return v - 273.15
        return v

    def from_c(self, v, u):
        if u == "fahrenheit":
            return v * 9 / 5 + 32
        if u == "kelvin":
            return v + 273.15
        return v

    def swap(self):
        a, b = self.a.get(), self.b.get()
        self.a.set(b)
        self.b.set(a)

    def go(self):
        try:
            v = float(self.e.get().replace(",", "."))
            if not math.isfinite(v):
                raise ValueError
        except ValueError:
            messagebox.showerror("input error", "enter a correct number")
            return

        c = self.to_c(v, self.a.get())
        if c < -273.15:
            messagebox.showerror("input error", "below absolute zero")
            return

        self.r.config(text=f"result: {self.from_c(c, self.b.get()):.2f} {self.b.get()}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
