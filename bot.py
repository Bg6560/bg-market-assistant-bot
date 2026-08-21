import os

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from openai import OpenAI


TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


client = OpenAI(api_key=OPENAI_API_KEY)


# Chargement du catalogue BG-MARKET
try:
    with open("catalogue_bg_market.txt", "r", encoding="utf-8") as fichier:
        catalogue = fichier.read()
except:
    catalogue = "Catalogue indisponible."


instructions = """
Tu es BG-MARKET Assistant, assistant commercial officiel de BG-MARKET.

Ton rôle :
- Conseiller les clients sur les smartphones.
- Utiliser uniquement le catalogue fourni pour les prix.
- Les prix du catalogue sont les prix clients en FCFA.
- Ne jamais inventer un prix absent du catalogue.

Règles commerciales :

Si le téléphone est dans le catalogue :
- Donne le prix exact.
- Présente brièvement les caractéristiques disponibles.
- Encourage l'achat naturellement.

Si le téléphone n'est pas dans le catalogue :
Réponds :
"Je vérifie la disponibilité et je vous reviens."

Ne dis jamais :
"Je vais vérifier auprès de BG-MARKET"
car tu représentes déjà BG-MARKET.

Garantie :
- Elle dépend du modèle.
- Les modèles récents : 6 mois à 1 an.
- Les anciens modèles : environ une semaine à un mois.

Livraison :
- Abidjan : paiement à la livraison.
- Autres villes : le client paie le téléphone et les frais d'expédition avant l'envoi.

Signature obligatoire :
BG-MARKET, la marque qui garantit la confiance et la satisfaction.
"""


async def répondre(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message.text

    réponse = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": instructions + "\n\nCatalogue officiel BG-MARKET :\n" + catalogue
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )


    await update.message.reply_text(
        réponse.choices[0].message.content
    )


app = Application.builder().token(TELEGRAM_TOKEN).build()


app.add_handler(
    MessageHandler(filters.TEXT, répondre)
)


app.run_polling()
