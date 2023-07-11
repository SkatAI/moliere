# metrics

import openai
import os
import re, json, csv
import time, datetime
from datetime import timedelta
import pandas as pd
import argparse
import glob

pd.options.display.max_columns = 100
pd.options.display.max_rows = 60
pd.options.display.max_colwidth = 100
# pd.options.display.max_colwidth = None

pd.options.display.precision = 10
pd.options.display.width = 160
pd.set_option("display.float_format", "{:.2f}".format)
import numpy as np

from lingx.core.lang_model import get_nlp_object
from lingx.utils.lx import get_sentence_lx
from lingx.metrics.monolingual.le import get_le_score
from lingx.metrics.monolingual.nnd import get_nnd_score

# import lingx.core.lang_model as lm
#
# lm.download_stanza_model("fr", package="partut")
# lm.download_stanza_model("fr", package="gsd")

class ReadScore():

    def __init__(self, nlp, text):
        self.nlp = nlp
        self.text = text
        self.doc = self.nlp[0](self.text)

    def score_sentences(self):
        self.idts = []
        self.les = []
        for i, sentence in enumerate(self.doc.sentences):
            tk_scores, idt = get_sentence_lx(
                sentence.text,
                self.nlp,
                result_format="segment",
                complexity_type="idt",
                aggregation_type="mean"
            )
            le = get_le_score(sentence.text,self.nlp, aggregator="mean")
            self.idts.append(idt)
            self.les.append(le)

            print(i, sentence.text, idt, le)

    def score(self):
        self.tk_scores, self.idt = get_sentence_lx(
            self.text,
            self.nlp,
            result_format="segment",
            complexity_type="idt",
            aggregation_type="mean"
        )
        self.le = get_le_score(self.text,self.nlp, aggregator="mean")

        # self.tk_scores, self.idt_dlt = get_sentence_lx(
        #     self.text,
        #     self.nlp,
        #     result_format="segment",
        #     complexity_type="idt_dlt",
        #     aggregation_type="mean"
        # )

        # self.tk_scores, self.dlt = get_sentence_lx(
        #     self.text,
        #     self.nlp,
        #     result_format="segment",
        #     complexity_type="dlt",
        #     aggregation_type="mean"
        # )

        # self.nnd = get_nnd_score(
        #               self.text,
        #               nlp=self.nlp,
        #               aggregator="mean",  # choose `sum`, `max` or `mean`
        #               ploraity = False
        #               )
        # self.nnd_pl = get_nnd_score(
        #               self.text,
        #               nlp=self.nlp,
        #               aggregator="mean",  # choose `sum`, `max` or `mean`
        #               ploraity = True
        #               )  # if set to `True` the score will be absolute.

        return self

    def to_dict(self):

        return {
            "tokens": len(self.tk_scores),
            "sentences": len(self.doc.sentences),
            "idt": self.idt,
            "le": self.le,
            "text": self.text,
            # "idt_dlt": self.idt_dlt,
            # "dlt": self.dlt,
            # "idts": self.idts,
            # "les": self.les,
            # "nnd": self.nnd,
            # "nnd_pl": self.nnd_pl,
            # "tk_scores": [ tk[1] for tk in self.tk_scores  ],
        }

    def __str__(self):
        json_formatted_str = json.dumps(
            self.to_dict(), ensure_ascii=False,
            indent=4,
        ).encode('utf8')
        return json_formatted_str.decode()


if __name__ == "__main__":

    inputs = [
        "Oui, je conçois, mon frère, quel doit être votre chagrin.",
        "Oui, mon frère, je comprends ton chagrin.",
        "Oui, je comprends ton chagrin mon frère.",
        "Oui, je comprends ton chagrin.",
        "Je comprends ton chagrin.",
        "Je crains fort de vous aimer un peu plus que je ne devrais.",
        "J'ai peur de t'aimer un peu trop.",
        "Non, c'est un homme extraordinaire, qui se plaît à cela, fantasque, bizarre, quinteux, et que vous ne prendriez jamais pour ce qu'il est. Il va vêtu d'une façon extravagante, affecte quelquefois de paroître ignorant, tient sa science renfermée, et ne fuit rien tant tous les jours que d'exercer les merveilleux talents qu'il a eus du Ciel pour la médecine.",
        "Non, c'est un personnage étrange et fantasque. Il s'habille de manière extravagante, parfois il feint d'être ignorant et cache sa connaissance médicale. Il évite de pratiquer la médecine autant que possible.",
        "Mais, a vous dire vrai, le succès me donne de l'inquiétude ; et je crains fort de vous aimer un peu plus que je ne devrais.",
        "Mais, pour être honnête, le succès me rend inquiète. Et j'ai peur de t'aimer un peu trop.",

    ]


    nlp = get_nlp_object("fr", use_critt_tokenization = False, package="gsd")
    data = []
    for text in inputs:
        rs = ReadScore(nlp, text).score()
        data.append(rs.to_dict())

    data = pd.DataFrame(data)
