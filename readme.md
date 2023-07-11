# flow

1. parse texte original into lines
    - script: parse_{XXX}
    - input: ./textes/original/medecin-malgre-lui.txt
    - resultat: ./textes/original/medecin-malgre-lui.json
    - input: ./textes/original/l-avare.txt
    - resultat: ./textes/original/l-avare.json

1.1. test different prompts
    - script: streamlit/pages/build_prompt
    - input: ./textes/original/l-avare.json
    - resultat: online

2. GPT transliteration

    write config file for experiment

    - script: modernize_{XXX}
    - input: ./textes/original/medecin-malgre-lui.json
    - input: ./textes/original/l-avare.json
    
    - resultat: ./textes/{experiment}/acte_xx_scene_xx.json

2.1 Review preparation
    - script: aggregate_experiments.py
    - input: ./textes/{experiment}/acte_xx_scene_xx.json
    - output: ./textes/review/medecin-malgre-lui_review.json

3. review - choose best version for each line
    - streamlit: ./pages/compare
    - input: ./textes/review/medecin-malgre-lui_review.json
    - output: ./textes/review/reviewed_acte_xx_scene_xx.json

4. finalize: create final json file for online display
    - script: finalize
    - from: ./textes/review/reviewed_acte_xx_scene_xx.json
    - to: ./textes/online/*.json



# vocabulaire theatre
- Une tirade est une réplique longue.
    -  La tirade ralentit le rythme de l'intrigue ; cela correspond à un moment important où l'attention est centrée sur un personnage qui développe ses pensées.

- Un monologue est une tirade prononcée par un personnage seul sur scène.
    - Au théâtre, le spectateur ne peut connaitre les pensées d'un personnage que si celui- ci les exprime à voix haute.

- Un aparté est une réplique prononcée « à part »
    - (pour qu'elle soit entendue par un personnage mais pas par un autre, ou alors quand elle n'est pas adressée aux autres personnages mais aux spectateurs).

- La stichomythie est une succession de répliques brèves.
    - Elle crée un rythme très rapide, dynamique, qui convient bien aux scènes d'affrontement entre deux personnages.
