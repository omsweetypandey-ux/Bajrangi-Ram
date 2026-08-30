import asyncio
import edge_tts
import streamlit as st

# ==========================================
# 1. ऑडियो (TTS) फ़ंक्शन - पीली लाइन हटाने के लिए
# ==========================================
def bol_web(text, part_id, container=None):
    try:
        clean_text = text.replace("*", "").replace("#", "")
        # part_id के आधार पर हर सेक्शन की फाइल अलग बनेगी
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
# 1. आवश्यक मास्टर डेटा (Master Dictionaries)
# ==========================================
grah_data = {
    1: {'grah': 'सूर्य'}, 2: {'grah': 'चंद्रमा'}, 3: {'grah': 'गुरु'},
    4: {'grah': 'राहु'}, 5: {'grah': 'बुध'}, 6: {'grah': 'शुक्र'},
    7: {'grah': 'केतु'}, 8: {'grah': 'शनि'}, 9: {'grah': 'मंगल'}
}

compound_master_81 = {
    10: "अंक 10 'भाग्य चक्र' है। यह मान-सम्मान और सफलता का प्रतीक है। आपकी योजनाएँ सफल होंगी।",
    11: "यह मास्टर नंबर है। यह महान अंतर्ज्ञान देता है, लेकिन छिपे हुए शत्रुओं से सावधान रहना चाहिए।",
    12: "यह अंक बलिदान और चिंता दर्शाता है। दूसरों के षड्यंत्र से बचने के लिए सतर्क रहें।",
    13: "यह बदलाव और सत्ता का अंक है। सही दिशा में मेहनत करने पर यह अपार शक्ति देता है।",
    14: "संचार और व्यापार के लिए उत्तम। यात्रा के योग बनते हैं, लेकिन जोखिम से बचें।",
    15: "आकर्षण और भौतिक सुखों का अंक। कला और व्यक्तित्व में जादुई प्रभाव देता है।",
    16: "यह अंक भविष्य के प्रति सचेत रहने की चेतावनी देता है। अचानक बदलाव संभव हैं।",
    17: "मूलांक 1 (सूर्य) और भाग्यांक 7 (केतु) का संयोजन नेतृत्व और आध्यात्मिकता का एक दुर्लभ और शक्तिशाली मिश्रण है। आप आत्मविश्वासी और महत्वाकांक्षी होने के साथ-साथ गहरी सोच, अनुसंधान (research) और अंतर्ज्ञान (intuition) में निपुण होते हैं। यह संयोजन जीवन में करियर के लिए उत्कृष्ट है, लेकिन मानसिक स्पष्टता के लिए संतुलन की आवश्यकता होती है। यह 'सितारा' अंक है। संघर्ष के बाद अमर प्रसिद्धि और शांति दिलाने वाला अंक।",
    18: "कठिन संघर्ष और वैचारिक मतभेद का संकेत। मानसिक मजबूती आवश्यक है।",
    19: "यह 'सूर्य का अंक' है। विजय, सफलता और सौभाग्य का सबसे शुभ प्रतीक।",
    20: "नई योजनाओं और मानसिक जाग्रति का अंक। आध्यात्मिक विकास के लिए श्रेष्ठ।",
    21: "लंबी लड़ाई के बाद अंतिम विजय और उन्नति को दर्शाता है। अत्यंत शुभ।",
    22: "भ्रम और गलत निर्णयों के प्रति चेतावनी। अपनी शक्तियों का प्रयोग सोच-समझकर करें।",
    23: "'शाही सफलता' का अंक। वरिष्ठों से मदद और बाधाओं का नाश करने वाला।",
    24: "प्रेम, धन और सहायता का अंक। प्रभावशाली मित्रों से लाभ मिलता है।",
    25: "अनुभव से प्राप्त ज्ञान। सफलता शुरुआती संघर्ष के बाद स्थायी रूप से आती है।",
    26: "भविष्य की सुरक्षा के प्रति चेतावनी। दूसरों की सलाह पर आँख मूँदकर भरोसा न करें।",
    27: "शक्ति और अधिकार का प्रतीक। नेतृत्व क्षमता और रचनात्मक विचार प्रदान करता है।",
    28: "महान क्षमता लेकिन बड़े जोखिम का अंक। सावधानी न बरतने पर नुकसान संभव है।",
    29: "अनिश्चितता और विश्वासघात का संकेत। रिश्तों और साझेदारी में सावधानी बरतें।",
    30: "मानसिक श्रेष्ठता और विचारशीलता का अंक। यह सामाजिक मेलजोल से दूर रख सकता है।",
    31: "एकाकीपन और आत्मनिरीक्षण का अंक। भौतिक सफलता में थोड़ी देरी हो सकती है।",
    32: "व्यापार और लोकप्रियता के लिए जादुई अंक। वाणी में गजब का आकर्षण देता है।",
    33: "यह सौभाग्य और सुरक्षा का अंक है। प्रेम और व्यापार में सफलता सुनिश्चित करता है।",
    34: "यह 25 की तरह है। मेहनत का फल देर से मिलता है, पर स्थायी होता है।",
    35: "वित्तीय लाभ और संचय का अंक। विरासत या व्यापार से धन लाभ के योग बनाता है।",
    36: "साहस और विजय का अंक। यह व्यक्ति को अपने विरोधियों पर जीत दिलाता है।",
    37: "प्रेम और मित्रता में सौभाग्य। सामाजिक प्रतिष्ठा और मित्रों का सहयोग मिलता है।",
    38: "सावधानी का अंक। स्वास्थ्य और कानूनी मामलों में सतर्कता बरतनी चाहिए।",
    39: "बौद्धिक क्षमता का अंक। यह व्यक्ति को किसी विशेष कला में निपुण बनाता है।",
    40: "परिवर्तन और उन्नति का अंक। पुराने को छोड़कर नए को अपनाने से लाभ होगा।",
    41: "लेखन और व्यापारिक विस्तार के लिए बहुत ही ऊर्जावान और शुभ अंक।",
    42: "शुक्र की ऊर्जा। कला, सौंदर्य और विलासिता के क्षेत्र में अपार प्रसिद्धि।",
    43: "संघर्ष और उतार-चढ़ाव का अंक। अनुशासन से ही सफलता प्राप्त होगी।",
    44: "गंभीरता और जिम्मेदारी का अंक। यह थोड़े भारी परिणाम दे सकता है।",
    45: "संगठन और शक्ति का अंक। बड़े व्यापारिक साम्राज्य बनाने के लिए शुभ।",
    46: "ज्ञान और बौद्धिक विजय। यह समाज में एक विशेष पहचान दिलाता है।",
    47: "अचानक आने वाली बाधाएं और उनका समाधान। धैर्य की परीक्षा लेता है।",
    48: "मानसिक द्वंद्व और चुनौतियों का अंक। शांत रहकर ही निर्णय लें।",
    49: "अधूरापन महसूस करा सकता है। कार्यों को पूरा करने के लिए दृढ़ संकल्प लें।",
    50: "बुद्धिमानी और संचार। यह अंक व्यक्ति को बहुमुखी प्रतिभा का धनी बनाता है।",
    51: "अत्यंत शक्तिशाली! अचानक पद-प्रतिष्ठा और राजनीतिक सफलता दिलाने वाला।",
    52: "अनुभव और अंतर्ज्ञान। यह 25 का उच्च रूप है, जो गहराई से ज्ञान देता है।",
    53: "नेतृत्व और साहस। यह अंक आपको भीड़ से अलग खड़ा करने की शक्ति देता है।",
    54: "स्थिरता और सुरक्षा। यह परिवार और समाज में सम्मान दिलाने वाला अंक है।",
    55: "स्वतंत्रता और परिवर्तन। यह पुरानी रूढ़ियों को तोड़ने वाला अंक है।",
    56: "रिश्तों में उतार-चढ़ाव। संतुलन बनाए रखना ही सबसे बड़ी चुनौती होगी।",
    57: "बुद्धि और शोध। जटिल समस्याओं को सुलझाने की अद्भुत क्षमता देता है।",
    58: "स्वास्थ्य के प्रति सचेत रहने वाला अंक। खान-पान पर ध्यान देना आवश्यक है।",
    59: "यात्रा और नए अनुभवों का अंक। यह जीवन में गतिशीलता बनाए रखता है।",
    60: "कलात्मक सफलता और पारिवारिक सुख। यह शांतिप्रिय जीवन प्रदान करता है।",
    61: "संघर्ष के बाद मान-सम्मान। यह अंक धीमे लेकिन पक्के परिणाम देता है।",
    62: "साझेदारी में लाभ। दूसरों के सहयोग से बड़े लक्ष्य प्राप्त होंगे।",
    63: "धार्मिक और आध्यात्मिक उन्नति। यह व्यक्ति को मानसिक शांति देता है।",
    64: "कठिन परिश्रम का अंक। बिना मेहनत के यहाँ कुछ भी हासिल नहीं होगा।",
    65: "वित्तीय स्थिरता। यह धन को संभालने और निवेश करने की समझ देता है।",
    66: "प्रेम और रिश्तों में मधुरता। यह एक बहुत ही सौम्य और शुभ अंक है।",
    67: "अचानक लाभ के योग। यह किस्मत का साथ दिलाने वाला अंक माना जाता है।",
    68: "जिम्मेदारी और अनुशासन। यह व्यक्ति को कर्तव्यपरायण बनाता है।",
    69: "पूर्णता और अंत। यह एक चक्र के समाप्त होने और नए के शुरू होने का अंक है।",
    70: "गहन चिंतन और एकांत। यह दार्शनिक विचारों के लिए श्रेष्ठ अंक है।",
    71: "प्रसिद्धि और अधिकार। यह व्यक्ति को समाज के उच्च स्तर पर ले जाता है।",
    72: "सेवा और परोपकार। दूसरों की मदद करने से ही आपका भाग्योदय होगा।",
    73: "बुद्धि और चातुर्य। व्यापारिक समझौतों में यह अंक बहुत लाभ देता है।",
    74: "अज्ञात भय और चिंता। आत्मविश्वास बनाए रखना ही एकमात्र उपाय है।",
    75: "परिवर्तन के माध्यम से लाभ। नई परिस्थितियों में ढलना आपके लिए अच्छा है।",
    76: "कलात्मक अभिरुचि। यह अंक रचनात्मक कार्यों में सफलता सुनिश्चित करता है।",
    77: "आध्यात्मिक शक्ति और अंतर्ज्ञान। यह 11 का एक अत्यंत उच्च रूप है।",
    78: "भौतिकवाद और सफलता। यह सुख-सुविधाओं के साधन जुटाने में मदद करता है।",
    79: "अंतिम सत्य की खोज। यह अंक व्यक्ति को आत्मज्ञानी बनाता है।",
    80: "शनि की ऊर्जा। यह कठोर परिश्रम और न्याय का अंक है। देरी संभव है।",
    81: "विजय का अंतिम अंक! यह 9 (मंगल) का सर्वोच्च रूप है, जो पूर्ण सफलता देता है।"
}

