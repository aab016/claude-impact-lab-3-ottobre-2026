"""
Esempio: rilevare se un messaggio di un cittadino trasmette urgenza,
usando la primitiva Noul delle TypeSafe AI API.

Contesto: nei servizi pubblici (Contact Center, sportelli, moduli di
segnalazione) può essere utile dare priorità a chi scrive in una situazione
urgente ("sono tre giorni che aspetto una risposta e devo partire domani")
rispetto a una richiesta informativa generica. Noul risponde a domande
sì/no restituendo la probabilità calibrata che la risposta sia "sì",
invece di generare testo libero — vedi la nota su RLCD nel README
principale del repository.

Documentazione:
- Primitiva Noul: https://docs.typesafe.ai/primitives/noul
- SDK Python:     https://docs.typesafe.ai/sdk/python

Setup:
    pip install typesafe-sdk
    export TYPESAFE_API_KEY=...   # https://console.typesafe.ai/
"""

from typesafe_sdk import Noul, TypeSafeClient

# Messaggi di esempio: alcuni con tono urgente, altri no.
MESSAGGI_DI_ESEMPIO = [
    "Aiuto! Sono tre giorni che il pagamento non va a buon fine e devo "
    "presentare il documento domani mattina, cosa faccio?",
    "Buongiorno, volevo sapere quali documenti servono per il rinnovo "
    "della carta d'identità, non c'è fretta.",
    "Ho già scritto due volte e nessuno mi ha risposto, mio figlio deve "
    "iscriversi a scuola entro venerdì e non so come fare.",
    "Solo per curiosità, a che ora chiude lo sportello anagrafe il giovedì?",
]


def rileva_urgenza(client: TypeSafeClient, messaggio: str) -> float:
    """Restituisce la probabilità (0-1) che il messaggio trasmetta urgenza."""
    risultato = client.system_one(
        state=messaggio,
        questions={
            "is_urgent": Noul(
                instructions="Il messaggio trasmette un tono di urgenza?",
                criteria={
                    "true": (
                        "Chi scrive segnala una scadenza imminente, un "
                        "disagio che si protrae da tempo senza risposta, o "
                        "chiede esplicitamente un intervento rapido."
                    ),
                    "false": (
                        "Richiesta informativa generica, senza scadenze o "
                        "pressione temporale."
                    ),
                },
            )
        },
    )
    return risultato.nouls["is_urgent"].noul


def main() -> None:
    with TypeSafeClient() as client:
        for messaggio in MESSAGGI_DI_ESEMPIO:
            probabilita = rileva_urgenza(client, messaggio)
            etichetta = "URGENTE" if probabilita >= 0.5 else "non urgente"
            print(f"[{probabilita:.2f} -> {etichetta}] {messaggio}")


if __name__ == "__main__":
    main()
