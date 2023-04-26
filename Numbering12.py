import os
from PyPDF4 import PdfFileReader, PdfFileWriter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red


def create_page_pdf(num, tmp, count):
    c = canvas.Canvas(tmp)
    for i in range(count, num + count):
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(red)
        c.drawString((212) * mm, (270) * mm, str(i))
        c.showPage()
    c.save()


def add_page_numbers(pdf_path, start, end):
    """
    Add page numbers to a pdf, save the result as a new pdf
    @param pdf_path: path to pdf
    @param start: starting page number
    @param end: ending page number
    """
    tmp = "__tmp.pdf"

    writer = PdfFileWriter()
    with open(pdf_path, "rb") as f:
        reader = PdfFileReader(f, strict=False)
        n = reader.getNumPages()

        # create new PDF with page numbers
        create_page_pdf(n, tmp, start)

        with open(tmp, "rb") as ftmp:
            number_pdf = PdfFileReader(ftmp)

            # iterate pages
            for p in range(n):
                page = reader.getPage(p)
                numberLayer = number_pdf.getPage(p)
                # merge number page with actual page
                page.mergePage(numberLayer)
                writer.addPage(page)

            # write result
            if writer.getNumPages():
                newpath = os.path.join("numbered_pdfs",
                                       f"{os.path.splitext(os.path.basename(pdf_path))[0]}_numbered.pdf")

                if not os.path.exists("numbered_pdfs"):
                    os.makedirs("numbered_pdfs")
                with open(newpath, "wb") as f:
                    writer.write(f)
        os.remove(tmp)
        return writer.getNumPages()


# set directory where PDF files are located
pdf_dir = "C:\\Users\\chunduri.t\\Downloads\\Study"

# set starting page number
count = 1

# list to hold information about numbered files
numbered_files = []

for file in os.listdir(pdf_dir):
    if file.endswith(".pdf"):
        # set start and end page numbers
        start = count
        end = count + add_page_numbers(os.path.join(pdf_dir, file), start, start) - 1

        # add file information to list
        numbered_files.append((file, start, end))

        # increment count
        count = end + 1

# write list of numbered files to file
with open("numbered_files.csv", "w") as f:
    for file_info in numbered_files:
        f.write(f"{file_info[0].split('.pdf')[0]},{file_info[1]}\n")
