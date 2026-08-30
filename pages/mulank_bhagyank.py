import os
import subprocess
import asyncio
import edge_tts
import streamlit as st

# =========================================================
# 1. ऑडियो (TTS) फ़ंक्शन - एरर-फ्री वर्ज़न
# =========================================================
# Line 8 की जगह यह लिखें:
def bol_web_mulank(text, part_id, container=None):
    try:
        clean_text = text.replace("*", "").replace("#", "").replace('"', '').replace("'", "")
        filename = f"output_{part_id}.mp3"

        # Edge-TTS कमांड से फ़ाइल बनाना
        cmd = f'edge-tts --text "{clean_text}" --voice hi-IN-MadhurNeural --write-media {filename}'
        subprocess.run(cmd, shell=True, check=True)

        # फ़ाइल सुरक्षित बनने के बाद प्ले करना
        if os.path.exists(filename):
            if container is not None:
                container.audio(filename, format="audio/mp3")
            else:
                st.audio(filename, format="audio/mp3")

    except Exception as e:
        st.error(f"ऑडियो जनरेट करने में त्रुटि आई: {e}")

# १. आवश्यक फ़ंक्शन / डिक्शनरी इंपोर्ट करें (यदि data_logic.py में हैं)
try:
    from data_logic import *  # या जो भी फ़ंक्शन आप डेटा कैलकुलेशन के लिए यूज़ कर रहे हैं
except ImportError:
    pass

# २. पेज का टाइटल या हेडिंग सेट करें
st.title("📊 मूलांक एवं भाग्यांक फल")

st.subheader("📍 पूरा विवरण सुनने के लिए play बटन दबाये")
audio_box = st.container()  # Line 39 - ऑडियो प्लेयर यहाँ ऊपर बनेगा

