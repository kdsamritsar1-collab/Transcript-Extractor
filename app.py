import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import io

# पेज सेटअप
st.set_page_config(page_title="YT Transcript Downloader", page_icon="📜")

st.markdown("<h1 style='text-align: center; color: #FF0000;'>🎥 YouTube Transcript Extractor</h1>", unsafe_allow_html=True)
st.write("---")

# इनपुट फील्ड
video_url = st.text_input("YouTube वीडियो का लिंक यहाँ पेस्ट करें:", placeholder="https://www.youtube.com/watch?v=...")

if video_url:
    if "v=" in video_url:
        video_id = video_url.split("v=")[1].split("&")[0]
        
        st.info(f"वीडियो ID: {video_id} के लिए ट्रांसक्रिप्ट खोजी जा रही है...")

        try:
            # ट्रांसक्रिप्ट प्राप्त करना (पंजाबी, हिंदी और अंग्रेजी को प्राथमिकता)
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['pa', 'hi', 'en'])
            
            # पूरे टेक्स्ट को एक साथ जोड़ना
            full_transcript = ""
            for t in transcript_list:
                full_transcript += f"{t['text']}\n"

            st.success("ट्रांसक्रिप्ट सफलतापूर्वक मिल गई!")

            # डिस्प्ले बॉक्स
            st.text_area("वीडियो के बोल (Transcript):", full_transcript, height=400)

            # डाउनलोड बटन
            st.download_button(
                label="ट्रांसक्रिप्ट डाउनलोड करें (.txt)",
                data=full_transcript,
                file_name=f"transcript_{video_id}.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as e:
            st.error("माफ़ करें! इस वीडियो के लिए ट्रांसक्रिप्ट उपलब्ध नहीं है।")
            st.warning("कारण: वीडियो बनाने वाले ने कैप्शंस बंद कर रखे हैं या इस भाषा में सबटाइटल मौजूद नहीं हैं।")
    else:
        st.error("कृपया एक सही YouTube लिंक डालें।")

st.markdown("---")
st.caption("Developed for @ruhanijot | Simple & Fast Transcript Tool")