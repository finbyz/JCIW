frappe.provide('frappe.dashboards.chart_sources');

frappe.dashboards.chart_sources["ISSUE STATUS"] = {
	method: "jciw.jciw.dashboard_chart_source.issue_status.issue_status.get",
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 0
		}
		
	]
};