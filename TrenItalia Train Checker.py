import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

# Soglie e flag
SOGLIA_RITARDO_SUPERIORE = 10
SOGLIA_RITARDO_RESET = 5
notifica_mostrata = False

# Funzione per ottenere i dati del treno
def aggiorna_treno(numero_treno, text_widget):
    global notifica_mostrata
    url = f"http://www.viaggiatreno.it/vt_pax_internet/mobile/numero?numeroTreno={numero_treno}"
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        divs = soup.find_all('div', class_='evidenziato')
        nome_treno = "Treno non trovato"
        ritardo_info = "Informazione sul ritardo non trovata"
        rilevamento_info = "Informazione sul rilevamento non trovata"
        partenza_prevista = "Partenza prevista non trovata"
        partenza_effettiva = "Partenza effettiva non trovata"
        orario_massimo = "Orario massimo non calcolato"

        ritardo_minuti = 0

        for div in divs:
            testo = div.get_text(strip=True)
            if "ritardo" in testo and "Ultimo rilevamento" in testo:
                match_ritardo = re.search(r'con\s+(\d+)\s+minuti', testo)
                if match_ritardo:
                    ritardo_minuti = int(match_ritardo.group(1))
                    ritardo_info = f"{ritardo_minuti} minuti di ritardo"

                match_rilevamento = re.search(r'Ultimo rilevamento a (.+?alle ore \d{2}:\d{2})', testo)
                if match_rilevamento:
                    rilevamento_info = match_rilevamento.group(1)
                break
        
        # Nome treno
        h1 = soup.find('h1')
        if h1:
            nome_treno = h1.get_text(strip=True)

        # Orari partenza
        corpocentrale_divs = soup.find_all('div', class_='corpocentrale')
        for div in corpocentrale_divs:
            testo = div.get_text(strip=True)
            if "Partenza programmata" in testo:
                partenza_match = re.search(r'Partenza programmata\s*:\s*(\d{2}:\d{2})', testo)
                if partenza_match:
                    partenza_prevista = partenza_match.group(1)
            if "Partenza effettiva" in testo:
                partenza_match_eff = re.search(r'Partenza effettiva\s*:\s*(\d{2}:\d{2})', testo)
                if partenza_match_eff:
                    partenza_effettiva = partenza_match_eff.group(1)

        # Orario massimo (alle 17:00 + ritardo)
        orario_iniziale = datetime.strptime("17:00", "%H:%M")
        orario_massimo = orario_iniziale + timedelta(minutes=ritardo_minuti)

        # Notifica ritardo
        if ritardo_minuti >= SOGLIA_RITARDO_SUPERIORE and not notifica_mostrata:
            messagebox.showwarning("Ritardo eccessivo", f"⚠️ Il treno ha {ritardo_minuti} minuti di ritardo!")
            notifica_mostrata = True
        elif ritardo_minuti < SOGLIA_RITARDO_RESET:
            notifica_mostrata = False

        # Output grafico
        text_widget.config(state="normal")
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, f"Treno {nome_treno}\n\nPartenza prevista: {partenza_prevista}\n\nPartenza effettiva: {partenza_effettiva}\n\nRitardo: {ritardo_info}\n\nUltimo rilevamento: {rilevamento_info}")
        text_widget.config(state="disabled")
    else:
        text_widget.config(state="normal")
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, "Errore nel recupero dei dati dal sito.")
        text_widget.config(state="disabled")

# Avvia monitoraggio
def avvia_monitoraggio():
    numero_treno = treno_entry.get()
    if numero_treno:
        global treno_attivo, notifica_mostrata
        treno_attivo = numero_treno
        notifica_mostrata = False
        reset_output()
        aggiorna_treno(treno_attivo, output_text)
        aggiorna_periodicamente()


# Aggiorna ogni 5 secondi
def aggiorna_periodicamente():
    if treno_attivo:
        aggiorna_treno(treno_attivo, output_text)
    global after_id
    after_id = root.after(5000, aggiorna_periodicamente)

# Reset caselle testo
def reset_output():
    for widget in root.winfo_children():
        if isinstance(widget, tk.Text):
            widget.destroy()
    global output_text
    output_text = tk.Text(root, height=12, width=50, wrap=tk.WORD, font=("Helvetica", 12), state="disabled")
    output_text.pack(pady=10)

# UI principale
root = tk.Tk()
root.title("TrenItalia Train Checker")
root.config(bg="#a7033a")

treno_label = ttk.Label(root, text="Inserisci numero del treno:", font=("Helvetica", 14), background="#a7033a", foreground="#ffffff")
treno_label.pack(pady=10)

treno_entry = ttk.Entry(root, font=("Helvetica", 12), width=15)
treno_entry.pack(pady=10)

avvia_button = ttk.Button(root, text="Avvia Monitoraggio", command=avvia_monitoraggio)
avvia_button.pack(pady=10)

treno_attivo = None
after_id = None

root.mainloop()
