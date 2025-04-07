import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

# Load cleaned dataset from local CSV
data = pd.read_csv("structured_linkedin_data_with_durations.csv")

# Set up resumes folder
os.makedirs("resumes", exist_ok=True)

# Function to generate PDF resume
def generate_pdf(profile):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, profile['Name'], ln=True)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Location: {profile['Location']}", ln=True)
    pdf.multi_cell(0, 10, f"Headline: {profile['Headline']}")

    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Experience", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"{profile['Job Title']} at {profile['Company']}\nDuration: {profile['Experience Duration']}\nDetails: {profile['Experience (Single)']}")

    pdf.ln(2)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Education", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"{profile['Degree']} at {profile['Institution']}\nDuration: {profile['Education Duration']}\nDetails: {profile['Education (Single)']}")

    filename = f"resumes/{profile['Name'].replace(' ', '_')}.pdf"
    pdf.output(filename)
    return filename

# Streamlit UI
st.set_page_config(layout="wide")
st.title("📄 LinkedIn Profile Dashboard")

# Sidebar to choose a person
st.sidebar.header("🔍 Select a Person")
selected_name = st.sidebar.selectbox("Name", sorted(data["Name"].unique()))

# Get selected profile
df_selected = data[data["Name"] == selected_name].iloc[0]

# Main area - Resume preview
st.header(f"Resume for {df_selected['Name']}")
st.subheader(df_selected['Headline'])
st.text(f"📍 {df_selected['Location']}")

st.markdown("---")
st.markdown("### 💼 Experience")
st.markdown(f"**{df_selected['Job Title']}** at *{df_selected['Company']}*  ")
st.markdown(f"🗓️ {df_selected['Experience Duration']}")
st.write(df_selected['Experience (Single)'])

st.markdown("---")
st.markdown("### 🎓 Education")
st.markdown(f"**{df_selected['Degree']}** at *{df_selected['Institution']}*  ")
st.markdown(f"🗓️ {df_selected['Education Duration']}")
st.write(df_selected['Education (Single)'])

# Generate PDF
pdf_file = generate_pdf(df_selected)

with open(pdf_file, "rb") as f:
    st.download_button(label="📥 Download Resume as PDF", data=f, file_name=os.path.basename(pdf_file), mime="application/pdf")
