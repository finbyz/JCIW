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