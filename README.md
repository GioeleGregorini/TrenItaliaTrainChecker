# 🚆 TrenItalia Train Checker

**TrenItalia Train Checker** è un'app desktop in Python con interfaccia Tkinter che ti permette di monitorare lo stato di un treno Trenitalia in tempo reale. Ricevi aggiornamenti automatici ogni 5 secondi, notifiche di ritardo e informazioni su orari di partenza e rilevamenti, tutto in un'interfaccia ispirata ai colori ufficiali Trenitalia.


---

## ✨ Funzionalità

- ✅ Inserisci il numero di un treno Trenitalia
- ⏱️ Monitoraggio automatico ogni 5 secondi
- ⚠️ Notifica in caso di ritardo ≥ 10 minuti
- 📄 Visualizza:
  - Orario di partenza previsto
  - Orario di partenza effettivo
  - Minuti di ritardo
  - Ultimo rilevamento noto
- 🖥️ Interfaccia semplice in stile rosso-bianco Trenitalia

---

## 📦 Requisiti

Assicurati di avere **Python 3** installato sul sistema.

Installa le dipendenze richieste con:

```bash
pip install requests beautifulsoup4
```

---

## 🚀 Avvio rapido

Clona la repository ed esegui lo script:

```bash
git clone https://github.com/GioeleGregorini/TrenItaliaTrainChecker
cd TrenItaliaTrainChecker
python trenitalia_checker.py
```

---

## 🧰 Tecnologie utilizzate

- [Python 3](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tk.html) – per la GUI
- [Requests](https://docs.python-requests.org/) – per l'accesso al sito ViaggiaTreno
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) – per il parsing HTML
- Regex e datetime per l’elaborazione dei dati

---

## 📷 Screenshot

*(Aggiungi qui un'immagine se vuoi mostrarla)*

---

## ⚠️ Note importanti

- Il monitoraggio si basa sul sito [ViaggiaTreno.it](http://www.viaggiatreno.it/).
- Se la struttura HTML del sito cambia, sarà necessario aggiornare il parser.

---

## 👤 Autore

**Gioele Gregorini**

🔗 GitHub: [@GioeleGregorini](https://github.com/GioeleGregorini)

---

✅ Progetto open-source — sentiti libero di contribuire o proporre miglioramenti!
