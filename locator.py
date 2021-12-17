import requests
import json
import pandas as pd
from tabulate import tabulate

# Escolha da classe, não deixar vazio #

print("Qual classe você busca?")
print("Aqua, Beast, Bird, Bug, Dawn, Musk, Mech, Plant ou Reptile")
classes_inp = input("Digite a classe: ")
if (classes_inp == "aqua"):
    classes_inp = "Aquatic"
classes = str.capitalize(classes_inp)

# Quantidade máxima de Axies na busca #

print("Quantidade máxima de Axies na busca?")
print("[1] 5 Axies [2] 10 Axies [3] 20 Axies [4] 40 Axies")
quantidadedebusca = str(input("Digite 1,2,3 ou 4: "))
size = "0"
if (quantidadedebusca == "1"):
    size = "5"
elif (quantidadedebusca == "2"):
    size = "10"
elif (quantidadedebusca == "3"):
    size = "20"
elif (quantidadedebusca == "4"):
    size = "40"
    

# Escolha do estado #

print("Qual o estado do Axie no Marketplace?")
print("[1] Todos  [2] A venda [3] Não está a venda?")
auctionType = input("Digite o número correspondente: ")

if (auctionType == 2):
    auctionType = ("Sale")
elif (auctionType == 3):
    auctionType = ("NotForSale")
else:
    auctionType = ("All")

# Escolha das partes, se deixar vazio, ele continua funcionando #

print("Qual a parte das costas?")
costas = input("Digite somente o nome da parte: ")
part_back = str(("\"back-{}\"").format(costas))
part_back = part_back.replace(" ", "-")


print("Qual a parte da boca?")
boca = input("Digite somente o nome da parte: ")
part_mouth = ("\"mouth-{}\"").format(boca)
part_mouth = part_mouth.replace(" ", "-")

print("Qual a parte do chifre?")
chifre = input("Digite somente o nome da parte: ")
part_horn = ("\"horn-{}\"").format(chifre)
part_horn = part_horn.replace(" ", "-")

print("Qual a parte da calda?")
cauda = input("Digite somente o nome da parte: ")
part_tail = ("\"tail-{}\"").format(cauda)
part_tail = part_tail.replace(" ", "-")

if (part_back == "\"back-\""):
    part_back = "\"null\""
if (part_mouth == "\"mouth-\""):
    part_mouth = "\"null\""
if (part_horn == "\"horn-\""):
    part_horn = "\"null\""
if (part_tail == "\"tail-\""):
    part_tail = "\"null\""

#auctionType = "Sale"
str_parts = ("[" + part_back + "," + part_mouth + "," +  part_horn + "," +  part_tail + "]" )
de = "0"
sort = "PriceAsc"
#size = quantidadebusca

# Request para puxar os axies que tem DOMINANTE das cartas escolhidas #

headers = {'content-type': 'application/json'}
query = """"query":"query GetAxieBriefList(\\n  $auctionType: AuctionType\\n  $criteria: AxieSearchCriteria\\n  $from: Int\\n  $sort: SortBy\\n  $size: Int\\n  $owner: String\\n) {\\n  axies(\\n    auctionType: $auctionType\\n    criteria: $criteria\\n    from: $from\\n    sort: $sort\\n    size: $size\\n    owner: $owner\\n  ) {\\n    results {\\n      id\\n    }\\n  }}"""
variables = str("\"variables\":{\"auctionType\":" + "\"" + auctionType + "\"" + ",\"criteria\":{\"classes\":" +  "\"" + classes + "\""  + ",\"parts\":" + str_parts + "},\"from\":" + de + ",\"sort\":" + "\"" + sort + "\"" + ",\"size\":"  + size + "}}" )
data = str("{" + query + "\"" + "," + variables)
response = requests.post('https://axieinfinity.com/graphql-server-v2/graphql', headers=headers, data=data)

# Pegar os id's e transformar em uma lista #

json_data = json.loads(response.text)
lista_ids = str(list(json_data.values()))


if "id" in lista_ids:
    lista_ids = lista_ids.replace("{", "")
    lista_ids = lista_ids.replace("}", "")
    lista_ids = lista_ids.replace("'results'", "")
    lista_ids = lista_ids.replace("'axies'", "")
    lista_ids = lista_ids.replace("'id'", "")
    lista_ids = lista_ids.replace(":", "")
    lista_ids = lista_ids.replace("[", "")
    lista_ids = lista_ids.replace("]", "")
    lista_ids = lista_ids.replace("'", "")
    lista_ids = lista_ids.replace(" ", "")
#    lista_ids = lista_ids.replace(",", "\",\"")
else:
    print("O Axie esolhido é único ou não está a venda")



# Puxar os genes D, R1 e R2 da lista de ids #
lista_ids = lista_ids.split(",")
url_id = lista_ids
i = 0
axie_list = []
while i < len(url_id):
    url_genes = ("https://api.axie.technology/getgenes/" + url_id[i])
    resultado = requests.get(url_genes)
    dict = json.loads(resultado.text)
    id_buscarr = (dict['axieId'])
    mouthd = (dict['mouth']['d']['partId'])
    mouthr1 = (dict['mouth']['r1']['partId'])
    mouthr2 = (dict['mouth']['r2']['partId'])
    backd = (dict['back']['d']['partId'])
    backr1 = (dict['back']['r1']['partId'])
    backr2 = (dict['back']['r2']['partId'])
    hornd = (dict['horn']['d']['partId'])
    hornr1 = (dict['horn']['r1']['partId'])
    hornr2 = (dict['horn']['r2']['partId'])
    taild = (dict['tail']['d']['partId'])
    tailr1 = (dict['tail']['r1']['partId'])
    tailr2 = (dict['tail']['r2']['partId'])
    axie_data = (id_buscarr, mouthd, mouthr1, mouthr2, backd, backr1, backr2, hornd, hornr1, hornr2, taild, tailr1, tailr2)
    axie_list.append(axie_data)
    i = i + 1


