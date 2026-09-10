from datetime import date, timedelta


def create_dummy_invoice_item(
    item_id,
    invoice_number,
    invoice_date,
    record_create_time,
    description,
    stock_code,
    unit_price,
    quantity
):
    net_amount = round(unit_price * quantity, 2)

    invoice_date_string = invoice_date.strftime("%d/%m/%Y")

    return {
        "id": item_id,
        "invoiceNumber": invoice_number,
        "description": description,
        "stockCode": stock_code,
        "nominal": "4000",
        "details": "",
        "taxCode": "T1",
        "taxRate": 20,
        "unitPrice": unit_price,
        "quantity": quantity,
        "discount": 0,
        "netAmount": net_amount,
        "foreignNetAmount": net_amount,
        "comment1": "",
        "comment2": "",
        "departmentNumber": 1,
        "projectId": 0,
        "recordCreateDate": (
            f"{invoice_date_string} {record_create_time}"
        )
    }


today = date.today()

yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
day_after_tomorrow = today + timedelta(days=2)


DUMMY_INVOICE_ITEMS = {
    "results": [
        # Invoice 10001 - Yesterday
        create_dummy_invoice_item(
            item_id=1,
            invoice_number=10001,
            invoice_date=yesterday,
            record_create_time="07:15:00",
            description="Fresh Beef",
            stock_code="BE4",
            unit_price=12.50,
            quantity=4
        ),
        create_dummy_invoice_item(
            item_id=2,
            invoice_number=10001,
            invoice_date=yesterday,
            record_create_time="07:15:00",
            description="Non Fresh Test Item",
            stock_code="M",
            unit_price=1,
            quantity=1
        ),

        # Invoice 10002 - Yesterday
        create_dummy_invoice_item(
            item_id=1,
            invoice_number=10002,
            invoice_date=yesterday,
            record_create_time="09:30:00",
            description="Fresh Beef",
            stock_code="BE4",
            unit_price=12.50,
            quantity=6
        ),
        create_dummy_invoice_item(
            item_id=2,
            invoice_number=10002,
            invoice_date=yesterday,
            record_create_time="09:30:00",
            description="Non Fresh Test Item",
            stock_code="M",
            unit_price=1,
            quantity=1
        ),

        # Invoice 10003 - Yesterday
        create_dummy_invoice_item(
            item_id=1,
            invoice_number=10003,
            invoice_date=yesterday,
            record_create_time="14:45:00",
            description="Fresh Beef",
            stock_code="BE4",
            unit_price=12.50,
            quantity=2
        ),
        create_dummy_invoice_item(
            item_id=2,
            invoice_number=10003,
            invoice_date=yesterday,
            record_create_time="14:45:00",
            description="Non Fresh Test Item",
            stock_code="M",
            unit_price=1,
            quantity=1
        ),

        # Invoice 10004 - Today
        create_dummy_invoice_item(
            item_id=1,
            invoice_number=10004,
            invoice_date=today,
            record_create_time="06:45:00",
            description="Fresh Beef",
            stock_code="BE4",
            unit_price=12.50,
            quantity=8
        ),
        create_dummy_invoice_item(
            item_id=2,
            invoice_number=10004,
            invoice_date=today,
            record_create_time="06:45:00",
            description="Non Fresh Test Item",
            stock_code="M",
            unit_price=1,
            quantity=1
        ),

        # Invoice 10005 - Today
        create_dummy_invoice_item(
            item_id=1,
            invoice_number=10005,
            invoice_date=today,
            record_create_time="08:20:00",
            description="Fresh Beef",
            stock_code="BE4",
            unit_price=12.50,
            quantity=5
        ),
        create_dummy_invoice_item(
            item_id=2,
            invoice_number=10005,
            invoice_date=today,
            record_create_time="08:20:00",
            description="Non Fresh Test Item",
            stock_code="M",
            unit_price=1,
            quantity=1
        ),

        # Invoice 10006 - Today
        create_dummy_invoice_item(
            item_id=1,
            invoice_number=10006,
            invoice_date=today,
            record_create_time="11:35:00",
            description="Fresh Beef",
            stock_code="BE4",
            unit_price=12.50,
            quantity=3
        ),
        create_dummy_invoice_item(
            item_id=2,
            invoice_number=10006,
            invoice_date=today,
            record_create_time="11:35:00",
            description="Non Fresh Test Item",
            stock_code="M",
            unit_price=1,
            quantity=1
        ),

        # Invoice 10007 - Today
        create_dummy_invoice_item(
            item_id=1,
            invoice_number=10007,
            invoice_date=today,
            record_create_time="15:10:00",
            description="Fresh Beef",
            stock_code="BE4",
            unit_price=12.50,
            quantity=7
        ),
        create_dummy_invoice_item(
            item_id=2,
            invoice_number=10007,
            invoice_date=today,
            record_create_time="15:10:00",
            description="Non Fresh Test Item",
            stock_code="M",
            unit_price=1,
            quantity=1
        ),

        # Invoice 10008 - Tomorrow
        create_dummy_invoice_item(
            item_id=1,
            invoice_number=10008,
            invoice_date=tomorrow,
            record_create_time="07:05:00",
            description="Fresh Beef",
            stock_code="BE4",
            unit_price=12.50,
            quantity=4
        ),
        create_dummy_invoice_item(
            item_id=2,
            invoice_number=10008,
            invoice_date=tomorrow,
            record_create_time="07:05:00",
            description="Non Fresh Test Item",
            stock_code="M",
            unit_price=1,
            quantity=1
        ),

        # Invoice 10009 - Tomorrow
        create_dummy_invoice_item(
            item_id=1,
            invoice_number=10009,
            invoice_date=tomorrow,
            record_create_time="09:25:00",
            description="Fresh Beef",
            stock_code="BE4",
            unit_price=12.50,
            quantity=9
        ),
        create_dummy_invoice_item(
            item_id=2,
            invoice_number=10009,
            invoice_date=tomorrow,
            record_create_time="09:25:00",
            description="Non Fresh Test Item",
            stock_code="M",
            unit_price=1,
            quantity=1
        ),

        # Invoice 10010 - Tomorrow
        create_dummy_invoice_item(
            item_id=1,
            invoice_number=10010,
            invoice_date=tomorrow,
            record_create_time="12:40:00",
            description="Fresh Beef",
            stock_code="BE4",
            unit_price=12.50,
            quantity=6
        ),
        create_dummy_invoice_item(
            item_id=2,
            invoice_number=10010,
            invoice_date=tomorrow,
            record_create_time="12:40:00",
            description="Non Fresh Test Item",
            stock_code="M",
            unit_price=1,
            quantity=1
        ),

        # Invoice 10011 - Tomorrow
        create_dummy_invoice_item(
            item_id=1,
            invoice_number=10011,
            invoice_date=tomorrow,
            record_create_time="16:15:00",
            description="Fresh Beef",
            stock_code="BE4",
            unit_price=12.50,
            quantity=5
        ),
        create_dummy_invoice_item(
            item_id=2,
            invoice_number=10011,
            invoice_date=tomorrow,
            record_create_time="16:15:00",
            description="Non Fresh Test Item",
            stock_code="M",
            unit_price=1,
            quantity=1
        ),

        # Invoice 10012 - Day after tomorrow
        create_dummy_invoice_item(
            item_id=1,
            invoice_number=10012,
            invoice_date=day_after_tomorrow,
            record_create_time="07:30:00",
            description="Fresh Beef",
            stock_code="BE4",
            unit_price=12.50,
            quantity=3
        ),
        create_dummy_invoice_item(
            item_id=2,
            invoice_number=10012,
            invoice_date=day_after_tomorrow,
            record_create_time="07:30:00",
            description="Non Fresh Test Item",
            stock_code="M",
            unit_price=1,
            quantity=1
        ),

        # Invoice 10013 - Day after tomorrow
        create_dummy_invoice_item(
            item_id=1,
            invoice_number=10013,
            invoice_date=day_after_tomorrow,
            record_create_time="10:50:00",
            description="Fresh Beef",
            stock_code="BE4",
            unit_price=12.50,
            quantity=10
        ),
        create_dummy_invoice_item(
            item_id=2,
            invoice_number=10013,
            invoice_date=day_after_tomorrow,
            record_create_time="10:50:00",
            description="Non Fresh Test Item",
            stock_code="M",
            unit_price=1,
            quantity=1
        ),

        # Invoice 10014 - Day after tomorrow
        create_dummy_invoice_item(
            item_id=1,
            invoice_number=10014,
            invoice_date=day_after_tomorrow,
            record_create_time="14:20:00",
            description="Fresh Beef",
            stock_code="BE4",
            unit_price=12.50,
            quantity=4
        ),
        create_dummy_invoice_item(
            item_id=2,
            invoice_number=10014,
            invoice_date=day_after_tomorrow,
            record_create_time="14:20:00",
            description="Non Fresh Test Item",
            stock_code="M",
            unit_price=1,
            quantity=1
        )
    ],
    "success": True,
    "code": 200,
    "response": None,
    "message": None
}
