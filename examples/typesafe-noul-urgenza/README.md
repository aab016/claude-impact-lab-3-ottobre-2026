# Rilevamento urgenza con TypeSafe AI (primitiva Noul)

Esempio minimo di uso delle [TypeSafe AI API](https://docs.typesafe.ai/) per
classificare se un messaggio di un cittadino trasmette un tono di urgenza,
usando la primitiva [**Noul**](https://docs.typesafe.ai/primitives/noul) —
una domanda sì/no che restituisce la probabilità calibrata della risposta,
invece di testo generato liberamente (vedi la nota su RLCD nel
[README principale](../../README.md#nota-su-rlcd-reinforcement-learning-for-calibrated-decisions)).

Perché è rilevante per l'Impact Lab: uno smistamento affidabile tra "urgente"
e "non urgente" può aiutare a dare priorità alle richieste dei cittadini più
in difficoltà (es. scadenze imminenti) rispetto a domande informative
generiche, senza dover far leggere ogni messaggio a un operatore.

## Setup

```bash
pip install -r requirements.txt
export TYPESAFE_API_KEY=...   # crea una chiave su https://console.typesafe.ai/
```

## Esecuzione

```bash
python rileva_urgenza.py
```

Per ogni messaggio di esempio stampa la probabilità calibrata (0–1) che
trasmetta urgenza, non un'etichetta generata dal modello:

```
[0.94 -> URGENTE] Aiuto! Sono tre giorni che il pagamento non va a buon fine...
[0.06 -> non urgente] Buongiorno, volevo sapere quali documenti servono...
```

## Come funziona

`rileva_urgenza()` invia il messaggio come `state` e pone una singola domanda
`Noul` con `instructions` e `criteria` che chiariscono cosa conta come "sì"
e cosa come "no" — la stessa distinzione emersa nelle
[note di ricerca](../../research/comune-milano-servizi-accessibilita.md) tra
casi chiari e casi limite che richiedono giudizio umano: qui la soglia (0.5)
è solo un punto di partenza da tarare, non una verità assoluta.
