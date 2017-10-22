from nltk.tree import *
from command import CommandLine
from corenlp import*
import json
corenlp=StanfordCoreNLP()
# list of punctuations
punctuations=[',','!','?',';']
negative_words=[]
Sentences=[]
#creates object of command line class	
config = CommandLine()

# get list of negative words from command line 
if config.negativeWords==1:
	f=open(config.negative_file,'r')
	arr = f.read().split(',')
	f.close()
	for i in range(len(arr)):
		negative_words.append(arr[i].strip())
# if no list given by comman dline then use the default list
else:
	negative_words=['no','not','without','minus','less','loose','except','excluding','dont']
set_negative_words=set(negative_words)
print negative_words

if config.sentence_flag==1:
	f=open(config.sentence_file,'r')
	arr=f.read().split('\n')
	f.close()
	for i in range(len(arr)):
		Sentences.append(arr[i].strip())
else:
	Sentences.append(config.sentence)


# ananylyse the sentence
def AnalyseSentence(ptree,negative_flag,last_negative_index,negative_phrase_list,positive_phrase_list):
	# iterate throughg all the trees of ptree
	for subtree in ptree.subtrees():
		 if (type(subtree) is ParentedTree):
		 	# checks for presence of negative word
		 	if len(subtree.leaves())==1:
# if negative word found 'negative_flag' is set to one
		 		if (subtree.leaves()[0] in set_negative_words):
		 			negative_flag=1
# saves the index of last negative word
		 			last_negative_index=ptree.leaves().index(subtree.leaves()[0])
# if punctutaion found then negative_flag is set to zero as the sentence might be changing the tone after ','
		 	if (subtree.label() in punctuations):
		 			negative_flag=0
# checking if the node is a conjunction as the tone of sentence might change after that.
		 	if(subtree.label()=="CC"):
# if conjunction is itslef a negative word, set the negative flag to zero
		 			if (subtree.leaves()[0] in set_negative_words):
		 				negative_flag=1
		 				
# else set the negative_flag to zero
		 			else:
			 			negative_flag=0
			 # if negative word already found			
		 	if negative_flag==1:
# if the negative word was a part of NP then we need to consider the words
# in right of the negative word. So check if th parent had the label NP 
#if yes then include the words in right to it.
		 		if (subtree.parent().label()=="NP"and subtree.label()!="NP"):
		 			currentTree=subtree
		 			while (currentTree!=None):
# do not include noun phrases with punctuations such as ',' in negative phrases as they might
#contain positive pasts aslo
		 				common_words=set(currentTree.leaves()).intersection(set(punctuations))
		 				if(len(common_words)==0):
		 					negative_phrase_list.append(currentTree.leaves())
		 				currentTree=currentTree.right_sibling()
# if a NP occours after the negative word then include it in negative phrase list
		 		if(subtree.label()=="NP"):
		 			common_words=set(subtree.leaves()).intersection(set(punctuations))
		 			if(len(common_words)==0):
		 				negative_phrase_list.append(subtree.leaves())
# if no negative word is found or tone of sentence has chnaged
# then include all the NP encountered in positive phrases
		 	else:
# checking if phrase itself has a negative word
		 		common_words=set(subtree.leaves()).intersection(set_negative_words)
		 		if(subtree.label()=="NP" and len(common_words)==0):
		 			
		 			positive_phrase_list.append(subtree.leaves())
# if negative word was found but no noun phrase was found then assume all words after negation 
# are part of negative phrase list
	if negative_flag==1:
		if len(negative_phrase_list)==0:
			negative_phrase_list.append(ptree.leaves()[last_negative_index+1:])
	#print "negative list:  ",negative_phrase_list
	#print "positive list:  ",positive_phrase_list
	first_tuple_list = [tuple(lst) for lst in negative_phrase_list]
	secnd_tuple_list = [tuple(lst) for lst in positive_phrase_list]
	print "negative list",set(first_tuple_list)
	print "positive list",set(secnd_tuple_list)
	print ""
	print ""

# starting point on analysis
for j in range (len(Sentences)):
	print "Sentence: ",Sentences[j]
	# parse each sentence using stanford parser
	result=corenlp.parse(Sentences[j])
	# get just the parse tree by coverting the string in json format
	result_dic=json.loads(result)
	pasre_tree_string=result_dic['sentences'][0]['parsetree']
	# form a parentedTree using the parsetree string obtained from stanford parser
	ptree=ParentedTree.fromstring(pasre_tree_string)
	# intialising negative flag and negative and positive phrases
	negative_flag=0
	last_negative_index=0
	negative_phrase_list=[]
	positive_phrase_list=[]
	# analyse one sentence at a time
	AnalyseSentence(ptree,negative_flag,last_negative_index,negative_phrase_list,positive_phrase_list)
		



