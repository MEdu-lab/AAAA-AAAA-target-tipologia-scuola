import yaml
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from liquid import Template

# --- Helpers ---

def generate_yaml_header(config):
    maestri = config.get('maestri', [])
    progetto = config.get('progetto', {})
    
    # Costruisci gli autori con minipage
    if len(maestri) <= 2:
        width = "0.45"
    else:
        width = "0.3"
    
    author_boxes = []
    for maestro in maestri:
        # Costruisci il contenuto della minipage con nome, ruolo e qualifica
        nome = maestro['nome']
        ruolo = maestro.get('ruolo', '')
        qualifica = maestro.get('qualifica', '')
        
        # Costruisci il testo con le righe separate
        content_lines = [f"\\textbf{{{nome}}}"]
        
        if ruolo:
            content_lines.append(f"\\textit{{{ruolo}}}")
        
        if qualifica:
            content_lines.append(f"\\textit{{{qualifica}}}")
        
        content = "\\\\".join(content_lines)
        
        box = f"""\\begin{{minipage}}{{{width}\\textwidth}}
        \\centering
        {content}
      \\end{{minipage}}"""
        author_boxes.append(box)
    
    authorlist = "\\hfill".join(author_boxes)
    
    # YAML PULITO!
    metadata = {
        'title': progetto.get('titolo', ''),
        'subtitle': f"{progetto.get('sottotitolo', '')} - {progetto.get('anno_scolastico', '')}",
        'documentclass': 'article',
        'author': ' ',
        'header-includes': [
            "\\usepackage{styles/mystyle}",
            f"\\newcommand{{\\gruppo}}{{{progetto.get('gruppo', '')}}}",
            f"\\newcommand{{\\authorlist}}{{{authorlist}}}"
        ]
    }
    
    return "---\n" + yaml.dump(metadata) + "---\n\n"
    
def get_day_of_week(day_name: str) -> int:
    days = {
        'domenica': 6, 'lunedì': 0, 'martedì': 1, 'mercoledì': 2,
        'giovedì': 3, 'venerdì': 4, 'sabato': 5
    }
    return days[day_name.lower()]

def is_in_vacation(date: datetime, vacanze: list) -> bool:
    for vacanza in vacanze:
        inizio = datetime.fromisoformat(vacanza["inizio"])
        fine = datetime.fromisoformat(vacanza["fine"])
        if inizio <= date <= fine:
            return True
    return False

# --- Calcoli programmazione ---

def calcola_mercoledi(config: dict) -> dict:
    programmazione = config["programmazione"]
    vacanze = config.get("vacanze", [])

    inizio_anno = datetime.fromisoformat(programmazione["inizio"])
    fine_anno = datetime.fromisoformat(programmazione["fine"])
    target_day = get_day_of_week(programmazione["giorno_settimana"])

    # Trova il primo giorno target
    current_date = inizio_anno
    while current_date.weekday() != target_day:
        current_date += timedelta(days=1)

    mercoledi_validi = []
    mercoledi_per_mese = {}

    nomi_mesi = [
        'Ottobre', 'Novembre', 'Dicembre', 'Gennaio',
        'Febbraio', 'Marzo', 'Aprile', 'Maggio'
    ]

    while current_date <= fine_anno:
        if not is_in_vacation(current_date, vacanze):
            mese = current_date.month
            indice_mese = mese - 10 if mese >= 10 else mese + 2
            nome_mese = nomi_mesi[indice_mese]

            mercoledi_validi.append(current_date)

            mercoledi_per_mese[nome_mese] = mercoledi_per_mese.get(nome_mese, 0) + 1

        current_date += timedelta(days=7)

    totale_mercoledi = len(mercoledi_validi)
    numero_mesi = len(mercoledi_per_mese)
    media_mercoledi_per_mese = round(totale_mercoledi / numero_mesi, 1) if numero_mesi > 0 else 0

    return {
        "totale_incontri": totale_mercoledi,
        "media_per_mese": media_mercoledi_per_mese,
        "dettaglio_per_mese": mercoledi_per_mese,
        "primo_incontro": mercoledi_validi[0].strftime("%d/%m/%Y") if mercoledi_validi else None,
        "ultimo_incontro": mercoledi_validi[-1].strftime("%d/%m/%Y") if mercoledi_validi else None,
    }

# --- Calcoli costi ---

def calcola_costi(config: dict) -> dict:
    costi = config["costi"]
    mesi_inclusi = costi["mesi_inclusi"]

    bimestri = [mesi_inclusi[i:i+2] for i in range(0, len(mesi_inclusi), 2) if i + 1 < len(mesi_inclusi)]
    numero_bimestri = len(bimestri)
    costo_totale = numero_bimestri * costi["quota_bimestrale"]

    dettaglio_pagamenti = [
        {
            "periodo": f"{b[0]}-{b[1]}",
            "importo": costi["quota_bimestrale"],
            "scadenza": f"inizio {b[0]}"
        }
        for b in bimestri
    ]

    return {
        "bimestri": bimestri,
        "numero_bimestri": numero_bimestri,
        "costo_totale": costo_totale,
        "dettaglio_pagamenti": dettaglio_pagamenti,
    }

# --- Main processing ---

def process_templates():
    try:
        # Carica configurazione
        with open("config.yml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        print("Config caricato:", list(config.keys()))

        tipo_scuola = config["progetto"].get("tipo_scuola", "privata")
        
        # Calcoli SOLO per scuole private
        if tipo_scuola == "privata":
            programmazione_calcolata = calcola_mercoledi(config)
            print("Programmazione calcolata:", programmazione_calcolata)
            config["programmazione_calcolata"] = programmazione_calcolata

            costi_calcolati = calcola_costi(config)
            print("Costi calcolati:", costi_calcolati)
            config["costi_calcolati"] = costi_calcolati
        else:
            print("Scuola pubblica: saltando calcoli costi e programmazione")

        # Processa template Liquid
        sezioni_path = Path("docs/sezioni")
        files = sorted([f for f in sezioni_path.iterdir() if f.suffix == ".md"])
        print("File trovati:", [f.name for f in files])

        # 1. Genera l'header YAML per Pandoc
        yaml_header = generate_yaml_header(config)
        
        # 2. Il documento inizia con l'header YAML (non più con il titolo manuale)
        final_doc = yaml_header

        for file in files:
            print("Processando:", file)
            with open(file, "r", encoding="utf-8") as f:
                template = Template(f.read())
            rendered = template.render(**config)
            final_doc += rendered + "\n\n"

        # Scrivi il documento finale
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(final_doc)
        print("Documento generato: README.md")

        # File debug JSON SOLO per scuole private
        if tipo_scuola == "privata":
            with open("debug-programmazione.json", "w", encoding="utf-8") as f:
                json.dump({
                    "programmazione": programmazione_calcolata,
                    "costi": costi_calcolati
                }, f, indent=2, ensure_ascii=False)

    except Exception as e:
        print("Errore durante il processing:", e)
        exit(1)

if __name__ == "__main__":
    process_templates()
