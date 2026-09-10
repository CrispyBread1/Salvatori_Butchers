from datetime import date, timedelta


def create_dummy_invoice(
    invoice_number,
    invoice_date,
    record_create_time,
    name,
    account_ref,
    order_number,
    contact_name,
    invoice_net
):
    invoice_tax = round(invoice_net * 0.2, 2)
    invoice_gross = round(invoice_net + invoice_tax, 2)

    invoice_date_string = invoice_date.strftime("%d/%m/%Y")
    payment_due_date = (
        invoice_date + timedelta(days=30)
    ).strftime("%d/%m/%Y")

    return {
        "invoiceNumber": str(invoice_number),
        "invoiceTypeCode": 1,
        "invoiceType": "Product Invoice (from SOP)",
        "invoiceOrCredit": "Invoice",
        "invoiceDate": f"{invoice_date_string} 00:00:00",
        "accountRef": account_ref,
        "name": name,
        "address1": "Dummy Address",
        "address2": "",
        "address3": "Whitstable",
        "address4": "Kent",
        "address5": "CT5 1AA",
        "cAddress1": "Dummy Address",
        "cAddress2": "",
        "cAddress3": "Whitstable",
        "cAddress4": "Kent",
        "cAddress5": "CT5 1AA",
        "delName": "",
        "delAddress1": "Dummy Address",
        "delAddress2": "",
        "delAddress3": "Whitstable",
        "delAddress4": "Kent",
        "delAddress5": "CT5 1AA",
        "vatRegNumber": "",
        "orderNumber": str(order_number),
        "orderNumberNumeric": str(order_number),
        "contactName": contact_name,
        "takenBy": "Development",
        "custOrderNumber": f"PO-{order_number}",
        "custTelNumber": "01234567890",
        "notes1": "Development dummy invoice",
        "notes2": "",
        "notes3": "",
        "custDiscRate": 0,
        "foreignItemsNet": invoice_net,
        "foreignItemsTax": invoice_tax,
        "foreignItemsGross": invoice_gross,
        "itemsNet": invoice_net,
        "itemsTax": invoice_tax,
        "itemsGross": invoice_gross,
        "taxRate1": 20,
        "taxRate2": 0,
        "taxRate3": 0,
        "taxRate4": 0,
        "taxRate5": 0,
        "netAmount1": invoice_net,
        "netAmount2": 0,
        "netAmount3": 0,
        "netAmount4": 0,
        "netAmount5": 0,
        "taxAmount1": invoice_tax,
        "taxAmount2": 0,
        "taxAmount3": 0,
        "taxAmount4": 0,
        "taxAmount5": 0,
        "globalNomCode": "",
        "globalDetails": "",
        "globalTaxCode": "T0",
        "globalDeptNumber": "0",
        "globalDeptName": "Default",
        "courierNumber": "1",
        "courierName": "Salvatori Delivery",
        "consignment": "",
        "carrNomCode": "",
        "carrTaxCode": "T0",
        "carrDeptNumber": "0",
        "carrDeptName": "Default",
        "foreignCarrNet": 0,
        "foreignCarrTax": 0,
        "foreignCarrGross": 0,
        "carrNet": 0,
        "carrTax": 0,
        "carrGross": 0,
        "foreignInvoiceNet": invoice_net,
        "foreignInvoiceTax": invoice_tax,
        "foreignInvoiceGross": invoice_gross,
        "invoiceNet": invoice_net,
        "invoiceTax": invoice_tax,
        "invoiceGross": invoice_gross,
        "currency": "1",
        "currencyType": "0",
        "euroGross": invoice_gross,
        "euroRate": 1,
        "foreignRate": 1,
        "settlementDueDays": "30",
        "settlementDiscRate": 0,
        "foreignSettlementDiscAmount": 0,
        "foreignSettlementTotal": invoice_gross,
        "foreignAmountPrepaid": 0,
        "settlementDiscAmount": 0,
        "settlementTotal": invoice_gross,
        "amountPrepaid": 0,
        "paymentRef": "",
        "printed": "",
        "printedCode": "0",
        "posted": "",
        "postedCode": "0",
        "quoteExpiryDate": "",
        "quoteStatus": "",
        "quoteStatusID": "0",
        "recurringRef": "",
        "dunsNumber": "",
        "netValueDiscountAmount": 0,
        "netValueDiscountRate": 0,
        "netValueDiscountDescription": "",
        "netValueDiscountComment1": "",
        "netValueDiscountComment2": "",
        "paymentType": "0",
        "bankRef": "",
        "gdnNumber": "0",
        "projectID": "0",
        "analysis1": "",
        "analysis2": "",
        "analysis3": "",
        "paymentDueDate": f"{payment_due_date} 00:00:00",
        "invoicePaymentID": "",
        "resubmitInvoicePaymentRequired": "0",
        "containsCisReverseChargeItems": "0",
        "recordCreateDate": (
            f"{invoice_date_string} {record_create_time}"
        ),
        "recordModifyDate": (
            f"{invoice_date_string} {record_create_time}"
        ),
        "recordDeleted": "0"
    }


