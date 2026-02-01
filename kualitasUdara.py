import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import matplotlib.pyplot as plt
import seaborn as sns

class Backend:
    def __init__(self):
        self.df = None
        self.fitur = ['PM2_5','PM10','SO2','CO','NO2','Suhu','Kelembaban']
        self.label_map = {'Baik': 0, 'Sedang': 1, 'Tidak Sehat': 2, 'Berbahaya': 3}

    def load_csv(self):
        file_csv = filedialog.askopenfilenames()
        self.df = pd.read_csv(file_csv)
        return "\n" + "=" * 20 + f"\nData berhasil dimuat.\nJumlah data = {len(self.df)} baris\n" + "=" * 20 + "\n"

    def preprocessing(self):
        missing_val = self.df.isna().sum().sum()
        duplicated_val = self.df.duplicated().sum().sum()
        data = self.df.dropna()
        data = self.df.drop_duplicates()

        for col in self.fitur:
            Q1, Q3 = data[col].quantile(0.25), data[col].quantile(0.75)
            IQR = Q3 - Q1

            data = data[(data[col] >= Q1 - 1.5 * IQR) & (data[col] <= Q3 + 1.5 * IQR)]

        self.df_clean = data
        return "\n" + "=" * 20 + f"\nPreprocessing data selesai.\nJumlah data hilang = {missing_val}\nJumlah data duplikat = {duplicated_val}\nJumlah data setelah dibersihkan = {len.df_clean} baris\n" + "=" * 20 + "\n"

    def preparation(self):
        df_latih = self.df_clean.sample(frac=0.8, random_state=42)
        self.tes_df_mentah = self.df_clean.drop(df_latih.index)

        X_lth_mnth = df_latih[self.fitur].values
        self.X_min, self, X_max = X_lth_mnth.min(axis=0), X_lth_mnth.max(axis=0)

        self.X_train = (X_lth_mnth - self.X_min) / (self.X_max - self.X_min)
        self.X_test = (self.tes_df_mentah[self.fitur].values - self.X_min) / (self.X_max - self.X_min)
        self.y_train = df_latih['Kategori'].map(self.label_map).values
        self.y_test = self.tes_df_mentah['Kategori'].map(self.label_map).values

        return "\n" + "=" * 20 + '\nData Preprocessing Selesai: Split 80/20.\nNormalisasi Min-Max.\n' + '=' * 20 + '\n'

    def training(self):
        pass

    def predict(self):
        pass

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Program ML | Linear Regression Classification")
        self.root.geometry("1200x750")

        self.backend = Backend()
        self.widgets()

    def widgets(self):
        side = ttk.Frame(self.root, padding=15, width=320)
        side.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(side, text="Memproses Data.").pack(pady=(0,5))
        self.btn_load = ttk.Button(side, text="Load Dataset", command=self.appLoad)
        self.btn_load.pack(fill=tk.X, pady=2)
        self.btn_prep = ttk.Button(side, text="Preparation", command=self.appPrep)
        self.btn_prep.pack(fill=tk.X, pady=2)
        self.btn_proc = ttk.Button(side, text="Processing", command=self.appProc)
        self.btn_proc.pack(fill=tk.X, pady=2)
        self.btn_train = ttk.Button(side, text="Train", command=self.appTrain)
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

        self.btn_pred = ttk.Button(side, text="Prediksi Sekarang", command=self.appPred)
        self.btn_pred.pack(fill=tk.X, pady=(10, 2))

        self.log = scrolledtext.ScrolledText(side, width=35, height=10)
        self.log.pack(fill=tk.BOTH, expand=True, pady=10)

        self.main = ttk.Frame(self.root, padding=10)
        self.main.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.plot_area = ttk.Frame(self.main)
        self.plot_area.pack(fill=tk.BOTH, expand=True)

    def log(self, message):
        self.log.insert(tk.END, f"> {message}\n")
        self.log.see(tk.END)

    def reset(self):
        self.log.delete('1.0', tk.END)

    def appLoad(self):
        pass
    
    def appPrep(self):
        pass

    def appProc(self):
        pass

    def appTrain(self):
        pass

    def appPred(self):
        pass

    def visual(self, df, title):
        pass

if __name__ == "__main__":
    root = tk.Tk
    app = AppGUI(root)
    root.mainloop()