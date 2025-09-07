# Documentazione Config.yaml - Generatore Progetti Scolastici

## Panoramica
Lo script Python legge il file `config.yml` e genera automaticamente un documento markdown completo del progetto scolastico. Il comportamento varia in base al tipo di scuola (privata/pubblica).

## Struttura del Config.yml

### 📋 Sezione `progetto` (obbligatoria)
```yaml
progetto:
  titolo: "Nome del progetto"                    # Titolo principale
  gruppo: "MEduLab"                              # Nome del gruppo/organizzazione
  sottotitolo: "Nome della scuola"               # Nome scuola (usato nel testo)
  anno_scolastico: "2025/2026"                   # Anno di riferimento
  tipo_scuola: "privata"                         # "privata" o "pubblica"
```

**Campo `tipo_scuola`:**
- `"privata"`: genera calcoli dettagliati di programmazione e costi
- `"pubblica"`: nasconde sezioni programmazione/costi (da discutere a voce)

### 👥 Sezione `maestri` (obbligatoria)
```yaml
maestri:
  - nome: "Pietro Barale"
    ruolo: "operatore"                           # es: operatore, coordinatore
    qualifica: "diplomato in..."                 # titoli di studio
  - nome: "Giulio Romano De Mattia"
    ruolo: "operatore"
    qualifica: "diplomato in..."
```

### 🎵 Sezione `corso` (obbligatoria)
```yaml
corso:
  tipologia: "musica d'insieme"
  fascia_eta: "3-5 anni"
  durata_incontro: "1 ora e mezza"
  frequenza: "settimanale"
  partecipanti_anno_precedente: "6-9 bambini"
  periodo: "intero anno educativo"
```

### 🎯 Sezione `metodologia` (obbligatoria)
```yaml
metodologia:
  focus_principale: "processo educativo"
  approccio: "dimensione del gioco"
  personalizzazione: true
  feedback_continuo: true
```

### 📅 Sezione `programmazione` (solo scuole private)
```yaml
programmazione:
  giorno_settimana: "mercoledì"                  # giorno della settimana
  inizio: "2025-10-01"                          # data inizio (YYYY-MM-DD)
  fine: "2026-05-28"                            # data fine (YYYY-MM-DD)
```

### 💰 Sezione `costi` (solo scuole private)
```yaml
costi:
  quota_bimestrale: 120                         # euro ogni 2 mesi
  modalita_pagamento: "all'inizio di ogni bimestre"
  mesi_inclusi: ["ottobre", "novembre", "dicembre", "gennaio", "febbraio", "marzo", "aprile", "maggio"]
  nota_giugno: "Il mese di giugno si decide per tempo..."
```

### 🏖️ Sezione `vacanze` (solo scuole private)
```yaml
vacanze:
  - nome: "Vacanze di Natale"
    inizio: "2025-12-23"                        # YYYY-MM-DD
    fine: "2026-01-06"                          # YYYY-MM-DD
  - nome: "Vacanze di Pasqua"
    inizio: "2026-04-01"
    fine: "2026-04-07"
```

## Esempi di Configurazione

### 🏫 Config per Scuola Privata
```yaml
progetto:
  titolo: "Laboratorio di Musica Contemporanea"
  gruppo: "MEduLab"
  sottotitolo: "Casa dei Bambini 'il Girasole'"
  anno_scolastico: "2025/2026"
  tipo_scuola: "privata"

maestri:
  - nome: "Marco Rossi"
    ruolo: "coordinatore"
    qualifica: "diplomato in Composizione"

corso:
  tipologia: "musica d'insieme"
  fascia_eta: "3-5 anni"
  # ... altri campi

programmazione:
  giorno_settimana: "mercoledì"
  inizio: "2025-10-01"
  fine: "2026-05-28"

costi:
  quota_bimestrale: 120
  # ... altri campi

vacanze:
  - nome: "Natale"
    inizio: "2025-12-23"
    fine: "2026-01-06"
```

### 🏛️ Config per Scuola Pubblica
```yaml
progetto:
  titolo: "Laboratorio di Musica Contemporanea"
  gruppo: "MEduLab"
  sottotitolo: "Scuola Elementare Dante Alighieri"
  anno_scolastico: "2025/2026"
  tipo_scuola: "pubblica"

maestri:
  - nome: "Marco Rossi"
    ruolo: "coordinatore"
    qualifica: "diplomato in Composizione"

corso:
  tipologia: "musica d'insieme"
  fascia_eta: "6-10 anni"
  # ... altri campi

metodologia:
  # ... campi metodologia

# NON servono: programmazione, costi, vacanze
```

## Utilizzo dello Script

### 1. Preparazione
```bash
# Assicurati di avere la struttura:
project/
├── config.yml
├── script.py
├── docs/sezioni/*.md
└── styles/mystyle.sty
```

### 2. Esecuzione
```bash
python script.py
```

### 3. Output
Lo script genera:
- `README.md` - documento finale pronto per Pandoc
- `debug-programmazione.json` - solo per scuole private (debug)

## Output per Tipo Scuola

### 🏫 Scuole Private
- ✅ Calcoli automatici programmazione (date, numero incontri)
- ✅ Calcoli automatici costi (totali, bimestri)
- ✅ Tabelle dettagliate
- ✅ File debug JSON

### 🏛️ Scuole Pubbliche  
- ❌ Sezioni programmazione/costi nascoste
- ✅ Solo informazioni generali e metodologia
- ✅ Frase generica: "da concordare con la scuola"

## Troubleshooting

### Errori Comuni
- **Data non valida**: usa formato `YYYY-MM-DD`
- **Giorno settimana errato**: scrivi per intero (es: "mercoledì")
- **YAML mal formato**: controlla indentazione e virgolette

### Debug
Controlla sempre l'output dello script:
```
Config caricato: ['progetto', 'maestri', 'corso'...]
Programmazione calcolata: {...}  # solo scuole private
Costi calcolati: {...}          # solo scuole private
```

## Note Tecniche
- **Engine template**: Liquid
- **Formato date**: ISO 8601 (YYYY-MM-DD)
- **Encoding**: UTF-8
- **Output**: Markdown compatibile Pandoc
