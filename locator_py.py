from js import console
from js import XMLHttpRequest
import json

search_btn = Element("search-btn")
parts_btn = Element("parts-btn")
clear_btn = Element("clear-btn")
back_part_list_group = Element("back-part-list-group")
mouth_part_list_group = Element("mouth-part-list-group")
horn_part_list_group = Element("horn-part-list-group")
tail_part_list_group = Element("tail-part-list-group")
axie_group = Element("axie-list-group")
axie_class = Element("axie-class")
axie_nbr = Element("axie-nbr")
axie_auction = Element("axie-auction")

def make_search(*args):
    if axie_group != None:
        axie_group.clear()
    quantity_choosen = int(axie_nbr.element.value)
    class_choosen = str(axie_class.element.value)
    payload = json.dumps({
    "operationName": "GetAxieBriefList",
    "variables": {
        "from": 0,
        "size": quantity_choosen,
        "sort": "PriceAsc",
        "auctionType": "Sale",
        "criteria": {
            "classes":class_choosen,
            "parts":[back_part_list_group.element.value,mouth_part_list_group.element.value,horn_part_list_group.element.value,tail_part_list_group.element.value],
            "stages":4,
            #"pureness":[1,2,3],
            #"breedCount":2
                }
    },
    "query": "query GetAxieBriefList($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\n  axies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\n    total\n    results {\n      ...AxieBrief\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieBrief on Axie {\n  id\n  name\n  stage\n  class\n  breedCount\n  image\n  title\n  battleInfo {\n    banned\n    __typename\n  }\n  auction {\n    currentPrice\n    currentPriceUSD\n    __typename\n  }\n  parts {\n    id\n    name\n    class\n    type\n    specialGenes\n    __typename\n  }\n  __typename\n}\n"
    })
    req = XMLHttpRequest.new()
    req.open("POST", "https://graphql-gateway.axieinfinity.com/graphql", False)
    req.setRequestHeader("content-type", "application/json")
    req.send(payload)
    axie_list = json.loads(req.response)
    if axie_list['data']['axies']['total'] == 0:
        axie_item = create("p", classes="axie-list-group")
        axie_item.element.innerText = "I cannot find an Axie!"
        axie_group.element.appendChild(axie_item.element)
        exit
    axie_list = axie_list['data']['axies']['results']
    for axie in axie_list:
        axie_item = create("tr", classes="axie-list-group-id")
        axie_item.element.innerHTML = '<th><a href = "https://marketplace.axieinfinity.com/axie/{}" target="_blank"'.format(axie['id']) + axie['id']+'>' + axie['id'] + '</a></th><td>' + axie['name'] + '</td>'+ '<td>' + axie['class'] + '</td>' + '<td>' + axie['auction']['currentPriceUSD'] + '</td>'
        axie_group.element.appendChild(axie_item.element)

def clear_search(*args):
    axie_group.clear()

req = XMLHttpRequest.new()
req.open("GET", "https://raw.githubusercontent.com/freakitties/axieExt/master/body-parts.json", False)
req.send(None)
parts_list = json.loads(req.response)

back_part_item = create("option", classes="back-part-list-group")
back_part_item.element.value = "Null"        
back_part_item.element.innerText = "None"
back_part_list_group.element.appendChild(back_part_item.element)

mouth_part_item = create("option", classes="mouth-part-list-group")
mouth_part_item.element.value = "Null"        
mouth_part_item.element.innerText = "None"
mouth_part_list_group.element.appendChild(mouth_part_item.element)

horn_part_item = create("option", classes="horn-part-list-group")
horn_part_item.element.value = "Null"        
horn_part_item.element.innerText = "None"
horn_part_list_group.element.appendChild(horn_part_item.element)

tail_part_item = create("option", classes="tail-part-list-group")
tail_part_item.element.value = "Null"        
tail_part_item.element.innerText = "None"
tail_part_list_group.element.appendChild(tail_part_item.element)

for parts in parts_list:
    if parts['type'] == "back":
        back_part_item = create("option", classes="back-part-list-group")
        back_part_item.element.value = "back-"+parts['name'].lower().replace(" ", "-")        
        back_part_item.element.innerText = parts['name'] + " | " + parts['class'].capitalize()
        back_part_list_group.element.appendChild(back_part_item.element)
    elif parts['type'] == "mouth":
        mouth_part_item = create("option", classes="back-part-list-group")
        mouth_part_item.element.value = "mouth-"+parts['name'].lower().replace(" ", "-")        
        mouth_part_item.element.innerText = parts['name'] + " | " + parts['class'].capitalize()
        mouth_part_list_group.element.appendChild(mouth_part_item.element)
    elif parts['type'] == "horn":
        horn_part_item = create("option", classes="horn-part-list-group")
        horn_part_item.element.value = "horn-"+parts['name'].lower().replace(" ", "-")        
        horn_part_item.element.innerText = parts['name'] + " | " + parts['class'].capitalize()
        horn_part_list_group.element.appendChild(horn_part_item.element) 
    elif parts['type'] == "tail":
        tail_part_item = create("option", classes="tail-part-list-group")
        tail_part_item.element.value = "tail-"+parts['name'].lower().replace(" ", "-")        
        tail_part_item.element.innerText = parts['name'] + " | " + parts['class'].capitalize()
        tail_part_list_group.element.appendChild(tail_part_item.element) 

search_btn.element.onclick = make_search
clear_btn.element.onclick = clear_search