friendship_logic = {
    1: {'friends': [1, 2, 3, 5, 9], 'enemies': [8], 'neutral': [4, 6, 7]},
    2: {'friends': [1, 3, 5, 9], 'enemies': [4, 8], 'neutral': [6, 7]},
    3: {'friends': [1, 2, 5, 7, 9], 'enemies': [6], 'neutral': [4, 8]},
    4: {'friends': [5, 6, 7, 8], 'enemies': [1, 2, 9], 'neutral': [3]},
    5: {'friends': [1, 3, 4, 6, 7, 8, 9], 'enemies': [2], 'neutral': []},
    6: {'friends': [4, 5, 7, 8], 'enemies': [3], 'neutral': [1, 2, 9]},
    7: {'friends': [3, 4, 5, 6], 'enemies': [1, 2, 9], 'neutral': [8]},
    8: {'friends': [4, 5, 6, 7], 'enemies': [1, 2, 9], 'neutral': [3]},
    9: {'friends': [1, 2, 3, 5], 'enemies': [4, 7, 8], 'neutral': [6]}
}
# 1. सुरक्षा जाँच (Session State Validation)
u_dob = st.session_state.get('u_dob')

if not u_dob:
    st.warning("⚠️ कृपया पहले मुख्य पेज (Main Page) पर अपना विवरण भरें!")
    if st.button("🏠 मुख्य पेज पर जाएँ"):
        st.switch_page("app.py")
    st.stop()

