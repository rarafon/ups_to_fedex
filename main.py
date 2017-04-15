import csv, shelve
import ffile

import ups_reader

py_filename = "ups"


def print_ups_data():
	for ups in ups_data:
		print(ups_data[ups])


def save_ups_data():
	ffile.move_dir('ups_data')

	shelfFile = shelve.open(py_filename)
	shelfFile['ups_data'] = ups_data
	shelfFile.close()

	ffile.dir_back()

ups_reader.read('data/ups_simple.csv')

# print_upKs_data()
# save_ups_data()

# with open('ups_detail.csv') as f_detail:
# 	reader = csv.reader(f_detail)