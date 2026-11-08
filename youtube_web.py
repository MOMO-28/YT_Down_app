import streamlit as st
import yt_dlp
import os

st.title("📥 Web YouTube Downloader")
st.write("iPhone ၏ Safari (သို့) မည်သည့် Browser မှမဆို အသုံးပြုနိုင်ပါသည်။")

url = st.text_input("YouTube Link ထည့်ပါ:")
format_choice = st.selectbox("Format ရွေးချယ်ပါ:", ["MP4 (Video)", "MP3 (Audio)"])

if st.button("Download စတင်မည်"):
    if not url:
        st.warning("Link ထည့်ရန် လိုအပ်ပါသည်။")
    else:
        with st.spinner("Server ပေါ်တွင် ဒေါင်းလုပ်ဆွဲနေပါသည်။ ခဏစောင့်ပါ..."):
            try:
                # Format နှင့် Quality သတ်မှတ်ခြင်း
                if format_choice == "MP3 (Audio)":
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'outtmpl': '%(title)s.%(ext)s',
                    }
                else:
                    ydl_opts = {
                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                        'outtmpl': '%(title)s.%(ext)s',
                    }
                
                # ဒေါင်းလုပ်ဆွဲခြင်း
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    # ဖိုင်နာမည် အတိအကျကို ရယူခြင်း
                    filename = ydl.prepare_filename(info)
                    if format_choice == "MP3 (Audio)":
                        filename = filename.rsplit('.', 1)[0] + '.mp3'

                st.success("✅ အောင်မြင်ပါသည်။ သင့်ဖုန်းထဲသို့ သိမ်းရန် အောက်ပါ ခလုတ်ကို နှိပ်ပါ။")
                
                # iPhone သို့ ပြန်လည် Download ဆွဲရန် ခလုတ်
                with open(filename, "rb") as file:
                    st.download_button(
                        label="⬇️ ဖုန်းထဲသို့ သိမ်းမည် (Save to Device)",
                        data=file,
                        file_name=filename,
                        mime="video/mp4" if format_choice == "MP4 (Video)" else "audio/mpeg"
                    )
            except Exception as e:
                st.error(f"Error ဖြစ်နေပါသည်။: {e}")