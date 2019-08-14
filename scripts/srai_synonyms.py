import json
from sys import argv
from nltk.corpus import wordnet


def main():
    with open(argv[1],'r') as f:
        data = json.load(f)

    for k in data['aiml']['category']:
        synonymns = [k]
        synonymns.extend(data['aiml']['category'][k]['srai'])
        synonymns.extend([l.name().replace("_"," ") for syn in wordnet.synsets(k) for l in syn.lemmas()])
        synonymns = include_wildcards(synonymns)
        synonymns = list(set(synonymns))
        if k in synonymns:
            synonymns.remove(k)
        data['aiml']['category'][k]['srai'] = synonymns

    with open(argv[1], 'w') as out:
        json.dump(data,out,indent=2)


def include_wildcards(srai_list):
    
    print(argv[1], "\tlist:\t", len(srai_list))

    tmp_list = [srai.replace("*","").replace("^","").strip() for srai in srai_list]

    print(argv[1], "\ttmp:\t", len(tmp_list))

    srai_set = set(filter(str.strip,tmp_list))

    print(argv[1], "\tset:\t", len(srai_set))

    new_list = []

    for srai in srai_set:
        new_list.append(srai)
        new_list.append("{} ^".format(srai))
        new_list.append("{} *".format(srai))
        new_list.append("^ {}".format(srai))
        new_list.append("* {}".format(srai))
        new_list.append("^ {} ^".format(srai))
        new_list.append("^ {} ^".format(srai))
        new_list.append("^ {} *".format(srai))
        new_list.append("* {} ^".format(srai))
        new_list.append("* {} *".format(srai))

    print(argv[1], "\tnew:\t", len(new_list))
    
    return new_list

# class Thesaurus(object):
#     import dictclient
#     def __init__(self, server='localhost'):
#         self.dict = 'moby-thesaurus'
#         self.connection = dictclient.Connection(hostname=server)
 
#     def query_synonyms(self, word):
#         definitions = self.connection.define(self.dict, word)
#         words = [w.strip() for d in definitions for l in d.getdefstr().split('\n')[1:] for w in l.split(',') if w]
#         return words

if __name__ == "__main__":
    main()