import asyncio
import edge_tts
import streamlit as st

# ==========================================
# १. ऑडियो (TTS) फ़ंक्शन - टॉप प्लेसहोल्डर सपोर्ट
# ==========================================
def bol_web(text, part_id, container=None):
    try:
        clean_text = (
            text.replace("-", " , ").replace("*", "").replace("#", "")
        )
        filename = f"output_{part_id}.mp3"
        
        async def _generate_edge():
            communicate = edge_tts.Communicate(clean_text, "hi-IN-MadhurNeural")
            await communicate.save(filename)
            
        asyncio.run(_generate_edge())
        
        if container:
            container.audio(filename, format="audio/mp3")
        else:
            st.audio(filename, format="audio/mp3")
    except Exception as e:
        st.error(f"ऑडियो जनरेट करने में त्रुटि आई: {e}")

# ==========================================
# २. आवश्यक मास्टर डिक्शनरी
# ==========================================
rajyog_fal = {
    "मानसिक शक्ति राजयोग (4-9-2)": "आपकी मानसिक क्षमता और निर्णय लेने की शक्ति अद्भुत है।",
    "इच्छा शक्ति राजयोग (3-5-7)": "आपकी इच्छाशक्ति और आत्मबल बहुत मजबूत है।",
    "कर्म शक्ति राजयोग (8-1-6)": "आप अत्यधिक परिश्रमी और कर्मनिष्ठ व्यक्ति हैं।",
    "विचार शक्ति राजयोग (4-3-8)": "आपकी योजना बनाने की क्षमता और दूरदर्शिता उत्कृष्ट है।",
    "सफलता राजयोग (9-5-1)": "यह राजयोग जीवन में प्रसिद्धि और सफलता दिलाता है।",
    "संतान और संपन्नता (2-7-6)": "यह योग सुख, संतान और आर्थिक संपन्नता लाता है।",
    "गोल्डन राजयोग (4-5-6)": "यह जीवन में हर प्रकार की भौतिक समृद्धि देता है।",
    "सिल्वर राजयोग (2-5-8)": "यह राजयोग भूमि, मकान और स्थायी धन लाभ देता है।"
}

remedy_info = {
    1: {"grah": "सूर्य देव", "upay": "तांबे के बर्तन से सूर्य देव को जल अर्पित करें।"},
    2: {"grah": "चंद्र देव", "upay": "चांदी के गिलास में पानी पीएं और माता का आशीर्वाद लें।"},
    3: {"grah": "गुरु देव", "upay": "केसर या हल्दी का तिलक लगाएं और गुरुजनों का सम्मान करें।"},
    4: {"grah": "राहु देव", "upay": "लकड़ी का पेन पास रखें और हरी घास पर चलें।"},
    5: {"grah": "बुध देव", "upay": "गाय को हरा चारा खिलाएं और घर का मध्य भाग साफ़ रखें।"},
    6: {"grah": "शुक्र देव", "upay": "इत्र का प्रयोग करें और महिलाओं का सम्मान करें।"},
    7: {"grah": "केतु देव", "upay": "कुत्ते को भोजन कराएं और गणेश जी की आराधना करें।"},
    8: {"grah": "शनि देव", "upay": "हनुमान चालीसा का पाठ करें और ज़रूरतमंदों की मदद करें।"},
    9: {"grah": "मंगल देव", "upay": "हनुमान जी को चोला चढ़ाएं और लाल रुमाल पास रखें।"}
}

# ==========================================
# ३. सेशन स्टेट से डेटा कलेक्शन
# ==========================================
u_name = st.session_state.get("user_name", "साधक")
dob = str(st.session_state.get("app_dob") or st.session_state.get("dob") or "")
mulank = st.session_state.get("app_mulank") or st.session_state.get("mulank") or 0
bhagyank = st.session_state.get("app_bhagyank") or st.session_state.get("bhagyank") or 0
name_num = st.session_state.get("namank") or st.session_state.get("app_namank") or 0
kua = st.session_state.get("kua_number") or st.session_state.get("app_kua") or 0

dob_digits = [int(ch) for ch in dob if ch.isdigit() and ch != '0']
all_present_nums = set(dob_digits) | {int(mulank), int(bhagyank), int(name_num), int(kua)} - {0}
all_present_list = dob_digits + [int(mulank), int(bhagyank), int(name_num), int(kua)]

# ==========================================
# ४. स्क्रीन हेडर और ऑडियो प्लेयर आरक्षित जगह
# ==========================================
st.markdown("<h2 style='color:#1E88E5;'>🔮 लो-शू ग्रिड, राजयोग एवं उपाय</h2>", unsafe_allow_html=True)
st.subheader(f"जय श्री राम **{u_name}** जी!")

# 📌 ऑडियो प्लेयर के लिए ऊपर ही जगह आरक्षित करना
st.subheader("📢 पूरा विवरण सुनने के लिए play बटन दबाएं")
audio_box = st.empty()

st.markdown("<p style='text-align: center; color: gray;'>आचार्य विशाल विक्रम पांडे</p>", unsafe_allow_html=True)
st.write("---")

