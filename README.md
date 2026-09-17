# Claude Impact Lab — 3 ottobre 2026

Repository di preparazione personale per l'**Impact Lab** del 3 ottobre 2026,
l'hackathon della community Claude Code Milano dedicato a: *come l'AI può
rendere i servizi pubblici raggiungibili per tutti.*

## Contesto

Il brief dell'Impact Lab nasce da **"Milano | Claude Conversation"**, una
serata di discussione tenutasi il 9 settembre 2026 e guidata da
[Alexio Cassani](https://www.linkedin.com/in/alexio), Claude Community
Ambassador per l'Italia. Il punto di partenza era il Comune di Milano, che
gestisce centinaia di servizi (certificati anagrafici, iscrizioni scolastiche,
casa, welfare, permessi, servizi sociali, mobilità) formalmente aperti a
tutti, ma di fatto difficili da raggiungere per chi non legge l'italiano
burocratico, usa uno screen reader, ha ottant'anni o è arrivato in città da
poco.

Le domande guida della serata:

- Dove le persone si bloccano davvero — quale passaggio, quale documento,
  quale parola?
- Quali barriere sono di linguaggio/comprensione e quali sono strutturali,
  irrisolvibili da un chatbot?
- Cosa può fare l'AI in modo realistico, e cosa deve restare umano?
- Cosa succede quando il sistema sbaglia e il cittadino non ha un fornitore
  alternativo a cui rivolgersi?
- Cosa rende una soluzione adottabile da una pubblica amministrazione, non
  solo dimostrabile a un meetup?

Da quella discussione è emerso un problema concreto, che diventa il brief
dell'Impact Lab del 3 ottobre — una build session pratica in cui la community
lavora insieme a una soluzione.

## Perché questo repository

Partecipo all'Impact Lab come builder e mi sto muovendo in anticipo: questo
repository raccoglie la preparazione fatta prima dell'evento, così da
arrivare il 3 ottobre con contesto concreto invece che a mani vuote.

## Struttura

- [`research/`](research/) — note di ricerca sui servizi del Comune di Milano,
  le barriere di accesso reali e le iniziative già esistenti (es. REMID@),
  come base di contesto prima di conoscere il problema esatto scelto il
  9 settembre.
- [`scaffold/`](scaffold/) — uno scheletro tecnico minimo (backend FastAPI +
  Claude API, frontend di chat senza dipendenze) pronto da clonare ed
  estendere velocemente durante le giornate di build.
- [`examples/typesafe-noul-urgenza/`](examples/typesafe-noul-urgenza/) —
  esempio di utilizzo delle [TypeSafe AI API](https://docs.typesafe.ai/) per
  rilevare il tono di urgenza in un messaggio, con la primitiva Noul (vedi
  nota su RLCD più sotto). Un possibile complemento all'assistente
  conversazionale in `scaffold/`: smistare per priorità le richieste dei
  cittadini prima ancora di rispondere.

## Nota su RLCD (Reinforcement Learning for Calibrated Decisions)

Le [TypeSafe AI API](https://docs.typesafe.ai/) (usate nell'esempio
`examples/typesafe-noul-urgenza/`) seguono un approccio diverso da Claude:
invece di generare testo, il loro modello `jev-latest` è addestrato con un
metodo che chiamano **RLCD — Reinforcement Learning for Calibrated
Decisions**, descritto nella documentazione come un metodo che "trains
TypeSafe to return decisions and calibrated probabilities instead of
generated text" ([fonte](https://docs.typesafe.ai/introduction/machine-learning-primer)).

In pratica: a una domanda sì/no (primitiva [`Noul`](https://docs.typesafe.ai/primitives/noul))
il modello non risponde con una frase, ma con un numero tra 0 e 1 — la
probabilità calibrata che la risposta sia "sì". "Calibrata" significa che,
su tante previsioni, le risposte a cui il modello assegna probabilità 0.8
dovrebbero rivelarsi corrette circa l'80% delle volte: la sicurezza
dichiarata riflette l'affidabilità reale, non solo la sicurezza con cui il
testo "suona giusto" (come nell'RLHF usato per i chatbot).

Perché interessa questo repository: è un tassello utile per la domanda
"cosa succede quando il sistema sbaglia" posta durante la Claude
Conversation del 9 settembre — un numero calibrato permette di decidere in
modo esplicito, nel codice, sotto quale soglia di confidenza una richiesta
del cittadino deve passare a un operatore umano invece che essere gestita
in automatico.

## Da fare prima del 3 ottobre

- [ ] Recuperare il problema concreto scelto durante la Claude Conversation
  del 9 settembre (canale della community:
  [t.me/+Rt7yOpOAp7A1NDQ0](https://t.me/+Rt7yOpOAp7A1NDQ0)).
- [ ] Aggiornare `research/` con quel problema specifico e con eventuali
  testimonianze raccolte durante la serata.
- [ ] Validare lo scaffold tecnico contro il problema reale, non solo contro
  le ipotesi generiche in queste note.
