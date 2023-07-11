from lingx.core.lang_model import get_nlp_object
from lingx.utils.lx import get_sentence_lx



nlp = get_nlp_object("fr", use_critt_tokenization = False, package="partut")


input = "Oui, je conçois, mon frère, quel doit être votre chagrin."
input = "Oui, mon frère, je comprends ton chagrin."

input = "Mais, a vous dire vrai, le succès me donne de l'inquiétude. Je crains fort de vous aimer un peu plus que je ne devrais."
get_sentence_lx(input,nlp, result_format="segment", complexity_type="idt", aggregation_type="mean")
input = "Mais, pour être honnête, le succès me rend inquiète ; et j'ai peur de t'aimer un peu trop."
get_sentence_lx(input,nlp, result_format="segment", complexity_type="idt", aggregation_type="mean")

input = "Je crains fort de vous aimer un peu plus que je ne devrais."
get_sentence_lx(input,nlp, result_format="segment", complexity_type="dlt", aggregation_type="mean")
input = "J'ai peur de t'aimer un peu trop."
get_sentence_lx(input,nlp, result_format="segment", complexity_type="dlt", aggregation_type="mean")

input = "Non, c'est un homme extraordinaire, qui se plaît à cela, fantasque, bizarre, quinteux, et que vous ne prendriez jamais pour ce qu'il est. Il va vêtu d'une façon extravagante, affecte quelquefois de paroître ignorant, tient sa science renfermée, et ne fuit rien tant tous les jours que d'exercer les merveilleux talents qu'il a eus du Ciel pour la médecine."
get_sentence_lx(input,nlp, result_format="segment", complexity_type="idt_dlt", aggregation_type="mean")
input = "Non, c'est un personnage étrange et fantasque. Il s'habille de manière extravagante, parfois il feint d'être ignorant et cache sa connaissance médicale. Il évite de pratiquer la médecine autant que possible."
get_sentence_lx(input,nlp, result_format="segment", complexity_type="idt_dlt", aggregation_type="mean")



from lingx.metrics.monolingual.le import get_le_score
input = "Non, c'est un homme extraordinaire, qui se plaît à cela, fantasque, bizarre, quinteux, et que vous ne prendriez jamais pour ce qu'il est. Il va vêtu d'une façon extravagante, affecte quelquefois de paroître ignorant, tient sa science renfermée, et ne fuit rien tant tous les jours que d'exercer les merveilleux talents qu'il a eus du Ciel pour la médecine."
get_le_score(input,nlp, aggregator="mean")
input = "Non, c'est un personnage étrange et fantasque. Il s'habille de manière extravagante, parfois il feint d'être ignorant et cache sa connaissance médicale. Il évite de pratiquer la médecine autant que possible."
get_le_score(input,nlp,  aggregator="mean")


--
stanza.download(lang="fr",package=None,processors={"tokenize":"combined"})
stanza.download(lang="fr",package=None,processors={"ner":"wikiner"})
stanza.download(lang="fr",package=None,processors={"tokenize":"combined"})
nlp = stanza.Pipeline(lang='fr', processors='tokenize')
doc = nlp('This is a test sentence for stanza. This is another sentence.')

input = "Non, c'est un personnage étrange et fantasque. Il s'habille de manière extravagante, parfois il feint d'être ignorant et cache sa connaissance médicale. Il évite de pratiquer la médecine autant que possible."
doc = nlp(input)
