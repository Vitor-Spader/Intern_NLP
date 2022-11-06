import function_nltk as nlp
from phrase_nlp import phrase_nlp
import json

#phrase = input("Digite a requisição: ")
phrase = "Quantos documentos com cpf e rg existem no computador 123456 e quais celulares possuem arquivos com cartão do sus e data de nascimento?"
#phrase = "Quanto documentos com rg e cpf existem no sistema?"


def error(phrase):
    p = []
    p.append(phrase)
    with open(r"data\error_data.json","a") as p2:
        json.dump(p,p2)
try:
    p1 = phrase_nlp(phrase)
except:
    error(phrase)
    exit(-1)

# testa se o retorno e o um dicionario
if type(p1.get_return()) is not dict:
    error(phrase)
    print("Input Error")
else:
    with open(r"data\request_data.json","w") as arq_j:
        json.dump(p1.get_return(),arq_j)

print(p1.get_return())