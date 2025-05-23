import tkinter as tk
from tkinter import messagebox, filedialog
import random
from PIL import Image, ImageDraw, ImageFont, ImageTk

# Beispielgründe, falls kein Grund eingegeben wird
gruende = [
    "hat heimlich den letzten Keks gegessen",
    "hat zu viele schlechte Witze gemacht",
    "hat den Boss im Game geblufft",
    "ist der unbestrittene Meme-König",
    "hat das geheime Passwort verraten",
    "wurde beim Schummeln erwischt",
    "hat den epischsten Fail 2025 hingelegt"
]

selected_image_path = None
image_preview = None

def zufaellige_summe():
    return random.randint(1, 1_000_000_000)

def zufaellige_aktenzeichen():
    buchstaben = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
    zahlen = ''.join(random.choices("0123456789", k=3))
    return buchstaben + zahlen

def bild_auswaehlen():
    global selected_image_path, image_preview
    path = filedialog.askopenfilename(filetypes=[("Bilddateien", "*.png *.jpg *.jpeg *.webp")])
    if path:
        selected_image_path = path
        lbl_bild.config(text="Bild ausgewählt ✓")
        try:
            img = Image.open(path)
            img = img.resize((150, 150))
            image_preview = ImageTk.PhotoImage(img)
            preview_label.config(image=image_preview)
        except Exception as e:
            print("Fehler beim Laden des Bildes:", e)
            image_preview = None
            preview_label.config(image="", text="Bild konnte nicht angezeigt werden")

def kopfgeld_generieren():
    sheriff = entry_sheriff.get().strip()
    name = entry_name.get().strip()
    grund = entry_grund.get().strip()
    tatort = entry_tatort.get().strip()
    summe = entry_summe.get().strip()
    aktenzeichen = entry_aktenzeichen.get().strip()
    sichtort = entry_sichtort.get().strip()
    gefahr = entry_gefahr.get().strip()

    # Pflichtfelder prüfen
    if not sheriff or not name:
        messagebox.showerror("Fehler", "Bitte mindestens Sheriff und Name ausfüllen.")
        return

    if not grund:
        grund = random.choice(gruende)
    if not tatort:
        tatort = "Unbekanntes Gebiet"
    if not aktenzeichen:
        aktenzeichen = zufaellige_aktenzeichen()
    if not sichtort:
        sichtort = "Unbekannt"
    if not gefahr:
        gefahr = "Gefährlich"

    try:
        summe_int = int(summe.replace(".", "").replace(",", "")) if summe else zufaellige_summe()
    except ValueError:
        summe_int = zufaellige_summe()

    text = (
        f"WANTED\n\n"
        f"Sheriff: {sheriff}\n"
        f"Name: {name}\n"
        f"Fahndungsnummer: {aktenzeichen}\n"
        f"Grund: {grund}\n"
        f"Tatort: {tatort}\n"
        f"Zuletzt gesehen: {sichtort}\n"
        f"Einstufung: {gefahr}\n"
        f"Kopfgeld: {summe_int:,.0f} €".replace(",", ".")
    )

    # Text in das Label setzen
    ausgabe_text.set(text)

def als_bild_exportieren():
    text = ausgabe_text.get()
    if not text.strip():
        messagebox.showinfo("Hinweis", "Bitte erst ein Kopfgeld generieren.")
        return

    font_path = "arial.ttf"
    try:
        font = ImageFont.truetype(font_path, 24)
    except IOError:
        font = ImageFont.load_default()

    lines = text.split("\n")
    width = 600
    y_start = 240 if selected_image_path else 40
    height = y_start + 40 * len(lines) + 40

    img = Image.new("RGB", (width, height), color=(255, 244, 225))
    draw = ImageDraw.Draw(img)

    if selected_image_path:
        try:
            bild = Image.open(selected_image_path).convert("RGB")
            bild = bild.resize((200, 200))
            img.paste(bild, (width // 2 - 100, 20))
        except Exception as e:
            print("Bildfehler:", e)

    for i, line in enumerate(lines):
        draw.text((40, y_start + i * 40), line, fill=(60, 40, 20), font=font)

    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Datei", "*.png")])
    if file_path:
        img.save(file_path)
        messagebox.showinfo("Erfolg", f"Bild gespeichert unter:\n{file_path}")

# GUI Setup
root = tk.Tk()
root.title("Wanted-Kopfgeld-Generator")
root.configure(bg="#f4f1e1")
root.geometry("600x900")

tk.Label(root, text="Wanted-Kopfgeld-Generator", font=("Georgia", 24), bg="#f4f1e1", fg="#5a4322").pack(pady=10)

frame = tk.Frame(root, bg="#f4f1e1")
frame.pack(pady=10)

def add_entry(label):
    tk.Label(frame, text=label, bg="#f4f1e1", fg="#3e2f1c").pack(anchor="w", padx=20)
    entry = tk.Entry(frame, width=50)
    entry.pack(pady=5, padx=20)
    return entry

entry_sheriff = add_entry("Sheriff (dein Name):")
entry_name = add_entry("Name des Gesuchten:")
entry_grund = add_entry("Grund (leer für Zufall):")
entry_tatort = add_entry("Tatort:")
entry_summe = add_entry("Kopfgeld (€ - leer für Zufall):")
entry_aktenzeichen = add_entry("Fahndungsnummer (leer für Zufall):")
entry_sichtort = add_entry("Zuletzt gesehen (leer für Zufall):")
entry_gefahr = add_entry("Einstufung (leer für Zufall):")

tk.Button(root, text="Bild auswählen", command=bild_auswaehlen, bg="#a98654", fg="white", font=("Georgia", 12)).pack(pady=5)
lbl_bild = tk.Label(root, text="Kein Bild ausgewählt", bg="#f4f1e1", fg="gray")
lbl_bild.pack()

preview_label = tk.Label(root, bg="#f4f1e1")
preview_label.pack(pady=5)

tk.Button(root, text="Kopfgeld generieren", command=kopfgeld_generieren, bg="#a9743f", fg="white", font=("Georgia", 14)).pack(pady=10)
tk.Button(root, text="Als Bild exportieren", command=als_bild_exportieren, bg="#85582f", fg="white", font=("Georgia", 12)).pack()

ausgabe_text = tk.StringVar()
# Label, in dem der Steckbrief angezeigt wird
tk.Label(root, textvariable=ausgabe_text, wraplength=550, justify="left", bg="#fff4e1", fg="#3e2f1c",
         font=("Georgia", 14), relief="solid", bd=3, padx=10, pady=20).pack(pady=20, fill="both", expand=True)

tk.Label(root, text="Hinweis: Nur zum Spaß gedacht!", font=("Arial", 10), bg="#f4f1e1", fg="gray").pack(pady=5)
tk.Label(root, text="Erstellt von: CodeMajorX", font=("Arial", 10, "italic"), bg="#f4f1e1", fg="#5a4322").pack()

root.mainloop()
