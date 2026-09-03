import streamlit as st

# १. आवश्यक फ़ंक्शन / डिक्शनरी इंपोर्ट करें (यदि data_logic.py में हैं)
try:
    from data_logic import *  # या जो भी फ़ंक्शन आप डेटा कैलकुलेशन के लिए यूज़ कर रहे हैं
except ImportError:
    pass

# २. पेज का टाइटल या हेडिंग सेट करें
st.title("📊 मूलांक एवं भाग्यांक फल")

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

# २. पहले से डिफाइन करें ताकि NameError न आए
tab1_audio = f"नमस्ते {u_name} जी। आपके मूलांक और भाग्यांक का विश्लेषण तैयार है।"
tab1_audio += f"जय बजरंगबली {u_name} जी। आपका बजरङ्गिराम अंक ज्योतिष में स्वागत है  "
tab1_audio += f"आपका मूलांक {mulank} और भाग्यांक {bhagyank} है। "
tab1_audio += f"नामांक {name_num} और कुआ नंबर {kua} है। "
tab1_audio += f"आपके ग्रहों का फल कहता है कि {comb_fal}। "


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
    
    # एक सुंदर कार्ड के रूप में दिखाने के लिए
st.info(f"**मूलांक {mulank} और भाग्यांक {bhagyank}:**\n\n{result_fal}")

    
        # ४. ऑडियो के लिए स्क्रिप्ट में जोड़ें
# यहाँ tab1_audio का इस्तेमाल करें
tab1_audio += f" आपके मूलांक और भाग्यांक का मेल {combination_key} है। {result_fal}"
tab1_audio += "अपने राजयोग फल तथा अपने अच्छे व बुरे ग्रहों की जानकारी एवं सलाह तथा अपने नाम और मोबाइल नंबर के की जाँच के लिए कृपया ऊपर दी गई कैटेगरीज़ को चुनें।"

# ५. व्यक्तित्व का मुख्य आधार सेक्शन
st.markdown("---")
st.markdown("#### 🌟 आपके व्यक्तित्व का मुख्य आधार")
st.write(f"मूलांक **{mulank}** और भाग्यांक **{bhagyank}** का यह मेल आपके जीवन में विशेष प्रभाव डालता है।")

# ६. ऑडियो को कॉल करें (अगर bol_web फंक्शन बना हुआ है)
bol_web(tab1_audio, "graha_voice")
st.write(f"आपकी जन्म तिथि: **{user_dob}**")

# यहाँ आपका 'आपके शुभ पैरामीटर्स', मूलांक फल, भाग्यांक फल, आदि का पूरा कोड रहेगा...