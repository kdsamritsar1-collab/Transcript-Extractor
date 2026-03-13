import streamlit as st
import yt_dlp
import os
import json

# पेज सेटअप
st.set_page_config(page_title="Pro YT Transcript Extractor", page_icon="📜")

st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>📜 Pro YT Transcript Extractor</h1>", unsafe_allow_html=True)
st.write("---")

video_url = st.text_input("YouTube URL यहाँ डालें:", placeholder="https://www.youtube.com/watch?v=5a14DmrIA1U")

if st.button("Extract Transcript"):
    if video_url:
        with st.spinner('Scraping Subtitles from YouTube...'):
            try:
                # yt-dlp कॉन्फ़िगरेशन
                ydl_opts = {
                    'skip_download': True,        # वीडियो डाउनलोड नहीं करना, सिर्फ डेटा चाहिए
                    'writesubtitles': True,       # सबटाइटल्स लिखें
                    'writeautomaticsub': True,   # ऑटो-जेनरेटेड भी उठाएं
                    'subtitleslangs': ['pa', 'hi', 'en', 'all'], # भाषाएं
                    'quiet': True,
                    'no_warnings': True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    
                    # सबटाइटल्स चेक करना
                    subtitles = info.get('requested_subtitles')
                    
                    if subtitles:
                        # हम पहली उपलब्ध भाषा का टेक्स्ट निकालेंगे
                        lang = list(subtitles.keys())[0]
                        sub_url = subtitles[lang]['url']
                        st.success(f"सफलतापूर्वक मिली! भाषा: {lang}")
                        
                        # नोट: यह URL सीधे सबटाइटल फाइल (VTT/JSON) का होता है
                        st.info("आप नीचे दिए गए लिंक से सीधे ट्रांसक्रिप्ट फाइल देख सकते हैं:")
                        st.markdown(f"[यहाँ क्लिक करके ट्रांसक्रिप्ट देखें]({sub_url})")
                    else:
                        # यदि सबटाइटल्स सीधे नहीं मिले, तो 'Automatic Captions' की जांच करें
                        st.warning("सीधे सबटाइटल्स नहीं मिले। कृपया सुनिश्चित करें कि वीडियो में 'CC' बटन चालू है।")
                        
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.error("कृपया लिंक डालें।")

st.markdown("---")
st.caption("Using yt-dlp Engine | Alternative to standard APIs")
