import frappe
from frappe.utils import now
from frappe.utils import nowdate, add_days, getdate, get_time, add_months
import datetime
from datetime import  timedelta, date, time

def issue_before_naming(self,method):
	pass
	# if self.series_value:
	# 	self.name = "JCIW-"+str(self.series_value)

def issue_before_validate(self,method):
	pass

def issue_validate(self,method):
	set_subject(self)
	set_escalation_due_date(self)

def set_subject(self):
	if self.subject == "Case Open Case Number #":
		self.subject = "Case Open Case Number - {}".format(self.name)

def set_escalation_due_date(self):
	hours = [{'hour':2,'min':15},{'hour':2,'min':30},{'hour':4,'min':0}]
	for hour in hours:	
		default_holiday = frappe.db.get_value("Company","JCIW",'default_holiday_list')
		holiday = frappe.get_doc("Holiday List",default_holiday)
		holiday_list =[row.holiday_date for row in holiday.holidays]
		
		default_shift = frappe.get_doc("Shift Type","Default Shift")
		default_shift.start_time = get_time(default_shift.start_time)
		default_shift.end_time = get_time(default_shift.end_time)
		
		due_date = getdate(self.opening_date)
		opening_time = get_time(self.opening_time)
		if due_date in holiday_list or opening_time > default_shift.end_time:
			due_date = add_days(due_date,1)
			due_time = (datetime.datetime.combine(datetime.date.today(), default_shift.start_time) + timedelta(hours=hour['hour'], minutes=hour['min'])).time()
		elif due_date in holiday_list or opening_time < default_shift.start_time:
			due_time = (datetime.datetime.combine(datetime.date.today(), default_shift.start_time) + timedelta(hours=hour['hour'], minutes=hour['min'])).time()
		else:
			due_time = (datetime.datetime.combine(datetime.date.today(), opening_time) + timedelta(hours=hour['hour'], minutes=hour['min'])).time()

		if due_date not in holiday_list:
			default_shift.lunch_start_time = get_time(default_shift.lunch_start_time)
			default_shift.lunch_end_time = get_time(default_shift.lunch_end_time)

			# convert to datetime.timedelta for addition and subtraction of time
			a = datetime.datetime.combine(datetime.date.today(), due_time)
			b = datetime.datetime.combine(datetime.date.today(), default_shift.lunch_start_time)
			c = datetime.datetime.combine(datetime.date.today(), default_shift.lunch_end_time)
			d = datetime.datetime.combine(datetime.date.today(), opening_time)
			extra_hrs = 0 
			
			# to add lunch extra hrs in due time
			if is_hour_between(opening_time,due_time,default_shift.lunch_start_time):
				extra_hrs = min((a - b),(c - b))	
			elif is_hour_between(opening_time,due_time,default_shift.lunch_end_time):
				extra_hrs = c - d	
			#frappe.msgprint(str(extra_hrs))
			if extra_hrs:
				due_time = max(due_time,default_shift.lunch_end_time)
				due_time = get_time(datetime.datetime.combine(datetime.date.today(), due_time) + extra_hrs)

		if due_time > default_shift.end_time:
			#due_time =  due_time
			date = datetime.date(1, 1, 1)
			datetime1 = datetime.datetime.combine(date, due_time)
			datetime2 = datetime.datetime.combine(date, default_shift.end_time)
			datetime3 = datetime.datetime.combine(date, default_shift.start_time)
			final_due_time = datetime1 - datetime2 + datetime3
			due_time = get_time(final_due_time)
			#due_time = (datetime.datetime.combine(datetime.date.today(), default_shift.start_time) + timedelta(hours=hour['hour'], minutes=hour['min'])).time()
			due_date = add_days(due_date,1)
			delta = timedelta(days=1)
			while due_date in holiday_list:
				due_date += delta
			if hours.index(hour) == 0:
				self.db_set('escalation_1_due__date',datetime.datetime.combine(due_date,due_time))
			if hours.index(hour) == 1:
				self.db_set('escalation_2_due__date',datetime.datetime.combine(due_date,due_time))
			else:
				self.db_set('escalation_3_due__date',datetime.datetime.combine(due_date,due_time))
		else:
			delta = timedelta(days=1)
			while due_date in holiday_list:
				due_date += delta
			if hours.index(hour) == 0:
				self.db_set('escalation_1_due__date',datetime.datetime.combine(due_date,due_time))
			if hours.index(hour) == 1:
				self.db_set('escalation_2_due__date',datetime.datetime.combine(due_date,due_time))
			else:
				self.db_set('escalation_3_due__date',datetime.datetime.combine(due_date,due_time))