# 2. सेशन स्टेट से डेटा निकालना
u_name = st.session_state.get('u_name', 'मित्र')
name_num = st.session_state.get('app_namank', 1)
mulank = st.session_state.get('app_mulank', 1)
bhagyank = st.session_state.get('app_bhagyank', 1)
name_val = st.session_state.get('app_name_val', name_num)
kua_num = st.session_state.get('kua_num', '')
dob_digits = st.session_state.get('dob_digits', '')

# =========================================================
# यहाँ Tab 2 वाला आपका पूरा विश्लेषण कोड आएगा (Same to Same)
# =========================================================
# ---------------------------------------------------------
# 3. UI, हेडर और हस्तलिखित स्क्रिप्ट का नया सेटअप
# ---------------------------------------------------------

# ग्रहों का नाम निकालने का फंक्शन
def get_g_n(n):
    return grah_data.get(int(n), {}).get('grah', 'अंक')

n_g = get_g_n(name_num)
m_g = get_g_n(mulank)
b_g = get_g_n(bhagyank)

# नामांक का मूलांक और भाग्यांक से संबंध तय करना (मित्र/सम/शत्रु)
f_list = friendship_logic.get(int(name_num), {}).get('friends', [])
e_list = friendship_logic.get(int(name_num), {}).get('enemies', [])

if int(mulank) in f_list:
    mulank_rel = "मित्रता"
elif int(mulank) in e_list:
    mulank_rel = "शत्रुता"
else:
    mulank_rel = "समता"

if int(bhagyank) in f_list:
    bhagyank_rel = "मित्रता"
elif int(bhagyank) in e_list:
    bhagyank_rel = "शत्रुता"
else:
    bhagyank_rel = "समता"

