import ffile, csv
from . import excel_helper

simple_ups_fieldnames = {
	"tracking_num": "Tracking Number",
	"service_level": "Service Level",
	"weight": "Weight",
	"zone": "Zone",
	# "Reference No": "Reference No.1",
	"pickup_date": "Pickup Date",
	"billed_charge": "Billed Charge",
	"invoice_section": "Invoice Section",
	"incentive_credit": "Incentive Credit",
	"invoice_date": "Invoice Date",
}

def read_simple_ups(simple_ups_filename, folder_name):
	fieldnames_index = {}

	ffile.move_dir(folder_name)

	total_simple_ups_data = {}

	def filter_data(simple_ups):
	# Input: detail_ups_dic
	# Return True if this detail_ups_dic should be added.
	# False otherwise.
		tracking_num = simple_ups["tracking_num"]
		if tracking_num == "":
			return False
		else:
			return True


	def get_fieldnames(row):
		fieldnames_dic = {}
		for infile_name, file_fieldname in simple_ups_fieldnames.items():
			fieldnames_dic[infile_name] = row.index(file_fieldname)
		return fieldnames_dic

	def extract_data(row):
		ups_simple_dic = {}
		for fieldname, column in fieldnames_index.items():
			if fieldname == "billed_charge":
				ups_simple_dic[fieldname] = excel_helper.convert_charge_string_to_float(row[column])
			else:
				ups_simple_dic[fieldname] = row[column]
		return ups_simple_dic


	with open(simple_ups_filename) as f_simple:
		reader = csv.reader(f_simple)

		# find row with fieldnames & set fieldnames_index
		for row in reader:
			try:
				if "Account Number" in row:
					fieldnames_index = get_fieldnames(row)
					break
			except IndexError:
				pass

		tracking_num_column = fieldnames_index["tracking_num"]

		for row in reader:
			tracking_num = row[tracking_num_column]
			# print(tracking_num, simple_ups_filename)
			simple_ups_data = extract_data(row)
			if not filter_data(simple_ups_data):
				continue
			if tracking_num not in total_simple_ups_data:
				total_simple_ups_data[tracking_num] = [simple_ups_data,]
			else:
				total_simple_ups_data[tracking_num].append(simple_ups_data)


	ffile.dir_back()

	return total_simple_ups_data

detail_ups_index = {
	#"N" seems to be inaccurate as the multiple packages
	# would have the same tracking num in "N"
	"tracking_num": "U",
	"charge_type": "AT",
	# "Charge Symbol": "AR",
	"billed_charge": "BA",
	"incentive_credit": "AZ",
}

def get_detail_fieldnames_index():
	f_index = {}
	for fieldname, column_letter in detail_ups_index.items():
		column_num = excel_helper.get_column_num(column_letter)
		f_index[fieldname] = column_num
	return f_index

def read_detail_ups(detail_ups_filename, folder_name):
	total_detail_ups_data = {}

	fieldnames_index = {}
	prev_track_num = ""

	def extract_data_from_row(row):
		# Extracts data from the row of csv file using
		# fieldnames_index dic which gives which and what columns to extract
		ups_detail_dic = {}
		for fieldname, column_num in fieldnames_index.items():
			if fieldname == "billed_charge":
				ups_detail_dic[fieldname] = excel_helper.convert_charge_string_to_float(row[column_num])
			else:
				ups_detail_dic[fieldname] = row[column_num]
		return ups_detail_dic

	def filter_data(detail_ups):
		# Input: detail_ups_dic
		# Return True if this detail_ups_dic should be added.
		# False otherwise.
		tracking_num = detail_ups["tracking_num"]
		billed_charge = detail_ups["billed_charge"]
		if tracking_num == "":
			return False
		elif billed_charge == 0:
			return False
		else:
			return True

	ffile.move_dir(folder_name)

	fieldnames_index = get_detail_fieldnames_index()

	with open(detail_ups_filename) as f_detail:
		reader = csv.reader(f_detail)

		for row in reader:
			detail_ups_dic = extract_data_from_row(row)

			tracking_num = detail_ups_dic["tracking_num"]

			# skip those without tracking number or with 0 billed charge
			if not filter_data(detail_ups_dic):
				continue

			if tracking_num not in total_detail_ups_data:
				total_detail_ups_data[tracking_num] = [[detail_ups_dic,]]
			else:
				d_list = total_detail_ups_data[tracking_num]
				if prev_track_num == tracking_num:
					# print(d_list[len(d_list) -1])
					last_ups_detail_list = d_list[len(d_list) -1]
					last_ups_detail_list.append(detail_ups_dic)
				else:
					d_list.append([detail_ups_dic,])
			# print(tracking_num, prev_track_num, tracking_num == prev_track_num, tracking_num not in total_detail_ups_data)
			prev_track_num = tracking_num


				# print(detail_ups_dic)
	# print(fieldnames_index)
	ffile.dir_back()

	# print(total_detail_ups_data['1Z0019850396816706'])

	return total_detail_ups_data