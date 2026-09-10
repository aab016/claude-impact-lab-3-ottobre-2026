"""
Scaffold per l'Impact Lab del 3 ottobre 2026.

Assistente conversazionale che aiuta i cittadini a orientarsi nei servizi
del Comune di Milano, con particolare attenzione a chi trova barriere di
accesso (linguaggio burocratico, screen reader, età, nuova immigrazione).

Punto di partenza volutamente minimo: un endpoint di chat in streaming sopra
Claude, con un system prompt che incorpora i principi emersi nelle note di
ricerca (research/comune-milano-servizi-accessibilita.md):
- non inventare procedure: rimanda sempre a fonti ufficiali quando non è sicuro
- indica sempre una via di uscita umana (Contact Center, Case di Quartiere, sportello)
- usa un linguaggio semplice e accessibile

Da estendere durante l'hackathon, ad esempio con:
- ricerca/RAG sulle pagine ufficiali del Comune invece del solo system prompt
- multilingua
- integrazione con i facilitatori digitali REMID@
"""

import os

import anthropic
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

MODEL = "claude-opus-5"

SYSTEM_PROMPT = """Sei un assistente che aiuta le persone a orientarsi tra i \
servizi online del Comune di Milano (certificati anagrafici, stato civile, \
iscrizioni scolastiche, permessi, servizi sociali, mobilità).

Il tuo pubblico include persone che trovano barriere reali: chi non legge \
bene l'italiano burocratico, chi usa uno screen reader, persone anziane, \
persone arrivate in città da poco.

Regole:
1. Usa un linguaggio semplice, frasi brevi, evita gergo burocratico. Se devi \
   usare un termine tecnico (es. "ANPR", "SPID"), spiegalo in una frase.
2. Non inventare mai procedure, requisiti, scadenze o URL che non conosci con \
   certezza. Se non sei sicuro, dillo chiaramente e indirizza al canale \
   ufficiale giusto invece di indovinare.
3. Indica sempre, quando ha senso, come raggiungere un aiuto umano: il Centro \
   di supporto del Comune, uno sportello, o i Punti di Facilitazione Digitale \
   REMID@ nelle Case di Quartiere (pensati proprio per chi ha difficoltà con \
   SPID/CIE o con i servizi online).
4. Se la richiesta riguarda un caso limite, un'eccezione normativa, o rischia \
   di avere conseguenze legali, non decidere tu: spiega che serve la verifica \
   di un operatore comunale e come contattarlo.
5. Fai una domanda di chiarimento se la situazione della persona non è chiara, \
   invece di rispondere alla cieca.

Questo è un prototipo dimostrativo per un hackathon (Claude Impact Lab), non \
un canale ufficiale del Comune di Milano: se pertinente, ricordalo."""


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]


app = FastAPI(title="Assistente servizi pubblici - Claude Impact Lab")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic()


@app.get("/api/health")
def health():
    return {"status": "ok", "model": MODEL}


@app.post("/api/chat")
def chat(request: ChatRequest):
    messages = [{"role": m.role, "content": m.content} for m in request.messages]

    def event_stream():
        with client.messages.stream(
            model=MODEL,
            max_tokens=4096,
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            output_config={"effort": "medium"},
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                yield text

    return StreamingResponse(event_stream(), media_type="text/plain")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
