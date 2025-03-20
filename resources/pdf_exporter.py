from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QFileDialog, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from datetime import datetime

def export_to_pdf(parent, data):
    """Generate a PDF by converting product list to HTML with larger columns"""

    # Set the number of rows per page
    rows_per_page = 20
    products = []

    # Flatten the data into a list of products
    for category, product_list in data.items():
        for product in product_list:
            products.append(product)

    # Number of rows is fixed at 20
    total_rows = rows_per_page
    rows = []
    # Split products into 20 rows
    for i in range(0, len(products), total_rows):
        rows.append(products[i:i + total_rows])

    # Construct HTML content with page scaling to ensure it fits
    html_content = """
    <html>
    <head>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                font-size: 12px; 
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                page-break-before: always;
            }
            h1 { 
                text-align: center; 
                margin-bottom: 30px; 
            }
            .category { 
                font-weight: bold; 
                font-size: 14px; 
                margin-top: 20px; 
            }
            .product-grid {
                display: grid;
                grid-template-columns: repeat(4, 2fr); /* Adjust this for more or less columns */
                grid-gap: 20px;
                margin-top: 10px;
            }
            .product { 
                text-align: center; 
                padding: 4px;  /* Increase padding for larger boxes */
                width: 100%;
                border: 1px solid #ddd;
                font-size: 8px; /* Increase font size */
    
                word-wrap: break-word;
                word-break: break-word;
                white-space: normal;
                text-overflow: ellipsis;
            }
            .empty-box { 
                display: inline-block; 
                width: 50px; 
                height: 20px; 
                border: 1px solid black; 
                margin-left: 10px; 
            }
            /* Page styling for print */
            @page { 
                size: A4;
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
            }
            /* Force everything to scale to fit one page */
            body {
                transform: scale(0.9); /* Adjust this scale to fit content on a single page */
                transform-origin: 0 0; /* Ensures scaling starts from top-left */
            }
        </style>
    </head>
    <body>
        <h1>Stock Take</h1>
    """

    # Add products dynamically with grid layout
    for i, row in enumerate(rows):
        html_content += f'<div class="product-grid">'
        
        # Each row can have dynamic columns
        for product in row:
            html_content += f'<div class="product">{product.name}<div class="empty-box"></div></div>'
        
        html_content += '</div>'  # End of product grid
    date = datetime.now().strftime('%d-%m-%y, %A')
    html_content += f'<div class="date"><h2>{date}</h2</div>'
    html_content += "</body></html>"

    # Use QFileDialog to select the save location
    file_name, _ = QFileDialog.getSaveFileName(parent, "Save PDF", "", "PDF Files (*.pdf)")
    if not file_name:
        return  # User canceled the save dialog

    # Create QWebEngineView to render HTML
    viewer = QWebEngineView()
    
    # Setup the PDF printer
    printer = QPrinter(QPrinter.HighResolution)
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName(file_name)

    # Ensure content fits on one page (by setting page size and margins)
    printer.setPageSize(QPrinter.A4)
    printer.setPageMargins(0, 0, 0, 0, QPrinter.Millimeter)
    printer.setFullPage(True)

    def on_load_finished(success):
        """Triggered when the page is fully loaded in QWebEngineView"""
        if not success:
            print("Failed to load HTML content.")
            return

        # Initiate the print process
        viewer.page().print(printer, on_print_done)

    def on_print_done(result):
        """Callback when printing to PDF is complete"""
        if result:
            print(f"✅ PDF saved successfully: {file_name}")
        else:
            print("❌ Failed to save PDF.")

        # Clean up after printing
        viewer.deleteLater()

    # Load the HTML content into the viewer
    viewer.setHtml(html_content)

    # Connect the signal that is emitted when the HTML content is loaded
    viewer.loadFinished.connect(on_load_finished)

    # Ensure QApplication exec() is not called here, since the main loop is already running
    if QApplication.instance() is None:
        app = QApplication([])  # Create an app instance only if none exists
        app.exec_()
