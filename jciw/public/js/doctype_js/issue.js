cur_frm.fields_dict.technician.get_query = function (doc) {
    if (doc.site){
        return {
            filters: {
                "site": doc.site        
            }
        }
    }

};

frappe.ui.form.on("Issue", {
    onload: function(frm){
        if(!frm.doc.subject){
            frm.set_value("subject","Case Open Case Number #")
        }
    },
    mobile_number: function(frm){
        if(frm.doc.mobile_number){
            frm.set_value("mobile_no_sms",frm.doc.mobile_number + ".amh@amh.mshastra.com")
        }
    },
    validate:function(frm){
        if(frm.doc.jci_project_number.length>=11){
            frappe.throw("JCI Project Number lenght should not be greater then 10")
        }
        if(frm.doc.mobile_number){
            frm.set_value("mobile_no_sms",frm.doc.mobile_number + ".amh@amh.mshastra.com")
        }
    },
    technician_contact_mobile: function(frm){
        if(frm.doc.technician_contact_mobile){
            message = "Test"
            frappe.call({
                method: "frappe.core.doctype.sms_settings.sms_settings.send_sms",
                args: {
                    receiver_list: [frm.doc.technician_contact_mobile],
                    msg: message
                }
                });
                alert(message)
        }
    }

})