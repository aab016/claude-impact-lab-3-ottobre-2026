"""
Stessa demo di examples/typesafe-noul-urgenza/ (rilevare se un messaggio ha
un tono di urgenza), ma con un modello open eseguito in locale invece delle
TypeSafe AI API ospitate.

Perché questa versione: TypeSafe è un servizio esterno con un modello
proprietario (Jev). Qui il modello gira in un processo backend sotto il
nostro controllo — non nel browser di chi visita il sito, e non su un
servizio di terzi — cosa che permette al Comune di Milano di scegliere quale
modello eseguire (bastano un altro file .gguf e la variabile d'ambiente
OPENJEV_MODEL_PATH, senza toccare il codice), tenere i dati entro i propri
sistemi, e cambiare modello nel tempo senza dipendere da un fornitore.

La tecnica — leggere la probabilità della risposta direttamente dai logit
del modello invece di generare testo e fare il parsing — è quella descritta
dal progetto OpenJev (https://openjev.com/, codice:
https://github.com/TheoLeeCJ/openjev), un tentativo indipendente di
riprodurre l'interfaccia dei "primitivi tipizzati" di TypeSafe (Choice,
Score, Noul) con modelli open. Non è un pacchetto/SDK da installare: è un
pattern, che qui reimplementiamo direttamente con llama-cpp-python.

Differenze importanti rispetto a examples/typesafe-noul-urgenza/:

1. Nessuna calibrazione RLCD. La probabilità qui è letta dai logit "grezzi"
   del modello di base e poi normalizzata (softmax tra sì/no): è una stima
   ragionevole, ma — a differenza dell'RLCD di TypeSafe (vedi la nota nel
   README principale) — non c'è alcuna garanzia che una probabilità di 0.8
   si riveli corretta l'80% delle volte. Non usarla come se fosse calibrata
   senza averla validata sui propri dati.

2. Modelli "thinking". Diversi modelli 2B-4B recenti (incluso MiniCPM5-2B,
   che secondo la sua documentazione supporta solo la modalità "Think", a
   differenza della versione 1B che ha anche un "No-think") possono generare
   qualche token di ragionamento prima della risposta vera e propria. Per
   questo la funzione noul() qui sotto concede un piccolo budget di token
   (non uno solo) e cerca il primo token sì/no tra quelli generati, invece
   di assumere che sia sempre il primissimo token — un compromesso più
   robusto ma meno estremo, in termini di velocità, della lettura in un solo
   forward pass che fa OpenJev con modelli senza ragionamento. Se nessun
   token sì/no viene trovato entro il budget, la funzione restituisce 0.5
   (incertezza massima) e lo segnala: da monitorare, non da ignorare.

3. `logits_all=True` è obbligatorio in llama-cpp-python per poter leggere i
   logprobs: aumenta l'uso di memoria rispetto a una chat normale, è il
   costo della tecnica.

Setup:
    pip install -r requirements.txt

    # Scarica un modello GGUF, ad es. MiniCPM5-2B quantizzato (~1.56 GB):
    huggingface-cli download openbmb/MiniCPM5-2B-GGUF \
        MiniCPM5-2B-Q4_K_M.gguf --local-dir ./modelli

    export OPENJEV_MODEL_PATH=./modelli/MiniCPM5-2B-Q4_K_M.gguf
    python rileva_urgenza_locale.py

Per cambiare modello (la scelta che spetta al Comune di Milano, non al
codice): punta OPENJEV_MODEL_PATH a un altro file .gguf compatibile con
llama.cpp. Il chat template viene letto automaticamente dai metadati del
file GGUF.
"""

from __future__ import annotations

import math
import os
from functools import lru_cache
from typing import Optional

from llama_cpp import Llama

MODEL_PATH = os.environ.get(
    "OPENJEV_MODEL_PATH", "./modelli/MiniCPM5-2B-Q4_K_M.gguf"
)
N_CTX = int(os.environ.get("OPENJEV_N_CTX", "4096"))

