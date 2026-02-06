// Copyright (c) 2026, Munene Morris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Main Event", {
	refresh(frm) {

	},
    start_date(frm) {
        if (frm.doc.start_date) {
            const today = frappe.datetime.get_today();
            if (frm.doc.start_date <= today) {
                frappe.msgprint("Start Date must be greater than today");
                frm.set_value("start_date", "");
            }
        }
    },
    end_date(frm) {
        if (frm.doc.end_date) {
            if (frm.doc.end_date < frm.doc.start_date) {
                frappe.msgprint("End Date must be greater or equal than Start Date");
                frm.set_value("end_date", "");
            }
        }
    }
});
