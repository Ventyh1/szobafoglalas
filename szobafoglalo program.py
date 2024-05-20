from abc import ABC, abstractmethod
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

    @abstractmethod
    def __str__(self):
        pass

class EgyAgyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 17000)

    def __str__(self):
        return f"Egyágyas Szoba - Szobaszám: {self.szobaszam}, Ár: {self.ar} Ft/éj, Reggeli"

class KetAgyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 24000)

    def __str__(self):
        return f"Kétágyas Szoba - Szobaszám: {self.szobaszam}, Ár: {self.ar} Ft/éj, Reggeli, Ebéd, Vacsora"

class KetPluszEgyAgyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 31000)

    def __str__(self):
        return f"2+1 ágyas Szoba - Szobaszám: {self.szobaszam}, Ár: {self.ar} Ft/éj, Reggeli, Ebéd, Vacsora, Wellness használat"

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def hozzaad_szoba(self, szoba):
        self.szobak.append(szoba)

    def __str__(self):
        return f"Szálloda neve: {self.nev}, Szobák száma: {len(self.szobak)}"

class Foglalas:
    def __init__(self, szoba, kezdo_datum, veg_datum):
        self.szoba = szoba
        self.kezdo_datum = kezdo_datum
        self.veg_datum = veg_datum

    def __str__(self):
        return f"Foglalás - Szobaszám: {self.szoba.szobaszam}, {self.kezdo_datum}-tól {self.veg_datum}-ig, Ár: {self.ar_szamolas()} Ft"

    def ar_szamolas(self):
        kezdo_datum_obj = datetime.strptime(self.kezdo_datum, "%Y-%m-%d")
        veg_datum_obj = datetime.strptime(self.veg_datum, "%Y-%m-%d")
        ejszakak = (veg_datum_obj - kezdo_datum_obj).days
        return self.szoba.ar * ejszakak

class FoglalasiRendszer:
    def __init__(self):
        self.szalloda = None
        self.foglalasok = []

    def letrehoz_szalloda(self, nev):
        self.szalloda = Szalloda(nev)

    def hozzaad_szoba(self, szoba):
        if self.szalloda:
            self.szalloda.hozzaad_szoba(szoba)

    def foglalas(self, szobaszam, kezdo_datum, veg_datum):
        if not self.szalloda:
            return "Nincs szálloda létrehozva."

        kezdo_datum_obj = datetime.strptime(kezdo_datum, "%Y-%m-%d")
        veg_datum_obj = datetime.strptime(veg_datum, "%Y-%m-%d")

        if kezdo_datum_obj >= veg_datum_obj:
            return "A kezdő dátumnak korábbinak kell lennie, mint a záró dátumnak."

        for foglalas in self.foglalasok:
            foglalas_kezdo_datum = datetime.strptime(foglalas.kezdo_datum, "%Y-%m-%d")
            foglalas_veg_datum = datetime.strptime(foglalas.veg_datum, "%Y-%m-%d")
            if foglalas.szoba.szobaszam == szobaszam:
                if not (veg_datum_obj <= foglalas_kezdo_datum or kezdo_datum_obj >= foglalas_veg_datum):
                    return "A szoba már foglalt ezen a dátumtartományon belül."

        for szoba in self.szalloda.szobak:
            if szoba.szobaszam == szobaszam:
                uj_foglalas = Foglalas(szoba, kezdo_datum, veg_datum)
                self.foglalasok.append(uj_foglalas)
                return f"Foglalás sikeres: {uj_foglalas}, Ár: {uj_foglalas.ar_szamolas()} Ft"

        return "Nincs ilyen szobaszám."

    def lemondas(self, szobaszam, kezdo_datum, veg_datum):
        for foglalas in self.foglalasok:
            if (foglalas.szoba.szobaszam == szobaszam and
                foglalas.kezdo_datum == kezdo_datum and
                foglalas.veg_datum == veg_datum):
                self.foglalasok.remove(foglalas)
                return "Foglalás sikeresen lemondva."

        return "Nincs ilyen foglalás."

    def listaz_foglalasok(self):
        if not self.foglalasok:
            return "Nincsenek foglalások."
        return "\n".join(str(foglalas) for foglalas in self.foglalasok)

