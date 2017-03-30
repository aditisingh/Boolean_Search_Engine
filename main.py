#!/usr/bin/env python

import numpy as np
import re,sys
import argparse

def get_listing(str1,dict):
	if str1 in dict.keys():
		listing1=dict[str1]
	else:
		listing1=[]
	return listing1

def intersection(listing1, listing2):
	intersect=[]
	p1=0
	p2=0
	while(p1<len(listing1))&(p2<len(listing2)):
		doc_id1=listing1[p1]
		doc_id2=listing2[p2]
		if(doc_id1==doc_id2):
			intersect.append(doc_id1)
			p1=p1+1
			p2=p2+1
		else:
			if(doc_id1<doc_id2):
				p1=p1+1
			else:
				p2=p2+1
	return intersect

			
def union(listing1, listing2):
	answer=list(set(listing1+listing2))
	answer.sort()
	return answer


def not_postings(listing1,k):	#k in len(doc_matrix)
	posting=[]
	for i in range(1,k+1):
		if i not in listing1:
			posting.append(i)
	return posting


vocab_map_file=open('vocab_map.txt','r')

vocab_map=vocab_map_file.readlines()
vocab_map_list=[]

for i in range(len(vocab_map)-1):
	idx=vocab_map[i].find('=')
	vocab_map_list.append(vocab_map[i][idx+2:-2])
	# print(vocab_map[i],vocab_map[i][idx+2:-2])

i=len(vocab_map)-1
idx=vocab_map[i].find('=')
vocab_map_list.append(vocab_map[i][idx+2:])
# print(vocab_map[i],vocab_map[i][idx+2:])
vocab_map_file.close()

doc_matrix_file=open('docs.txt','r')

doc_matrix=[]
for line in doc_matrix_file.readlines():
	line=line.strip('\r\n')
	line=line[1:-1]
	line=re.split(', ',line)
	doc_matrix.append(line)

doc_matrix_file.close()

#generate postings
postings_dict={}

for i in range(len(vocab_map)):
	#go through different words in the vocabulary, as mapped in the map
	id=str(i)
	postings=[]
	for j in range(len(doc_matrix)):
		if id in doc_matrix[j]:
			postings.append(j+1) #j+1, since we want index from 1
	if(postings):
		postings_dict.update({vocab_map_list[i]:postings})


total=len(sys.argv)
if(total==4):
	if(sys.argv[1]=='PLIST'):
		word=sys.argv[2].lower()
		outfile=sys.argv[3]
		f=open(outfile,'w')
		l=get_listing(str(word),postings_dict)
		# print(l)
		f.write(word)
		f.write(' -> ')
		f.write(str(l))
		f.close()
	else:
		print('Invalid Usage')
else: 
	if(total==6):
		if(sys.argv[1]=='AND'):
			if(sys.argv[3]=='AND'):
				word1=sys.argv[2].lower()
				word2=sys.argv[4].lower()
				outfile=sys.argv[5]
				l=intersection(get_listing(str(word1),postings_dict),get_listing(str(word2),postings_dict))
				# print(l)
				f=open(outfile,'w')
				f.write(word1)
				f.write(' AND ')
				f.write(word2)
				f.write(' -> ')
				f.write(str(l))
				f.close
			else:
				print('Invalid Usage')
		else:
			if(sys.argv[1]=='OR'):
				if(sys.argv[3]=='OR'):
					word1=sys.argv[2].lower()
					word2=sys.argv[4].lower()
					outfile=sys.argv[5]
					l=union(get_listing(str(word1),postings_dict),get_listing(str(word2),postings_dict))
					# print(l)
					f=open(outfile,'w')
					f.write(word1)
					f.write(' OR ')
					f.write(word2)
					f.write(' -> ')
					f.write(str(l))
					f.close
				else:
					print('Invalid Usage')
			else:
				if(sys.argv[1]=='AND_NOT'):
					if(sys.argv[3]=='AND_NOT'):
						word1=sys.argv[2].lower()
						word2=sys.argv[4].lower()
						outfile=sys.argv[5]
						l1=get_listing(str(word1),postings_dict)
						l2=not_postings(get_listing(str(word2),postings_dict),len(doc_matrix))
						l=intersection(l1,l2)
						# print(l)
						f=open(outfile,'w')
						f.write(word1)
						f.write(' AND (NOT ')
						f.write(word2)
						f.write(') -> ')
						f.write(str(l))
						f.close()
					else:
						print('Invalid Usage')
				else:
					print('Invalid Usage')
	else:
		print('Invalid Usage')

