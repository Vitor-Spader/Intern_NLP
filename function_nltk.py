import nltk,json
import general_functions as f

stopwords = nltk.corpus.stopwords.words('portuguese')

#base de dados
def get_bd(mode="disp_tag_ID"):
    if mode == "docs":
        with open(r"data\tags_doc.json","r") as x1:
            docs = json.load(x1)
            return docs
    if mode == "disp_tag_ID":
        with open(r"data\lista_dispositivos.json","r") as x0:
            list_disp = json.load(x0)
        with open(r"data\tags_disp.json","r") as x2:
            disp_tag = json.load(x2)
        with open(r"data\tags_det.json","r") as x3:
            det_tag = json.load(x3)
        with open(r"data\tags_intent.json","r") as x4:
            intent_tag = json.load(x4)
        return list_disp,disp_tag,det_tag,intent_tag

def word_related(token_phrase,question):
    docs = get_bd(mode="docs")
    #print(get_bd(mode="docs"))

    for x,y in docs.items():
        for z in y:
            if type(z) is list:
                if all(v in token_phrase for v in x):
                    question["docs"].append(x)
                    break
            elif z in token_phrase:
                question["docs"].append(x)
                break
    return question

#retorna o codigo que representa a a frase processada
def return_question(token_phrase):

    #list_disp = lista de dispositivos(ID)
    #doc_tag = tags para documento e sinonimos
    #disp_tag = tags para tipos de dispositivos
    list_disp,disp_tag,det_tag,intent_tag = get_bd()

    #inicializa vetor de retorno
    question = {"intent":[],"docs":[],"disp":[],"ID_disp":[]}
    #tuplas com determinante e sua posição
    det = []
    #tuplas com referencia da daterminante e sua posição
    intent = [] 
    det_aux = []
    intent_aux = []
    aux = []
    aux0 = []

    #adiciona a tupla tag/posição 
    for d in det_tag:
        if d in token_phrase:
            det.append((d,token_phrase.index(d)))
    for r in intent_tag:
        if r in token_phrase:
            intent.append((r,token_phrase.index(r)))
    #########
    if len(det) == 0 and len(intent) == 0:
        return "Error!"
    #########
    for d,d0 in det:
        for r,r0 in intent:
            if d0 > r0:
                continue
            elif (r0 - 1) == d0:
                question["intent"].append({d:r})
                aux.append(d0)
                aux0.append(r0)
                break 
            else:
                det_aux.append(d0)
                intent_aux.append(r0)
    det_aux,intent_aux = f.less_equals(aux,det_aux,aux0,intent_aux) #retira da lista os valores aux,aux0
    for i in range(0,len((det_aux if len(det_aux) > len(intent_aux) else intent_aux))):
        if len(det_aux) < 1: break 
        x,y = f.less(det_aux,intent_aux)        #pega os menores valores
        f.det_append(question,det,intent,x,y)   #adiciona os menores valores ao dicionario
        aux = [x]
        aux0 = [y]
        det_aux,intent_aux = f.less_equals(aux,det_aux,aux0,intent_aux)#retira os valores ja inseridos no dicionario
   
    for x in disp_tag:
        if x in token_phrase:
            if not f.test_exist(question,x):
                question["disp"].append(x)
    for x in list_disp:    
        if x in token_phrase:
            question["ID_disp"].append(x)
    question = word_related(token_phrase,question)

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