import streamlit as st
import requests

def sendTranscript(transcript):
    with st.spinner("Sending transcript to API..."):
            response = requests.post(
                API_URL,
                data={"transcript": transcript}
            )
            if response.status_code == 200:
             result = response.json()
             st.success("Transcript processed successfully!")
             st.write("### Extracted Fields:")
             print(result["value"])
            #  st.json(result)
             output_lines = []
             for i, (field, value, confidence) in enumerate(result["value"], start=1):
                line = f"{i} {field}: {value} (Confidence: {confidence:.2f})"
                output_lines.append(line)
             st.text("\n".join(output_lines))
            else:
             st.error(f"API Error: {response.text}")    

st.set_page_config(page_title="Call Transcript Analyzer", layout="centered")

st.title("📞 Call Transcript Analyzer")

# Upload transcript
transcript_file = st.file_uploader("Upload Call Transcript (TXT)", type=["txt"])

# Or text area input
transcript_text = st.text_area("Or paste transcript here")
  
API_URL = "http://127.0.0.1:8000/extract-fields"  
if st.button("Submit for Processing"):
    if transcript_file:
        transcript = transcript_file.read().decode("utf-8")
        st.success("Transcript uploaded successfully!")
        sendTranscript(transcript)
        # st.write("### Transcript Preview:")
        # st.write(transcript[:500])  # show first 500 chars
    elif transcript_text.strip():
        st.success("Transcript submitted successfully!")
        sendTranscript(transcript_text.strip())
        # st.write("### Transcript Preview:")
        # st.write(transcript_text[:500])
    else:
        st.error("Please upload a transcript file or paste text.")

  