today = date.today()

yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
day_after_tomorrow = today + timedelta(days=2)


DUMMY_INVOICES = {
    "results": [
        # Yesterday
        create_dummy_invoice(
            invoice_number="10001",
            invoice_date=yesterday,
            record_create_time="07:15:00",
            name="The Crown Inn",
            account_ref="CHARHOU",
            order_number="5001",
            contact_name="John Smith",
            invoice_net=245.50
        ),
        create_dummy_invoice(
            invoice_number="10002",
            invoice_date=yesterday,
            record_create_time="09:30:00",
            name="Whitstable Kitchen",
            account_ref="WHITK01",
            order_number="5002",
            contact_name="Sarah Jones",
            invoice_net=382.75
        ),
        create_dummy_invoice(
            invoice_number="10003",
            invoice_date=yesterday,
            record_create_time="14:45:00",
            name="Harbour Fish Bar",
            account_ref="HARBOUR01",
            order_number="5003",
            contact_name="James Brown",
            invoice_net=128.20
        ),

        # Today
        create_dummy_invoice(
            invoice_number="10004",
            invoice_date=today,
            record_create_time="06:45:00",
            name="Kent Catering",
            account_ref="KENTC01",
            order_number="5004",
            contact_name="Emma Wilson",
            invoice_net=625.00
        ),
        create_dummy_invoice(
            invoice_number="10005",
            invoice_date=today,
            record_create_time="08:20:00",
            name="Seaside Hotel",
            account_ref="SEA01",
            order_number="5005",
            contact_name="Michael Green",
            invoice_net=410.60
        ),
        create_dummy_invoice(
            invoice_number="10006",
            invoice_date=today,
            record_create_time="11:35:00",
            name="Kent Catering",
            account_ref="KENTC01",
            order_number="5006",
            contact_name="Emma Wilson",
            invoice_net=185.40
        ),
        create_dummy_invoice(
            invoice_number="10007",
            invoice_date=today,
            record_create_time="15:10:00",
            name="The Crown Inn",
            account_ref="CHARHOU",
            order_number="5007",
            contact_name="John Smith",
            invoice_net=302.15
        ),

        # Tomorrow
        create_dummy_invoice(
            invoice_number="10008",
            invoice_date=tomorrow,
            record_create_time="07:05:00",
            name="Farm Shop",
            account_ref="FARM01",
            order_number="5008",
            contact_name="David Taylor",
            invoice_net=290.25
        ),
        create_dummy_invoice(
            invoice_number="10009",
            invoice_date=tomorrow,
            record_create_time="09:25:00",
            name="The Crown Inn",
            account_ref="CHARHOU",
            order_number="5009",
            contact_name="John Smith",
            invoice_net=175.80
        ),
        create_dummy_invoice(
            invoice_number="10010",
            invoice_date=tomorrow,
            record_create_time="12:40:00",
            name="Whitstable Kitchen",
            account_ref="WHITK01",
            order_number="5010",
            contact_name="Sarah Jones",
            invoice_net=520.10
        ),
        create_dummy_invoice(
            invoice_number="10011",
            invoice_date=tomorrow,
            record_create_time="16:15:00",
            name="Seaside Hotel",
            account_ref="SEA01",
            order_number="5011",
            contact_name="Michael Green",
            invoice_net=215.75
        ),

        # Day after tomorrow
        create_dummy_invoice(
            invoice_number="10012",
            invoice_date=day_after_tomorrow,
            record_create_time="07:30:00",
            name="Harbour Fish Bar",
            account_ref="HARBOUR01",
            order_number="5012",
            contact_name="James Brown",
            invoice_net=340.00
        ),
        create_dummy_invoice(
            invoice_number="10013",
            invoice_date=day_after_tomorrow,
            record_create_time="10:50:00",
            name="Kent Catering",
            account_ref="KENTC01",
            order_number="5013",
            contact_name="Emma Wilson",
            invoice_net=735.25
        ),
        create_dummy_invoice(
            invoice_number="10014",
            invoice_date=day_after_tomorrow,
            record_create_time="14:20:00",
            name="Farm Shop",
            account_ref="FARM01",
            order_number="5014",
            contact_name="David Taylor",
            invoice_net=196.40
        )
    ],
    "success": True,
    "code": 200,
    "response": None,
    "message": None
}
