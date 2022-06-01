import borb.pdf
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
import borb
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from decimal import Decimal



def split_half_half():

  # Read PDF
  with open("output.pdf", "rb") as pdf_file_handle:
    input_pdf = PDF.loads(pdf_file_handle)

  # Create two empty PDFs to hold each half of the split
  output_pdf_001 = borb.pdf.Document()
  output_pdf_002 = borb.pdf.Document()

  # Split
  for i in range(0, 10):
    if i < 5:
      output_pdf_001.append_page(input_pdf.get_page(i))
    else:
      output_pdf_002.append_page(input_pdf.get_page(i))

  # Write PDF
  with open("output_001.pdf", "wb") as pdf_out_handle:
    PDF.dumps(pdf_out_handle, output_pdf_001)

  # Write PDF
  with open("output_002.pdf", "wb") as pdf_out_handle:
    PDF.dumps(pdf_out_handle, output_pdf_002)