import openai
import os
import random

def get_completion(prompt, model="gpt-3.5-turbo", temp=0.5):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature = temp,  
    )
    return response.choices[0].message["content"]




def analyze(sentence, model="gpt-3.5-turbo", temp=0):
    prompt = f"""
    Analyse grammaticalement la phrase entre parenthese et ecris les resultats de l'analyse au point de vue des accords en genre et en nombre.
    Si la phrase contient des erreurs de grammaires, liste ces erreurs et écris la phrase corrigé.
    ({sentence}). 
    """
    prompt = f"""
    Si la phrase suivante contient des erreurs de grammaires, liste ces erreurs et écris la phrase corrigé:
    {sentence}. 
    """

    prompt = f"""
    Fais les tâches suivantes:
    1. Si la phrase entre parenthèse contient des erreurs de grammaires, liste ces erreurs,
    2. écris la phrase corrigé.
    3. Écris l'analyse grammaticale de la phrase corrigée, au point de vue des accords en genre et en nombre.

    utilise le format suivant pour tes réponses:
    Erreurs: <liste des erreurs grammaticales>
    Phrase corrigée: <phrase corrigée>
    Analyse: <liste de l'analyse grammaticale>

    Insère une ligne entre chaque réponse.
    ({sentence})
    """
    prompt = f"""
    Ecris une série de phrases sur ce que font les oiseaux au printemps. Utilise des noms d'oiseaux précis.
    Mets les phrases au singulier.
    """

    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"], prompt

def feedback(sentence):
   prompt = f"""
   La phrase entre parenthèses est-elle correct grammaticalement?
   ({sentence})
   Si la phrase n'est pas correcte:
   - explique les erreurs 
   - écris la phrase corrigée à la ligne précédée de ---
   """
   response =get_completion(prompt, model="gpt-3.5-turbo", temp=0.5) 
   return response,prompt 


if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")

    del_start = "["
    del_end= "]"
    
    if False:
        prompt = f"""
            Ecris une série de phrases sur ce que fait un oiseau au printemps. 
            Utilise des noms d'oiseaux précis.
            Mets les phrases au singulier.
        """
        response =get_completion(prompt, model="gpt-3.5-turbo", temp=0.5) 
        print(response)

    if True:
        with open('sentences.txt') as file:
            lines = [line.rstrip() for line in file]

        sentence = random.choice(lines)
        print(f"Mettre la phrase au pluriel: \n{sentence} ")
        answer = input(">> ")
        
        print("-- essai 1")
        response, prompt =feedback(answer)
        print(prompt)
        correct = sentence[sentence.find(del_start)+1:sentence.find(del_end)]

        print(response)
        print(f"correct: {correct}")

        print("-- essai 2")
        response, prompt =feedback(answer)
        print(prompt)
        print(response)






