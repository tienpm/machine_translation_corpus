import nltk
import underthesea
import os
from NLPToolkit import EnToolkit
from NLPToolkit import ViToolkit
import re

def word_segmentation(En_writeFile, Vi_writeFile, pair_sent):
	
	en_tokens = EnTool.word_seg(pair_sent['en'])
	for token in en_tokens:
		En_writeFile.write(f"[{token}] ")
	En_writeFile.write(f"\n\n")

	vi_tokens = ViTool.word_seg(pair_sent['vi'])
	for token in vi_tokens:
		Vi_writeFile.write(f"[{token}] ")
	Vi_writeFile.write(f"\n\n")

def pos_tagging(En_writeFile, Vi_writeFile, pair_sent):
	en_tokens = EnTool.word_seg(pair_sent['en'])
	en_tags = EnTool.pos_tagging(en_tokens)
	En_writeFile.write(f"{en_tags}")
	En_writeFile.write("\n\n")
		
	vi_tags = ViTool.pos_tagging(pair_sent['vi'])
	Vi_writeFile.write(f"{vi_tags} ")
	Vi_writeFile.write("\n\n")

def chunking(En_writeFile, Vi_writeFile, pair_sent):
	en_tokens = EnTool.word_seg(pair_sent['en'])
	en_tags = EnTool.pos_tagging(en_tokens)
	enChunking = EnTool.chunking(en_tags)
	En_writeFile.write(f"{enChunking}")
	En_writeFile.write("\n\n")

	viChunking = ViTool.chunking(pair_sent['vi'])
	Vi_writeFile.write(f"{viChunking}")
	Vi_writeFile.write("\n\n")

if __name__ == '__main__':
	# nltk.download()
	cur_path = os.getcwd()
	data_path = os.path.join(cur_path, 'data')
	eng_data_path = os.path.join(data_path, 'clean.en')
	vi_data_path = os.path.join(data_path, 'clean.vi')

	eng_doc = list()
	en_file = open(eng_data_path, 'r')
	eng_doc = en_file.readlines()
	en_file.close()

	print(f"Number sentences of English dataset: {len(eng_doc)}")

	vi_doc = list()
	vi_file = open(vi_data_path, 'r')
	vi_doc = vi_file.readlines()
	vi_file.close()

	print(f"Number sentences of Vietnamese dataset: {len(vi_doc)}")

	pair_sentence = list()
	no_sentence = min(len(eng_doc), len(vi_doc)) 

	for i in range(no_sentence):
		# Remove "\n" in last digit
		enSentence = eng_doc[i][:-1]
		viSentence = vi_doc[i][:-1]
		# Remove punction in sentence
		enSentence = re.sub(r'[^\w\s]', '', enSentence)
		viSentence = re.sub(r'[^\w\s]', '', viSentence)
		pair_sentence.append(
				{
					'en': enSentence.lower(),
					'vi': viSentence.lower()
				}
			)

	del eng_doc
	del vi_doc

	EnTool = EnToolkit()
	ViTool = ViToolkit()
	num_sent = 50

	# Word  Segmentation results path
	wordPath = os.path.join(cur_path, "words")
	if not os.path.exists(wordPath):
		os.makedirs(wordPath)

	'''
	enWord_path = os.path.join(wordPath, "en")
	if not os.path.exists(enWord_path):
		os.makedirs(enWord_path)

	viWord_path = os.path.join(wordPath, "vi")
	if not os.path.exists(viWord_path):
		os.makedirs(viWord_path)
	'''

	# Pos Tagging results path
	tagPath = os.path.join(cur_path, "tags")
	if not os.path.exists(tagPath):
		os.makedirs(tagPath)

	'''
	enTag_path = os.path.join(tagPath, "en")
	if not os.path.exists(enTag_path):
		os.makedirs(enTag_path)

	viTag_path = os.path.join(tagPath, "vi")
	if not os.path.exists(viTag_path):
		os.makedirs(viTag_path)
	'''

	# Chunking results path
	chunkPath = os.path.join(cur_path, "chunk")
	if not os.path.exists(chunkPath):
		os.makedirs(chunkPath)

	'''
	enChunk_path = os.path.join(chunkPath, "en")
	if not os.path.exists(enChunk_path):
		os.makedirs(enChunk_path)

	viChunk_path = os.path.join(chunkPath, "vi")
	if not os.path.exists(viChunk_path):
		os.makedirs(viChunk_path)		
	'''

	Word_enFile_path = os.path.join(wordPath, "EnWordSegmentation.txt")
	En_wordFile = open(Word_enFile_path, "w")
	Word_viFile_path = os.path.join(wordPath, "ViWordSegmentation.txt")
	Vi_wordFile = open(Word_viFile_path, "w")
	Tag_enFile_path = os.path.join(tagPath, "EnTag.txt")
	En_tagFile = open(Tag_enFile_path, "w")
	Tag_viFile_path = os.path.join(tagPath, "ViTag.txt")
	Vi_tagFile = open(Tag_viFile_path, "w")
	Chunk_enFile_path = os.path.join(chunkPath, "EnChunk.txt")
	En_chunkFile = open(Chunk_enFile_path, "w")
	Chunk_viFile_path = os.path.join(chunkPath, "ViChunk.txt")
	Vi_chunkFile = open(Chunk_viFile_path, "w")

	for i in range(num_sent):
		print(f"===== WORD SEGMENTATION PAIR SENTENCE {i+1}=====\n")
		word_segmentation(En_wordFile, Vi_wordFile, pair_sentence[i])
		print(f"================================================\n")
		print(f"======= POS TAGGING PAIR SENTENCE {i+1} ========\n")
		pos_tagging(En_tagFile, Vi_tagFile, pair_sentence[i])
		print(f"=============================\n")
		print(f"========= CHUNKING PAIR SENTENCE {i+1} =========\n")
		chunking(En_chunkFile, Vi_chunkFile, pair_sentence[i])
		print(f"================================================\n")

	En_wordFile.close()	
	Vi_wordFile.close()
	En_tagFile.close()
	Vi_tagFile.close()
	En_chunkFile.close()
	Vi_chunkFile.close()

	del pair_sentence