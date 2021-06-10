// Copyright (c) 2016, FInByz Tech Pvt Ltd and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Request Summary"] = {
	"filters": [
		{
			fieldname: "based_on",
			label: __("Based On"),
			fieldtype: "Select",
			options: ["Technician","Level","Priority"],
			default: "Technician",
			reqd: 1
		}
	]
};
