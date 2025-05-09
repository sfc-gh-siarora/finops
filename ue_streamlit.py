import os
from concurrent.futures import ThreadPoolExecutor

import streamlit as st
from ue_summarized import call_unit_economics



# Your Python function
def process_company(info):
    input_list = [item.strip() for item in info.split(",")]
    return call_unit_economics(input_list)

# Streamlit UI
st.title("Unit economics Calculator")

user_input = st.text_area(  """**Enter Company Information here in format:**
\n**Value Engineer, Salesforce Name, Salesforce Id**""", height=100)

if st.button("Submit"):
    if user_input.strip():
        with st.spinner("Processing... please wait (this may take a while)"):
            lines = [line for line in user_input.splitlines() if line.strip()]
            if lines:
                with ThreadPoolExecutor() as executor:
                    results = list(executor.map(process_company, lines))
                st.session_state["ppt_files"] = results
        st.success("Running Unit Economics Calculator Success")
    else:
        st.warning("Please enter some text before submitting.")

if "ppt_files" in st.session_state:
    st.write("### Processed Results:")
    for ppt_file in st.session_state["ppt_files"]:
        filename = os.path.basename(ppt_file)
        st.download_button(
            label=f"Download {filename}",
            data=open(ppt_file, "rb"),
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
