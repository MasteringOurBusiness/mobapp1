# mob_grant_finder_final.py

import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date

# -------------------------------
# CONFIGURATION
st.set_page_config(page_title="MOB Grant & Funding Finder", layout="wide")

st.markdown("""
    <style>
    .stButton>button {
        color: white;
        background-color: #D4AF37;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# INITIAL DATA (Simulated for demo)
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame([
        {"Name": "Black Founders Fund", "Funding Type": "Grant", "Amount": "$100K", "Business Type": "Tech", "Location": "National", "Deadline": "Sept 15, 2025", "Free Submission": True, "Link": "https://example.com"},
        {"Name": "ATL Micro-Grant", "Funding Type": "Grant", "Amount": "$5K", "Business Type": "Retail", "Location": "Atlanta, GA", "Deadline": "Aug 31, 2025", "Free Submission": True, "Link": "https://example.com"},
        {"Name": "Creative Ventures Loan", "Funding Type": "Loan", "Amount": "$50K", "Business Type": "Art & Media", "Location": "Florida", "Deadline": "Rolling", "Free Submission": False, "Link": "https://example.com"},
        {"Name": "Women of Color Grant", "Funding Type": "Grant", "Amount": "$25K", "Business Type": "Beauty & Wellness", "Location": "National", "Deadline": "Dec 1, 2025", "Free Submission": True, "Link": "https://example.com"},
        {"Name": "Green Startup Accelerator", "Funding Type": "Equity Investment", "Amount": "$75K", "Business Type": "Sustainability", "Location": "California", "Deadline": "Oct 10, 2025", "Free Submission": False, "Link": "https://example.com"},
        {"Name": "Black-Owned Biz Boost", "Funding Type": "Grant", "Amount": "$10K", "Business Type": "Food & Beverage", "Location": "Texas", "Deadline": "Nov 20, 2025", "Free Submission": True, "Link": "https://example.com"},
    ])

df = st.session_state.data

# -------------------------------
# SIDEBAR FILTERS
st.sidebar.header("🔎 Filter Opportunities")
biz_type = st.sidebar.selectbox("Business Type", ["All"] + sorted(df["Business Type"].unique()))
location = st.sidebar.selectbox("Location", ["All"] + sorted(df["Location"].unique()))
funding_type = st.sidebar.selectbox("Funding Type", ["All"] + sorted(df["Funding Type"].unique()))
free_only = st.sidebar.checkbox("✅ Only show free submissions")

# APPLY FILTERS
filtered = df.copy()
if biz_type != "All":
    filtered = filtered[filtered["Business Type"] == biz_type]
if location != "All":
    filtered = filtered[filtered["Location"] == location]
if funding_type != "All":
    filtered = filtered[filtered["Funding Type"] == funding_type]
if free_only:
    filtered = filtered[filtered["Free Submission"] == True]

# -------------------------------
# MAIN UI
st.title("💰 M.O.B. Grant & Funding Finder")
st.write("Discover grants, loans, and funding opportunities for your business.")

st.dataframe(filtered.drop(columns=["Link", "Free Submission"]), use_container_width=True)

# -------------------------------
# EXPORT SECTION
st.markdown("### 📊 Export Grants")
export_format = st.selectbox("Choose format", ["CSV", "Excel"])
if st.button("📁 Export Filtered List"):
    output = BytesIO()
    if export_format == "CSV":
        filtered.to_csv(output, index=False)
        st.download_button("Download CSV", output.getvalue(), file_name="mob_grants.csv", mime="text/csv")
    else:
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            filtered.to_excel(writer, index=False, sheet_name="Grants")
        st.download_button("Download Excel", output.getvalue(), file_name="mob_grants.xlsx", mime="application/vnd.ms-excel")

# -------------------------------
# APPLICATION LINKS
with st.expander("🔗 View Application Links"):
    for _, row in filtered.iterrows():
        st.markdown(f"- [{row['Name']}]({row['Link']}) — **Deadline:** {row['Deadline']}")

# -------------------------------
# ADMIN UPLOAD PANEL
st.markdown("---")
st.header("📝 Admin Grant Submission")

with st.form("admin_form"):
    name = st.text_input("Grant Name")
    amount = st.text_input("Amount (e.g., $10K)")
    biz = st.selectbox("Business Type", sorted(df["Business Type"].unique()) + ["Other"])
    new_biz = st.text_input("If Other, enter new Business Type")
    fund_type = st.selectbox("Funding Type", ["Grant", "Loan", "Equity Investment"])
    location = st.text_input("Location")
    deadline = st.date_input("Deadline", value=date.today())
    free = st.checkbox("Free Submission", value=True)
    link = st.text_input("Application Link")

    submitted = st.form_submit_button("Submit Grant")
    if submitted:
        new_entry = {
            "Name": name,
            "Amount": amount,
            "Business Type": new_biz if biz == "Other" else biz,
            "Funding Type": fund_type,
            "Location": location,
            "Deadline": deadline.strftime("%b %d, %Y"),
            "Free Submission": free,
            "Link": link
        }
        st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_entry])], ignore_index=True)
        st.success("New grant opportunity submitted!")

# -------------------------------
# FAQ SECTION
st.markdown("---")
st.header("🧠 Recently Asked Questions")
faq_data = {
    "How do I apply?": "Click the application link listed for each grant.",
    "What does 'Free Submission' mean?": "It means there's no application fee.",
    "Can I export the list?": "Yes! Use the export section above to download CSV or Excel.",
    "Can I apply for more than one?": "Yes, if you qualify, apply to as many as you want.",
    "Do I need a business license?": "Some grants require it; check each program's rules."
}
for question, answer in faq_data.items():
    with st.expander(f"❓ {question}"):
        st.write(answer)

# -------------------------------
# SIMPLE CHATBOT
st.markdown("---")
st.header("🤖 Ask the MOB Funding Bot")
user_input = st.text_input("Type your question:")
if user_input:
    msg = user_input.lower()
    if "deadline" in msg:
        st.info("Deadlines are shown in the table. Click the link to get full details.")
    elif "free" in msg:
        st.info("Free submission means no cost to apply. You can filter for that in the sidebar.")
    elif "loan" in msg:
        st.info("Loans must be repaid; grants don’t. Filter by 'Funding Type' for your needs.")
    elif "how to apply" in msg or "apply" in msg:
        st.info("Click the grant name to access the official application page.")
    else:
        st.info("Check the FAQs or try rephrasing your question.")
