#  Receipt & Bill Analyzer – Full Stack Python Application

A complete full-stack mini-application that allows users to upload receipts and bills in various formats (PDF, JPG, PNG, TXT), extract structured data using OCR, and display insights such as total spending, top vendors, and monthly billing trends.
---
Video Demonstration (Link) - https://youtu.be/CSHEDJ-ekBA
---

##  Features

-  Upload `.jpg`, `.png`, `.pdf`, `.txt` receipt files
-  Extract structured data using OCR (`pytesseract`)
-  Review and manually edit extracted data before saving
-  Store records in a lightweight relational DB (`SQLite`)
-  Search by vendor, filter by amount
-  Visual analytics: top vendors, summary stats, monthly trends
-  Export data to `.csv` and `.json`

---

##  Design Choices & Architecture

###  Tech Stack
| Layer       | Technology              |
|-------------|--------------------------|
| UI          | Streamlit (Python-based) |
| OCR Engine  | pytesseract              |
| File Parser | pdf2image + PIL          |
| Database    | SQLite                   |
| Language    | Python                   |

###  Folder Structure
```
receipt_app/
│
├── backend/
│   ├── parser.py       # OCR + parsing logic
│   ├── db.py           # SQLite database functions
│   └── __init__.py
│
├── ui/
│   └── app.py          # Streamlit dashboard
│
├── requirements.txt
└── README.md
```

###  User Flow

1. User uploads a receipt (`.jpg`, `.pdf`, `.txt`)
2. App extracts text using OCR
3. Data (vendor, date, amount) is parsed and shown in editable form
4. User confirms and saves to SQLite
5. Dashboard displays:
   - Record table with search/sort
   - Bar chart of vendors
   - Line chart of monthly spending
   - Export buttons (CSV, JSON)

---

## ⚙️ Setup Instructions

###  Prerequisites
- Python 3.8+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Poppler](https://github.com/oschwartz10612/poppler-windows) (for PDF support)

###  Install Dependencies

```bash
# Create virtual environment (Very Much recommended)
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Install required packages
pip install -r requirements.txt
```

###  Run the App

```bash
streamlit run ui/app.py
```

---

##  Limitations

- OCR accuracy depends on image quality and clarity
- Only English-language receipts are supported
- Date parsing assumes common formats (DD/MM/YYYY)

---

##  Assumptions

- Receipts follow a semi-standard format (have Vendor, Date, Amount)
- Amount lines contain clear numerical values (e.g., "Total: Rs. 1450.00")
- Dates are formatted using slashes (e.g., "12/03/2024")

---

##  Example Supported Formats

- ✅ `.pdf`, `.png`, `.jpg`, `.txt`
- ✅ Automatically extracts vendor, date, amount
- ✅ Manually correct fields before saving
- ✅ Export data for reporting

---

##  Exported Outputs

- `receipts.csv`: structured table of all receipts
- `receipts.json`: JSON list of all receipt records

---

##  Built With

- [Streamlit](https://streamlit.io/)
- [Pytesseract](https://pypi.org/project/pytesseract/)
- [pdf2image](https://pypi.org/project/pdf2image/)
- [SQLite (built-in)]

---

##  Author

Developed by: **Ishaan Saxena :)** 
