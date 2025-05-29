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

        ritardo_minuti = 0

        # Unisce tutto il testo utile dei div evidenziati
        testo_completo = " ".join(div.get_text(strip=True) for div in divs)

        # Estrai ritardo o anticipo
        match_ritardo = re.search(r'con\s+(\d+)\s+minuti\s+di\s+(ritardo|anticipo)', testo_completo, re.IGNORECASE)
        if match_ritardo:
            minuti = int(match_ritardo.group(1))
            tipo = match_ritardo.group(2).lower()
            unità = "minuto" if minuti == 1 else "minuti"
            if tipo == "ritardo":
                ritardo_minuti = minuti
                ritardo_info = f"{minuti} {unità} di ritardo"
            else:
                ritardo_minuti = -minuti
                ritardo_info = f"{minuti} {unità} di anticipo"

        # Estrai info ultimo rilevamento
        match_rilevamento = re.search(r'Ultimo rilevamento a (.+?alle ore \d{2}:\d{2})', testo_completo)
        if match_rilevamento:
            rilevamento_info = match_rilevamento.group(1)

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

        
        # Valori predefiniti
        ultima_fermata = "Non trovata"
        arrivo_programmato = "Non trovato"
        arrivo_effettivo = "Non trovato"

        # Ciclo sui div principali
        divs = soup.find_all('div')
        for i in range(len(divs)):
            div = divs[i]

            # Cerca la sezione dell'ultima fermata
            if div.get_text(strip=True) == "Ultima fermata effettuata:":
                if i + 1 < len(divs):
                    next_div = divs[i + 1]
                    if "corpocentrale" in next_div.get("class", []):
                        h2 = next_div.find("h2")
                        if h2:
                            ultima_fermata = h2.get_text(strip=True)

                        p_tags = next_div.find_all("p")
                        for p in p_tags:
                            text = p.get_text(strip=True)
                            if "Arrivo Programmato" in text:
                                strong = p.find("strong")
                                if strong:
                                    arrivo_programmato = strong.get_text(strip=True)
                            elif "Arrivo effettivo" in text:
                                strong = p.find("strong")
                                if strong:
                                    arrivo_effettivo = strong.get_text(strip=True)
                break  # Trovata, basta
        
        # Estrai info ultimo rilevamento
        match_rilevamento = re.search(r'Ultimo rilevamento a (.+?alle ore \d{2}:\d{2})', testo_completo)
        if match_rilevamento:
            rilevamento_info = match_rilevamento.group(1)

        # Notifica solo se il ritardo supera la soglia
        if ritardo_minuti >= SOGLIA_RITARDO_SUPERIORE and not notifica_mostrata:
            messagebox.showwarning("Ritardo eccessivo", f"⚠️ Il treno {nome_treno} ha {ritardo_minuti} minuti di ritardo!")
            notifica_mostrata = True
        elif ritardo_minuti < SOGLIA_RITARDO_RESET and notifica_mostrata:
            messagebox.showwarning("Ritardo eccessivo", f"✅ Il treno {nome_treno} sta recuperando il ritardo!")
            notifica_mostrata = False



        # Controlla se il treno non è ancora partito o è arrivato
        for div in divs:
            testo = div.get_text(strip=True).lower()
            if "non è ancora partito" in testo:
                ultima_fermata = "Il treno non è ancora partito"
                rilevamento_info = "Il treno non è ancora partito"
                ritardo_info = "Il treno non è ancora partito"
                arrivo_programmato = "Il treno non è ancora partito"
                arrivo_effettivo = "Il treno non è ancora partito"
                break
            elif "arrivato" in testo:
                ultima_fermata = "Il treno è arrivato a destinazione"
                rilevamento_info = "Il treno è arrivato a destinazione"
                arrivo_programmato = "Il treno è arrivato a destinazione"
                arrivo_effettivo = "Il treno è arrivato a destinazione"
                break


        # Aggiungi i tag per colorare solo la scritta dello stato
        text_widget.config(state="normal")
        text_widget.delete(1.0, tk.END)

        # Definisci i tag
        text_widget.tag_configure("ritardo", foreground="red")
        text_widget.tag_configure("anticipo_orario", foreground="green")

        # Scrittura del testo con tag applicati solo per lo stato
        text_widget.insert(tk.END, f"Treno {nome_treno}\n\nPartenza prevista: {partenza_prevista}\n\nPartenza effettiva: {partenza_effettiva}\n\n")

        text_widget.insert(tk.END, f"Ultima Fermata: {ultima_fermata}\n\nArrivo programmato: {arrivo_programmato}\n\nArrivo effettivo: {arrivo_effettivo}\n\n")

        # Stato del treno con il colore appropriato
        if ritardo_minuti > 0:
            text_widget.insert(tk.END, "Stato del Treno: ", "ritardo")
            text_widget.insert(tk.END, f"{ritardo_info}\n\n", "ritardo")
        elif ritardo_minuti < 0:
            text_widget.insert(tk.END, "Stato del Treno: ", "anticipo_orario")
            text_widget.insert(tk.END, f"{ritardo_info}\n\n", "anticipo_orario")
        else:
            text_widget.insert(tk.END, "Stato del Treno: ", "anticipo_orario")  
            text_widget.insert(tk.END, f"Treno in Orario\n\n", "anticipo_orario")


        # Aggiungi dati ultimo rilevamento
        text_widget.insert(tk.END, f"Ultimo rilevamento: {rilevamento_info}")

        root.geometry("400x450")

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
        reset_output()  # Reset dell'area di testo prima di fare la ricerca
        aggiorna_treno(treno_attivo, output_text)  # Aggiorna i dati
        aggiorna_periodicamente()  # Start del monitoraggio periodico

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
    output_text = tk.Text(root, height=25, width=70, wrap=tk.WORD, font=("Helvetica", 12), state="disabled")  # Più largo e alto
    output_text.pack(pady=10)

# UI principale
root = tk.Tk()
root.title("TrenItalia Train Checker")
root.config(bg="#a7033a")
root.geometry("400x150")  # Finestra piccola all'inizio
root.resizable(False, False)  # Finestra non ridimensionabile


treno_label = ttk.Label(root, text="Inserisci numero del treno:", font=("Helvetica", 14), background="#a7033a", foreground="#ffffff")
treno_label.pack(pady=10)

treno_entry = ttk.Entry(root, font=("Helvetica", 12), width=15)
treno_entry.pack(pady=10)

treno_entry.bind("<Return>", lambda event: avvia_monitoraggio())

avvia_button = ttk.Button(root, text="Avvia Monitoraggio", command=avvia_monitoraggio)
avvia_button.pack(pady=10)

treno_attivo = None
after_id = None

root.mainloop()
