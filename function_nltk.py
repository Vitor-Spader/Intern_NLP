import nltk,json

stopwords = nltk.corpus.stopwords.words('portuguese')
'''
legenda
[det] determinante
1- Quantidade de arquivo
2- Quantidade de dispositivo
3- Identificação do dispositivo
4- Identificação do arquivo
'''
#base de dados
def get_bd(mode="disp_tag_ID"):

    if mode == "docs":
        with open(r"data\tags_doc.json","r") as x1:
            docs = json.load(x1)
            return docs
    if mode == "disp_tag_ID":
        aux = []
        with open(r"data\lista_dispositivos.json","r") as x0:
            list_disp = json.load(x0)
        with open(r"data\tags_doc_type.json","r") as x2:
            doc_tag = json.load(x2)
        with open(r"data\tags_disp.json","r") as x3:
            disp_tag = json.load(x3)
        return list_disp,doc_tag,disp_tag

#adiciona legenda a instancia que seja None no dicionario
def dict_def(question,kword):
    for x,y in question.items():
        if x == "docs":
            question[x].append(kword)
            break
    return question

def word_related(token_phrase,question):
    docs = get_bd(mode="docs")
    #print(get_bd(mode="docs"))

    for x,y in docs.items():
        for z in y:
            if type(z) is list:
                if all(v in token_phrase for v in x):
                    question = dict_def(question,x)
                    break
            elif z in token_phrase:
                question = dict_def(question,x)
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
    question = {"det":[],"docs":[],"disp":[],"ID_disp":[]}
    #verifica palavras e seus relacionamentos na 
    if "quant" in token_phrase:
        index = token_phrase.index("quant") + 1
        if token_phrase[index] in doc_tag: #busca a palavra document/arquiv...
            question["det"].append("quanto_arq")
            for x in disp_tag:
                if x in token_phrase:
                    question["disp"].append(x)
                    index = token_phrase.index(x) + 1
                    if token_phrase[index] in list_disp:
                        question["ID_disp"].append(token_phrase[index])
                        break
            question = word_related(token_phrase,question)
        elif token_phrase[index] in disp_tag: 
            question["det"].append("quanto_disp")
            for x in doc_tag:
                if x in token_phrase:
                    question = word_related(token_phrase,question)
                    for x in list_disp:
                        if x in token_phrase:
                            question["ID_disp"].append(x)
                            break
                    break
        else:
            return "Error"
    if "qual" in token_phrase:
        index = token_phrase.index("qual") + 1
        if token_phrase[index] in doc_tag:
            question["det"].append("qual_doc")
            for x in disp_tag:
                if x in token_phrase:
                    question["disp"].append(x)
                    index = token_phrase.index(x) + 1
                    if token_phrase[index] in list_disp:
                        question["ID_disp"].append(token_phrase[index])
                        break
            question = word_related(token_phrase,question)
        elif token_phrase[index] in disp_tag: 
            question["det"].append("qual_disp")
            for x in doc_tag:
                if x in token_phrase:
                    question = word_related(token_phrase,question)
                    for x in list_disp:
                        if x in token_phrase:
                            question["ID_disp"].append(x)
                            break
                    break
            # frase sem "Qual"
    elif not all(question):
        for x in doc_tag:
            if x in token_phrase:
                for y in disp_tag:
                    if y in token_phrase:
                        if token_phrase.index(x) > token_phrase.index(y):
                            question["det"].append("qual_disp")
                            question = word_related(token_phrase,question)
                            break
                        else:
                            question["det"].append("qual_arq")
                            question = word_related(token_phrase,question)
                            break
                if question["det"] is None:
                    question["det"].append("qual_arq")
                    for x in list_disp:
                        if x in token_phrase:
                            question["ID_disp"] = token_phrase.index(x)
                    question = word_related(token_phrase,question)
                break
        if question["det"] is None:
            for x in disp_tag:
                if x in token_phrase:
                    question["det"].append("qual_disp")
                    question["disp"].append(x)
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