'''
results should
- rewrite in modern french
- keep dialogue structure: no summary
- keep most or all verses
- reduce length of long verses
- be able to perform on extracts or full version of the scene
'''

import openai
import os
import re
import time
import pandas as pd
pd.options.display.max_columns = 100
pd.options.display.max_rows = 60
pd.options.display.max_colwidth = 100
pd.options.display.precision = 10
pd.options.display.width = 160
pd.set_option("display.float_format", "{:.2f}".format)
import numpy as np

def get_completion(prompt, model="gpt-3.5-turbo", temp=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature = temp,
    )
    return response.choices[0].message["content"]


instructions = [
    '''Le texte suivant est une pièce de theatre de Molière. Reecris chaque vers en francais avec un vocabulaire simple et moderne.'''
]

def save(df, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        df.to_json(f , force_ascii=False, orient = 'records', indent = 4)


if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")
    model   ="gpt-3.5-turbo"
    filename = 'textes/medecin-malgre-lui_02.json'

    df = pd.read_json(filename)

    if False:
        cols = ['acte', 'scene', 'texte' ]
        df = df[cols]
        save(df, filename)

    # filename = 'textes/sandbox_medecin-malgre-lui.json'
    for i, d in df.iterrows():
        print('=='*20)
        print(d.texte[:200])
        print('=='*20)
        print()
        k = 0
        for instruction in instructions:
            # next instructions
            k +=1
            m_col = f"modern_{str(k).zfill(2)}"
            # p_col = f"prompt_{str(k).zfill(2)}"
            # cond = np.isnan(df.loc[i, m_col]) & np.isnan(df.loc[i, p_col])
            if m_col not in df.columns:
                df[m_col] = None
            cond = df.loc[i, m_col] is None

            if cond:
                print(f">> new {m_col}")
                prompt = '\n'.join([instruction, f"le texte : {d.texte}"])
                response = get_completion(prompt, model=model, temp=0)
                # response = f"{k} {m_col} {d.texte[:10]}"
                response = re.sub('\n\n', '\n', response)

                df.loc[i, m_col] = response
                save(df, filename)

                print('--'*20)
                print(instruction)
                print('--'*10)
                print(response[:200])
                print('*** sleep 30')
                time.sleep(30)
                print('*** wake up')
                print()
