{% if progetto.tipo_scuola != "pubblica" %}

## ASPETTI ORGANIZZATIVI

Il laboratorio si svolge ogni {{ programmazione.giorno_settimana }} dal {{ programmazione_calcolata.primo_incontro }} al {{ programmazione_calcolata.ultimo_incontro }}, per un totale di **{{ programmazione_calcolata.totale_incontri }} incontri** (media di {{ programmazione_calcolata.media_per_mese }} incontri al mese).
Ogni incontro dura circa un'ora e mezza: i bambini ci vengono affidati direttamente dalle educatrici entro le 16:30 e vengono riconsegnati alle famiglie tra le 17:45 e le 17:55. Gli ultimi minuti fino alle 18 servono agli organizzatori per lasciare ambienti puliti e adatti all'attività scolastica del giorno successivo, quindi si raccomanda puntualità per il ritiro dei bambini.

Ogni incontro si articola nel modo seguente:  
- 16:30 inizio attività musicale   
- 17:15 merenda e svago   
- 17:40 preparazione per l'uscita   

**Incontri mensili:**

|{% for mese in programmazione_calcolata.dettaglio_per_mese %} {{ mese[0] }} |{% endfor %}
|{% for mese in programmazione_calcolata.dettaglio_per_mese %} :---: |{% endfor %}
|{% for mese in programmazione_calcolata.dettaglio_per_mese %} **{{ mese[1] }}** |{% endfor %}

La programmazione tiene conto delle pause per le vacanze di Natale.

**Costi:**

- Quota bimestrale: {{ costi.quota_bimestrale }}€ per bambino    
<!-- - Pagamento: {{ costi.modalita_pagamento }}   -->
- **Costo totale del corso: {{ costi_calcolati.costo_totale }}€** ({{ costi_calcolati.numero_bimestri }} bimestri)    

<!---
**Calendario pagamenti:**
| Periodo | Importo | Scadenza |
| :--- | ---: | :---: |
{% for pagamento in costi_calcolati.dettaglio_pagamenti %}| {{ pagamento.periodo | capitalize }} | {{ pagamento.importo }}€ | {{ pagamento.scadenza }} |
{% endfor %}
-->
*{{ costi.nota_giugno }}*

{% else %}

---

La programmazione dettagliata, i costi e le modalità organizzative verranno concordati direttamente con la scuola in base alle vostre specifiche esigenze e disponibilità.
{% endif %}
