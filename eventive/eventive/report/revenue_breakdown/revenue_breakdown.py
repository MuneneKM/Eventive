# Copyright (c) 2026, Munene Morris and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {
            "label": "Main Event",
            "fieldname": "event",
            "fieldtype": "Link",
            "options": "Main Event",
            "width": 200,
        },
        {
            "label": "Event Name",
            "fieldname": "event_name",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": "Registration Revenue",
            "fieldname": "registration_revenue",
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "label": "Sponsor Revenue",
            "fieldname": "sponsor_revenue",
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "label": "Booth Revenue",
            "fieldname": "booth_revenue",
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "label": "Total Revenue",
            "fieldname": "total_revenue",
            "fieldtype": "Currency",
            "width": 150,
        },
    ]


def get_data(filters):
    events = frappe.get_all("Main Event", fields=["name"])

    result = []

    for event in events:
        registration_revenue = get_registration_revenue(event.name)
        sponsor_revenue = get_sponsor_revenue(event.name)
        booth_revenue = get_booth_revenue(event.name)

        total_revenue = registration_revenue + sponsor_revenue + booth_revenue

        result.append({
            "event": event.name,
            "event_name": frappe.db.get_value("Main Event", event.name, "event_name"),
            "registration_revenue": registration_revenue,
            "sponsor_revenue": sponsor_revenue,
            "booth_revenue": booth_revenue,
            "total_revenue": total_revenue,
        })

    return result


def get_registration_revenue(event_name):
    revenue = frappe.db.sql("""
        SELECT
            SUM(total_amount)
        FROM
            `tabEvent Registration`
        WHERE
            event = %s
    """, event_name)

    return revenue[0][0] or 0


def get_sponsor_revenue(event_name):
    revenue = frappe.db.sql("""
        SELECT
            SUM(st.amount)
        FROM
            `tabSponsor` s
        JOIN
            `tabSponsor Tier` st
            ON s.tier = st.name
        WHERE
            s.event = %s
    """, event_name)

    return revenue[0][0] or 0


def get_booth_revenue(event_name):
    revenue = frappe.db.sql("""
        SELECT
            SUM(bp.price)
        FROM
            `tabExhibitor` e
        JOIN
            `tabBooth Package` bp
            ON e.booth_package = bp.name
        WHERE
            e.event = %s
    """, event_name)

    return revenue[0][0] or 0
