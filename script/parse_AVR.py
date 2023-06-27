"""
Medecin malgre lui
== ACTE
\n\n
-- SCENE {numscene}
\n
Character list
\n\n
    {character} {comment}
    {comment}
    \n
        {verse}
        {verse}
"""

import json
import re
import pandas as pd


if __name__ == "__main__":
    input_filename = "../textes/original/l-avare.txt"
    output_filename = "../textes/original/l-avare.json"
    char_pattern = r"(SGANARELLE|MARTINE|M. ROBERT|GÉRONTE|LÉANDRE|LUCINDE|JACQUELINE|PERRIN|LUCAS|VALÈRE|THIBAUT)"
    acte_count = 0
    scene_count = 0

    lines = []
    with open(input_filename, "r") as file:
        for line in file:
            lines.append(line)

    items = []
    for n in range(len(lines)):
        line = lines[n].strip()

        if "ACTE " in line:
            # reset scene count
            acte_count += 1
            scene_count = 0
            items.append(
                {
                    "category": "acte",
                    "acte": acte_count,
                    "scene": 1,
                    # "pos": n + 1,
                    "text": line,
                }
            )
        elif "Scène" in line:
            scene_str = line.split('-')[0].strip()
            char_list = line.split('-')[1].strip()

            scene_count += 1
            items.append(
                {
                    "category": "scene",
                    "acte": acte_count,
                    "scene": scene_count,
                    # "pos": n + 1,
                    "text": scene_str,
                }
            items.append(
                {
                    "category": "char_list",
                    "acte": acte_count,
                    "scene": scene_count,
                    # "pos": n + 1,
                    "text": char_list,
                }

            )

        elif "- Valère -" in line:
            items.append(
                {
                    "category": "character",
                    "acte": acte_count,
                    "scene": scene_count,
                    # "pos": n + 1,
                    "text": line,
                }
            )
        elif "-action- (" in line:
            items.append(
                {
                    "category": "action",
                    "acte": acte_count,
                    "scene": scene_count,
                    # "pos": n + 1,
                    "text": line,
                }
            )
        else:
            paragraph = []
            while (line.strip() != "") & (n < len(lines) - 1):
                paragraph.append(line)
                n +=1
                line = lines[n].strip()

                items.append(
                    {
                        "category": "replique",
                        "acte": acte_count,
                        "scene": scene_count,
                        "text": "\n".join(paragraph),
                    }
                )

    items = pd.DataFrame(items)
    items = items[items.text != ""].copy()



    # post parsing
    # remove []
    items["text"] = items.text.apply(lambda t: re.sub(r"\(\d+\)", "", t))

    # verse_id
    verse_id = 0
    for i, d in items.iterrows():
        if d["category"] == "character":
            verse_id += 1
        items.loc[i, "verse_id"] = verse_id
    items["verse_id"] = items.verse_id.astype(int)

    items.loc[items.category == 'acte', 'verse_id' ] = 0
    items.loc[items.category == 'scene', 'verse_id' ] = 0
    items.loc[items.category == 'character list', 'verse_id' ] = 0

    # anomaly: "== ACTE ..." as replique => delete
    # items = items.drop(index = items[(items.category == 'replique') & (items.text.str.contains('== ACTE'))].index).copy()
    items.reset_index(drop = True, inplace = True)

    items = items[['pos','acte', 'scene', 'category', 'verse_id', 'text']]

    assert items[(items.acte == 1) & (items.scene == 1)].shape[0] == 105
    # save
    with open(output_filename, "w", encoding="utf-8") as f:
        items.to_json(f, force_ascii=False, orient="records", indent=4)
