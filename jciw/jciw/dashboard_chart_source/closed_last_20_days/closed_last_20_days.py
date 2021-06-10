import frappe
from frappe.utils.dashboard import cache_source
from frappe import _

@frappe.whitelist()
@cache_source
def get(chart_name = None, chart = None, no_cache = None, filters = None, from_date = None,
	to_date = None, timespan = None, time_interval = None, heatmap_year = None):

	data = frappe.db.sql("""
		select CAST(resolution_date AS DATE) as resolution_date,count(name) as total_issue
		from `tabIssue`
		where 
		status = "Closed" and CAST(resolution_date AS DATE) BETWEEN CURDATE() - INTERVAL 20 DAY AND CURDATE()
		group by CAST(resolution_date AS DATE) 
	""",as_dict=True)
	
	labels = []
	datapoint = []
	for row in data:
		labels.append(row.resolution_date)
		datapoint.append(row.total_issue)	
	return{
		"labels": labels,
		"datasets": [{
			"name": _("Request"),
			"values": datapoint
		}],
		"type": "bar"
	}