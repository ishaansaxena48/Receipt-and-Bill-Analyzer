import streamlit as st
import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend import parser, db

from pydantic import BaseModel, validator
from datetime import datetime

class Receipt(BaseModel):
    vendor: str
    date: str
    amount: float
    currency: str = "INR"

    @validator("date")
    def validate_date(cls, value):
        try:
            datetime.strptime(value, "%d/%m/%Y")
            return value
        except:
            raise ValueError("Date should be in DD/MM/YYYY format")

    @validator("amount")
    def validate_amount(cls, value):
        if value < 0:
            raise ValueError("Amount must be positive")
        return value

def main():
    st.title("📄 Receipt Tracker")

    uploaded = st.file_uploader("Upload a receipt (.jpg/.png/.pdf/.txt)", type=["jpg", "png", "pdf", "txt"])
    
    if uploaded:
        os.makedirs("data", exist_ok=True)
        path = os.path.join("data", uploaded.name)
        with open(path, "wb") as f:
            f.write(uploaded.read())
        st.success("File uploaded!")

        try:
            text = parser.extract_text(path)
            result = parser.parse_receipt(text)

            st.subheader("Parsed Fields (Edit if needed)")
            vendor = st.text_input("Vendor", result.get("vendor", ""))
            date = st.text_input("Date", result.get("date", ""))
            amount = st.number_input("Amount", value=result.get("amount", 0.0), min_value=0.0)
            currency = st.text_input("Currency", result.get("currency", "INR"))

            if st.button("Save to Database"):
                try:
                    receipt = Receipt(vendor=vendor, date=date, amount=amount, currency=currency)
                    db.insert_receipt(receipt.dict())
                    st.success("Saved successfully!")
                except Exception as e:
                    st.error(f"Validation error: {e}")

            st.subheader("Extracted Raw Text")
            st.text_area("Text from receipt", text, height=150)

        except Exception as e:
            st.error(f"Failed to process file: {e}")

    st.header("Saved Receipts")
    data = db.fetch_all()

    if data:
        if len(data[0]) == 4:
            data = [row + ("INR",) for row in data]

        df = pd.DataFrame(data, columns=["ID", "Vendor", "Date", "Amount", "Currency"])
        st.dataframe(df)

        st.subheader("Filter & Sort")
        search = st.text_input("Search by Vendor")
        min_amt = st.number_input("Minimum Amount", 0.0)
        sort = st.selectbox("Sort by Amount", ["None", "Low to High", "High to Low"])

        filtered = df[df["Amount"] >= min_amt]
        if search:
            filtered = filtered[filtered["Vendor"].str.contains(search, case=False)]
        if sort == "Low to High":
            filtered = filtered.sort_values("Amount")
        elif sort == "High to Low":
            filtered = filtered.sort_values("Amount", ascending=False)

        st.dataframe(filtered)

        st.subheader("Summary")
        currency = filtered["Currency"].iloc[0] if not filtered.empty else "INR"
        st.write(f"**Total:** {currency} {filtered['Amount'].sum():.2f}")
        st.write(f"**Average:** {currency} {filtered['Amount'].mean():.2f}")
        st.write(f"**Median:** {currency} {filtered['Amount'].median():.2f}")

        st.subheader("Export") 
        st.download_button("Download as CSV", filtered.to_csv(index=False), "receipts.csv", "text/csv")
        st.download_button("Download as JSON", filtered.to_json(orient="records", indent=2), "receipts.json", "application/json")

        st.header("Insights")

        st.subheader("Top Vendors")
        top_vendors = filtered.groupby("Vendor")["Amount"].sum().sort_values(ascending=False).head(5)
        st.bar_chart(top_vendors)

        st.subheader("Monthly Spending")
        filtered["Date"] = pd.to_datetime(filtered["Date"], errors="coerce")
        filtered["Month"] = filtered["Date"].dt.to_period("M").astype(str)
        monthly = filtered.groupby("Month")["Amount"].sum().sort_index()
        st.line_chart(monthly)

    else:
        st.info("No receipts saved yet. Upload one above.")

if __name__ == "__main__":
    main()