# GUI
class SzobafoglalasGUI:
    def __init__(self, root, foglalasi_rendszer):
        self.root = root
        self.foglalasi_rendszer = foglalasi_rendszer
        self.root.title("Szobafoglalás")

        self.label = tk.Label(root, text="ABC Hotel", font=("Helvetica", 16))
        self.label.pack(pady=10)
        self.label = tk.Label(root, text="Szobafoglalás", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.szoba_info = tk.Label(root, text=self.get_szoba_info(), justify=tk.LEFT)
        self.szoba_info.pack(pady=10)

        self.foglalas_button = tk.Button(root, text="Szoba foglalása", command=self.foglalas)
        self.foglalas_button.pack(pady=5)

        self.lemondas_button = tk.Button(root, text="Foglalás lemondása", command=self.lemondas)
        self.lemondas_button.pack(pady=5)

        self.listazas_button = tk.Button(root, text="Foglalások listázása", command=self.listazas)
        self.listazas_button.pack(pady=5)

    def get_szoba_info(self):
        szoba_info = "Elérhető szobák:\n"
        for szoba in self.foglalasi_rendszer.szalloda.szobak:
            szoba_info += f"{szoba}\n"
        return szoba_info

    def foglalas(self):
        foglalas_window = tk.Toplevel(self.root)
        foglalas_window.title("Szoba foglalása")

        tk.Label(foglalas_window, text="Szobaszám:").grid(row=0, column=0)
        szobaszam_entry = tk.Entry(foglalas_window)
        szobaszam_entry.grid(row=0, column=1)

        tk.Label(foglalas_window, text="Ettől:").grid(row=1, column=0)
        kezdo_datum_entry = self.create_placeholder_entry(foglalas_window, "ÉÉÉÉ-HH-NN")
        kezdo_datum_entry.grid(row=1, column=1)

        tk.Label(foglalas_window, text="Eddig:").grid(row=2, column=0)
        veg_datum_entry = self.create_placeholder_entry(foglalas_window, "ÉÉÉÉ-HH-NN")
        veg_datum_entry.grid(row=2, column=1)

        def confirm_foglalas():
            szobaszam = szobaszam_entry.get()
            kezdo_datum = kezdo_datum_entry.get()
            veg_datum = veg_datum_entry.get()

            try:
                kezdo_datum_obj = datetime.strptime(kezdo_datum, "%Y-%m-%d")
                veg_datum_obj = datetime.strptime(veg_datum, "%Y-%m-%d")
                if kezdo_datum_obj <= datetime.now():
                    messagebox.showerror("Hiba", "A kezdő dátumnak a jövőben kell lennie.")
                    return
            except ValueError:
                messagebox.showerror("Hiba", "Érvénytelen dátum formátum.")
                return

            eredmeny = self.foglalasi_rendszer.foglalas(int(szobaszam), kezdo_datum, veg_datum)
            messagebox.showinfo("Foglalás eredménye", eredmeny)

        confirm_button = tk.Button(foglalas_window, text="Foglalás megerősítése", command=confirm_foglalas)
        confirm_button.grid(row=3, columnspan=2, pady=10)

    def create_placeholder_entry(self, parent, placeholder):
        entry = tk.Entry(parent)
        entry.insert(0, placeholder)
        entry.config(fg="grey")
        entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, placeholder))
        entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, placeholder))
        return entry

    def clear_placeholder(self, event, placeholder):
        entry = event.widget
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def add_placeholder(self, event, placeholder):
        entry = event.widget
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="grey")

    def lemondas(self):
        lemondas_window = tk.Toplevel(self.root)
        lemondas_window.title("Foglalás lemondása")

        tk.Label(lemondas_window, text="Szobaszám:").grid(row=0, column=0)
        szobaszam_entry = tk.Entry(lemondas_window)
        szobaszam_entry.grid(row=0, column=1)

        tk.Label(lemondas_window, text="Ettől:").grid(row=1, column=0)
        kezdo_datum_entry = self.create_placeholder_entry(lemondas_window, "ÉÉÉÉ-HH-NN")
        kezdo_datum_entry.grid(row=1, column=1)

        tk.Label(lemondas_window, text="Eddig:").grid(row=2, column=0)
        veg_datum_entry = self.create_placeholder_entry(lemondas_window, "ÉÉÉÉ-HH-NN")
        veg_datum_entry.grid(row=2, column=1)

        def confirm_lemondas():
            szobaszam = szobaszam_entry.get()
            kezdo_datum = kezdo_datum_entry.get()
            veg_datum = veg_datum_entry.get()

            eredmeny = self.foglalasi_rendszer.lemondas(int(szobaszam), kezdo_datum, veg_datum)
            messagebox.showinfo("Lemondás eredménye", eredmeny)

        confirm_button = tk.Button(lemondas_window, text="Lemondás megerősítése", command=confirm_lemondas)
        confirm_button.grid(row=3, columnspan=2, pady=10)

    def listazas(self):
        foglalasok = self.foglalasi_rendszer.listaz_foglalasok()
        messagebox.showinfo("Foglalások", foglalasok)

foglalasi_rendszer = FoglalasiRendszer()
foglalasi_rendszer.letrehoz_szalloda("ABC Hotel")
foglalasi_rendszer.hozzaad_szoba(EgyAgyasSzoba(101))
foglalasi_rendszer.hozzaad_szoba(EgyAgyasSzoba(102))
foglalasi_rendszer.hozzaad_szoba(KetAgyasSzoba(201))
foglalasi_rendszer.hozzaad_szoba(KetAgyasSzoba(202))
foglalasi_rendszer.hozzaad_szoba(KetPluszEgyAgyasSzoba(301))
foglalasi_rendszer.hozzaad_szoba(KetPluszEgyAgyasSzoba(302))
foglalasi_rendszer.foglalas(101, "2024-06-01", "2024-06-02")
foglalasi_rendszer.foglalas(101, "2024-06-03", "2024-06-04")
foglalasi_rendszer.foglalas(201, "2024-06-01", "2024-06-02")
foglalasi_rendszer.foglalas(201, "2024-06-05", "2024-06-06")
foglalasi_rendszer.foglalas(301, "2024-06-01", "2024-06-02")

root = tk.Tk()
app = SzobafoglalasGUI(root, foglalasi_rendszer)
root.mainloop()
