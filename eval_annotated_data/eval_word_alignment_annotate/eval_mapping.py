'''
	Name: Evaluation of English and Vietnamese mapping process between chunking and word aligment
	author: Tien M. Pham
	last updated: 23.11.21
'''

import os
import logging

def annotated_senctence_to_list(sen1, sen2):
	'''
		params:
			sen1, sen2: raw annotated text. ex: 1-2,3;2-4,5 
		return:
			word_align_sen1, word_align_sen2: list each align word in list. ex [(1,2), (1,3), (2,4), (2,5)]
	'''
	word_align_sen1 = []
	word_align_sen2 = []

	sen1 = sen1.split(";")[:-1] # Remove empty string result of last ";" digit
	for pattern in sen1:
		label = pattern.split("-")
		for order1 in label[0].split(","):
			for order2 in label[1].split(","):
				word_align_sen1.append((order1, order2))

	sen2 = sen2.split(";")[:-1] # Remove empty string result of last ";" digit
	for pattern in sen2:	
		label = pattern.split("-")
		for order1 in label[0].split(","):
			for order2 in label[1].split(","):
				word_align_sen2.append((order1, order2))

	return word_align_sen1, word_align_sen2


def calculate_F1_score(word_align1, word_align2, logger):
	'''
		params:
			word_align1, word_align2: word alignment mapping label 

		return:
			F1 score - Inner annotator agreement of one word alignment sentence
	'''

	tp = 0 		# True Positive
	fp = 0		# False Positive
	fn = 0		# False Negative

	sorted(word_align1, key = lambda x : x[0])
	sorted(word_align2, key = lambda x : x[0])
	for i in range(len(word_align1)):
		found_first_val = False
		found_second_val = False
		for j in range(len(word_align2)):
			if (word_align1[i][0] == word_align2[j][0]):
				found_first_val = True
				if word_align1[i][1] == word_align2[j][1]:
					tp += 1
					found_second_val = True
					break


		if found_first_val and not found_second_val:
			fp += 1
			continue

		if not found_first_val and not found_second_val:
			fn += 1

	logger.info(f"TP = {tp}, FP = {fp}, FN = {fn}")
	if tp + fp == 0 or  tp + fn == 0:
		raise ZeroDivisionError

	precision = tp / (tp + fp)
	recall= tp / (tp + fn)

	return 2 * precision * recall / (precision + recall)


def main():
	# create logger with inner annotator agrement evaluate application
	logger = logging.getLogger('iaa_evaluation')
	logger.setLevel(logging.DEBUG)
	# create handlers 
	fh = logging.FileHandler('iaa_evaluation.log')
	fh.setLevel(logging.INFO)
	ch = logging.StreamHandler()
	ch.setLevel(logging.INFO)
	# create formatter and add it to the handlers
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)
	ch.setFormatter(formatter)
	# add the handlers to the logger
	logger.addHandler(fh)
	logger.addHandler(ch)

	basePath = os.getcwd()
    # Suppose 2 annotator
	annotatorDir_paths = []
	for annotator in sorted(os.listdir(basePath)):
		path = os.path.join(basePath, annotator)
		if os.path.isdir(path):
			annotatorDir_paths.append(path)

	annotator1 = [os.path.join(annotatorDir_paths[0], nameset) for nameset in sorted(os.listdir(annotatorDir_paths[0]))]
	annotator2 = [os.path.join(annotatorDir_paths[1], nameset) for nameset in sorted(os.listdir(annotatorDir_paths[1]))]

	for num_set in range(min(len(annotator1), len(annotator2))):
		anno1 = open(annotator1[num_set], "r")
		map_contents1 = anno1.readlines()
		anno1.close()
		for i in range(len(map_contents1)):
			map_contents1[i] = map_contents1[i][:-1]

		anno2 = open(annotator2[num_set], "r")
		map_contents2 = anno2.readlines()
		anno2.close()
		for i in range(len(map_contents2)):
			map_contents2[i] = map_contents2[i][:-1]

		logger.info(f"Evaluating mapping & correct for SET {num_set + 1}...")

		average_f1_score = 0
		for i in range(len(map_contents1)):
			word_align1, word_align2 = annotated_senctence_to_list(map_contents1[i], map_contents2[i])
			sen_f1_score = calculate_F1_score(word_align1, word_align2, logger)
			average_f1_score += sen_f1_score
			logger.info(f"F1 score of sentence {i+1}: {sen_f1_score*100:2f}")
		
		average_f1_score = average_f1_score / len(map_contents1)
		logger.info(f"Inner annotator agreement of SET {num_set + 1}: {average_f1_score*100:2f}")

if __name__ == '__main__':
	main()