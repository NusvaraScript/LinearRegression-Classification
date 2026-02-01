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

    def preparation(self):
        pass

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
        pass

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

    def visual(self, df, title):
        pass

if __name__ == "__main__":
    root = tk.Tk
    app = AppGUI(root)
    root.mainloop()