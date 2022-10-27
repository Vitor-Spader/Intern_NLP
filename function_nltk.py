from ast import Num
from lib2to3.pgen2 import token
import nltk,json


stopwords = nltk.corpus.stopwords.words('portuguese')
'''
legenda
[det] determinante
1- Quantidade de arquivo
2- Quantidade de dispositivo
3- Identificação do dispositivo
4- Identificação do arquivo

[doc0,doc1,doc2,doc3,doc4,doc5,doc6] documento
1-RG
2-CPF
3-passaporte
4- pis
5-matricula
6-data de nascimento
7- cartão do SUS

[8] dispositivo
1-computador
2-celular
3-dispositivo(indeterminado)
[9] ID dispositivo
'''
#base de dados
def get_bd(all_tags=False):


    with open(r"data\lista_dispositivos.json","r") as x0:
        l0 = json.load(x0)

    with open(r"data\tags.json","r") as x2:
        aux = json.load(x2)
        l1 = aux["w_doc"]
        l2 = aux["w_disp"]
        if all_tags == True:
            l3 = aux["w_rg"]
            l4 = aux["w_cpf"]
            l5 = aux["w_pass"]
            l6 = aux["w_pis"]
            l7 = aux["w_matr"]
            l8 = aux["w_nasc"]
            l9 = aux["w_sus"]
            return l3,l4,l5,l6,l7,l8,l9

    return l0,l1,l2

#adiciona legenda a instancia que seja None no dicionario
def dict_def(question,num):
    for x,y in question.items():
        if y is None:
            question[x] = num
            break
    return question

def word_related(token_phrase,question):
    rg,cpf,passport,pis,matr,nasc,sus = get_bd(True)
    for x in rg:
        if type(x) is tuple:
            v,y = x
            if x in token_phrase and y in token_phrase:
                question = dict_def(question,1)
                break  
        if x in token_phrase:
            question = dict_def(question,1)
            break
    for x in cpf:
        if type(x) is tuple:
            v,y = x
            if x in token_phrase and y in token_phrase:
                question = dict_def(question,2)
                break  
        if x in token_phrase:
            question = dict_def(question,2)
            break
    for x in passport:
        if type(x) is tuple:
            v,y = x
            if x in token_phrase and y in token_phrase:
                question = dict_def(question,3)
                break  
        if x in token_phrase:
            question = dict_def(question,3)
            break
    for x in pis:
        if type(x) is tuple:
            v,y = x
            if x in token_phrase and y in token_phrase:
                question = dict_def(question,4)
                break    
        if x in token_phrase:
            question = dict_def(question,4)
            break
    for x in matr:
        if type(x) is tuple:
            v,y = x
            if x in token_phrase and y in token_phrase:
                question = dict_def(question,5)
                break
        if x in token_phrase:
            question = dict_def(question,5)
            break
    for x in nasc:
        if type(x) is tuple:
            v,y = x
            if x in token_phrase and y in token_phrase:
                question = dict_def(question,6)
                break
        if x in token_phrase:
            question = dict_def(question,6)
            break
    for x in sus:
        if type(x) is tuple:
            v,y = x
            if x in token_phrase and y in token_phrase:
                question = dict_def(question,7)
                break
        if x in token_phrase:
            question = dict_def(question,7)
            break
    return question

#retorna o codigo que representa a a frase processada
def return_question(token_phrase):

    #base de dados de dispositivos
    list_disp,doc_tag,disp_tag = get_bd()
    #list_disp = lista de dispositivos(ID)
    #doc_tag = tags para documento e sinonimos
    #disp_tag = tags para tipos de dispositivos


    #inicializa vetor de retorno
    #add docs
    question = {"det":None,"doc0":None,"doc1":None,"doc3":None,"doc4":None,"doc5":None,"doc6":None,"disp":None,"ID_disp":None}
    #verifica palavras e seus relacionamentos na 
    if "quant" in token_phrase:
        index = token_phrase.index("quant") + 1
        if token_phrase[index] in doc_tag: #busca a palavra document/arquiv...
            question["det"] = 1
            for x in disp_tag:
                if x in token_phrase:
                    question["disp"] = 3
                    index = token_phrase.index(x) + 1
                    if token_phrase[index] in list_disp:
                        question["ID_disp"] = token_phrase[index]
                        break
            question = word_related(token_phrase,question)
        elif token_phrase[index] in disp_tag: 
            question["det"] = 2
            for x in doc_tag:
                if x in token_phrase:
                    question = word_related(token_phrase,question)
                    break
        else:
            return "Error"
    elif "qual" in token_phrase:
        index = token_phrase.index("qual") + 1
        question["det"] = 3
        if token_phrase[index] in doc_tag:
            question["det"] = 4
            for x in disp_tag:
                if x in token_phrase:
                    question["disp"] = 3
                    index = token_phrase.index(x) + 1
                    if token_phrase[index] in list_disp:
                        question["ID_disp"] = token_phrase[index]
                        break
            question = word_related(token_phrase,question)
        elif token_phrase[index] == "comput" or token_phrase[index] == "celul" or token_phrase[index] == "smart" or token_phrase[index] == "disposi": 
            question["det"] = 3
            for x in doc_tag:
                if x in token_phrase:
                    question = word_related(token_phrase,question)
                    break
    # frase sem "Qual"
    else:
        for x in doc_tag:
            if x in token_phrase:
                for y in disp_tag:
                    if y in token_phrase:
                        if token_phrase.index(x) > token_phrase.index(y):
                            question["det"] = 3
                            question = word_related(token_phrase,question)
                            break
                        else:
                            question["det"] = 4
                            question = word_related(token_phrase,question)
                            break
                if question["det"] is None:
                    question["det"] = 4
                    for x in list_disp:
                        if x in token_phrase:
                            question["ID_disp"] = token_phrase.index(x)
                    question = word_related(token_phrase,question)
                break
        if question["det"] is None:
            for x in disp_tag:
                if x in token_phrase:
                    question["det"] = 3
                    question["disp"] = 3
                    for y in list_disp:
                        if y in token_phrase:
                            question["ID_disp"] = token_phrase.index(x)
                    question = word_related(token_phrase,question) 
    #print(question)
    return question
        

    

#processa a frase restando somente o radical das palavras
def aply_stemmer(token_phrase):
    stemmer = nltk.stem.RSLPStemmer()
    comstemming = []
    for word in token_phrase:
        #print(word)
        if word not in stopwords:
            #print(stemmer.stem(word))
            comstemming.append(str(stemmer.stem(word)))
    return comstemming

#transforma a frase em tokens
def token_stemm(phrase):
    return aply_stemmer(nltk.tokenize.word_tokenize(phrase))