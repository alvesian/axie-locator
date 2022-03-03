import requests
import json
import pandas as pd

def run_code():

    choose_class()
    choose_quantity()
    choose_auction_type()
    choose_parts()
    request_query()

    id = 0
    id_list = []
    while id < quantity_choosen:
        axie_id = (response_json["data"]["axies"]["results"][id]["id"])
        id_list.append(axie_id)
        id += 1

    genes_compilator(id_list) 
    
    calculate_back_probability()
    calculate_mouth_probability()
    calculate_horn_probability()
    calculate_tail_probability()
    
    print(back_probability_list)
    print(mouth_probability_list)
    print(horn_probability_list)
    print(tail_probability_list)

    ######################## PROBABILITY CALCULATOR ####################################
    #id = 0
    #general_probability = []
    #while id < quantity_choosen:
    #    product = (back_probability_list[id]/100 * mouth_probability_list[id]/100 * horn_probability_list[id]/100 * tail_probability_list[id]/100)*100
    #    if product > 100:
    #        
    #        general_probability.append(product)
    #    else:
    #        general_probability.append(product)
    #    id += 1

    dataframe = pd.DataFrame(axie_data).swapaxes("index", "columns")
    print(dataframe)



def choose_class():
    global class_choosen
    classes = ["aquatic", "beast", "bird", "bug", "dawn", "musk", "mech", "plant", "reptile"]
    class_choosen = ""
    print("Which class you want?")
    print("Aquatic, Beast, Bird, Bug, Dawn, Musk, Mech, Plant, Reptile")
    while class_choosen not in classes:
        class_choosen = input("Type the class: ").lower().strip() 
        if class_choosen in classes:
            break
        else:
            print("Invalid choice. Please write a valid class!")

def choose_quantity():
    global quantity_choosen
    quantity_choosen = 0
    print("How much axies are you searching? (máx 50)")
    print("For 10 axies, please write: 10.")
    while True and quantity_choosen == 0:
        try:
            quantity_choosen = int(input("Type how much: ")) 
            if quantity_choosen in range (0,50):
                break
        except ValueError:
            print("Invalid choice. Please write a number!")
 
def choose_auction_type():
    global auction_type_choosen
    auction_type = ["Sale", "NotForSale", "All"]
    auction_type_choosen = ""
    print("Which state in Marketplace?")
    print("Sale | Not for sale | All")
    while auction_type_choosen not in auction_type:
        auction_type_choosen = input("Type the number here: ").title().replace(" ", "")
        if auction_type_choosen in auction_type:
            break
        else:
            print("Invalid choice. Please write a valid type!")

def choose_parts():
    global part_back
    global part_mouth
    global part_tail
    global part_horn

    part = 0
    parts = []
    parts_list= json.load(open("parts.json"))
    for part in parts_list:
        parts.append(part['partId'])
    
    ##### BACK PART #####

    part_back = ""
    while part_back == "":
        print("What back part are you looking for? (Null for skipping)")
        back = input("Type just the part name: ").lower().strip().replace(" ", "-")
        part_back = ("back-{}").format(back)
        if part_back in parts:
            break
        elif (back == "null"):
            part_back = "Null"
        else:
            part_back = ""
            print("Class not found. Please write a valid one!")

    ##### MOUTH PART #####

    part_mouth = ""
    while part_mouth == "":
        print("What mouth part are you looking for? (Null for skipping)")
        mouth = input("Type just the part name: ").lower().strip().replace(" ", "-")
        part_mouth = ("mouth-{}").format(mouth)
        if part_mouth in parts:
            break
        elif (mouth == "null"):
            part_mouth = "Null"
        else:
            part_mouth = ""
            print("Class not found. Please write a valid one!")

    ##### HORN PART #####

    part_horn = ""
    while part_horn == "":
        print("What horn part are you looking for? (Null for skipping)")
        horn = input("Type just the part name: ").lower().strip().replace(" ", "-")
        part_horn = ("horn-{}").format(horn)
        if part_horn in parts:
            break
        elif (horn == "null"):
            part_horn = "Null"
        else:
            part_horn = ""
            print("Class not found. Please write a valid one!")

    #### TAIL PART #####

    part_tail = ""
    while part_tail == "":
        print("What tail part are you looking for? (Null for skipping)")
        tail = input("Type just the part name: ").lower().strip().replace(" ", "-")
        part_tail = ("tail-{}").format(tail)
        if part_tail in parts:
            break
        elif (tail == "null"):
            part_tail = "Null"
        else:
            part_tail = ""
            print("Class not found. Please write a valid one!")

