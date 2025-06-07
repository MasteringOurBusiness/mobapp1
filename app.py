import streamlit as st
import pandas as pd
import openai
import csv
import io
from datetime import datetime

# Optional: for Google Sheet sync
import gspread
from google.oauth2.service_account import Credentials

# Optional: for PDF export
import pdfkit

# ----------------------------
# CONFIG
st.set_page_config(page_title="MOB Grant & Funding Finder", layout="wide")
st.markdown("<style>.stButton>button{background-color:#D4AF37;color:white;border-radius:8px}</style>", unsafe_allow_html=True)

# ----------------------------
# Google Sheets Setup (replace with your actual credentials or use st.secrets)
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/your_sheet_id_here"
GSHEET_SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDENTIALS = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=GSHEET_SCOPE)
gc = gspread.authorize(CREDENTIALS)
sh = gc.open_by_url(GOOGLE_SHEET_URL)
worksheet = sh.sheet1

# Load data
@st.cache_data(ttl=60)
def load_data():
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

# ----------------------------
# ChatGPT Config
openai.api_key = st.secrets["OPENAI_API_KEY"]

def ask_gpt(question):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You're a helpful funding assistant for entrepreneurs."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message['content']

# ----------------------------
# Upload Panel (Admin Only)
with st.expander("📝 Submit a New Grant Opportunity (Admins Only)"):
    with st.form("add_form"):
        name = st.text_input("Grant Name")
        amount = st.text_input("Amount")
        btype = st.selectbox("Business Type", ["Tech", "Retail", "Food & Beverage", "Beauty & Wellness", "Sustainability", "Art & Media"])
        location = st.text_input("Location")
        ftype = st.selectbox("Funding Type", ["Grant", "Loan", "Equity Investment"])
        deadline = st.date_input("Deadline")
        free = st.checkbox("Free Submission?")
        link = st.text_input("Application Link")
        submit_btn = st.form_submit_button("➕ Submit")

        if submit_btn:
            worksheet.append_row([name, ftype, amount, btype, location, deadline.strftime("%b %d, %Y"), str(free), link])
            st.success("Grant successfully added!")

# ----------------------------
# Load & Filter Data
df = load_data()

st.sidebar.header("🔍 Filter")
biz_type = st.sidebar.selectbox("Business Type", ["All"] + sorted(df["Business Type"].unique()))
location = st.sidebar.selectbox("Location", ["All"] + sorted(df["Location"].unique()))
funding_type = st.sidebar.selectbox("Funding Type", ["All"] + sorted(df["Funding Type"].unique()))
free_only = st.sidebar.checkbox("✅ Free Submissions Only")

filtered = df.copy()
if biz_type != "All":
    filtered = filtered[filtered["Business Type"] == biz_type]
if location != "All":
    filtered = filtered[filtered["Location"] == location]
if funding_type != "All":
    filtered = filtered[filtered["Funding Type"] == funding_type]
if free_only:
    filtered = filtered[filtered["Free Submission"].astype(str) == "True"]

# ----------------------------
# Display Data
st.title("💰 MOB Grant & Funding Finder")
st.write("Explore grants, loans, and investments for entrepreneurs across the nation.")

st.dataframe(filtered.drop(columns=["Link", "Free Submission"]), use_container_width=True)

with st.expander("🔗 Grant Links"):
    for _, row in filtered.iterrows():
        st.markdown(f"- [{row['Name']}]({row['Link']}) — **Deadline:** {row['Deadline']}")

# ----------------------------
# Export Section
st.markdown("### 📤 Export Results")
col1, col2 = st.columns(2)

with col1:
    csv_data = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("📁 Download CSV", csv_data, file_name="grants_filtered.csv", mime="text/csv")

with col2:
    try:
        html = filtered.to_html(index=False)
        pdf = pdfkit.from_string(html, False)
        st.download_button("📄 Download PDF", pdf, file_name="grants_filtered.pdf", mime="application/pdf")
    except:
        st.error("PDF export requires wkhtmltopdf installed.")

# ----------------------------
# FAQs
st.markdown("---")
st.subheader("🧠 Recently Asked Questions")
faqs = {
    "How do I apply for a grant?": "Click the 'Grant Links' section to go directly to the application page.",
    "What does 'Free Submission' mean?": "There’s no application fee required to apply for that opportunity.",
    "Can I apply for multiple grants?": "Yes, as long as you qualify based on the criteria listed.",
}
for q, a in faqs.items():
    with st.expander(f"❓ {q}"):
        st.write(a)

# ----------------------------
# Chatbot
st.markdown("---")
st.subheader("🤖 Ask the MOB Funding Bot")
user_input = st.text_input("Type your funding question here...")
if user_input:
    response = ask_gpt(user_input)
    st.success(response)
