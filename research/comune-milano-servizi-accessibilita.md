# Servizi del Comune di Milano e barriere di accesso — note di preparazione

> Materiale raccolto in preparazione dell'Impact Lab del 3 ottobre 2026, a partire
> dalle domande poste durante "Milano | Claude Conversation" (9 settembre 2026):
> *dove le persone si bloccano davvero, cosa può fare l'AI e cosa deve restare umano,
> cosa succede quando il sistema sbaglia, cosa rende una soluzione adottabile da una PA.*
>
> Fonti raccolte tramite ricerca web il 10 settembre 2026 — da verificare e
> aggiornare con testimonianze dirette durante l'evento del 3 ottobre.

## 1. Cosa offre oggi il Comune di Milano online

- **Certificati anagrafici**: dal 2 agosto 2023 i certificati anagrafici in bollo
  sono disponibili online tramite il portale ANPR (accesso con SPID/CIE) collegato
  a PagoPA, senza doversi recare allo sportello.
  ([comune.milano.it](https://www.comune.milano.it/en/w/servizi-civici.-certificati-anagrafici-in-bollo-disponibili-online))
- **Estratti e atti di stato civile** (nascita, matrimonio, decesso): richiedibili
  online per gli atti successivi al 1° gennaio 2026.
  ([comune.milano.it](https://www.comune.milano.it/en/servizi/anagrafe/atti-integrali-ed-estratti-di-nascita-matrimonio-decesso))
- **Prenotazione appuntamenti allo sportello**, anche per richieste per conto terzi.
- **Centro di supporto / CRM**: knowledge base con schede guidate
  (es. "Come chiedere un certificato anagrafico?") e un percorso "Serve altro aiuto?"
  per chi ha difficoltà a scaricare documenti o prenotare senza SPID/CIE.
  ([servizicrm.comune.milano.it](https://servizicrm.comune.milano.it/centro-supporto/KA-00455/Richiesta-certificati-anagrafici-online))

**Osservazione**: il punto di accesso a quasi tutti i servizi civici è SPID/CIE.
Questo è già il primo, grande scoglio strutturale — non un problema di linguaggio
o di interfaccia, ma di possesso di credenziali digitali e di un dispositivo/numero
di telefono attivo per riceverle.

## 2. Iniziative esistenti contro il divario digitale

- **REMID@ — Rendere Milano Inclusiva e Digitale**: 11 centri di facilitazione
  digitale nelle Case di Quartiere della città, promossi dal Comune con Fondazione
  Mondo Digitale e MigliorAttivaMente APS. Offrono: alfabetizzazione digitale,
  supporto all'uso di SPID/CIE e dei servizi online, dispositivi rigenerati in
  comodato, attività di apprendimento intergenerazionale (giovani che aiutano
  anziani). Target dichiarato: fragilità economico-sociale, anziani, stranieri,
  persone in cerca di lavoro.
  ([comune.milano.it](https://www.comune.milano.it/en/-/case-di-quartiere.-undici-centri-di-facilitazione-digitale-per-supportare-la-cittadinanza),
  [mitomorrow.it](https://www.mitomorrow.it/cambiamilano/punti-di-facilitazione-digitale-milano/))
- **Competenze digitali** — pagina istituzionale che raccoglie i programmi di
  alfabetizzazione digitale del Comune.
  ([comune.milano.it](https://www.comune.milano.it/en/home/competenze-digitali))
- **Accessibilità dei trasporti**: linea rossa (M1) della metro completamente
  accessibile, linea verde (M2) al 91%; servizio "Informazioni Senza Barriere"
  per ascensori/scale mobili; indicazione di accessibilità per bus/tram/filobus.
  ([urbanfile.org](https://blog.urbanfile.org/2026/02/13/milano-trasporti-m1-accessibile-m2-91-accessibilita/))

**Osservazione**: esiste già un'infrastruttura umana e fisica (Case di Quartiere,
REMID@) pensata esattamente per le persone che un chatbot da solo non
raggiungerebbe. Una soluzione AI credibile dovrebbe integrarsi con questa rete,
non sostituirla — es. come strumento in mano ai facilitatori, non solo come
self-service sul sito.

## 3. Dove le persone si bloccano davvero (ipotesi da validare il 3 ottobre)

Da incrociare con le "storie di sportello fallito" raccolte durante la Claude
Conversation del 9 settembre. Ipotesi di lavoro:

1. **Credenziali, non contenuti**: non sapere di avere/come attivare SPID/CIE è
   probabilmente la barriera più comune e strutturale — nessun chatbot la risolve
   se non indirizzando concretamente a REMID@ o allo sportello.
2. **Quale servizio tra decine**: le pagine sono organizzate per procedimento
   amministrativo (es. "atti di stato civile" vs "certificati anagrafici"), non
   per bisogno della persona ("mi sono appena trasferito", "devo iscrivere mio
   figlio a scuola"). Chi non conosce il lessico burocratico non sa da dove
   iniziare.
3. **Lingua e alfabetizzazione**: cittadini di nuova immigrazione, persone anziane,
   persone con bassa scolarizzazione — bureaucratic Italian è una barriera anche
   per madrelingua.
4. **Accessibilità assistiva**: uso di screen reader, moduli PDF non accessibili,
   form online (es. elixForms) che possono non essere ottimizzati per tecnologie
   assistive — da verificare tecnicamente.
5. **Cosa succede quando il sistema sbaglia**: a differenza di un servizio privato,
   il cittadino non può "cambiare fornitore". Un errore di un assistente AI (es.
   indicazione sbagliata su documenti richiesti, scadenze, requisiti) ha un costo
   reale e nessuna alternativa — da qui l'importanza di: citare sempre la fonte
   ufficiale, non inventare procedure, e offrire sempre un'via di escalation umana
   chiara (Contact Center, sportello, Case di Quartiere).

## 4. Cosa può fare l'AI, cosa deve restare umano

**Terreno favorevole all'AI (assistenza, non decisione):**
- Tradurre il linguaggio burocratico in linguaggio semplice/plain language,
  eventualmente multilingue.
- Orientamento: "in base a quello che mi hai detto, il servizio che cerchi si
  chiama X, si trova qui, i documenti richiesti sono questi, questi sono i tempi".
- Riassumere/spiegare un modulo prima che l'utente lo compili.
- Fare da "traduttore" tra il linguaggio del cittadino e la tassonomia del sito.
- Supportare gli operatori di REMID@/sportello come strumento di lavoro (non solo
  rivolto al cittadino finale).

**Terreno che deve restare umano/strutturale:**
- L'atto amministrativo finale (rilascio, approvazione, verifica identità).
- I casi limite e le eccezioni normative — dove un errore ha conseguenze legali.
- L'attivazione delle credenziali digitali (SPID/CIE) per chi non le ha.
- La relazione di fiducia con le fasce più fragili — l'AI può preparare il
  terreno, non sostituire il facilitatore umano nelle Case di Quartiere.

## 5. Cosa rende una soluzione adottabile da una PA (non solo demoabile)

Punti da cui partire per valutare le proposte che emergeranno il 3 ottobre:

- **Nessuna invenzione**: la risposta deve poter essere ancorata a fonti
  ufficiali verificabili (pagine del Comune, CRM), mai generata "a memoria".
- **Via di uscita umana sempre visibile**: ogni risposta deve indicare come
  raggiungere un umano (Contact Center, Case di Quartiere, sportello) quando
  l'AI non è sicura o il caso è un'eccezione.
- **Accessibilità reale**: compatibile con screen reader, leggibile a bassa
  scolarizzazione, eventualmente multilingue — non solo un'interfaccia bella.
- **Si aggancia a ciò che esiste**: integrazione con REMID@ e Case di Quartiere
  piuttosto che un canale nuovo e parallelo.
- **Manutenibilità**: chi aggiorna i contenuti quando una procedura cambia?
  Una PA non può gestire un sistema che richiede tuning manuale continuo.
- **Misurabilità**: come si verifica che l'assistente non stia dando indicazioni
  sbagliate? Serve un meccanismo di feedback/segnalazione errori visibile agli
  operatori comunali.

## 6. Domande aperte da portare il 3 ottobre

- Qual è stato il "problema concreto" scelto durante la Claude Conversation del
  9 settembre? (Da recuperare da Alexio Cassani / dai partecipanti / dal canale
  Telegram della community: https://t.me/+Rt7yOpOAp7A1NDQ0)
- Il target prioritario è: chi non parla italiano, chi ha bassa alfabetizzazione
  digitale, chi ha disabilità, o una combinazione — e con quali priorità?
- Con quali dati/contenuti ufficiali si può lavorare in un hackathon (pagine
  pubbliche del sito, knowledge base del CRM, FAQ) senza accesso a sistemi interni
  del Comune?
