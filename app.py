# app.py (Interactive Plotly Chart + Search Filter)
import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
import matplotlib.pyplot as plt
import plotly.express as px
st.set_page_config(layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("structured_linkedin_data_with_durations.csv")
    df.fillna("", inplace=True)
    return df

data = load_data()
os.makedirs("resumes", exist_ok=True)

# Helper for PDF
def generate_pdf(profile):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, profile['Name'], ln=True)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Location: {profile['Location']}", ln=True)
    pdf.multi_cell(0, 10, f"Headline: {profile['Headline']}" + "\n")

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Experience", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"{profile['Job Title']} at {profile['Company']}\nDuration: {profile['Experience Duration']}\n{profile['Experience (Single)']}")

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Education", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"{profile['Degree']} at {profile['Institution']}\nDuration: {profile['Education Duration']}\n{profile['Education (Single)']}")

    filename = f"resumes/{profile['Name'].replace(' ', '_')}.pdf"
    pdf.output(filename)
    return filename

# Sidebar Navigation
st.set_page_config(layout="wide")
st.sidebar.title("🔎 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📄 Resumes"])

if page == "🏠 Home":
    st.title("📊 Dashboard Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("👥 Total Profiles", len(data))
        top_locations = data['Location'].value_counts()
        st.bar_chart(top_locations)

    with col2:
        all_titles = data['Job Title'].value_counts()
        st.bar_chart(all_titles)

    st.markdown("---")
    st.subheader("🥧 Role Breakdown (Exact Titles)")

    # Pie Chart - Matplotlib
    role_counts = data['Job Title'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(role_counts, labels=role_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    # Pie Chart - Plotly
    st.subheader("📈 Interactive Role Breakdown")
    plotly_fig = px.pie(values=role_counts.values, names=role_counts.index, title='Interactive Job Title Distribution')
    st.plotly_chart(plotly_fig, use_container_width=True)

elif page == "📄 Resumes":
    st.title("📄 Resume Viewer")

    # Filters
    st.sidebar.subheader("📍 Filter Candidates")
    locations = st.sidebar.multiselect("Location", sorted(data["Location"].unique()))
    companies = st.sidebar.multiselect("Company", sorted(data["Company"].unique()))

    job_search = st.sidebar.text_input("🔍 Search Job Title (optional)")
    if job_search:
        position_matches = data[data['Job Title'].str.contains(job_search, case=False, na=False)]['Job Title'].unique()
        positions = st.sidebar.multiselect("Matched Job Titles", sorted(position_matches))
    else:
        positions = st.sidebar.multiselect("Job Title", sorted(data["Job Title"].unique()))

    filtered = data
    if locations:
        filtered = filtered[filtered["Location"].isin(locations)]
    if companies:
        filtered = filtered[filtered["Company"].isin(companies)]
    if positions:
        filtered = filtered[filtered["Job Title"].isin(positions)]

    selected_name = st.selectbox("Select a Candidate", filtered["Name"].unique() if not filtered.empty else ["No match"])

    if selected_name != "No match":
        profile = filtered[filtered["Name"] == selected_name].iloc[0]

        st.header(f"Resume for {profile['Name']}")
        st.subheader(profile['Headline'])
        st.text(f"📍 {profile['Location']}")

        st.markdown("---")
        st.markdown("### 💼 Experience")
        st.markdown(f"**{profile['Job Title']}** at *{profile['Company']}*")
        st.markdown(f"🗓️ {profile['Experience Duration']}")
        st.write(profile['Experience (Single)'])

        st.markdown("---")
        st.markdown("### 🎓 Education")
        st.markdown(f"**{profile['Degree']}** at *{profile['Institution']}*")
        st.markdown(f"🗓️ {profile['Education Duration']}")
        st.write(profile['Education (Single)'])

        pdf_file = generate_pdf(profile)
        with open(pdf_file, "rb") as f:
            st.download_button(label="📥 Download Resume as PDF", data=f, file_name=os.path.basename(pdf_file), mime="application/pdf")
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
