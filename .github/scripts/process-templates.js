const { Liquid } = require('liquidjs');
const yaml = require('js-yaml');
const fs = require('fs');
const path = require('path');

// Funzione per ottenere il numero del giorno della settimana (0=domenica, 3=mercoledì)
function getDayOfWeek(dayName) {
  const days = {
    'domenica': 0, 'lunedì': 1, 'martedì': 2, 'mercoledì': 3,
    'giovedì': 4, 'venerdì': 5, 'sabato': 6
  };
  return days[dayName.toLowerCase()];
}

// Funzione per verificare se una data è durante le vacanze
function isInVacation(date, vacanze) {
  return vacanze.some(vacanza => {
    const inizio = new Date(vacanza.inizio);
    const fine = new Date(vacanza.fine);
    return date >= inizio && date <= fine;
  });
}

// Funzione principale per calcolare i mercoledì
function calcolaMercoledi(config) {
  const { programmazione, vacanze } = config;
  
  const inizioAnno = new Date(programmazione.inizio);
  const fineAnno = new Date(programmazione.fine);
  const targetDay = getDayOfWeek(programmazione.giorno_settimana);
  
  // Trova il primo mercoledì nel periodo
  let currentDate = new Date(inizioAnno);
  while (currentDate.getDay() !== targetDay) {
    currentDate.setDate(currentDate.getDate() + 1);
  }
  
  const mercolediValidi = [];
  const mercolediPerMese = {};
  
  // Conta tutti i mercoledì nel periodo, escludendo le vacanze
  while (currentDate <= fineAnno) {
    if (!isInVacation(currentDate, vacanze)) {
      const mese = currentDate.getMonth(); // 0-11
      const nomesMesi = [
        'Ottobre', 'Novembre', 'Dicembre', 'Gennaio', 
        'Febbraio', 'Marzo', 'Aprile', 'Maggio'
      ];
      const indiceMese = mese >= 9 ? mese - 9 : mese + 3; // Converti per anno scolastico
      const nomeMese = nomesMesi[indiceMese];
      
      mercolediValidi.push(new Date(currentDate));
      
      if (!mercolediPerMese[nomeMese]) {
        mercolediPerMese[nomeMese] = 0;
      }
      mercolediPerMese[nomeMese]++;
    }
    
    // Vai al mercoledì successivo
    currentDate.setDate(currentDate.getDate() + 7);
  }
  
  const totaleMercoledi = mercolediValidi.length;
  const numeroMesi = Object.keys(mercolediPerMese).length;
  const mediaMercolediPerMese = Math.round((totaleMercoledi / numeroMesi) * 10) / 10;
  
  return {
    totale_incontri: totaleMercoledi,
    media_per_mese: mediaMercolediPerMese,
    dettaglio_per_mese: mercolediPerMese,
    primo_incontro: mercolediValidi[0]?.toLocaleDateString('it-IT'),
    ultimo_incontro: mercolediValidi[mercolediValidi.length - 1]?.toLocaleDateString('it-IT')
  };
}

// Funzione per calcolare i costi automaticamente
function calcolaCosti(config) {
  const { costi } = config;
  const mesiInclusi = costi.mesi_inclusi;
  
  // Raggruppa i mesi in bimestri
  const bimestri = [];
  for (let i = 0; i < mesiInclusi.length; i += 2) {
    if (i + 1 < mesiInclusi.length) {
      bimestri.push([mesiInclusi[i], mesiInclusi[i + 1]]);
    }
  }
  
  const numeroBimestri = bimestri.length;
  const costoTotale = numeroBimestri * costi.quota_bimestrale;
  
  return {
    bimestri: bimestri,
    numero_bimestri: numeroBimestri,
    costo_totale: costoTotale,
    dettaglio_pagamenti: bimestri.map((bimestre, index) => ({
      periodo: `${bimestre[0]}-${bimestre[1]}`,
      importo: costi.quota_bimestrale,
      scadenza: `inizio ${bimestre[0]}`
    }))
  };
}

async function processTemplates() {
  try {
    // Carica configurazione dalla root
    const config = yaml.load(fs.readFileSync('config.yml', 'utf8'));
    console.log('Config caricato:', Object.keys(config));
    
    // Calcola la programmazione automaticamente
    const programmazione_calcolata = calcolaMercoledi(config);
    console.log('Programmazione calcolata:', programmazione_calcolata);
    
    // Aggiungi i calcoli al config per i template
    config.programmazione_calcolata = programmazione_calcolata;
    
    // Calcola i costi automaticamente
    const costi_calcolati = calcolaCosti(config);
    console.log('Costi calcolati:', costi_calcolati);

    // Aggiungi anche questo al config
    config.costi_calcolati = costi_calcolati;

    // Setup Liquid engine
    const engine = new Liquid();
    
    // Leggi tutti i file dalla cartella sezioni
    const sezionePath = 'docs/sezioni';
    const files = fs.readdirSync(sezionePath)
      .filter(file => file.endsWith('.md'))
      .sort();
    
    console.log('File trovati:', files);
    
    let finalDoc = `# ${config.progetto.titolo}\n`;
    finalDoc += `### ${config.progetto.sottotitolo} - Anno educativo ${config.progetto.anno_scolastico}\n\n`;
    
    // Processa ogni sezione
    for (const file of files) {
      const templatePath = path.join(sezionePath, file);
      console.log('Processando:', templatePath);
      
      const template = fs.readFileSync(templatePath, 'utf8');
      const rendered = await engine.parseAndRender(template, config);
      
      finalDoc += rendered + '\n\n---\n\n';
    }
    
    // Scrivi il documento finale
    fs.writeFileSync('progetto-completo.md', finalDoc);
    console.log('Documento generato: progetto-completo.md');
    
    // Salva anche un file di debug con i calcoli
    fs.writeFileSync('debug-programmazione.json', JSON.stringify({
      programmazione: programmazione_calcolata,
      costi: costi_calcolati
    }, null, 2));

  } catch (error) {
    console.error('Errore durante il processing:', error);
    process.exit(1);
  }
}

// Esegui il processing
processTemplates();
