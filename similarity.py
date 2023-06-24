import openai
import os
import re, json
import time, datetime
from datetime import timedelta
import pandas as pd

pd.options.display.max_columns = 100
pd.options.display.max_rows = 60
pd.options.display.max_colwidth = 100
pd.options.display.precision = 10
pd.options.display.width = 160
pd.set_option("display.float_format", "{:.2f}".format)
import numpy as np
from sentence_similarity import sentence_similarity


sentence_a = "Fi! c'est une bagatelle; allons, allons."
sentence_b = "Oh, c'est rien. Allez, allez."

model = sentence_similarity(model_name="distilbert-base-uncased", embedding_type="cls_token_embedding")
score = model.get_score(sentence_a, sentence_b, metric="cosine")
print(score)


model = sentence_similarity(model_name="distilbert-base-uncased", embedding_type="sentence_embedding")
score = model.get_score(sentence_a, sentence_b, metric="cosine")
print(score)


from sentence_transformers import SentenceTransformer, util


origin = ("Tu t'en lèveras plus matin.",)
origin = ("Tu te lèveras plus tard.",)
modern = ("Tu te lèveras plus tôt.",)


# Compute embedding for both lists
embedding_1 = model.encode("il fait chaud", convert_to_tensor=True)
embedding_2 = model.encode("il fait froid", convert_to_tensor=True)
embedding_2 = model.encode("je passe la tondeuse", convert_to_tensor=True)

score = util.pytorch_cos_sim(embedding_1, embedding_2)
print(score)


embedding_1 = model.encode("It's hot", convert_to_tensor=True)
embedding_2 = model.encode("I'm mowing the lawn", convert_to_tensor=True)

score = util.pytorch_cos_sim(embedding_1, embedding_2)
print(score)

# --
from sentence_transformers import SentenceTransformer

models = [
    "sentence-transformers/all-MiniLM-L6-v2",
    "sentence-transformers/all-mpnet-base-v2",
]

data = []
for model_name in models:
    model = SentenceTransformer(model_name)
    en_sentences = ["It's hot.", "C'est chaud.", "C'est froid"]
    fr_sentences = ["Cela m'est égal", "Je m'en fiche", "il est 12h"]
    en_embeddings = model.encode(en_sentences)
    fr_embeddings = model.encode(fr_sentences)
    print("--", model_name)
    score = util.pytorch_cos_sim(en_embeddings[0], en_embeddings[1])
    data.append(
        {
            "model": model_name,
            "lang": "en",
            "relation": "opposite",
            "score": np.round(float(score[0][0]), 3),
        }
    )

    print("en - opposite", np.round(float(score[0][0]), 3))
    score = util.pytorch_cos_sim(en_embeddings[0], en_embeddings[2])
    data.append(
        {
            "model": model_name,
            "lang": "en",
            "relation": "unrelated",
            "score": np.round(float(score[0][0]), 3),
        }
    )
    print("en - unrelated", np.round(float(score[0][0]), 3))
    score = util.pytorch_cos_sim(fr_embeddings[0], fr_embeddings[1])
    data.append(
        {
            "model": model_name,
            "lang": "fr",
            "relation": "opposite",
            "score": np.round(float(score[0][0]), 3),
        }
    )
    print("fr - opposite", np.round(float(score[0][0]), 3))
    score = util.pytorch_cos_sim(fr_embeddings[0], fr_embeddings[2])
    data.append(
        {
            "model": model_name,
            "lang": "fr",
            "relation": "unrelated",
            "score": np.round(float(score[0][0]), 3),
        }
    )
    print("fr - unrelated", np.round(float(score[0][0]), 3))

data = pd.DataFrame(data)

df = pd.read_json(output_filename).to_dict(orient="records")
text = df[idx][source].strip()
print(f"-- [{source}] tokens: {count_tokens(text)} verses: ", len(text.split("\n")))
# if show_text:
print(text.replace("\n", "\n\n"))
