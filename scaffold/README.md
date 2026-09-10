# Scaffold tecnico — Assistente servizi Comune di Milano

Punto di partenza minimo per il build session del 3 ottobre: un backend
FastAPI che parla con Claude in streaming, più una pagina HTML/JS senza
dipendenze come interfaccia di chat. Pensato per essere clonato e modificato
in fretta durante l'hackathon, non come prodotto finito.

Il system prompt in `backend/app.py` incorpora già i principi emersi nelle
note di ricerca (`../research/comune-milano-servizi-accessibilita.md`): non
inventare procedure, indicare sempre una via di uscita umana, usare un
linguaggio semplice.

## Avvio rapido

### Backend

```bash
cd scaffold/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Autenticazione: `ant auth login` oppure copia .env.example in .env
# e inserisci ANTHROPIC_API_KEY, poi `export $(cat .env | xargs)`
uvicorn app:app --reload --port 8000
```

Verifica che sia attivo: `curl http://localhost:8000/api/health`

### Frontend

Apri `frontend/index.html` direttamente nel browser (nessuna build richiesta).
Punta a `http://localhost:8000/api/chat`, quindi il backend deve essere avviato.

## Idee per estendere durante l'hackathon

- **Fondare le risposte su fonti reali**: invece del solo system prompt, fare
  RAG sulle pagine pubbliche del Comune (es. `comune.milano.it`, la knowledge
  base `servizicrm.comune.milano.it`) o passarle come contesto/documenti.
- **Multilingua**: rilevare la lingua dell'utente e rispondere di conseguenza.
- **Accessibilità**: test reale con screen reader (VoiceOver/NVDA), non solo
  markup semantico.
- **Integrazione con REMID@**: pensare lo strumento anche come supporto per i
  facilitatori digitali nelle Case di Quartiere, non solo come self-service.
- **Feedback loop**: un modo per segnalare risposte sbagliate, visibile a chi
  gestisce i contenuti.

## Note

- Modello: `claude-opus-5` (vedi `backend/app.py` — cambia `MODEL` se preferisci
  `claude-sonnet-5` per costi/latenza inferiori durante lo sviluppo).
- CORS aperto a `*` solo per comodità di sviluppo locale: da restringere prima
  di qualsiasi deploy.
- Nessun salvataggio della cronologia lato server: lo stato vive solo nel
  browser per la durata della sessione.
