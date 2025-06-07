# grant_funding_finder.py

import streamlit as st
import pandas as pd

# ------------------------------
# App Settings
st.set_page_config(page_title="MOB Grant & Funding Finder", layout="wide")

# ------------------------------
# Custom Styling
st.markdown("""
    <style>
    body {
        background-color: #ffffff;
        color: #000000;
    }
    .main {
        background-color: #ffffff;
    }
    .stButton>button {
        color: white;
        background-color: #D4AF37;
        border-radius: 10px;
    }
    .css-18e3th9 {
        background-color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# Dummy Data
data = [
    {
        "Name": "Black Founders Fund by Google",
        "Funding Type": "Grant",
        "Amount": "$100K",
        "Business Type": "Tech",
        "Location": "National",
        "Deadline": "Sept 15, 2025",
        "Link": "https://example.com"
    },
    {
        "Name": "Local Biz Micro-Grant ATL",
        "Funding Type": "Grant",
        "Amount": "$5K",
        "Business Type": "Retail",
        "Location": "Atlanta, GA",
        "Deadline": "Aug 31, 2025",
        "Link": "https://example.com"
    },
    {
        "Name": "Women of Color Startup Grant",
        "Funding Type": "Grant",
        "Amount": "$25K",
        "Business Type": "Any",
        "Location": "National",
        "Deadline": "Dec 1, 2025",
        "Link": "https://example.com"
    },
    {
        "Name": "Creative Ventures Fund",
        "Funding Type": "Loan",
        "Amount": "$50K",
        "Business Type": "Art & Media",
        "Location": "Florida",
        "Deadline": "Rolling",
        "Link": "https://example.com"
    },
]

df = pd.DataFrame(data)

# ------------------------------
# Sidebar Filters
st.sidebar.title("🔍 Filter Opportunities")
biz_type = st.sidebar.selectbox("Select Business Type", ["All"] + sorted(df["Business Type"].unique()))
location = st.sidebar.selectbox("Select Location", ["All"] + sorted(df["Location"].unique()))
funding_type = st.sidebar.selectbox("Funding Type", ["All"] + sorted(df["Funding Type"].unique()))

# ------------------------------
# Apply Filters
filtered_df = df.copy()
if biz_type != "All":
    filtered_df = filtered_df[filtered_df["Business Type"] == biz_type]
if location != "All":
    filtered_df = filtered_df[filtered_df["Location"] == location]
if funding_type != "All":
    filtered_df = filtered_df[filtered_df["Funding Type"] == funding_type]

# ------------------------------
# Main UI
st.title("💰 MOB Grant & Funding Finder")
st.write("Find the best opportunities for your business! Filter by business type, location, or grant type.")

# Display table
st.dataframe(filtered_df.drop(columns=["Link"]), use_container_width=True)

# Expandable section for links
with st.expander("🔗 View Grant Application Links"):
    for _, row in filtered_df.iterrows():
        st.markdown(f"[{row['Name']}]({row['Link']}) - Apply by **{row['Deadline']}**")

# ------------------------------
# Optional Additions:
# - Integrate with Google Sheets for live updates
# - Add upload form for users to suggest grants
