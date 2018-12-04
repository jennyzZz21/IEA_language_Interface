'''
Language interface alpha version for IEA system.
Use NLP technique to extract semanctic meanings from user queries.
Copyright: Yueling Zeng, Min Jian Yang 
'''

'''Packages required:
1) Python pattern library:
    pip install pattern
2) Stanford CoreNLP parser
    wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-02-27.zip
    unzip stanford-corenlp-full-2018-02-27.zip
    cd stanford-corenlp-full-2018-02-27
    java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
    -preload tokenize,ssplit,pos,lemma,ner,parse,depparse \
    -status_port 9000 -port 9000 -timeout 15000 &
Resource: https://stackoverflow.com/questions/13883277/stanford-parser-and-nltk/51981566#51981566

OBSOLETE: Download resource package from nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')'''

'''Usage:
    python parse5Method.py chunking/stanford-cfg outputfilename
'''

import nltk 
import sys 
import os

method = sys.argv[1]
output = sys.argv[2]

# query = "did you get the final results for analyzing our correlation graphs from yield plot twenty five ?"
with open("IEAdemoSpeech.txt", 'r') as f:
    query = f.read().splitlines()

def parseRegexp(query, output):
    from pattern.en import parsetree
    from pattern.en import pprint

    outfile1 = open(output, 'w')

    for s in query:
    #tokens = nltk.word_tokenize(s)
    #tagged = nltk.pos_tag(tokens)
        print(s)
        outfile1.write(s +'\n')

        outfile1 = open(output, 'a')
        '''parsetree using PENN treebank II by default 
        https://www.clips.uantwerpen.be/pages/MBSP-tags'''
        tree = parsetree(s, relations=True, lemmata=True)
        #pprint(tree)
        for node in tree:
            ''' node object contains 
                    node.lemmata
                    node.relations
                    node.chunks
                    ...
            '''
            for chunk in node.chunks:
                chunked = [(word.string, word.type) for word in chunk.words]
                outfile1.write(chunk.type+', '+str(chunked)+'\n')
        outfile1.write('\n')
    outfile1.close()

def parseStanfordCFG(query, output):
    from nltk.parse import CoreNLPParser

    parser = CoreNLPParser(url='http://localhost:9000')
    outfile2 = open(output, 'w')

    for s in query:
        outfile2 = open(output, 'a')
        outfile2.write(s+'\n')
        parsed = parser.raw_parse(s)
        for inx, obj in enumerate(parsed):
            outfile2.write(str(obj)+'\n')
        outfile2.write('\n')
    outfile2.close()



if method == 'chunking':
    parseRegexp(query, output)
elif method == 'stanford-cfg':
    parseStanfordCFG(query, output)

'''print(tagged)
[('did', 'VBD'), ('you', 'PRP'), ('get', 'VB'), ('the', 'DT'), ('results', 'NNS'), ('for', 'IN'), ('correlation', 'NN'), 
('analysis', 'NN'), ('from', 'IN'), ('yield', 'NN'), ('plot', 'NN'), ('five', 'CD'), ('?', '.')]
'''

phrase_pattern =  r"""NP:		{<DT>?<JJ>*<N.*>*<CD>*} 
                         		{<NNP>*}
                     QUESTION:	{^<V.*><PRP>?}"""

'''NLTK Book Chap 7: extract information from text with chunking
Example: 
	(S
  	(QUESTION did/VBD you/PRP)
  	get/VB
  	(NP the/DT final/JJ results/NNS)
  	for/IN
  	analyzing/VBG
  	our/PRP$
  	(NP correlation/NN graphs/NN)
  	from/IN
  	(NP yield/NN plot/NN twenty/NN five/CD)
  	?/.)'''

#cp = nltk.RegexpParser(phrase_pattern)
#chunked = cp.parse(tagged)


'''for node in chunked:
	if type(node) is nltk.tree.Tree:
		print(node.label())
		print(node.leaves())'''
 	
grammar = nltk.CFG.fromstring("""
 	S -> NP VP
  	VP -> V NP | V NP PP
  	PP -> P NP 
  	NP ->  Det N | Det N PP
  	V -> "get" | "generate" | "extract"
  	NP ->  Det N | Det N PP |"John" | "Mary" | "Bob" |
  	Det -> "a" | "an" | "the" | "my"
  	N -> "results" | "correlation" | "analysis" | "yield" | "plot"
  	P -> "in" | "on" | "by" | "with"
  	""")

