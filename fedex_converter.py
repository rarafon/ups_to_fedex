service_level_index = {
	"Ground Commercial": True,
	"Ground Hundredweight": False,
	"Ground Residential": True,
	"2nd Day Air Commercial": True,
	"2nd Day Air Residential": True,
	"UPS SurePost - 1 LB or Greater": True,

	"Worldwide Expedited": False,
	"Ground Undeliverable Return": False,
	# Probably Adjustments
	"Residential": False,
	# Probably Adjustments
	"Ground": False,
	# Usually adjustments
	"Residential Surcharge": False,
	#Adjustments
	"Expedited": False,
	"Standard Shipment": False,
	"Worldwide Express": False,
	"Worldwide Standard": False,
	"Ground Return to Sender": False,
}

def convert(ups_data, fedex_list, max_service_level_num):
	for date, data_track_num_obj in ups_data.items():
		for track_num, ups_data_obj in data_track_num_obj.items():
			formatted_ups_data = ups_data_obj.get_rate_data()
			fedex_list.add_data(date, track_num, formatted_ups_data)