# ==========================================
# ५. डायनेमिक ऑडियो स्क्रिप्ट तैयार करना
# ==========================================
script_audio_text = f"जय श्री राम {u_name} जी। "
script_audio_text += f"आपके चार्ट में मूलांक {mulank}, भाग्यांक {bhagyank}, नामांक {name_num} और कुआं नंबर {kua} है। "

# --- लो-शू ग्रिड टेबल प्रदर्शन ---
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.markdown(f"""
    <div style='line-height: 2.2; font-size: 16px; font-weight: 500;'>
        <span style='color: #d9534f;'>मूलांक:</span> <b>{mulank}</b><br>
        <span style='color: #0275d8;'>भाग्यांक:</span> <b>{bhagyank}</b><br>
        <span style='color: #5cb85c;'>नामांक:</span> <b>{name_num}</b><br>
        <span style='color: #6c757d;'>कुआं नंबर:</span> <b>{kua}</b>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    loshu_nums = [4, 9, 2, 3, 5, 7, 8, 1, 6]
    grid_cells = {num: str(num) * all_present_list.count(num) if all_present_list.count(num) > 0 else "" for num in loshu_nums}
    table_html = f"""
    <div style="text-align: center; font-size: 15px; font-weight: bold; margin-bottom: 6px;">📅 लो-शू ग्रिड</div>
    <table style="width:100%; border-collapse: collapse; text-align: center; border: 1px solid #adb5bd;">
        <tr><td style="border:1px solid #adb5bd; padding:10px;">{grid_cells[4]}</td><td style="border:1px solid #adb5bd; padding:10px;">{grid_cells[9]}</td><td style="border:1px solid #adb5bd; padding:10px;">{grid_cells[2]}</td></tr>
        <tr><td style="border:1px solid #adb5bd; padding:10px;">{grid_cells[3]}</td><td style="border:1px solid #adb5bd; padding:10px;">{grid_cells[5]}</td><td style="border:1px solid #adb5bd; padding:10px;">{grid_cells[7]}</td></tr>
        <tr><td style="border:1px solid #adb5bd; padding:10px;">{grid_cells[8]}</td><td style="border:1px solid #adb5bd; padding:10px;">{grid_cells[1]}</td><td style="border:1px solid #adb5bd; padding:10px;">{grid_cells[6]}</td></tr>
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)

st.divider()

# --- राजयोग सेक्शन व वॉइस स्क्रिप्ट ---
st.subheader("✨ आपके लो-शू ग्रिड के राजयोग")

active_rajyog = []
planes = [
    ([4, 9, 2], "मानसिक शक्ति राजयोग (4-9-2)"),
    ([3, 5, 7], "इच्छा शक्ति राजयोग (3-5-7)"),
    ([8, 1, 6], "कर्म शक्ति राजयोग (8-1-6)"),
    ([4, 3, 8], "विचार शक्ति राजयोग (4-3-8)"),
    ([9, 5, 1], "सफलता राजयोग (9-5-1)"),
    ([2, 7, 6], "संतान और संपन्नता (2-7-6)"),
    ([4, 5, 6], "गोल्डन राजयोग (4-5-6)"),
    ([2, 5, 8], "सिल्वर राजयोग (2-5-8)")
]

for p_nums, p_name in planes:
    if all(num in all_present_nums for num in p_nums):
        active_rajyog.append(p_name)

if active_rajyog:
    script_audio_text += "अब आपके चार्ट के राजयोगों की बात करते हैं। "
    for ry in active_rajyog:
        fal = rajyog_fal.get(ry, "यह एक अत्यंत शुभ राजयोग है।")
        st.success(f"✅ **{ry}**")
        st.info(f"💡 **फल:** {fal}")
        script_audio_text += f"{ry}। {fal} "
else:
    st.write("वर्तमान ग्रिड में कोई पूर्ण राजयोग नहीं बन रहा है।")
    script_audio_text += "वर्तमान ग्रिड में कोई पूर्ण राजयोग नहीं बन रहा है। "

st.divider()

# --- मिसिंग नंबर व उपाय स्क्रिप्ट ---
st.subheader("🔍 मिसिंग नंबर्स और उपाय")

missing_nums = [n for n in range(1, 10) if n not in all_present_nums]

if missing_nums:
    script_audio_text += "अब आपके चार्ट में मौजूद अनुपस्थित यानी मिसिंग नंबरों के उपायों की चर्चा करते हैं। "
    for n in missing_nums:
        if n in remedy_info:
            g = remedy_info[n]['grah']
            u = remedy_info[n]['upay']
            st.warning(f"अंक {n} ({g}) अनुपस्थित है")
            st.write(f"👉 **उपाय:** {u}")
            script_audio_text += f"अंक {n} जो {g} का है, उसके लिए उपाय है: {u}। "
else:
    st.success("🎉 बधाई हो! आपके चार्ट में सभी अंक उपस्थित हैं।")
    script_audio_text += "बधाई हो, आपके चार्ट में सभी आवश्यक अंक उपस्थित हैं। "

script_audio_text += "विशेष परामर्श हेतु आचार्य विशाल विक्रम पांडे जी से संपर्क करें।"

# ==========================================
# ६. ऊपर आरक्षित प्लेसहोल्डर (audio_box) में ऑडियो भेजना
# ==========================================
bol_web(script_audio_text, "grid_upay_voice", container=audio_box)