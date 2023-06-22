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
    input_filename = "../textes/original/medecin-malgre-lui.txt"
    output_filename = "../textes/original/medecin-malgre-lui.json"
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
        if "== ACTE" in line:
            # reset scene count
            acte_count += 1
            scene_count = 0
            items.append(
                {
                    "type": "acte",
                    "acte": acte_count,
                    "scene": 1,
                    "pos": n + 1,
                    "text": line,
                }
            )
        if "-- SCENE" in line:
            scene_count += 1
            items.append(
                {
                    "type": "scene",
                    "acte": acte_count,
                    "scene": scene_count,
                    "pos": n + 1,
                    "text": line,
                }
            )
            n += 2
            line = lines[n].strip()
            items.append(
                {
                    "type": "character list",
                    "acte": acte_count,
                    "scene": scene_count,
                    "pos": n + 1,
                    "text": line,
                }
            )
            n += 2

            while ("-- SCENE" not in line) & (n < len(lines) - 1):
                n += 1
                line = lines[n].strip()
                if re.match(char_pattern, line):
                    # catches character over multiple lines
                    text = []
                    while (line != "") & (n < len(lines) - 1):
                        text.append(line)
                        n += 1
                        line = lines[n].strip()

                    items.append(
                        {
                            "type": "character",
                            "acte": acte_count,
                            "scene": scene_count,
                            "pos": n,
                            "text": " ".join(text),
                        }
                    )

                else:
                    # catches repliques over multiple lines
                    text = []
                    while (
                        (line != "") & (n < len(lines) - 1) & ("-- SCENE" not in line)
                    ):
                        text.append(line)
                        n += 1
                        line = lines[n].strip()

                    items.append(
                        {
                            "type": "replique",
                            "acte": acte_count,
                            "scene": scene_count,
                            "pos": n,
                            "text": " ".join(text),
                        }
                    )

    items = pd.DataFrame(items)
    items = items[items.text != ""].copy()

    assert items[(items.acte == 1) & (items.scene == 1)].shape[0] == 105
    assert items[(items.acte == 1) & (items.scene == 2)].shape[0] == 105
    assert items[(items.acte == 1) & (items.scene == 3)].shape[0] == 3
    assert items[(items.acte == 1) & (items.scene == 4)].shape[0] == 72
    assert items[(items.acte == 1) & (items.scene == 5)].shape[0] == 213
    assert items[(items.acte == 3) & (items.scene == 1)].shape[0] == 23
    assert (
        items[
            items.text.str.contains("GÉRONTE") & (items["type"] == "character")
        ].shape[0]
        == 110
    )
    assert items[items.text.str.contains("GÉRONTE")].shape[0] == 121
    assert (
        items[
            items.text.str.contains("LÉANDRE") & (items["type"] == "character")
        ].shape[0]
        == 16
    )
    assert (
        items[
            items.text.str.contains("LÉANDRE") & (items["type"] == "character list")
        ].shape[0]
        == 5
    )
    assert (
        items[
            items.text.str.contains("SGANARELLE") & (items["type"] == "character")
        ].shape[0]
        == 226
    )

    assert len(items[items.pos == 239].text.values[0]) == 101

    # post parsing
    # remove []
    items["text"] = items.text.apply(lambda t: re.sub(r"\[\d+\]", "", t))

    items.loc[items["type"] == "acte", "text"] = items[
        items["type"] == "acte"
    ].text.apply(lambda t: t[3:])
    items.loc[items["type"] == "scene", "text"] = items[
        items["type"] == "scene"
    ].text.apply(lambda t: t[3:])

    # save
    with open(output_filename, "w", encoding="utf-8") as f:
        items.to_json(f, force_ascii=False, orient="records", indent=4)
