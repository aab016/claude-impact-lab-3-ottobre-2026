# Rilevamento urgenza in locale (tecnica OpenJev, backend)

Stessa demo di [`examples/typesafe-noul-urgenza/`](../typesafe-noul-urgenza/)
— classificare se un messaggio trasmette urgenza — ma senza chiamare un
servizio esterno: il modello gira in un processo backend sotto il nostro
controllo, con la tecnica descritta dal progetto
[**OpenJev**](https://openjev.com/) ([codice](https://github.com/TheoLeeCJ/openjev)).

## Cos'è OpenJev, esattamente

[openjev.com](https://openjev.com/) è una demo **eseguita nel browser**
(tramite WebGPU/WASM) che confronta due modi di ottenere una decisione
tipizzata da un modello open: generare testo/JSON e fare il parsing, oppure
leggere la probabilità delle opzioni **direttamente dai logit del modello**
in un unico forward pass, senza generare testo. È un tentativo indipendente
di riprodurre l'*interfaccia* dei primitivi di TypeSafe (Choice, Score,
Noul) con modelli open — non riproduce il modello Jev né il suo
addestramento RLCD (vedi nota nel [README principale](../../README.md)).

**Non esiste un pacchetto Python `openjev` da installare** — è un pattern,
dimostrato nel browser. Qui lo reimplementiamo noi stessi, lato backend, con
[`llama-cpp-python`](https://github.com/abetlen/llama-cpp-python), così che
giri su un server (es. quelli del Comune di Milano) invece che nel browser
di chi visita un sito.

## Perché in backend e non nel browser

Il browser va bene per una demo personale, ma per un servizio pubblico:

- **Scelta del modello centralizzata**: il Comune decide quale modello
  eseguire (dimensione, lingua, licenza, hardware disponibile) cambiando una
  variabile d'ambiente, senza dover far scaricare gigabyte di modello a ogni
  cittadino che visita il sito.
- **Hardware prevedibile**: un server con GPU/CPU dedicata invece del
  dispositivo (spesso modesto) del cittadino — proprio i dispositivi che,
  secondo le note in [`research/`](../../research/), sono già una barriera
  di accesso.
- **Nessun dato che lascia il perimetro del Comune** verso un servizio
  esterno (né TypeSafe né altri).

## Setup

```bash
pip install -r requirements.txt

# Scarica un modello GGUF, ad es. MiniCPM5-2B quantizzato (~1.56 GB) —
# lo stesso indicato tra i modelli disponibili su openjev.com:
# https://huggingface.co/openbmb/MiniCPM5-2B-GGUF
huggingface-cli download openbmb/MiniCPM5-2B-GGUF \
    MiniCPM5-2B-Q4_K_M.gguf --local-dir ./modelli

export OPENJEV_MODEL_PATH=./modelli/MiniCPM5-2B-Q4_K_M.gguf
python rileva_urgenza_locale.py
```

Per cambiare modello: punta `OPENJEV_MODEL_PATH` a un altro file `.gguf`
compatibile con `llama.cpp` (es. una versione più piccola per hardware
limitato, o una più grande se serve più accuratezza) — il codice non cambia.

## Limiti da conoscere prima di usarla per decisioni reali

- **Nessuna calibrazione RLCD.** La probabilità restituita è letta dai logit
  del modello di base e normalizzata (softmax tra "sì" e "no"), non
  addestrata per essere calibrata come Jev/TypeSafe. Un valore di 0.8 qui
  *non* garantisce che la risposta sia corretta nell'80% dei casi: da
  validare sui propri dati prima di usarla per instradare richieste vere.
- **Modelli "thinking".** MiniCPM5-2B, secondo la sua documentazione,
  supporta solo la modalità "Think" (a differenza della versione 1B, che ha
  anche un "No-think"): può quindi generare alcuni token di ragionamento
  prima della risposta. Per questo `noul()` concede un piccolo budget di
  token e cerca il primo token sì/no generato, invece di leggere solo il
  primissimo token come nel caso ideale (un modello senza ragionamento) —
  un compromesso più robusto ma meno estremo in termini di velocità.
- **`logits_all=True` è obbligatorio** in `llama-cpp-python` per poter
  leggere i logprobs: aumenta l'uso di memoria.

## Fonti verificate

- Tecnica e benchmark: [github.com/TheoLeeCJ/openjev](https://github.com/TheoLeeCJ/openjev)
  (README verificato sul branch `master`)
- Modello: [huggingface.co/openbmb/MiniCPM5-2B-GGUF](https://huggingface.co/openbmb/MiniCPM5-2B-GGUF)
  e [guida di deploy con llama.cpp](https://github.com/OpenBMB/MiniCPM/blob/main/docs/deployment/llama_cpp.md)
- API di `llama-cpp-python`: [github.com/abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
  (parametri `logprobs`/`top_logprobs`/`logits_all` verificati sul sorgente)
