import numpy as np
import xml.etree.ElementTree as ET
import math
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer



#parsing xml file to retrieve data
tree = ET.parse('xml.xml')

#get the root tag and length of data
root = tree.getroot()
length = len(root)

all_sentences = []

def Filter_out():
    TenderBrief = []
    for i in range(length):
        TenderBrief.append(root[i][2].text)

    stop_words = set(stopwords.words('english'))
    #stop_words.update(('br'))

    tokenizer = RegexpTokenizer(r'\w+')
    word_tokens = []
    for i in range(len(TenderBrief)):
        word_tokens.append(tokenizer.tokenize(TenderBrief[i]))
    
    words = [item for i in word_tokens for item in i]
    
    filtered_sentence = []
    filtered_sentence = [w.lower() for w in words if not w.lower() in stop_words and w.lower()!="br"]
    
    for i in range(len(word_tokens)):
        word_tokens[i] = [w.lower() for w in word_tokens[i] if not w.lower() in stop_words and w.lower()!="br"]

    return word_tokens, filtered_sentence

def count_prob(f1,f2,f3,count1,count2,count3):
    p1 = []
    p2 = []
    p3 = []

    for i in range(len(f1)):
        p1.append(f1[i]/count1)
        p2.append(f2[i]/count2)
        p3.append(f3[i]/count3)

    return [p1, p2, p3]

def final_prob(p1,p2,p3,p_buy, p_contract, p_sell,p_key):
    prob1 = []
    prob2 = []
    prob3 = []

    for i in range(len(p_key)):
        prob1.append((p1[i]*p_buy)/p_key[i])
        prob2.append((p2[i]*p_contract)/p_key[i])
        prob3.append((p3[i]*p_sell)/p_key[i])

    return [prob1, prob2, prob3]


filtered_sentence = []
all_sentences, filtered_sentence = Filter_out()

filter_list = []
for i in range(len(filtered_sentence)):
    if filtered_sentence[i] not in filter_list:
        filter_list.append(filtered_sentence[i])

"""for i in range(len(all_sentences)):
    for j in range(len(all_sentences[i])):
        if all_sentences[i][j] == "auction":
            print(all_sentences[i])"""
#print(all_sentences)
"""for i in range(len(filter_list)):
    if filter_list[i] == "auction":
        print(i)"""

f1 = []
f2 = []
f3 = []

for i in range(len(filter_list)):
    f1.append(0)
    f2.append(0)
    f3.append(0)

count1 = 0
count2 = 0
count3 = 0

for j in range(len(all_sentences)):
    for i in range(len(all_sentences[j])):
        index1 = filter_list.index(all_sentences[j][i])
        if((root[j][9].text) == "Buy"):
            f1[index1] += 1
        elif((root[j][9].text) == "Contract"):
            f2[index1] += 1 
        elif((root[j][9].text) == "Sell"):
            f3[index1] += 1
     
p_key_buy =[] 
p_key_contract = [] 
p_key_sell = []
p_buy_key = []
p_contract_key = []
p_sell_key = []

for i in range(len(filter_list)):
    p_key_buy.append(0)
    p_key_contract.append(0)
    p_key_sell.append(0)
    p_buy_key.append(0)
    p_contract_key.append(0)
    p_sell_key.append(0)

for i in range(length):
    if((root[i][9].text) == "Buy"):
        count1 += 1
    elif((root[i][9].text) == "Contract"):
        count2 += 1 
    elif((root[i][9].text) == "Sell"):
        count3 += 1

p_buy = count1/length
p_contract = count2/length
p_sell = count3/length

p_key = []
for i in range(len(f1)):
    p_key.append((f1[i]+f2[i]+f3[i])/length)

[p_key_buy, p_key_contract, p_key_sell] = count_prob(f1,f2,f3,count1,count2,count3)
[p_buy_key, p_contract_key, p_sell_key] = final_prob(p_key_buy, p_key_contract, p_key_sell, p_buy, p_contract, p_sell, p_key)

max_key = []
for i in range(len(p_key)):  
    max_val = max(p_buy_key[i],p_contract_key[i],p_sell_key[i])
    if(max_val == p_buy_key[i]):
        max_key.append("Buy")
    elif(max_val == p_contract_key[i]):
        max_key.append("Contract")
    elif(max_val == p_sell_key[i]):
        max_key.append("Sell")

var = input("Enter the tender description: ")
ex = Filter_out(var)
if(ex):
    index = filter_list.index(ex)
    print(ex, " belongs to class: " ,max_key[index])



