'''
	Name:  Evaluating English and Vietnamese chunking annotation.
	author: Tien M. Pham
	last updated: 11.21.21
'''

import os
import logging


def chunk_info(chunk_label):
	word = chunk_label[0]
	label = chunk_label[1]
	return {
				"NumWords" : len(word.split(" ")),
				"word" : word,
				"label" : label
			}

def calculate_F1_score(chunking_phase01, chunking_phase02, logger):
	'''
		params:
			chunking_phase01: chunking label of annotator 1
			chunking_phase02: chunking label of annotator 2

		return:
			F1 score - Inner annotator agreement
	'''
	tp = 0 			# True Positive value
	fp = 0 			# False Positive value
	fn = 0 			# False Negative value

	chunk01 = []
	for chunk_label in chunking_phase01:
		chunk01.append(chunk_info(chunk_label))

	chunk02 = []
	for chunk_label in chunking_phase02:
		chunk02.append(chunk_info(chunk_label))

	# print(chunk01,"\n",chunk02)
	cur_chunk01 = 0
	cur_chunk02 = 0
	i = 0
	j = 0
	len_phase01 = len(chunk01)
	len_phase02 = len(chunk02)
	change_i = True
	change_j = True
	while i < len_phase01 and j < len_phase02:
		if change_i:
			cur_chunk01 += chunk01[i]["NumWords"]
			change_i = False

		if change_j:
			cur_chunk02 += chunk02[j]["NumWords"]
			change_j = False

		# print(f"{i} - {j} - {cur_chunk01} - {cur_chunk02}")
		if cur_chunk01 > cur_chunk02:
			j += 1
			change_j = True
		elif cur_chunk01 == cur_chunk02:
			if chunk01[i]["NumWords"] == chunk02[j]["NumWords"]:
				if chunk01[i]["word"] == chunk02[j]["word"]:
					if chunk01[i]["label"] == chunk02[j]["label"]:
						tp += 1
					else:
						fp += 1
			else:
				fn += 1

			i += 1
			j += 1
			change_i = True
			change_j = True
		elif cur_chunk01 < cur_chunk02:
			i += 1
			fn += 1
			change_i = True

	# print(f"[INFO] {tp} {fp} {fn}")
	logger.info(f"TP = {tp}, FP = {fp}, FN = {fn}")
	if tp + fp == 0 or  tp + fn == 0:
		raise ZeroDivisionError

	precision = tp / (tp + fp)
	recall= tp / (tp + fn)

	return 2 * precision * recall / (precision + recall)

def sentence_to_chunking_label(sentence):
	'''
		params:
			sentence: annotated chunking sentence
		return:
			list chunking label with format ["words", "chunking label"]
	'''

	i = 0
	n = len(sentence)
	label = ""
	chunking_phase = []
	while i < n:
		if sentence[i] == '(':
			label = ""
		elif sentence[i] == ')':
			space_pos = sentence.find(" ", i+1)
			if space_pos == -1:
				break

			label += sentence[i:space_pos]
			label = label.split("/")
			label[0] = label[0][:-1]		# Remove '(' and ')'
			chunking_phase.append(tuple(label))
			i = space_pos
		else: 
			label += sentence[i]
		i += 1

	return chunking_phase

def main():
	# create logger with inner annotator agrement evaluate application
	logger = logging.getLogger('iaa_evaluation')
	logger.setLevel(logging.DEBUG)
	# create file handler which logs even debug messages
	fh = logging.FileHandler('iaa_evaluation.log')
	fh.setLevel(logging.DEBUG)
	# create console handler with a higher log level
	ch = logging.StreamHandler()
	ch.setLevel(logging.INFO)
	# create formatter and add it to the handlers
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)
	ch.setFormatter(formatter)
	# add the handlers to the logger
	logger.addHandler(fh)
	logger.addHandler(ch)

	base_path = os.getcwd()
	annoDir_paths = []
	for basename in sorted(os.listdir(base_path)):
		path = os.path.join(base_path, basename)
		if os.path.isdir(path):
			annoDir_paths.append(path)

	for annoDir_path in annoDir_paths:
		# print(f"[INFO] ===== {os.path.basename(annoDir_path)} =====")
		# print(f"[INFO] ============ ENGLISH =================")
		logger.info(f"{os.path.basename(annoDir_path)}")
		logger.info(f"Evaluate English annotation")
		enAnnotated_file_paths = []
		viAnnotated_file_paths = []
		Annotated_files = sorted(os.listdir(annoDir_path))
		for filename in Annotated_files:
			filePath = os.path.join(annoDir_path, filename)
			if filename.split(".")[0].split("_")[-1] == "en":
				enAnnotated_file_paths.append(filePath)
			elif filename.split(".")[0].split("_")[-1] == "vi":
				viAnnotated_file_paths.append(filePath)

		# Evaluate English chunking
		enfile01 = open(enAnnotated_file_paths[0], "r")
		enContent01 = enfile01.readlines()
		enfile01.close()
		enfile02 = open(enAnnotated_file_paths[1], "r")
		enContent02 = enfile02.readlines()
		enfile02.close()
		enChunking01 = []
		for sentence in enContent01:
			enChunking01.append(sentence_to_chunking_label(sentence))

		enChunking02 = []
		for sentence in enContent02:
			enChunking02.append(sentence_to_chunking_label(sentence))

		# print(f"Length of English chunking 01: {len(enChunking01)}", "\n", enChunking01)
		# print(f"Length of English chunking 02: {len(enChunking02)}", "\n", enChunking02)
		enF1Score = 0
		for i in range(len(enChunking01)):
			# print(f"[INFO] sentence {i+1}")
			logger.info(f"Evaluating in sentence {i+1}...")
			enF1Score += calculate_F1_score(enChunking01[i], enChunking02[i], logger)
		enF1Score /= len(enChunking01)
		# print(f"[INFO] Inner Annotaer Agreement for English in {os.path.basename(annoDir_path)}: {enF1Score*100:02f}")
		logger.info(f"Inner Annotaer Agreement for English in {os.path.basename(annoDir_path)}: {enF1Score*100:02f}")

		# print(f"[INFO] ============== VIETNAMESE ================")
		logger.info(f"Evaluate Vietnamese annotation")
		# Evaluate Vietnamese chunking
		vifile01 = open(viAnnotated_file_paths[0], "r")
		viContent01 = vifile01.readlines()
		vifile01.close()
		vifile02 = open(viAnnotated_file_paths[1], "r")
		viContent02 = vifile02.readlines()
		vifile02.close()
		viChunking01 = []
		for sentence in viContent01:
			viChunking01.append(sentence_to_chunking_label(sentence))

		viChunking02 = []
		for sentence in viContent02:
			viChunking02.append(sentence_to_chunking_label(sentence))

		# print(f"Length of Vietnamese chunking 01: {len(viChunking01)}", "\n" ,viChunking01)
		# print(f"Length of Vietnamese chunking 02: {len(viChunking02)}", "\n", viChunking02)
		viF1Score = 0
		for i in range(len(viChunking01)):
			# print(f"[INFO] sentence {i+1}")
			logger.info(f"Evaluate in sentence {i+1}...")
			viF1Score += calculate_F1_score(viChunking01[i], viChunking02[i], logger)
		viF1Score /= len(viChunking01)
		# print(f"[INFO] Inner Annotaer Agreement for Vietnamese in {os.path.basename(annoDir_path)}: {viF1Score*100:02f}")
		logger.info(f"Inner Annotaer Agreement for Vietnamese in {os.path.basename(annoDir_path)}: {viF1Score*100:02f}")


if __name__ == '__main__':
	main()