import function_nltk as nlp
from phrase_nlp import phrase_nlp
import json

phrase = input("Digite a requisição: ")
#phrase = "computador possui documentos com data de nascimento ?"

def error(phrase):
    with open(r"data\error_data.json","r") as p2:
        aux = json.load(p2)
        print(aux)
        aux.append(phrase)
    with open(r"data\error_data.json","w") as p2:
        json.dump(aux,p2)
try:
    p1 = phrase_nlp(phrase)
except:
    error(phrase)
    exit(-1)

# testa 
if type(p1.get_return()) is not dict:
    error(phrase)
    print("Input Error")
else:
    with open(r"G:\My Drive\Python\projeto estagio\data\request_data.json","w") as arq_j:
        json.dump(p1.get_return(),arq_j)

#print(p1)