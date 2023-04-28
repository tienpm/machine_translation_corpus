import nltk
import underthesea
import os
from NLPToolkit import EnToolkit
from NLPToolkit import ViToolkit
import re

def word_segmentation(namefile, enPath, viPath, pair_sent):
	enFile_path = os.path.join(enPath, namefile)
	print(f"[INFO] English word segmentation file {enFile_path}")
	
	enFile = open(enFile_path, "w")
	en_tokens = EnToolkit.word_seg(pair_sent['en'])
	for token in en_tokens:
		enFile.write(f"[{token}/]NP ")
	enFile.close()

	viFile_path = os.path.join(viPath, namefile)
	print(f"[INFO] Vietnamese word segmentation file {viFile_path}")
	
	viFile = open(viFile_path, "w")

	vi_tokens = ViToolkit.word_seg(pair_sent['vi'])
	for token in vi_tokens:
		viFile.write(f"[{token}/]NP ")

	viFile.close()

def pos_tagging(namefile, enPath, viPath, pair_sent):
	enFile_path = os.path.join(enPath, namefile)
	print(f"[INFO] English Pas Tagging file {enFile_path}")
	
	enFile = open(enFile_path, "w")
	en_tokens = EnToolkit.word_seg(pair_sent['en'])
	en_tags = EnToolkit.pos_tagging(en_tokens)
	for tag in  en_tags:
		for text in tag:
			enFile.write(f"{text} ")
		enFile.write("\n")

	enFile.close()

	viFile_path = os.path.join(viPath, namefile)
	print(f"[INFO] Vietnamese Pos Tagging file {viFile_path}")
	
	viFile = open(viFile_path, "w")

	vi_tags = ViToolkit.pos_tagging(pair_sent['vi'])
	for tag in vi_tags:
		for text in tag:
			viFile.write(f"{text} ")
		viFile.write("\n")

	viFile.close()

def chunking(namefile, enPath, viPath, pair_sent):
	enFile_path = os.path.join(enPath, namefile)
	print(f"[INFO] English Chunking file {enFile_path}")
	
	enFile = open(enFile_path, "w")
	en_tokens = EnToolkit.word_seg(pair_sent['en'])
	en_tags = EnToolkit.pos_tagging(en_tokens)
	enChunking = EnToolkit.chunking(en_tags)
	enFile.write(f"{enChunking}")

	enFile.close()

	viFile_path = os.path.join(viPath, namefile)
	print(f"[INFO] Vietnamese Chunking file {viFile_path}")
	
	viFile = open(viFile_path, "w")

	viChunking = ViToolkit.chunking(pair_sent['vi'])
	viFile.write(f"{viChunking}")

	viFile.close()

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

	enWord_path = os.path.join(wordPath, "en")
	if not os.path.exists(enWord_path):
		os.makedirs(enWord_path)

	viWord_path = os.path.join(wordPath, "vi")
	if not os.path.exists(viWord_path):
		os.makedirs(viWord_path)

	# Pos Tagging results path
	tagPath = os.path.join(cur_path, "tags")
	if not os.path.exists(tagPath):
		os.makedirs(tagPath)

	enTag_path = os.path.join(tagPath, "en")
	if not os.path.exists(enTag_path):
		os.makedirs(enTag_path)

	viTag_path = os.path.join(tagPath, "vi")
	if not os.path.exists(viTag_path):
		os.makedirs(viTag_path)

	# Chunking results path
	chunkPath = os.path.join(cur_path, "chunk")
	if not os.path.exists(chunkPath):
		os.makedirs(chunkPath)

	enChunk_path = os.path.join(chunkPath, "en")
	if not os.path.exists(enChunk_path):
		os.makedirs(enChunk_path)

	viChunk_path = os.path.join(chunkPath, "vi")
	if not os.path.exists(viChunk_path):
		os.makedirs(viChunk_path)		

	for i in range(num_sent):
		namefile = str(i+1)
		while len(namefile) != 6:
			namefile = "0" + namefile
		namefile += ".txt"

		print(f"===== WORD SEGMENTATION =====\n")
		word_segmentation(namefile, enWord_path, viWord_path, pair_sentence[i])
		print(f"=============================\n")
		print(f"======== POS TAGGING ========\n")
		pos_tagging(namefile, enTag_path, viTag_path, pair_sentence[i])
		print(f"=============================\n")
		print(f"========= CHUNKING ==========\n")
		chunking(namefile, enChunk_path, viChunk_path, pair_sentence[i])
		print(f"=============================\n")


	del pair_sentence