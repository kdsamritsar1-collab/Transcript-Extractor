import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import io

# पेज सेटअप
st.set_page_config(page_title="Advanced YT Transcript Extractor", page_icon="📜")

st.markdown("<h1 style='text-align: center; color: #FF0000;'>🎥 Advanced YouTube Transcript Extractor</h1>", unsafe_allow_html=True)
st.write("---")

# इनपुट फील्ड
video_url = st.text_input("YouTube वीडियो का लिंक यहाँ पेस्ट करें (जैसे: https://www.youtube.com/watch?v=5a14DmrIA1U):")

if video_url:
    # वीडियो ID निकालना (लिंक या केवल ID दोनों काम करेंगे)
    video_id = ""
    if "v=" in video_url:
        video_id = video_url.split("v=")[1].split("&")[0]
    else:
        video_id = video_url.strip()

    if video_id:
        st.info(f"वीडियो ID: {video_id} के लिए उपलब्ध स्क्रिप्ट्स की जांच हो रही है...")

        try:
            # 1. पहले उपलब्ध सभी ट्रांसक्रिप्ट्स की लिस्ट निकालें
            transcript_list_meta = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # 2. सबसे पहले 'Manual' (इंसान द्वारा लिखी गई) स्क्रिप्ट ढूंढें, 
            # वरना 'Auto-generated' (AI द्वारा बनाई गई) चुनें
            try:
                # पंजाबी, हिंदी या अंग्रेजी में से जो भी मिल जाए
                transcript = transcript_list_meta.find_transcript(['pa', 'hi', 'en'])
            except:
                # यदि ऊपर वाली भाषाएं नहीं मिली, तो जो भी पहली भाषा उपलब्ध हो उसे उठा लें
                transcript = transcript_list_meta.find_generated_transcript(['en', 'pa', 'hi']) or transcript_list_meta.find_transcript([])

            # डेटा फेच करना
            transcript_data = transcript.fetch()
            
            # टेक्स्ट को फॉर्मेट करना
            full_transcript = ""
            for t in transcript_data:
                full_transcript += f"{t['text']}\n"

            st.success(f"सफलतापूर्वक ट्रांसक्रिप्ट मिल गई! (भाषा: {transcript.language})")

            # डिस्प्ले और डाउनलोड
            st.text_area("वीडियो के बोल (Transcript):", full_transcript, height=400)
            st.download_button(
                label="डाउनलोड करें (.txt)",
                data=full_transcript,
                file_name=f"transcript_{video_id}.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as e:
            st.error("माफ़ करें! इस वीडियो के लिए स्क्रिप्ट लॉक है या एक्सेस नहीं की जा सकती।")
            st.warning(f"तकनीकी विवरण: {str(e)}")
            st.info("सुझाव: सुनिश्चित करें कि वीडियो 'Public' है और उसमें कम से कम एक भाषा के सबटाइटल चालू हैं।")
    else:
        st.error("कृपया एक सही YouTube लिंक या वीडियो ID डालें।")

st.markdown("---")
st.caption("Developed for @ruhanijot | Advanced Language Logic Applied")