# 📜 मूलांक एवं भाग्यांक की परिभाषा कार्ड
st.markdown("""
<div style="
    background: linear-gradient(135deg, #f0f4ff 0%, #e6eeef 100%);
    border-left: 6px solid #1e3c72;
    padding: 16px 20px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.06);
    margin-bottom: 20px;
">
    <div style="margin-bottom: 10px;">
        <span style="font-size: 16px; font-weight: bold; color: #1e3c72;">📌 मूलांक (Driver Number)</span>
        <p style="margin: 4px 0 0 0; color: #2d3748; font-size: 14px; line-height: 1.5;">
            मूलांक व्यक्ति के जन्म की तारीख का योग होता है। यह आपके आंतरिक व्यक्तित्व, सोच, शारीरिक बनावट, स्वभाव और दैनिक आचरण को दर्शाता है।
        </p>
    </div>
    <hr style="border: none; border-top: 1px dashed #cbd5e0; margin: 8px 0;">
    <div>
        <span style="font-size: 16px; font-weight: bold; color: #2a5298;">🎯 भाग्यांक (Conductor Number)</span>
        <p style="margin: 4px 0 0 0; color: #2d3748; font-size: 14px; line-height: 1.5;">
            भाग्यांक आपकी पूरी जन्मतिथि (दिन + माह + वर्ष) का कुल योग है। यह जीवन के लक्ष्य, मिलने वाले अवसरों, करियर की दिशा और भाग्य की सफलता को तय करता है।
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ३. app.py से Save किया हुआ डेटा (Session State) प्राप्त करें
user_dob = st.session_state.get('u_dob')
user_name = st.session_state.get('user_name')

# ४. सुरक्षा जाँच: यदि यूज़र ने अभी तक main page पर फॉर्म नहीं भरा है
if not user_dob:
    st.warning("⚠️ कृपया पहले मुख्य पेज (Main Page) पर अपनी जन्म तिथि भरें!")
    if st.button("⬅️ मुख्य पेज पर जाएँ"):
        st.switch_page("app.py")
    st.stop()  # इसके आगे का कोड तब तक नहीं चलेगा जब तक dob न मिल जाए

# मूलांक, भाग्यांक, कुआं और नामांक डेटा निकालना
mulank = st.session_state.get('app_mulank', 1)
bhagyank = st.session_state.get('app_bhagyank', 1)
kua = st.session_state.get('app_kua', 1)
name_num = st.session_state.get('app_namank', 1)
u_name = st.session_state.get('u_name', '')
comb_fal = f"{mulank}-{bhagyank}"

# १. डेटा को सुरक्षित रूप से निकालें
m_data = grah_deta.get(mulank, {})
b_data = grah_deta.get(bhagyank, {})

# मूलांक के डेटा निकालना
m_grah = m_data.get('grah', 'न न')
m_din = m_data.get('day', 'न न')
m_rang = m_data.get('color', 'न न')

# भाग्यांक के डेटा निकालना
b_grah = b_data.get('grah', 'न न')
b_din = b_data.get('day', 'न न')
b_rang = b_data.get('color', 'न न')

# १. ऑडियो के लिए शुरुआती स्क्रिप्ट तैयार करना
tab1_audio = (
    f"जय श्री राम {u_name} जी! "
    f"मूलांक जिसे इंग्लिश में ड्राइवर नंबर बोलते हैं, यह आपके आंतरिक व्यक्तित्व, सोच, शारीरिक बनावट, स्वभाव और दैनिक आचरण को दर्शाता है। "
    f"जबकि वही भाग्यांक जिसको इंग्लिश में कंडक्टर नंबर बोला जाता है, यह आपके जीवन के लक्ष्य, मिलने वाले अवसरों, करियर की दिशा और भाग्य की सफलता को तय करता है। "
    f"आपके शुभ पैरामीटर्स इस प्रकार हैं। "
    f"आपका मूलांक {mulank} है, जिसके शुभ ग्रह {m_grah}, शुभ दिन {m_din} और शुभ रंग {m_rang} है। "
    f"आपका भाग्यांक {bhagyank} है, जिसके शुभ ग्रह {b_grah}, शुभ दिन {b_din} और शुभ रंग {b_rang} है। "
)

# ३. प्रीमियम कार्ड का डिज़ाइन (CSS)
st.markdown("""
<style>
    .lucky-container {
        background: linear-gradient(135deg, #ffffff 0%, #f9f9f9 100%);
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.05);
    }
    .flex-box { display: flex; justify-content: space-between; gap: 15px; }
    .info-col { flex: 1; padding: 15px; border-radius: 12px; }
    .m-bg { background-color: #e3f2fd; border: 1px solid #bbdefb; }
    .b-bg { background-color: #f3e5f5; border: 1px solid #e1bee7; }
    .label { font-weight: bold; color: #333; }
</style>
""", unsafe_allow_html=True)

# ४. कार्ड का डिस्प्ले (HTML)
st.markdown(f"""
<div class="lucky-container">
    <h5 style="text-align: center; color: #1a508b; margin-top: 0;">🌟 आपके शुभ पैरामीटर्स</h5>
    <div class="flex-box">
        <div class="info-col m-bg">
            <h6 style="color: red; margin-top: 0;">मूलांक: {mulank} (स्वभाव)</h6>
            <p><span class="label">🪐 ग्रह:</span> <span style="color: red; font-weight: bold;">{m_data.get('grah', 'N/A')}</span></p>
<p><span class="label">📅 दिन:</span> <span style="color: red; font-weight: bold;">{m_data.get('day', 'N/A')}</span></p>
<p><span class="label">🎨 रंग:</span> <span style="color: red; font-weight: bold;">{m_data.get('color', 'N/A')}</span></p>
            <p style="font-size: 12px; color: red; font-style: italic;">उपयोग: दैनिक शांति व आत्मविश्वास हेतु।</p>
        </div>
        <div class="info-col b-bg">
            <h6 style="color: blue; margin-top: 0;">भाग्यांक: {bhagyank} (भाग्य)</h6>
            <p><span class="label">🪐 ग्रह:</span> <span style="color: blue; font-weight: bold;">{b_data.get('grah', 'N/A')}</span></p>
<p><span class="label">📅 दिन:</span> <span style="color: blue; font-weight: bold;">{b_data.get('day', 'N/A')}</span></p>
<p><span class="label">🎨 रंग:</span> <span style="color: blue; font-weight: bold;">{b_data.get('color', 'N/A')}</span></p>
            <p style="font-size: 12px; color: blue; font-style: italic;">उपयोग: करियर व बड़ी सफलताओं हेतु।</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
# १. डेटा वेरिएबल्स (यह जोड़ना जरूरी है)
m_grah = m_data.get('grah', 'विशेष ग्रह')
m_din = m_data.get('day', 'शुभ दिन')
m_rang = m_data.get('color', 'शुभ रंग')

b_grah = b_data.get('grah', 'विशेष ग्रह')
b_din = b_data.get('day', 'शुभ दिन')
b_rang = b_data.get('color', 'शुभ रंग')

# २. ऑडियो स्क्रिप्ट
tab1_audio = (
    f"प्रणाम {u_name} जी! आपके मूलांक {mulank} के आधार पर, जो आपके स्वभाव को दर्शाता है, "
    f"आपका शुभ ग्रह {m_grah} है, शुभ दिन {m_din} है और आपका सबसे अनुकूल रंग {m_rang} है। "
    f"वहीं आपके भाग्यांक {bhagyank} के अनुसार, आपका स्वामी ग्रह {b_grah} है। शुभ दिन {b_din} है और आपका सबसे अनुकूल रंग {b_rang} है।"
)
    
    # एक लाइन खींचने के लिएst.divider() 
    
    # १. फल के लिए 'Key' तैयार करें
combination_key = f"{mulank}-{bhagyank}"

    # २. डिक्शनरी से फल प्राप्त करें
    # faladesh_dict वही है जो आपने फोटो 7ff1cf19-9461-4913-944a-fdb1c349e391 में बनाई है
result_fal = faladesh_dict.get(combination_key, "इस विशेष कॉम्बिनेशन का विश्लेषण अभी तैयार किया जा रहा है।")

    # ३. स्क्रीन पर प्रदर्शित करें
st.markdown(f"#### 🚩 व्यक्तित्व विश्लेषण (कॉम्बिनेशन {combination_key})")
    
# २. व्यक्तित्व विश्लेषण (कॉम्बीनेशन फल) ऑडियो में जोड़ें
tab1_audio += f"आपके मूलांक {mulank} और भाग्यांक {bhagyank} का मेल बताता है कि {result_fal} "

    
        # ४. ऑडियो के लिए स्क्रिप्ट में जोड़ें
# यहाँ tab1_audio का इस्तेमाल करें
tab1_audio += f" आपके मूलांक और भाग्यांक का मेल {combination_key} है। {result_fal}"
tab1_audio += "अपने राजयोग फल तथा अपने अच्छे व बुरे ग्रहों की जानकारी एवं सलाह तथा अपने नाम और मोबाइल नंबर के की जाँच के लिए कृपया ऊपर दी गई कैटेगरीज़ को चुनें।"

# ५. व्यक्तित्व का मुख्य आधार सेक्शन
st.markdown("---")
st.markdown("#### 🌟 आपके व्यक्तित्व का मुख्य आधार")
st.write(f"मूलांक **{mulank}** और भाग्यांक **{bhagyank}** का यह मेल आपके जीवन में विशेष प्रभाव डालता है।")

# ---------------------------------------------------------
# 💼 करियर एवं आजीविका दिशा (Job vs Business)
# ---------------------------------------------------------
st.subheader("💼 करियर एवं आजीविका दिशा (Job vs Business)")

# 1. ग्रिड के अंकों को सुरक्षित रूप से एकत्रित करना
d_str = str(st.session_state.get('dob_digits', locals().get('dob_digits', '')))
m_str = str(locals().get('mulank', st.session_state.get('mulank', '')))
b_str = str(locals().get('bhagyank', st.session_state.get('bhagyank', '')))
k_str = str(locals().get('kua_num', st.session_state.get('kua_num', '')))
n_str = str(st.session_state.get('name_num', locals().get('name_num', '')))

full_digits_str = f"{d_str}{m_str}{b_str}{k_str}{n_str}"
grid_digits = [int(c) for c in full_digits_str if c.isdigit()]

# 2. ग्रहों/अंकों का वर्गीकरण
biz_nums = [3, 5, 6, 9]  # व्यापारिक अंक (गुरु, बुध, शुक्र, मंगल)
job_nums = [1, 4, 7, 8]  # नौकरी/सेवा अंक (सूर्य, राहु, केतु, शनि)

# अंकों की गिनती के आधार पर प्राथमिक स्कोर
biz_score = sum(grid_digits.count(n) for n in biz_nums)
job_score = sum(grid_digits.count(n) for n in job_nums)

# मूलांक और भाग्यांक का विशेष वेटेज (1.5x)
m_val = int(mulank) if 'mulank' in locals() and str(mulank).isdigit() else 0
b_val = int(bhagyank) if 'bhagyank' in locals() and str(bhagyank).isdigit() else 0

if m_val in biz_nums: biz_score += 1.5
if m_val in job_nums: job_score += 1.5
if b_val in biz_nums: biz_score += 1.5
if b_val in job_nums: job_score += 1.5

# प्रतिशत की गणना
total_score = biz_score + job_score
if total_score > 0:
    biz_pct = round((biz_score / total_score) * 100)
    job_pct = 100 - biz_pct
else:
    biz_pct, job_pct = 50, 50

# 3. स्कोर के आधार पर निष्कर्ष व सुझाव
if biz_pct > job_pct + 10:
    recommendation = "🏢 स्वतंत्र व्यापार / बिजनेस (Business Mindset)"
    detail_msg = "आपकी ग्रिड में व्यापारिक ग्रहों (बुध, शुक्र, गुरु, मंगल) की प्रबलता है। आप स्वतंत्र रूप से काम करने, जोखिम लेने और अपने विचार लागू करने में अधिक सफल रहेंगे।"
    fields = "ट्रेडिंग, रियल एस्टेट, कंसल्टेंसी, फैशन/डिजाइनिंग, रेस्टोरेंट, मैन्युफैक्चरिंग या खुद की एजेंसी।"
    bg_color = "#e6fffa"
    border_color = "#319795"
elif job_pct > biz_pct + 10:
    recommendation = "👔 नौकरी एवं सेवा क्षेत्र (Corporate & Service Mindset)"
    detail_msg = "आपकी ग्रिड में प्रशासनिक व सेवा ग्रहों (सूर्य, राहु, शनि, केतु) का वर्चस्व है। आपके लिए नियमित आय, पद-प्रतिष्ठा और व्यवस्थित सिस्टम के साथ काम करना अधिक सुरक्षित व फलदायी रहेगा।"
    fields = "सरकारी नौकरी, IT/सॉफ्टवेयर, प्रशासनिक सेवाएं (IAS/PCS), बैंकिंग, कानून या मेडिकल/रिसर्च।"
    bg_color = "#ebf8ff"
    border_color = "#3182ce"
else:
    recommendation = "🔄 मिश्रित करियर (Hybrid Model: Job to Business)"
    detail_msg = "आपकी ग्रिड में नौकरी और व्यापार दोनों के अंक संतुलित हैं। आपके लिए करियर की शुरुआत नौकरी से करना और 32-35 वर्ष की आयु के बाद अपना खुद का व्यवसाय शुरू करना सर्वोत्तम रहेगा।"
    fields = "प्रबंधन (Management), फ्रीलांसिंग, कॉर्पोरेट जॉब के साथ साइड-बिजनेस।"
    bg_color = "#fefcbf"
    border_color = "#d69e2e"

# 4. सुंदर UI कार्ड डिस्प्ले
st.markdown(f"""
<div style="
    background-color: {bg_color};
    border-left: 6px solid {border_color};
    padding: 18px 20px;
    border-radius: 10px;
    margin-top: 15px;
    margin-bottom: 25px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
">
    <h4 style="margin: 0 0 8px 0; color: #2d3748; font-size: 18px;">{recommendation}</h4>
    <p style="margin: 0 0 12px 0; font-size: 14px; color: #4a5568; line-height: 1.5;">{detail_msg}</p>
    <hr style="border: 0; border-top: 1px dashed #cbd5e0; margin: 10px 0;">
    <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-weight: bold; font-size: 14px;">
        <span style="color: #2b6cb0;">👔 नौकरी की अनुकूलता: {job_pct}%</span>
        <span style="color: #276749;">💼 व्यापार की अनुकूलता: {biz_pct}%</span>
    </div>
    <p style="margin: 6px 0 0 0; font-size: 13px; color: #2d3748;"><b>🎯 सर्वोत्तम कार्यक्षेत्र:</b> {fields}</p>
</div>
""", unsafe_allow_html=True)

# ६. ऑडियो को कॉल करें (अगर bol_web फंक्शन बना हुआ है)
# ३. करियर का सुझाव ऑडियो में जोड़ें
tab1_audio += f"करियर एवं आजीविका के लिए: {recommendation}। {detail_msg} आपके लिए सर्वोत्तम कार्यक्षेत्र {fields} हैं। नौकरी की अनुकूलता {job_pct} प्रतिशत और व्यापार की अनुकूलता {biz_pct} प्रतिशत है।"

# ४. ऊपर आरक्षित 'audio_box' में ऑडियो जनरेट और प्ले करें
# Line 280 पर यह लिखें:
bol_web_mulank(tab1_audio, "tab1_mulank_voice", container=audio_box)