# आपकी डायरी की हस्तलिखित स्क्रिप्ट का ऑडियो एवं टेक्स्ट
script_audio_text = (
    f"जय श्री राम {u_name} जी! "
    f"आपका नामांक {name_num} है जो {n_g} का अंक है। "
    f"मूलांक तथा भाग्यांक जन्म से ही होता है, इसमें कोई भी बदलाव नहीं किया जा सकता। "
    f"परंतु हम अपने नाम में बदलाव कर सकते हैं। "
    f"जीवन में उन्नति के लिए नामांक, मूलांक तथा भाग्यांक का मित्र होना अनिवार्य है। "
    f"आपका नामांक {name_num} ({n_g}) है जो मूलांक से {mulank_rel} तथा भाग्यांक से {bhagyank_rel} का संबंध रखता है। "
    f"सूक्ष्म गणना हेतु विशाल विक्रम पांडे जी से संपर्क करें।"
)

# 1. मुख्य शीर्षक
st.markdown("<h2 style='color: #1E88E5; font-size: 26px; margin-bottom: 0px;'>🔤 नामांक एवं नाम भाग्य फलादेश</h2>", unsafe_allow_html=True)
st.subheader(f"जय श्री राम **{u_name}** जी!")

# 2. गुरु का वैज्ञानिक परामर्श (सबसे ऊपर ऑडियो प्लेयर)
st.subheader("💡 पूरा विवरण सुनाने के लिए play बटन दबाये")

# यहाँ प्लेयर के लिए खाली जगह आरक्षित करें
audio_box = st.empty() 

st.markdown("<p style='text-align: center; color: gray;'>© आचार्य विशाल विक्रम पांडे</p>", unsafe_allow_html=True)
st.write("---")

# 1 से 9 नामांक (ग्रह एवं विशेषताएँ) की डिक्शनरी
namank_dict = {
    1: {"grah": "सूर्य", "features": "नेतृत्व क्षमता, आत्मविश्वासी, स्वतंत्र सोच, साहसी और समाज में मान-प्रतिष्ठा पाने वाला व्यक्तित्व।"},
    2: {"grah": "चंद्रमा", "features": "भावुक, कल्पनाशील, शांतिप्रिय, कलात्मक स्वभाव और दूसरों की सहायता करने की प्रवृत्ति।"},
    3: {"grah": "गुरु (बृहस्पति)", "features": "ज्ञानवान, आध्यात्मिक, मार्गदर्शक, सकारात्मक सोच और रचनात्मक कार्यों में निपुण।"},
    4: {"grah": "राहु", "features": "व्यवहारिक, लीक से हटकर सोचने वाले, अनुशासित, मेहनती और रणनीतिक सोच रखने वाले।"},
    5: {"grah": "बुध", "features": "बुद्धिमान, कुशल वक्ता, व्यापारिक बुद्धि, चंचल और तुरंत सटीक निर्णय लेने की क्षमता।"},
    6: {"grah": "शुक्र", "features": "सौंदर्यप्रेमी, आकर्षक व्यक्तित्व, कला एवं लग्जरी के प्रति झुकाव और मधुर वाणी।"},
    7: {"grah": "केतु", "features": "गंभीर सोच, शोधकर्ता (Research-oriented), आध्यात्मिक दृष्टि और रहस्यमयी विषयों के जानकार।"},
    8: {"grah": "शनि", "features": "कर्मठ, न्यायप्रिय, संघर्षशील, धैर्यवान और दीर्घकालिक सफलता पाने वाले।"},
    9: {"grah": "मंगल", "features": "ऊर्जावान, साहसी, निडर, रक्षक प्रवृत्ति और किसी भी चुनौती का सामना करने वाले।"}
}

# ==========================================
    # १. नामांक एवं मूलांक विवरण (UI Layout)
    # ==========================================
# वर्तमान नामांक के अनुसार डेटा निकालना
current_namank = int(name_num) if str(name_num).isdigit() else 3
info = namank_dict.get(current_namank, {"grah": "", "features": "विशेषताएँ उपलब्ध नहीं हैं।"})

# दोनों कार्ड्स को प्रदर्शित करना
col_card1, col_card2 = st.columns([1, 1.5])

with col_card1:
    st.markdown(f"""
    <div style="background-color: #e8f4f8; padding: 15px; border-radius: 10px; text-align: center; border-left: 5px solid #1E90FF;">
        <h4 style="margin: 0; color: #1E90FF;">📱 आपका नामांक: {current_namank}</h4>
        <p style="margin: 5px 0 0 0; color: #555; font-weight: bold;">ग्रह: {info['grah']}</p>
    </div>
    """, unsafe_allow_html=True)