# Budget di generazione: non un solo token, per lasciare spazio a un
# eventuale breve ragionamento prima della risposta (vedi punto 2 sopra).
BUDGET_TOKEN_RISPOSTA = 32

TOKEN_SI = {"si", "sì", "yes", "true"}
TOKEN_NO = {"no", "false"}

MESSAGGI_DI_ESEMPIO = [
    "Aiuto! Sono tre giorni che il pagamento non va a buon fine e devo "
    "presentare il documento domani mattina, cosa faccio?",
    "Buongiorno, volevo sapere quali documenti servono per il rinnovo "
    "della carta d'identità, non c'è fretta.",
    "Ho già scritto due volte e nessuno mi ha risposto, mio figlio deve "
    "iscriversi a scuola entro venerdì e non so come fare.",
    "Solo per curiosità, a che ora chiude lo sportello anagrafe il giovedì?",
]


@lru_cache(maxsize=1)
def _carica_modello() -> Llama:
    """Carica il modello una sola volta per processo. `logits_all=True` è
    necessario per poter leggere i logprobs (vedi punto 3 nel docstring)."""
    return Llama(
        model_path=MODEL_PATH,
        n_ctx=N_CTX,
        logits_all=True,
        verbose=False,
    )


def _massa_probabilita(
    top_logprobs: dict[str, float], candidati: set[str]
) -> float:
    return sum(
        math.exp(logprob)
        for token, logprob in top_logprobs.items()
        if token.strip().lower() in candidati
    )


def noul(
    state: str, instructions: str, criteria: Optional[dict[str, str]] = None
) -> float:
    """Equivalente locale della primitiva Noul di TypeSafe: risponde a una
    domanda sì/no leggendo i logit del token di risposta invece di generare
    una frase da interpretare.

    Restituisce un numero tra 0 e 1: la probabilità (non calibrata — vedi il
    punto 1 nel docstring del modulo) che la risposta sia "sì". Se il
    modello non produce un token sì/no riconoscibile entro il budget,
    restituisce 0.5 e va trattato come "non determinato", non come un
    giudizio neutro nel merito.
    """
    criteri = ""
    if criteria:
        righe = "\n".join(
            f"- {esito}: {descrizione}" for esito, descrizione in criteria.items()
        )
        criteri = f"\n\nCriteri:\n{righe}"

    prompt = (
        f"Testo da valutare:\n{state}\n\n"
        f"Domanda: {instructions}{criteri}\n\n"
        "Rispondi con una sola parola: sì oppure no."
    )

    modello = _carica_modello()
    risposta = modello.create_chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=BUDGET_TOKEN_RISPOSTA,
        temperature=0.0,
        logprobs=True,
        top_logprobs=20,
    )

    logprobs = risposta["choices"][0]["logprobs"]
    if logprobs is None:
        return 0.5

    for top in logprobs["top_logprobs"]:
        if not top:
            continue
        massa_si = _massa_probabilita(top, TOKEN_SI)
        massa_no = _massa_probabilita(top, TOKEN_NO)
        if massa_si + massa_no > 0:
            return massa_si / (massa_si + massa_no)

    # Nessun token sì/no trovato entro il budget: il modello ha "divagato"
    # (es. ha continuato a ragionare) più del previsto.
    return 0.5


def main() -> None:
    for messaggio in MESSAGGI_DI_ESEMPIO:
        probabilita = noul(
            state=messaggio,
            instructions="Il messaggio trasmette un tono di urgenza?",
            criteria={
                "sì": (
                    "Chi scrive segnala una scadenza imminente, un disagio "
                    "che si protrae da tempo senza risposta, o chiede "
                    "esplicitamente un intervento rapido."
                ),
                "no": (
                    "Richiesta informativa generica, senza scadenze o "
                    "pressione temporale."
                ),
            },
        )
        etichetta = "URGENTE" if probabilita >= 0.5 else "non urgente"
        print(f"[{probabilita:.2f} -> {etichetta}] {messaggio}")


if __name__ == "__main__":
    main()
