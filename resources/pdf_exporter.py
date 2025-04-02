from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QFileDialog, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from datetime import datetime, timedelta

def get_week_dates():
    """Returns the Monday to Friday dates for the current week."""
    today = datetime.today()
    monday = today - timedelta(days=today.weekday())  # Get Monday of the current week
    return [(monday + timedelta(days=i)).strftime('%d-%m-%Y') for i in range(5)]

def export_to_pdf(parent, data):
    """Generate a PDF with one large table split into two parts (left & right columns)."""
    
    # Get Monday–Friday dates dynamically
    week_dates = get_week_dates()
    
    # Group products by category
    categories = {}
    for category, product_list in data.items():
        for product in product_list:
            if product.product_category not in categories:
                categories[product.product_category] = []
            categories[product.product_category].append(product)

    # ✅ **Ensure HTML content is properly formatted**
    html_content = f"""
    <html>
    <head>
        <style>
            @page {{
                size: A4 landscape;
                margin: 5mm; /* Minimize margins to maximize space */
            }}
            body {{
                font-family: Arial, sans-serif;
                font-size: 8px; /* Reduce font size slightly */
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
            }}
            h1 {{
                text-align: center;
                font-size: 14px;
                margin-bottom: 5px;
            }}
            .table-container {{
                width: 100%;
                height: 100%;
                display: flex;
                justify-content: center;
            }}
            table {{
                width: 100%;
                height: 100%;
                border-collapse: collapse;
                margin-bottom: 5px;
                table-layout: fixed; /* Ensure even column widths */
                page-break-inside: avoid;
            }}
            th, td {{
                border: 1px solid #000;
                padding: 3px;
                text-align: center;
                word-wrap: break-word;
                overflow: hidden;
                height: auto; /* Allow dynamic height expansion */
                min-height: 15px;
            }}
            th {{
                background-color: #ddd;
                font-size: 10px;
            }}
            td {{
                font-size: 8px;
                height: auto; /* Allow dynamic height expansion */
                min-height: 15px;
            }}
            tr {{
                height: auto; /* Allow rows to stretch */
            }}
            .category-header {{
                background-color: #bbb;
                font-weight: bold;
                text-align: left;
                padding-left: 5px;
            }}
        </style>
    </head>
    <body>
        <h1>Stock Take - Week of {week_dates[0]}</h1>
        <div class="table-container">
            <table>
                <colgroup>
                    <col style="width: 30%;">  <!-- Product column is larger -->
                    <col style="width: 14%;">
                    <col style="width: 14%;">
                    <col style="width: 14%;">
                    <col style="width: 14%;">
                    <col style="width: 14%;">
                    <col style="width: 30%;">  <!-- Product column is larger -->
                    <col style="width: 14%;">
                    <col style="width: 14%;">
                    <col style="width: 14%;">
                    <col style="width: 14%;">
                    <col style="width: 14%;">
                </colgroup>
            
                <tr>
                    <th>Product</th> {"".join(f"<th>{date}</th>" for date in week_dates[:5])}  
                    <th>Product</th> {"".join(f"<th>{date}</th>" for date in week_dates[:5])}
                </tr>
    """

    # Convert categories into a flat product list and split into two parts
    all_products = []
    for category, products in categories.items():
        all_products.append({"category": category, "is_category": True})  # Category header row
        all_products.extend(products)

    mid_index = len(all_products) // 2
    left_products = all_products[:mid_index]
    right_products = all_products[mid_index:]

    # **Ensure both sides have the same row count by padding**
    max_rows = max(len(left_products), len(right_products))
    left_products.extend([""] * (max_rows - len(left_products)))
    right_products.extend([""] * (max_rows - len(right_products)))

    # ✅ **Generate table rows**
    for left, right in zip(left_products, right_products):
        html_content += "<tr>"

        # Left Column
        if isinstance(left, dict) and left.get("is_category"):
            html_content += f"<td class='category-header' colspan='6'>{left['category']}</td>"
        elif left:
            html_content += f"<td>{left.name}</td>" + "".join("<td></td>" for _ in range(5))
        else:
            html_content += "<td colspan='6'></td>"

        # Right Column
        if isinstance(right, dict) and right.get("is_category"):
            html_content += f"<td class='category-header' colspan='6'>{right['category']}</td>"
        elif right:
            html_content += f"<td>{right.name}</td>" + "".join("<td></td>" for _ in range(5))
        else:
            html_content += "<td colspan='6'></td>"

        html_content += "</tr>"

    html_content += """
            </table>
        </div>
    </body>
    </html>
    """

    # ✅ **Check if the user selected a file name**
    file_name, _ = QFileDialog.getSaveFileName(parent, "Save PDF", "", "PDF Files (*.pdf)")
    if not file_name:
        return

    viewer = QWebEngineView()
    printer = QPrinter(QPrinter.HighResolution)
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOrientation(QPrinter.Landscape)  # Ensure landscape mode
    printer.setOutputFileName(file_name)
    printer.setPageSize(QPrinter.A4)
    printer.setPageMargins(2, 2, 2, 2, QPrinter.Millimeter)  # Tighten margins to prevent spillover

    def on_load_finished(success):
        if not success:
            print("Failed to load HTML content.")
            return
        viewer.page().print(printer, on_print_done)

    def on_print_done(result):
        if result:
            print(f"✅ PDF saved successfully: {file_name}")
        else:
            print("❌ Failed to save PDF.")
        viewer.deleteLater()

    viewer.setHtml(html_content)
    viewer.loadFinished.connect(on_load_finished)

    if QApplication.instance() is None:
        app = QApplication([])
        app.exec_()