with col_card2:
    st.markdown(f"""
    <div style="background-color: #f0fdf4; padding: 15px; border-radius: 10px; border-left: 5px solid #2ECC71;">
        <h4 style="margin: 0 0 8px 0; color: #2ECC71;">⭐ नामांक {current_namank} ({info['grah']}) की विशेषताएँ</h4>
        <p style="margin: 0; color: #333; font-size: 14px; line-height: 1.5;">{info['features']}</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown("#### ⚖️ नामांक का मूलांक तथा भाग्यांक से संबंध")
st.warning("📌 **नोट:** मूलांक तथा भाग्यांक जन्म से ही होता है, इसमें कोई भी बदलाव नहीं किया जा सकता। परंतु हम अपने नाम में बदलाव कर सकते हैं।")
st.info("👉 **जीवन में उन्नति के लिए नामांक, मूलांक तथा भाग्यांक का मित्र होना आवश्यक/अनिवार्य है।**")

# 4. फोटो 1 वाला सबसे नीचे का ब्रैकेट (Bold & Highlighting Box)
st.markdown(
    f"""<div style="background-color: #fff3cd; border: 2px solid #ffe8a1; border-radius: 10px; padding: 15px; margin-top: 15px; margin-bottom: 20px; box-shadow: 2px 2px 6px rgba(0,0,0,0.08);">
<h3 style="color: #556404; margin: 0; text-align: center; font-weight: bold; font-size: 19px;">
आपका नामांक {name_num} ({n_g}) है, जो मूलांक {mulank} ({m_g}) से ({mulank_rel}) तथा भाग्यांक {bhagyank} ({b_g}) से ({bhagyank_rel}) का सम्बन्ध रखता है।
</h3>
</div>""",
    unsafe_allow_html=True,
)


            
# name_sum ko define karna taaki peeli line hat jaye
if 'name_sum' not in locals() and 'name_sum' not in globals():
    name_sum = name_num 

# 1. Sanyukt Namank ka Phal (Compound Number Logic)
if name_sum > 1:
    st.markdown("<p style='font-size: 22px; font-weight: bold; color: #1F618D;'>🔮नामांक के संयुक्त अंको का फलादेश</p>", unsafe_allow_html=True)
    
    # app.py के session_state से 2-डिजिट वाला असली कुल योग उठाना
    c_num = st.session_state.get('app_name_val', 0)
    
    # Safe Integer Conversion
    try:
        c_num = int(c_num)
    
    except:
        c_num = 0

    # ---------------------------------------------------------
    # 1. संयुक्त अंक ब्रेकडाउन एवं फलादेश
    # ---------------------------------------------------------
    c_str = str(c_num)

    # compound_fal को बाहर ही एक बार सही से निकाल लें
    compound_fal = compound_master_81.get(c_num) or compound_master_81.get(str(c_num), "")

    if len(c_str) >= 2:
        d1 = int(c_str[0])
        d2 = int(c_str[1])
        g1 = grah_data.get(d1, {}).get('grah', '')
        g2 = grah_data.get(d2, {}).get('grah', '')
        st.info(f"💡 **आपका संयुक्त अंक {c_num} है:** {d1} ({g1}) और {d2} ({g2})। {compound_fal}")
    else:
        st.info(f"💡 **आपका संयुक्त अंक {c_num} है:** {compound_fal}")

    st.divider()

    tab2_audio = ""

    m_en = friendship_logic.get(int(mulank), {}).get('enemies', [])
    b_en = friendship_logic.get(int(bhagyank), {}).get('enemies', [])

# ---------------------------------------------------------
# मोबाइल-फ्रेंडली साइड-बाई-साइड लो-शू ग्रिड एवं बेसिक विवरण
# ---------------------------------------------------------

# 1. ऐप (app.py) के अनुसार सटीक रंग कोड
c_mulank = "#E74C3C"   # लाल (Red) - मूलांक
c_bhagya = "#1E90FF"   # नीला (Blue) - भाग्यांक
c_namaank = "#2ECC71"  # हरा (Green) - नामांक
c_kua = "#8E44AD"      # बैंगनी (Purple) - कुआं नंबर

# 2. आवश्यक मान (Values) प्राप्त करना
kua_val = locals().get('kua_num') or globals().get('kua_num') or st.session_state.get('kua_num') or st.session_state.get('app_kua') or ''
dob_val = st.session_state.get('dob') or st.session_state.get('u_dob') or locals().get('dob') or ''

# 3. DOB के सभी अंक निकालना
dob_digits = []
if dob_val:
    if hasattr(dob_val, 'strftime'):
        dob_str = dob_val.strftime("%Y%m%d")
    else:
        dob_str = str(dob_val)
    dob_digits = [int(c) for c in dob_str if c.isdigit()]

# 4. लो-शू ग्रिड मैपिंग (3x3 पोजीशन)
grid_pos = {4:(0,0), 9:(0,1), 2:(0,2), 3:(1,0), 5:(1,1), 7:(1,2), 8:(2,0), 1:(2,1), 6:(2,2)}
display_grid = [[[] for _ in range(3)] for _ in range(3)]

# DOB के अंकों को काले (Black) रंग में जोड़ना
for n in dob_digits:
    if n in grid_pos:
        r, c = grid_pos[n]
        display_grid[r][c].append(f"<span style='color:black;'>{n}</span>")

# विशेष अंकों को उनके सही रंगों में जोड़ना
special_nums = [
    (int(mulank) if str(mulank).isdigit() else None, c_mulank),
    (int(bhagyank) if str(bhagyank).isdigit() else None, c_bhagya),
    (int(name_num) if str(name_num).isdigit() else None, c_namaank),
    (int(kua_val) if str(kua_val).isdigit() else None, c_kua)
]

for num, color in special_nums:
    if num is not None and num in grid_pos:
        r, c = grid_pos[num]
        display_grid[r][c].append(f"<span style='color:{color}; font-weight:bold;'>{num}</span>")

# ग्रिड की HTML टेबल तैयार करना
grid_rows_html = ""
for row in display_grid:
    grid_rows_html += "<tr style='height:36px;'>"
    for cell_list in row:
        content = " ".join(cell_list) if cell_list else "&nbsp;"
        grid_rows_html += f"<td style='border:1px solid #b0b0b0; width:33%; height:36px; text-align:center; font-size:13px;'>{content}</td>"
    grid_rows_html += "</tr>"

# 5. फ्लेक्स-बॉक्स HTML (app.py के समान डिज़ाइन और रंग)
grid_card_html = f"""<div style="display: flex; flex-direction: row; align-items: center; justify-content: space-between; background-color: #fafafa; padding: 10px; border-radius: 8px;">
<div style="flex: 1; border-right: 1px solid #e0e0e0; padding-right: 8px; font-size: 13px; font-weight: bold;">
<div style="color: {c_mulank}; margin-bottom: 4px;">मूलांक: {mulank}</div>
<div style="color: {c_bhagya}; margin-bottom: 4px;">भाग्यांक: {bhagyank}</div>
<div style="color: {c_namaank}; margin-bottom: 4px;">नामांक: {name_num}</div>
<div style="color: {c_kua};">कुआं नंबर: {kua_val if kua_val != '' else kua_num}</div>
</div>
<div style="flex: 1.2; text-align: center; padding-left: 8px;">
<div style="font-size: 13px; font-weight: bold; margin-bottom: 4px; color: #333;">🗓️ लो-शू ग्रिड</div>
<table style="width: 100%; border-collapse: collapse; font-size: 12px; font-weight: bold;">
{grid_rows_html}
</table>
</div>
</div>"""
st.markdown(grid_card_html, unsafe_allow_html=True)

    # 3. Rajyog Logic (Mangal 9 ko prathmikta)
st.subheader("💡 गुरु का विशेष राजयोग सुझाव")

# यहाँ हम यूज़र के सभी मुख्य अंकों को मिला रहे हैं
शुद्ध_अंक_स्ट्रिंग = str(mulank) + str(bhagyank) + str(name_num)

# १. कुआ नंबर की जांच (session_state तथा स्थानीय वेरिएबल दोनों में)
if 'kua_num' in st.session_state and st.session_state['kua_num']:
    शुद्ध_अंक_स्ट्रिंग += str(st.session_state['kua_num'])
elif 'kua_num' in locals() or 'kua_num' in globals():
    शुद्ध_अंक_स्ट्रिंग += str(kua_num)

# २. जन्मतिथि के अंकों (dob_digits) की जांच
if 'dob_digits' in st.session_state and st.session_state['dob_digits']:
    शुद्ध_अंक_स्ट्रिंग += str(st.session_state['dob_digits'])
elif 'dob_digits' in locals() or 'dob_digits' in globals():
    शुद्ध_अंक_स्ट्रिंग += str(dob_digits)

    # यूज़र के पास जितने भी असली अंक मौजूद हैं, उनकी एक शुद्ध लिस्ट
    मौजूद_अंक_लिस्ट = [int(char) for char in शुद्ध_अंक_स्ट्रिंग if char.isdigit()]
    priorities = [
    {'t': 4, 'others': [5, 6], 'name': "गोल्डन राजयोग (4-5-6)"},
    {'t': 5, 'others': [4, 6], 'name': "गोल्डन राजयोग (4-5-6)"},
    {'t': 6, 'others': [4, 6], 'name': "गोल्डन राजयोग (4-5-6)"},
    {'t': 2, 'others': [5, 8], 'name': "रजत राजयोग (2-5-8)"},
    {'t': 5, 'others': [2, 8], 'name': "रजत राजयोग (2-5-8)"},
    {'t': 8, 'others': [2, 5], 'name': "रजत राजयोग (2-5-8)"},
    {'t': 4, 'others': [3, 8], 'name': "विचार शक्ति राजयोग (4-3-8)"},
    {'t': 3, 'others': [4, 8], 'name': "विचार शक्ति राजयोग (4-3-8)"},
    {'t': 8, 'others': [4, 3], 'name': "विचार शक्ति राजयोग (4-3-8)"},
    {'t': 9, 'others': [5, 1], 'name': "सफलता राजयोग (9-5-1)"},
    {'t': 5, 'others': [9, 1], 'name': "सफलता राजयोग (9-5-1)"},
    {'t': 1, 'others': [9, 5], 'name': "सफलता राजयोग (9-5-1)"},
    {'t': 4, 'others': [9, 2], 'name': "मानसिक शक्ति राजयोग (4-9-2)"},
    {'t': 9, 'others': [4, 2], 'name': "मानसिक शक्ति राजयोग (4-9-2)"},
    {'t': 2, 'others': [4, 9], 'name': "मानसिक शक्ति राजयोग (4-9-2)"},
    {'t': 3, 'others': [5, 7], 'name': " इच्छा शक्ति राजयोग (3-5-7)"},
    {'t': 5, 'others': [3, 7], 'name': " इच्छा शक्ति राजयोग (3-5-7)"},
    {'t': 7, 'others': [5, 3], 'name': " इच्छा शक्ति राजयोग (3-5-7)"},
    {'t': 8, 'others': [1, 6], 'name': "  कर्म शक्ति राजयोग (8-1-6)"},
    {'t': 1, 'others': [8, 6], 'name': "  कर्म शक्ति राजयोग (8-1-6)"},
    {'t': 6, 'others': [1, 8], 'name': "  कर्म शक्ति राजयोग (8-1-6)"},
    {'t': 2, 'others': [7, 6], 'name': "  संतान और संपन्नता (2-7-6)"},
    {'t': 7, 'others': [2, 6], 'name': "  संतान और संपन्नता (2-7-6)"},
    {'t': 6, 'others': [7, 2], 'name': "  संतान और संपन्नता (2-7-6)"},
    {'t': 3, 'others': [5, 7], 'name': "  इच्छा शक्ति राजयोग (3-5-7)"},
    {'t': 5, 'others': [3, 7], 'name': "  इच्छा शक्ति राजयोग (3-5-7)"},
    {'t': 7, 'others': [5, 3], 'name': "  इच्छा शक्ति राजयोग (3-5-7)"},
    ]
    राजयोग_मिला = False

    for p in priorities:
        target = p['t']
        
        # शर्त १: जो अंक चाहिए (target) वह यूज़र के पास मौजूद नहीं होना चाहिए
        # शर्त २: राजयोग को पूरा करने वाले बाकी दोनों अंक यूज़र के पास सच में मौजूद होने चाहिए
        if (target not in मौजूद_अंक_लिस्ट) and all(x in मौजूद_अंक_लिस्ट for x in p['others']):

            # मूलांक और भाग्यांक के शत्रु (Enemy) अंकों की डिक्शनरी
            shatru_dict = {
                1: [8],
                2: [8, 4, 9],
                3: [6],
                4: [1, 2, 8, 9],
                5: [],
                6: [3],
                7: [],
                8: [1, 2, 4, 8, 9],
                9: [2, 4, 8]
            }

            # m_en (मूलांक शत्रु) और b_en (भाग्यांक शत्रु) सुरक्षात्मक तरीके से निकालना
            m_val = int(mulank) if str(mulank).isdigit() else 1
            b_val = int(bhagyank) if str(bhagyank).isdigit() else 1

            m_en = shatru_dict.get(m_val, [])
            b_en = shatru_dict.get(b_val, [])
            tab2_audio = ""
            # शत्रु अंकों की जांच (मूलांक और भाग्यांक से)
            if target not in m_en and target not in b_en:
                t_grah = get_g_n(target)
                msg = f"{p['name']} पूरा करने हेतु {target} ({t_grah}) अपनाएं, यह आपके मूलांक {mulank} और भाग्यांक {bhagyank} का मित्र है।"
                st.success(f"🌟 {msg}")
                tab2_audio += f"Sujhav hai ki {msg} "
                राजयोग_मिला = True
                break  # एक मुख्य राजयोग का सुझाव मिलने पर लूप रोकें
            else:
                # अगर वह अंक शत्रु है, तो चेतावनी दें और दूसरा राजयोग चेक करें
                shatru_of = "मूलांक" if target in m_en else "भाग्यांक"
                t_grah = get_g_n(target)
                msg = f"अंक {target} ({t_grah}) से आपका {p['name']} बन सकता है, पर यह आपके {shatru_of} का शत्रु है, अतः इसे न अपनाएं।"
                st.warning(f"⚠️ {msg}")
                tab2_audio += f"Chetavni! {msg} "
                # यहाँ break नहीं करेंगे ताकि सिस्टम लिस्ट में अगला सुरक्षित राजयोग ढूंढ सके

    if not राजयोग_मिला:
        st.info("ℹ️ वर्तमान में आपके लिए कोई नया विशेष राजयोग सुझाव उपलब्ध नहीं है।")
            # यूज़र के पास जितने भी असली अंक मौजूद हैं, उनकी एक शुद्ध लिस्ट
        मौजूद_अंक_लिस्ट = [int(char) for char in शुद्ध_अंक_स्ट्रिंग if char.isdigit()]

        st.write("---")

            # ==========================================
    # 🆕 संशोधित लॉजिक: ग्रिड के कंबाइंड टेक्स्ट में से अंकों की सही गिनती
    # ==========================================

    # वर्तमान नामांक के अनुसार डेटा निकालना
    current_namank = int(name_num) if str(name_num).isdigit() else 3
    info = namank_dict.get(current_namank, {"grah": "", "features": "विशेषताएँ उपलब्ध नहीं हैं।"})


    # ==========================================
    # २. नामांक और मूलांक का संबंध (Compatibility)
    # ==========================================
    st.markdown("### ⚖️ नामांक और मूलांक का संबंध (Compatibility)")

    if name_num == mulank:
        st.success("✨ **अद्भुत तालमेल:** आपका नामांक और मूलांक एक ही है!")
    else:
        st.info("💡 **संतुलन:** आपका नामांक और मूलांक मिलकर आपके व्यक्तित्व को संतुलित करते हैं।")

    # =========================================================
    # ३. डायनेमिक ऑडियो स्क्रिप्ट तैयार करना
    # =========================================================
    grah_name = grah_data.get(name_num, {}).get('grah', '')
    namank_features = namank_dict.get(name_num, {}).get('features', '')

    script_audio_text = f"जय श्री राम {u_name} जी। "
    script_audio_text += f"आपका नामांक {name_num} है, जिसका ग्रह {grah_name} है। "
    script_audio_text += f"नामांक {name_num} ({grah_name}) की विशेषताएँ: {namank_features}। "
    script_audio_text += "मूलांक तथा भाग्यांक जन्म से ही होता है, इसमें कोई भी बदलाव नहीं किया जा सकता, परंतु हम अपने नाम में बदलाव कर सकते हैं। "
    script_audio_text += "जीवन में उन्नति के लिए नामांक, मूलांक तथा भाग्यांक का मित्र होना आवश्यक और अनिवार्य है। "
    script_audio_text += f"आपका नामांक {name_num} ({grah_name}) है, जो मूलांक {mulank} से ({mulank_rel}) तथा भाग्यांक {bhagyank} से ({bhagyank_rel}) का सम्बन्ध रखता है। "

    # संयुक्त अंक फलादेश (सुरक्षित तरीका)
safe_c_num = locals().get('c_num', name_num)
safe_compound_fal = locals().get('compound_fal', '')

if safe_compound_fal:
    script_audio_text += f"नामांक के संयुक्त अंकों का फलादेश: आपका संयुक्त अंक {safe_c_num} है। {safe_compound_fal} "

    # राजयोग का संदेश
    if 'msg' in locals() and msg:
        clean_msg = msg.replace('-', ', ')
        script_audio_text += f"गुरु का विशेष राजयोग सुझाव: {clean_msg}। "

    # नामांक-मूलांक संतुलन का संदेश
    if name_num == mulank:
        script_audio_text += "अद्भुत तालमेल: आपका नामांक और मूलांक एक ही है। "
    else:
        script_audio_text += "संतुलन: आपका नामांक और मूलांक मिलकर आपके व्यक्तित्व को संतुलित करते हैं। "

    # नई परामर्श लाइन (ऑडियो के लिए)
    script_audio_text += "अपने नाम में सुधार कराने हेतु एवं अन्य जानकारी हेतु आप आचार्य विशाल विक्रम पांडे से नीचे दिए गए बटन पर क्लिक करके बात कर सकते हैं बिल्कुल मुफ्त।"

    # ऊपर आरक्षित प्लेसहॉल्डर में ऑडियो भेजना
    bol_web(script_audio_text, "tab2_voice", container=audio_box)

    # =========================================================
    # ४. मुफ़्त परामर्श कॉलिंग बटन (UI के लिए)
    # =========================================================
    st.write("---")
    st.markdown("""
    <div style="text-align: center; margin-top: 15px; margin-bottom: 20px;">
        <a href="tel:+916392311093" style="
            background-color: #28a745; 
            color: white; 
            padding: 14px 28px; 
            text-decoration: none; 
            font-weight: bold; 
            border-radius: 30px; 
            font-size: 18px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
            display: inline-block;">
            📞 आचार्य विशाल विक्रम पांडे जी से मुफ़्त बात करें
        </a>
    </div>
    """, unsafe_allow_html=True)
        
    bol_web(script_audio_text, "tab2_voice", container=audio_box)
    # ==========================================
    # ४. मुख्य पृष्ठ पर लौटने का बटन
    # ==========================================
    if st.button("⬅️ मुख्य पृष्ठ पर वापस जाएँ", use_container_width=True):
        st.switch_page("app.py")
        