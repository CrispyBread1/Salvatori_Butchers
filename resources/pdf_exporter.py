from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QFileDialog, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView


def export_to_pdf(parent, data):
    """Generate the PDF by converting product list to HTML"""

    # Construct HTML content
    html_content = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; font-size: 12px; margin: 20px; }
            h1 { text-align: center; }
            .category { font-weight: bold; font-size: 14px; margin-top: 20px; }
            .product { margin-left: 20px; }
            .empty-box { display: inline-block; width: 50px; height: 20px; border: 1px solid black; margin-left: 10px; }
        </style>
    </head>
    <body>
        <h1>Stock Take Report</h1>
    """

    # Add products dynamically
    for category, products in data.items():
        html_content += f'<div class="category">{category}</div>'
        for product in products:
            html_content += f'<div class="product">{product.name}<div class="empty-box"></div></div>'

    html_content += """
    </body>
    </html>
    """

    # Use QWebEngineView to render the HTML content
    viewer = QWebEngineView()
    viewer.setHtml(html_content)

    # Use QFileDialog to choose the location to save the PDF
    options = QFileDialog.Options()
    file_name, _ = QFileDialog.getSaveFileName(parent, "Save PDF", "", "PDF Files (*.pdf)", options=options)

    if file_name:
        # When the content is loaded, export it to PDF
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(file_name)

        # Define the callback function for when the page finishes loading
        def on_load_finished(success):
            if success:
                # Print the page to the PDF
                viewer.page().print(printer, lambda result: on_print_done(result))
            else:
                print("Failed to load the HTML content.")

        def on_print_done(success):
            """Callback to confirm if the print was successful"""
            if success:
                print("PDF saved successfully!")
            else:
                print("Failed to save the PDF.")

        # Connect the loadFinished signal to our callback
        viewer.loadFinished.connect(on_load_finished)

        # Ensure QApplication exec() is running if it's not already
        if not QApplication.instance():
            app = QApplication([])  # Start Qt application if not already running
            app.exec_()

