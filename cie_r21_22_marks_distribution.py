import streamlit as st
import pandas as pd
import random
import io

# Function to generate random distribution of marks
def generate_marks_distribution():
    # Part A: 12 questions with marks 0 or 1, total 12 marks
    part_a = [random.choice([0, 1]) for _ in range(12)]
    while sum(part_a) != 12:
        part_a = [random.choice([0, 1]) for _ in range(12)]

    # Part B: 3 questions randomly selected out of 5 (or more), total 18 marks
    part_b = [random.randint(0, 6) for _ in range(3)]
    while sum(part_b) != 18:
        part_b = [random.randint(0, 6) for _ in range(3)]

    return part_a, part_b

# Streamlit app
st.set_page_config(page_title="CIE R21-22 Marks Distribution", layout="centered")
st.title("CIE R21-22 Marks Distribution Generator")

st.markdown("""
Upload an Excel file containing at least 12 questions.  
The app will randomly distribute 12 marks across **Part A** (12 questions, 1 mark each),  
and 18 marks across **Part B** (3 questions randomly selected out of remaining questions).
""")

uploaded_file = st.file_uploader("📤 Upload Excel file (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        if len(df) < 12:
            st.error("❌ The file must have at least 12 questions.")
        else:
            part_a, part_b = generate_marks_distribution()

            # Assign Part A marks
            df['Part A Marks'] = [*part_a, *[None] * (len(df) - 12)]

            # Select 3 random questions for Part B from remaining
            remaining_idx = list(range(12, len(df)))
            if len(remaining_idx) < 3:
                st.warning("⚠️ Less than 3 questions available for Part B. Part B will be skipped.")
            else:
                selected_indices = random.sample(remaining_idx, 3)
                part_b_marks = [None] * len(df)
                for i, idx in enumerate(selected_indices):
                    part_b_marks[idx] = part_b[i]
                df['Part B Marks'] = part_b_marks

            # Save to output Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Marks Distribution')
            output.seek(0)

            st.success("✅ Marks distribution completed!")
            st.download_button(
                label="📥 Download Updated Excel",
                data=output,
                file_name="CIE-R21-22-marks-distribution.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            st.dataframe(df)

    except Exception as e:
        st.error(f"Error reading file: {e}")
