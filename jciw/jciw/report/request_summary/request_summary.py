# Copyright (c) 2013, FInByz Tech Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from itertools import zip_longest
from frappe import _
from frappe.utils import flt

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	chart = get_chart_data(data,filters)
	return columns, data, None, chart

def get_columns(filters):
	columns= [{ "label": _("Particulars"),"fieldname": "particulars","fieldtype": "data","width": 300},
	{ "label": _("Open"),"fieldname": "open","fieldtype": "Int","width": 100},
	{ "label": _("On Hold"),"fieldname": "hold","fieldtype": "Int","width": 100},
	{ "label": _("Overdue"),"fieldname": "overdue","fieldtype": "Int","width": 100}]

	return columns

def get_data(filters):
	if filters.get("based_on"):
		
		open_data = frappe.db.sql("""
			select IFNULL(count(name), 0) as open, {0} as particulars
			from `tabIssue` where status = "Open"
			group by {0}
		""".format(filters.get("based_on").lower()),as_dict=True)

		hold_data = frappe.db.sql("""
			select IFNULL(count(name), 0) as hold, {0}
			from `tabIssue` where status = "Hold"
			group by {0}
		""".format(filters.get("based_on").lower()),as_dict=True)

		overdue_data = frappe.db.sql("""
			select IFNULL(count(name), 0) as overdue, {0}
			from `tabIssue` where sla_status = "Overdue" and status = "Open"
			group by {0}
		""".format(filters.get("based_on").lower()),as_dict=True)

		data = [{**u, **v, **m } for u, v, m in zip_longest(open_data, hold_data, overdue_data, fillvalue={})]

		return data

def get_chart_data(data,filters):

	total_open = []
	total_hold = []
	total_overdue = []
	labels = []
	for row in data:
		total_open.append(flt(row.get('open')))
		total_hold.append(flt(row.get('hold')))
		total_overdue.append(flt(row.get('overdue')))
		labels.append(row.get('particulars'))

	datasets = []

	if total_open:
		datasets.append({
			'name': "Open",
			'values': total_open
		})
	
	if total_hold:
		datasets.append({
			'name': "Hold",
			'values': total_hold
		})

	if total_overdue:
		datasets.append({
			'name': "Overdue",
			'values': total_overdue
		})

	chart = {
		"data": {
			'labels': labels,
			'datasets': datasets
		}
	}
	chart["type"] = "bar"
	return chart