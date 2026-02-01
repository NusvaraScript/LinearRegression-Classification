import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import matplotlib.pyplot as plt

class Backend:
    def __init__(self):
        self.df = None
        self.df_clean = None
        self.X_train, self.X_test = None, None
        self.y_train, self.y_test = None, None
        self.tes_df_mentah = None
        self.X_min, self.X_max = None, None
        self.fitur = ['PM2_5','PM10','SO2','CO','NO2','Suhu','Kelembaban']
        self.label_map = {'Baik': 0, 'Sedang': 1, 'Tidak Sehat': 2, 'Berbahaya': 3}

    def load_csv(self, file_csv):
        self.df = pd.read_csv(file_csv)
        return "\n" + "=" * 30 + f"\n>>> Data berhasil dimuat.\n>>> Jumlah data = {len(self.df)} baris\n" + "=" * 30 + "\n"

    def preparation(self):
        missing_val = self.df.isna().sum().sum()
        duplicated_val = self.df.duplicated().sum().sum()
        data = self.df.dropna()
        data = self.df.drop_duplicates()

        for col in self.fitur:
            Q1, Q3 = data[col].quantile(0.25), data[col].quantile(0.75)
            IQR = Q3 - Q1

            data = data[(data[col] >= Q1 - 1.5 * IQR) & (data[col] <= Q3 + 1.5 * IQR)]

        self.df_clean = data
        return "\n" + "=" * 30 + f"\n>>> Data Preparation selesai.\n>>> Jumlah data hilang = {missing_val}\n>>> Jumlah data duplikat = {duplicated_val}\n>>> Jumlah data setelah dibersihkan = {len(self.df_clean)} baris\n" + "=" * 30 + "\n"

    def preprocessing(self):
        df_latih = self.df_clean.sample(frac=0.8, random_state=42)
        self.tes_df_mentah = self.df_clean.drop(df_latih.index)

        X_lth_mnth = df_latih[self.fitur].values
        self.X_min, self, X_max = X_lth_mnth.min(axis=0), X_lth_mnth.max(axis=0)

        self.X_train = (X_lth_mnth - self.X_min) / (self.X_max - self.X_min)
        self.X_test = (self.tes_df_mentah[self.fitur].values - self.X_min) / (self.X_max - self.X_min)
        self.y_train = df_latih['Kategori'].map(self.label_map).values
        self.y_test = self.tes_df_mentah['Kategori'].map(self.label_map).values

        return "\n" + "=" * 30 + '\n>>> Data Preprocessing Selesai: Split 80/20.\n>>> Normalisasi Min-Max.\n' + '=' * 30 + '\n'

    def training(self):
        pass

    def predict(self):
        pass

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Program ML | Linear Regression Classification")
        self.root.geometry("700x425")

        self.backend = Backend()
        self.widgets()

    def widgets(self):
        side = ttk.Frame(self.root, padding=15, width=320)
        side.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(side, text="Memproses Data.").pack(pady=(0,5))
        self.btn_load = ttk.Button(side, text="Load Dataset", command=self.appLoad)
        self.btn_load.pack(fill=tk.X, pady=2)
        self.btn_prep = ttk.Button(side, text="Preparation", state="disabled", command=self.appPrep)
        self.btn_prep.pack(fill=tk.X, pady=2)
        self.btn_proc = ttk.Button(side, text="Processing", state="disabled", command=self.appProc)
        self.btn_proc.pack(fill=tk.X, pady=2)
        self.btn_train = ttk.Button(side, text="Train", state="disabled", command=self.appTrain)
        self.btn_train.pack(fill=tk.X, pady=2)

        ttk.Separator(side, orient="horizontal").pack(fill=tk.X, pady=15)

        ttk.Label(side, text="Test Data Baru").pack(pady=(0, 5))
        self.entry = {}
        for f in self.backend.fitur:
            f_frame = ttk.Frame(side)
            f_frame.pack(fill=tk.X)
            ttk.Label(f_frame, text=f).pack(side=tk.LEFT)
            ent = ttk.Entry(f_frame, width=15)
            ent.pack(side=tk.RIGHT, pady=1)
            self.entry = ent

        self.btn_pred = ttk.Button(side, text="Prediksi Sekarang", state="disabled", command=self.appPred)
        self.btn_pred.pack(fill=tk.X, pady=(10, 2))

        main = ttk.Frame(self.root, padding=10)
        main.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.log = scrolledtext.ScrolledText(main, width=35, height=10)
        self.log.pack(fill=tk.BOTH, expand=True, pady=10)

        self.btn_reset = ttk.Button(main, text="Reset Log", command=self.reset)
        self.btn_reset.pack(fill=tk.BOTH, pady=10)

    def log_text(self, message):
        self.log.insert(tk.END, f"{message}\n")
        self.log.see(tk.END)

    def reset(self):
        self.log.delete('1.0', tk.END)

    def appLoad(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if path:
            self.log_text(self.backend.load_csv(path))
            self.btn_prep.config(state='normal')
            self.visual(self.backend.df, "Data Asli")
        else:
            messagebox.showerror("Gagal", "Gagal memuat data.")
    
    def appPrep(self):
        self.log_text(self.backend.preparation())
        self.btn_proc.config(state='normal')

    def appProc(self):
        self.log_text(self.backend.preprocessing())
        self.btn_train.config(state='normal')

    def appTrain(self):
        self.log_text(self.backend.training())
        messagebox.showinfo("Sukses", "Model siap di gunakan!")
        self.btn_pred.config(state='normal')

    def appPred(self):
        try:
            vals = [float(self.entry[f].get()) for f in self.backend.fitur]
            res = self.backend.predict(vals)

            self.log_text(f">>> Hasil Prediksi Kualitas Udara = {res}")
            messagebox.showinfo("Hasil Prediksi", f"Kualitas Udara = {res}")
        except ValueError:
            self.log_text(">>> Input tidak valid!")
            messagebox.showerror("Error", "Input tidak valid!")

    def visual(self, df, title):
        fig, ax = plt.subplots(figsize=(7,4))

        for col in self.backend.fitur:
            ax.scatter(range(len(df)), df[col], s=10, alpha=0.5)

        ax.set_title(title)
        ax.set_xlabel("Data Index")
        ax.set_ylabel("Value")

        fig.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()