def is_hour_between(start, end, now):
	is_between = False

	is_between |= start <= now <= end
	is_between |= end < start and (start <= now or now <= end)

	return is_between

@frappe.whitelist()
def escalation_email():
	data = frappe.get_list("Issue",filters = {'technician':['=',''],'status':"Open"},fields = 'name')
	for row in data:
		doc = frappe.get_doc("Issue",row.name)
		recipients_1 = []
		recipients_2 = []
		recipients_3 = []


		header = ""
		subject = ""
		
		if doc.escalation_1_due__date:
			if str(doc.escalation_1_due__date) <= now() and not doc.escalation_1_sent:
				recipients_1 = doc.escalation_1_email.split(",")
				header = "<p>This is a warning notification for a first response time getting overdue at {}</p>".format(doc.escalation_1_due__date.strftime('%B %d %Y, %I:%M %p'))
				subject = "SLA Escalation. Case Number {} Request due at : {}".format(doc.name,doc.escalation_1_due__date.strftime('%B %d %Y, %I:%M %p'))
				doc.db_set('escalation_1_sent',1)

		if doc.escalation_2_due__date:
			if str(doc.escalation_2_due__date) <= now() and not doc.escalation_2_sent:
				recipients_2 = doc.escalation_2_email.split(",")
				header = "<p>This is a warning notification for a first response time getting overdue at {}</p>".format(doc.escalation_2_due__date.strftime('%B %d %Y, %I:%M %p'))
				subject = "SLA Escalation. Case Number {} Request due at : {}".format(doc.name,doc.escalation_2_due__date.strftime('%B %d %Y, %I:%M %p'))
				doc.db_set('escalation_2_sent',1)

		if doc.escalation_3_due__date:
			if str(doc.escalation_3_due__date) <= now() and not doc.escalation_3_sent:
				recipients_3 = doc.escalation_3_email.split(",")
				if doc.site:
					site_manager = frappe.db.get_value("Technician",{"site":doc.site},"reports_to")
					if site_manager:
						recipients_3.append(site_manager)
				header = "<p>This is a warning notification for a first response time getting overdue at {}</p>".format(doc.escalation_3_due__date.strftime('%B %d %Y, %I:%M %p'))
				subject = "SLA Escalation. Case Number {} Request due at : {}".format(doc.name,doc.escalation_3_due__date.strftime('%B %d %Y, %I:%M %p'))
				doc.db_set('escalation_3_sent',1)

		body = """
				<ul>
				<li>Company Name</li> : {0}
				<li>Project Name</li> : {1}
				<li>Project Num</li> : {2}
				<li>Unit Type</li> : {3}
				<li>Failure Details</li> : {4}
				<li>JCIW Ticket</li> : {5}
				</ul>
				<a href="/desk#Form/Issue/{6}">
				Click here to view the ticket.
				</a>
			""".format(
				doc.company_name or '',
				doc.project_name or '',
				doc.jci_project_number or '',
				doc.unit_type or '',
				doc.failure_details or '',
				doc.name or '',
				doc.name or ''
			)

		message = header + body
		recipients = recipients_1 + recipients_2 + recipients_3
		if recipients:
			frappe.sendmail(
				recipients=recipients,
				cc = '',
				subject = subject ,
				#sender = sender,
				message = message,
				now = 1
			)

@frappe.whitelist()			
def make_status_overdue():
	data = frappe.get_list("Issue",filters = {'escalation_3_due__date':['<',now()],'status':'Open','sla_status':['!=','Overdue']},fields = 'name')
	for row in data:
		doc = frappe.get_doc("Issue",row.name)
		doc.db_set('sla_status',"Overdue")