df = pd.DataFrame(axie_list, columns=['AxieId', 'Mouth D', 'Mouth R1', 'Mouth R2', 'Back D', 'Back R1', 'Back R2', 'Horn D', 'Horn R1', 'Horn R2', 'Tail D', 'Tail R1', 'Tail R2'])

df_novo = df.to_dict('index')


part_back = part_back.replace("\"", "")


probabilidade_boca = []
if "mouth" in part_mouth:
    p = 0
    while p < len(df_novo):
        probabilidade_mouth = 37.5
        if (df_novo[p]["Mouth D"]) == (df_novo[p]["Mouth R1"]):
                probabilidade_mouth = probabilidade_mouth + 9.375
                if (df_novo[p]["Mouth D"]) == (df_novo[p]["Mouth R2"]):
                    probabilidade_mouth = probabilidade_mouth + 3.125
        probabilidade_boca.append(probabilidade_mouth)
        p = p + 1
else:
    p = 0
    while p < len(df_novo):
        probabilidade_mouth = 1
        probabilidade_boca.append(probabilidade_mouth)
        p = p + 1

probabilidade_costas = []
if "back" in part_back:
    p = 0
    while p < len(df_novo):
        probabilidade_back = 37.5
        if (df_novo[p]["Back D"]) == (df_novo[p]["Back R1"]):
                probabilidade_back = probabilidade_back + 9.375
                if (df_novo[p]["Back D"]) == (df_novo[p]["Back R2"]):
                    probabilidade_back = probabilidade_back + 3.125
        probabilidade_costas.append(probabilidade_back)
        p = p + 1
else:
    p = 0
    while p < len(df_novo):
        probabilidade_back = 1
        probabilidade_costas.append(probabilidade_back)
        p = p + 1
        
probabilidade_chifre = []        
if "horn" in part_horn:
    p = 0
    while p < len(df_novo):
        probabilidade_horn = 37.5
        if (df_novo[p]["Horn D"]) == (df_novo[p]["Horn R1"]):
                probabilidade_horn = probabilidade_horn + 9.375
                if (df_novo[p]["Horn D"]) == (df_novo[p]["Horn R2"]):
                    probabilidade_horn = probabilidade_horn + 3.125
        probabilidade_chifre.append(probabilidade_horn)
        p = p + 1
else:
    p = 0
    while p < len(df_novo):
        probabilidade_horn = 1
        probabilidade_chifre.append(probabilidade_horn)
        p = p + 1
        
probabilidade_rabo = []
if "tail" in part_tail:
    p = 0
    while p < len(df_novo):
        probabilidade_tail = 37.5
        if (df_novo[p]["Tail D"]) == (df_novo[p]["Tail R1"]):
                probabilidade_tail = probabilidade_tail + 9.375
                if (df_novo[p]["Tail D"]) == (df_novo[p]["Tail R2"]):
                    probabilidade_tail = probabilidade_tail + 3.125
        probabilidade_rabo.append(probabilidade_tail)
        p = p + 1
else:
    p = 0
    while p < len(df_novo):
        probabilidade_tail = 1
        probabilidade_rabo.append(probabilidade_tail)
        p = p + 1


df["Probabilidade Boca"] = (probabilidade_boca)
df["Probabilidade Costas"] = (probabilidade_costas)
df["Probabilidade Chifre"] = (probabilidade_chifre)
df["Probabilidade Rabo"] = (probabilidade_rabo)

probabilidade = []
p=0
while p < len(df):
    if ((df["Probabilidade Boca"][p]) + (df["Probabilidade Costas"][p]) + (df["Probabilidade Chifre"][p]) + (df["Probabilidade Rabo"][p]) >= 54):
        probabilidade_total = ((df["Probabilidade Boca"][p])*(df["Probabilidade Costas"][p])*(df["Probabilidade Chifre"][p])*(df["Probabilidade Rabo"][p])/100).round(2)
        probabilidade.append(probabilidade_total)
        p = p + 1
    else:
        probabilidade_total = ((df["Probabilidade Boca"][p])*(df["Probabilidade Costas"][p])*(df["Probabilidade Chifre"][p])*(df["Probabilidade Rabo"][p])).round(2)
        probabilidade.append(probabilidade_total)
        p = p + 1


df.drop('Mouth R1', axis = 1, inplace = True)
df.drop('Mouth R2', axis = 1, inplace = True)
df.drop('Back R1', axis = 1, inplace = True)
df.drop('Back R2', axis = 1, inplace = True)
df.drop('Horn R1', axis = 1, inplace = True)
df.drop('Horn R2', axis = 1, inplace = True)
df.drop('Tail R1', axis = 1, inplace = True)
df.drop('Tail R2', axis = 1, inplace = True)
df.drop('Probabilidade Boca', axis = 1, inplace = True)
df.drop('Probabilidade Costas', axis = 1, inplace = True)
df.drop('Probabilidade Chifre', axis = 1, inplace = True)
df.drop('Probabilidade Rabo', axis = 1, inplace = True)


df["Probabilidade"] = (probabilidade)

print(tabulate(df, headers=['AxieId', 'Mouth D', 'Back D', 'Horn D', 'Tail D', 'Probabilidade']))