def request_query():

    url = "https://axieinfinity.com/graphql-server-v2/graphql"

    query = "{\"query\":\"query GetAxieBriefList($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\\n  axies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\\n    total\\n    results {\\n      ...AxieBrief\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment AxieBrief on Axie {\\n  id\\n  name\\n  stage\\n  class\\n  breedCount\\n  image\\n  title\\n  battleInfo {\\n    banned\\n    __typename\\n  }\\n  auction {\\n    currentPrice\\n    currentPriceUSD\\n    __typename\\n  }\\n  parts {\\n    id\\n    name\\n    class\\n    type\\n    specialGenes\\n    __typename\\n  }\\n  __typename\\n}\\n\",\"variables\": "
    variables = json.dumps({
        "from":0,
        "size":quantity_choosen,
        "sort":"PriceAsc",
        "auctionType":"Sale",
        "criteria":{
            "classes":class_choosen.capitalize(),
            "parts":[part_back,part_mouth,part_horn,part_tail],
            "stages":4,
            #"pureness":[1,2,3],
            #"breedCount":2
                }
        })
    data = (query+variables+"}")
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=data, headers = headers)
    global response_json
    response_json = json.loads(response.text)       

def genes_compilator(id_list):
    id = 0
    global axie_data
    axie_data = {}
    while id < quantity_choosen:
        url_genes = ("https://api.axie.technology/getgenes/" + id_list[id])
        genes_results = json.loads((requests.get(url_genes).text))
        axie_data[id] = {"id":"", "mouthd": "", "mouthr1": "","mouthr2": "","backd": "","backr1": "","backr2": "","hornd": "","hornr1": "","hornr2": "","taild": "","tailr1": "","tailr2": ""}
        axie_data[id]["id"] = (genes_results['axieId'])
        axie_data[id]["mouthd"] = (genes_results['mouth']['d']['partId'])
        axie_data[id]["mouthr1"] = (genes_results['mouth']['r1']['partId'])
        axie_data[id]["mouthr2"] = (genes_results['mouth']['r2']['partId'])
        axie_data[id]["backd"] = (genes_results['back']['d']['partId'])
        axie_data[id]["backr1"] = (genes_results['back']['r1']['partId'])
        axie_data[id]["backr2"] = (genes_results['back']['r2']['partId'])
        axie_data[id]["hornd"] = (genes_results['horn']['d']['partId'])
        axie_data[id]["hornr1"] = (genes_results['horn']['r1']['partId'])
        axie_data[id]["hornr2"] = (genes_results['horn']['r2']['partId'])
        axie_data[id]["taild"] = (genes_results['tail']['d']['partId'])
        axie_data[id]["tailr1"] = (genes_results['tail']['r1']['partId'])
        axie_data[id]["tailr2"] = (genes_results['tail']['r2']['partId'])
        id += 1

def calculate_back_probability():
    global back_probability_list
    back_probability_list = []
    if part_back != "Null":
        id = 0
        while id < quantity_choosen:
            back_probability = 37.5
            if axie_data[id]["backd"] == axie_data[id]["backr1"]:
                back_probability += 9.375
            elif axie_data[id]["backd"] == axie_data[id]["backr2"]:
                back_probability += 3.125
            back_probability_list.append(back_probability)
            id += 1
    else:
        id = 0
        while id < quantity_choosen:
            back_probability = 1
            back_probability_list.append(back_probability)
            id += 1

def calculate_mouth_probability():
    global mouth_probability_list
    mouth_probability_list = []
    if part_mouth != "Null":
        id = 0
        while id < quantity_choosen:
            mouth_probability = 37.5
            if axie_data[id]["mouthd"] == axie_data[id]["mouthr1"]:
                mouth_probability += 9.375
            elif axie_data[id]["mouthd"] == axie_data[id]["mouthr2"]:
                mouth_probability += 3.125
            mouth_probability_list.append(mouth_probability)
            id += 1
    else:
        id = 0
        while id < quantity_choosen:
            mouth_probability = 1
            mouth_probability_list.append(mouth_probability)
            id += 1

def calculate_horn_probability():
    global horn_probability_list
    horn_probability_list = []
    if part_horn != "Null":
        id = 0
        while id < quantity_choosen:
            horn_probability = 37.5
            if axie_data[id]["hornd"] == axie_data[id]["mouthr1"]:
                horn_probability += 9.375
            if axie_data[id]["mouthd"] == axie_data[id]["mouthr2"]:
                horn_probability += 3.125
            horn_probability_list.append(horn_probability)
            id += 1
    else:
        id = 0
        while id < quantity_choosen:
            horn_probability = 1
            horn_probability_list.append(horn_probability)
            id += 1

def calculate_tail_probability():
    global tail_probability_list
    tail_probability_list = []
    if part_tail != "Null":
        id = 0
        while id < quantity_choosen:
            tail_probability = 37.5
            if axie_data[id]["taild"] == axie_data[id]["mouthr1"]:
                tail_probability += 9.375
            if axie_data[id]["mouthd"] == axie_data[id]["mouthr2"]:
                tail_probability += 3.125
            tail_probability_list.append(tail_probability)
            id += 1
    else:
        id = 0
        while id < quantity_choosen:
            tail_probability = 1
            tail_probability_list.append(tail_probability)
            id += 1

if(__name__== "__main__"):
  run_code()