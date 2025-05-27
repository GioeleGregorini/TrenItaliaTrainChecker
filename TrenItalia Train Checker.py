import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

# Funzione per ottenere i dati del treno
def aggiorna_treno(numero_treno, text_widget):
    url = f"http://www.viaggiatreno.it/vt_pax_internet/mobile/numero?numeroTreno={numero_treno}"
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Cerca tutti i div con classe 'evidenziato'
        divs = soup.find_all('div', class_='evidenziato')
        nome_treno = "Treno non trovato"
        ritardo_info = "Informazione sul ritardo non trovata"
        rilevamento_info = "Informazione sul rilevamento non trovata"
        partenza_prevista = "Partenza prevista non trovata"
        partenza_effettiva = "Partenza effettiva non trovata"
        orario_massimo = "Orario massimo non calcolato"

        ritardo_minuti = 0  # Variabile per il ritardo in minuti

        for div in divs:
            testo = div.get_text(strip=True)
            if "ritardo" in testo and "Ultimo rilevamento" in testo:
                # Estrazione ritardo
                match_ritardo = re.search(r'con\s+(\d+)\s+minuti', testo)
                if match_ritardo:
                    ritardo_minuti = int(match_ritardo.group(1))
                    ritardo_info = f"{ritardo_minuti} minuti di ritardo"

                # Estrazione rilevamento
                match_rilevamento = re.search(r'Ultimo rilevamento a (.+?alle ore \d{2}:\d{2})', testo)
                if match_rilevamento:
                    rilevamento_info = match_rilevamento.group(1)
                break
        
        # Estrazione nome treno
        nome_treno= soup.find('h1').get_text(strip=True)

        # Estrazione della partenza prevista ed effettiva dal div con class='corpocentrale'
        corpocentrale_divs = soup.find_all('div', class_='corpocentrale')

        for div in corpocentrale_divs:
            testo = div.get_text(strip=True)
            # Cerca la partenza prevista
            if "Partenza programmata" in testo:
                partenza_match = re.search(r'Partenza programmata\s*:\s*(\d{2}:\d{2})', testo)
                if partenza_match:
                    partenza_prevista = partenza_match.group(1)
            # Cerca la partenza effettiva
            if "Partenza effettiva" in testo:
                partenza_match_eff = re.search(r'Partenza effettiva\s*:\s*(\d{2}:\d{2})', testo)
                if partenza_match_eff:
                    partenza_effettiva = partenza_match_eff.group(1)

        # Calcola l'orario massimo (somma del ritardo alle 17:00)
        orario_iniziale = datetime.strptime("17:00", "%H:%M")  # Orario iniziale: 17:00
        orario_massimo = orario_iniziale + timedelta(minutes=ritardo_minuti)

        # Mostra il risultato nel box di output
        text_widget.config(state="normal")  # Imposta lo stato su "normal"
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, f"Treno {nome_treno}\n\nPartenza prevista: {partenza_prevista}\n\nPartenza effettiva: {partenza_effettiva}\n\nRitardo: {ritardo_info}\n\nUltimo rilevamento: {rilevamento_info}")
        text_widget.config(state="disabled")  # Ripristina lo stato su "disabled"
    else:
        text_widget.config(state="normal")  # Imposta lo stato su "normal"
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, "Errore nel recupero dei dati dal sito.")
        text_widget.config(state="disabled")  # Ripristina lo stato su "disabled"

# Funzione per avviare il monitoraggio di un solo treno
def avvia_monitoraggio():
    numero_treno = treno_entry.get()
    if numero_treno:
        global treno_attivo
        treno_attivo = numero_treno
        reset_output()
        aggiorna_treno(treno_attivo, output_text)
        aggiorna_periodicamente()

# Funzione per aggiornare periodicamente ogni 5 secondi
def aggiorna_periodicamente():
    if treno_attivo:
        aggiorna_treno(treno_attivo, output_text)
    global after_id
    after_id = root.after(5000, aggiorna_periodicamente)

# Funzione per resettare l'output e rimuovere tutte le caselle di testo
def reset_output():
    for widget in root.winfo_children():
        if isinstance(widget, tk.Text):
            widget.destroy()

    # Crea una nuova casella di testo per visualizzare l'output
    global output_text
    output_text = tk.Text(root, height=12, width=50, wrap=tk.WORD, font=("Helvetica", 12), state="disabled")
    output_text.pack(pady=10)

# Crea la finestra principale
root = tk.Tk()
root.title("TrenItalia Train Checker")
root.config(bg="#a7033a")

# Etichetta per il numero del treno
treno_label = ttk.Label(root, text="Inserisci numero del treno:", font=("Helvetica", 14), background="#a7033a", foreground="#ffffff")
treno_label.pack(pady=10)

# Casella di testo per l'inserimento del numero del treno
treno_entry = ttk.Entry(root, font=("Helvetica", 12), width=15)
treno_entry.pack(pady=10)

# Bottone per avviare il monitoraggio
avvia_button = ttk.Button(root, text="Avvia Monitoraggio", command=avvia_monitoraggio)
avvia_button.pack(pady=10)

# Variabile globale per il treno attivo
treno_attivo = None
after_id = None

# Avvia l'interfaccia grafica
root.mainloop()
