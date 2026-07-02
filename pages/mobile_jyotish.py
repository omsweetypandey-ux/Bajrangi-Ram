import streamlit as st
import os
from gtts import gTTS
import uuid
from io import BytesIO
# =====================================================================
# १. पेज की प्राथमिक सेटिंग और हेडर
# =====================================================================
# =====================================================================
# 🔐 मूलांक और भाग्यांक को सुरक्षित रूप से सेशन से निकालना
# =====================================================================
user_mulank = st.session_state.get('app_mulank', 2)     # यदि न मिले तो डिफ़ॉल्ट २ लेगा
user_bhagyank = st.session_state.get('app_bhagyank', 9) # यदि न मिले तो डिफ़ॉल्ट ९ लेगा
# =====================================================================
st.markdown("# 📱 मोबाइल नंबर ज्योतिष विश्लेषण")
st.markdown("अपने मोबाइल नंबर के भाग्य और अनुकूलता की गहरी जांच करें।")
st.markdown("---")

# अंकों से ग्रहों के नाम की डिक्शनरी
graha_dict = {
    1: "सूर्य (Sun)", 2: "चंद्रमा (Moon)", 3: "बृहस्पति/गुरु (Jupiter)",
    4: "राहु (Rahu)", 5: "बुध (Mercury)", 6: "शुक्र (Venus)",
    7: "केतु (Ketu)", 8: "शनि (Saturn)", 9: "मंगल (Mars)"
}

# शत्रु ग्रहों की सूची (मूलांक के आधार पर)
anti_numbers_dict = {
    1: [8], 2: [4, 8, 9], 3: [6], 4: [1, 2, 9], 
    5: [], 6: [1, 2, 3], 7: [2], 8: [1, 2, 4, 9], 9: [4, 6]
}

# ✨ गुरु जी, आपकी नई युति फलादेश डिक्शनरी बिल्कुल सही जगह पर सेट है:
pairs_dict = {
    "28": {
        "title": "🪐 चंद्रमा + शनि (विष योग दोष)",
        "desc": "आपके मोबाइल में २ और ८ की युति लगातार है। २ नंबर चंद्रमा (मन) का है और ८ नंबर शनि देव (संघर्ष) का है। यह दोनों मिलकर **'विष योग'** बनाते हैं, जिसके कारण व्यक्ति को मानसिक तनाव, ओवरथिंकिंग, अनिद्रा (Insomnia) और कार्यों में अकारण देरी का सामना करना पड़ सकता है।"
    },
    "82": {
        "title": "🪐 शनि + चंद्रमा (विष योग दोष)",
        "desc": "आपके मोबाइल में ८ और २ की युति लगातार है। ८ नंबर शनि देव का है और २ नंबर चंद्रमा का है। यह युति **'विष योग'** का निर्माण करती है, जो मानसिक अशांति, मूड स्विंग्स और बनते हुए कार्यों में ऐन वक्त पर रुकावटें पैदा करती है।"
    },
    "18": {
        "title": "🪐 सूर्य + शनि (वैचारिक मतभेद योग)",
        "desc": "आपके मोबाइल में १ और ८ की युति है। १ नंबर सूर्य (पिता/सफलता) का है और ८ नंबर शनि (पुत्र/अवरोध) का है। इन दोनों में शत्रुता होने के कारण यह युति करियर में सरकारी बाधाएं, अधिकारियों से अनबन या पिता के साथ वैचारिक मतभेद पैदा कर सकती है।"
    },
    "81": {
        "title": "🪐 शनि + सूर्य (संघर्ष योग)",
        "desc": "आपके मोबाइल में ८ और १ की युति है। शनि और सूर्य की यह स्थिति जीवन में मान-सम्मान के लिए अत्यधिक संघर्ष कराती है। कार्यक्षेत्र में मेहनत का पूरा क्रेडिट मिलने में रुकावट आती है।"
    },
    "49": {
        "title": "🪐 राहु + मंगल (अंगारक/विवाद योग)",
        "desc": "आपके मोबाइल में ४ और ९ की युति है। ४ नंबर राहु (भ्रम/अचानक घटना) का है और ९ नंबर मंगल (अग्नि/क्रोध) का है। यह युति **'अंगारक योग'** जैसा प्रभाव देती है, जिससे व्यक्ति में अचानक अत्यधिक क्रोध आना, जल्दबाजी में गलत फैसले लेना या कानूनी विवादों में फंसने की आशंका रहती है।"
    },
    "94": {
        "title": "🪐 मंगल + राहु (दुर्घटना/आवेग योग)",
        "desc": "आपके मोबाइल में ९ और ४ की युति है। मंगल और राहु का यह मेल स्वभाव में उग्रता देता है। वाहन चलाते समय या बड़े आर्थिक निवेश करते समय विशेष सावधानी रखनी चाहिए, क्योंकि यह अचानक चोट या नुकसान का योग बनाता है।"
    },
    "36": {
        "title": "🪐 बृहस्पति + शुक्र (वैचारिक द्वंद्व योग)",
        "desc": "आपके मोबाइल में ३ और ६ की युति है। ३ नंबर देवगुरु बृहस्पति का है और ६ नंबर दैत्यगुरु शुक्र का है। दोनों ही अत्यंत शुभ ग्रह हैं, परंतु विरोधी विचारधारा के होने के कारण यह युति व्यक्ति के वैवाहिक जीवन में मीठी अनबन, खर्चों की अधिकता या सही निर्णय लेने में भ्रम पैदा करती है।"
    },
    "63": {
        "title": "🪐 शुक्र + बृहस्पति (ज्ञान बनाम विलासिता)",
        "desc": "आपके मोबाइल में ६ और ३ की युति है। यह स्थिति ज्ञान और भौतिक सुखों के बीच संतुलन बनाने में संघर्ष देती है। व्यक्ति बहुत ज्ञानी होता है, लेकिन धन के संचय (Savings) में रुकावटें आती हैं।"
    },
    "45": {
        "title": "🪐 राहु + बुध (चतुर व्यापारिक योग - शुभ)",
        "desc": "आपके मोबाइल में ४ और ५ की युति है। ४ नंबर राहु (आउट ऑफ बॉक्स सोच) और ५ नंबर बुध (व्यापार/बुद्धि) का है। यह बहुत ही चतुर और तेज दिमाग देता है। ऐसा व्यक्ति व्यापार, शेयर मार्केट या कूटनीति में बहुत जल्दी तरक्की करता है।"
    },
    "56": {
        "title": "🪐 बुध + शुक्र (लक्ष्मी नारायण योग - शुभ)",
        "desc": "आपके मोबाइल में ५ और ६ की युति है। ५ नंबर बुध (बुद्धि) का है और ६ नंबर शुक्र (लक्जरी/धन) का है। यह एक अत्यंत **शुभ लक्ष्मी नारायण योग** बनाता है, जो व्यक्ति को समाज में आकर्षण, वैभव, मीडिया-ग्लेमर में सफलता और प्रचुर धन-संपत्ति दिलाता है।"
    }
}

# =====================================================================
# २. संबंध विश्लेषक फंक्शन (Unified Administrative Logic)
# =====================================================================
def analyze_planet_relation(single_digit, m_ank, b_ank, title_context):
    friendship_matrix = {
        1: {"friends": [1, 2, 3, 5, 9], "enemies": [6, 8], "neutral": [4, 7]},
        2: {"friends": [1, 2, 3, 5], "enemies": [4, 7, 8], "neutral": [6, 9]},
        3: {"friends": [1, 2, 3, 5, 7, 9], "enemies": [6], "neutral": [4, 8]},
        4: {"friends": [5, 6, 7, 8], "enemies": [1, 2, 9], "neutral": [3, 4]},
        5: {"friends": [1, 2, 3, 5, 6, 7, 8], "enemies": [], "neutral": [4, 9]},
        6: {"friends": [5, 6, 7, 8], "enemies": [1, 2, 3], "neutral": [4, 9]},
        7: {"friends": [1, 3, 4, 5, 6, 8, 9], "enemies": [2], "neutral": [7]},
        8: {"friends": [4, 5, 6, 7], "enemies": [1, 2, 9], "neutral": [3, 8]},
        9: {"friends": [1, 2, 3, 5, 7, 9], "enemies": [4, 6], "neutral": [8]}
    }
    
    if m_ank in friendship_matrix.get(single_digit, {}).get("friends", []):
        m_relation = "🔴 **मित्रता का संबंध है (अत्यंत शुभ)!** यह अंक आपके स्वभाव के अनुकूल है।"
    elif m_ank in friendship_matrix.get(single_digit, {}).get("enemies", []):
        m_relation = "❌ **शत्रुता का संबंध है (अशुभात्मक)!** यह अंक आपके मूलांक के अनुकूल नहीं है।"
    else:
        m_relation = "🟡 **सम (Neutral) संबंध है।** यह अंक आपके मूलांक के प्रति सामान्य है।"

    if b_ank in friendship_matrix.get(single_digit, {}).get("friends", []):
        b_relation = "🔴 **मित्रता का संबंध है (परम भाग्यशाली)!** यह अंक आपके भाग्य को बल देगा।"
    elif b_ank in friendship_matrix.get(single_digit, {}).get("enemies", []):
        b_relation = "❌ **शत्रुता का संबंध है (बाधाकारक)!** यह अंक आपके भाग्य में रुकावट ला सकता है।"
    else:
        b_relation = "🟡 **सम (Neutral) संबंध है।** भाग्य के दृष्टिकोण से यह सामान्य रहेगा।"

    st.markdown(f"#### 📊 {title_context} (एकल अंक: `{single_digit}` - {graha_dict.get(single_digit, 'अज्ञात')})")
    col_m, col_b = st.columns(2)
    with col_m:
        st.info(f"💼 **मूलांक ({m_ank}) के साथ संबंध:**\n\n{m_relation}")
    with col_b:
        st.success(f"🚀 **भाग्यांक ({b_ank}) के साथ संबंध:**\n\n{b_relation}")
    st.markdown("---")

# =====================================================================
# ३. इनपुट फॉर्म और मुख्य गणना
# =====================================================================
cust_mobile = st.text_input("अपना १० अंकों का मोबाइल नंबर दर्ज करें:", key="cust_mobile_input")
mobile_submit = st.button("विवरण देखें 🔍", use_container_width=True)

if mobile_submit:
    # 📱 मोबाइल नंबर के अंकों की लंबाई जांचना
    phone_len = len(cust_mobile)
    
    if phone_len < 10:
        st.error(f"❌ आपके नंबर में केवल {phone_len} अंक हैं। आपकी संख्या 10 से कम है, कृपया अपने नंबर की जांच करें।")
        st.session_state.mobile_analyzed = False
    elif phone_len > 10:
        st.error(f"❌ आपके नंबर में {phone_len} अंक हो गए हैं। आपकी संख्या 10 से अधिक है, कृपया अपने नंबर की जांच करें।")
        st.session_state.mobile_analyzed = False
    elif not cust_mobile.isdigit():
        st.error("❌ कृपया मोबाइल नंबर में केवल अंक (0-9) ही दर्ज करें।")
        st.session_state.mobile_analyzed = False
    else:
        # अगर पूरे 10 अंक हैं, तभी ट्रू होगा और आगे बढ़ेगा
        st.session_state.mobile_analyzed = True

# आगे की मुख्य गणना तभी चलेगी जब नंबर बिल्कुल सही (10 अंकों का) होगा
if st.session_state.get('mobile_analyzed', False):
    if cust_mobile:
        # मुख्य फ़ाइल से मूलांक और भाग्यांक उठाना
        user_mulank = st.session_state.get('app_mulank')
        user_bhagyank = st.session_state.get('app_bhagyank')
        u_name = st.session_state.get('app_user_name', 'user')

        if user_mulank is None or user_bhagyank is None:
            st.error("⚠️ मुख्य पेज से मूलांक और भाग्यांक का डेटा नहीं मिल पाया! कृपया पहले मुख्य पेज पर जन्म विवरण भरकर 'विवरण देखें' पर क्लिक करें।")
        else:
            # A. पूरे १० अंकों का एकल अंक निकालना
            digit_sum = sum(int(d) for d in cust_mobile)
            while digit_sum > 9:
                digit_sum = sum(int(d) for d in str(digit_sum))
            
            # B. आखिरी ४ अंकों का एकल अंक निकालना
            last_4_digits = cust_mobile[-4:]
            last_4_sum = sum(int(d) for d in last_4_digits)
            while last_4_sum > 9:
                last_4_sum = sum(int(d) for d in str(last_4_sum))
            
            # C. एसेंडिंग / डिसेंडिंग चेक करना
            is_ascending = int(last_4_digits[0]) < int(last_4_digits[-1])
            is_descending = int(last_4_digits[0]) > int(last_4_digits[-1])
            
            # स्वामी ग्रहों के नाम निकालना
            mobile_graha = graha_dict.get(digit_sum, "अज्ञात")
            mulank_graha = graha_dict.get(user_mulank, "अज्ञात")
            bhagyank_graha = graha_dict.get(user_bhagyank, "अज्ञात")

            # सुंदर ३ मुख्य डिब्बे (Cards Layout)
            st.markdown("### 🪐 मुख्य अंक एवं संबंधित ग्रहों का विवरण")
            
            card_col1, card_col2, card_col3 = st.columns(3)
            with card_col1:
                st.markdown(
                    f"""
                    <div style="background-color: #e8f4f8; padding: 20px; border-radius: 10px; border-left: 5px solid #2980b9; text-align: center;">
                        <h4 style="color: #2980b9; margin: 0;">📱 मोबाइल कुल योग</h4>
                        <p style="font-size: 32px; font-weight: bold; margin: 10px 0; color: #2c3e50;">{digit_sum}</p>
                        <span style="font-size: 14px; color: #7f8c8d; font-weight: bold;">स्वामी: {mobile_graha}</span>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
            with card_col2:
                st.markdown(
                    f"""
                    <div style="background-color: #eafaf1; padding: 20px; border-radius: 10px; border-left: 5px solid #27ae60; text-align: center;">
                        <h4 style="color: #27ae60; margin: 0;">👤 आपका मूलांक</h4>
                        <p style="font-size: 32px; font-weight: bold; margin: 10px 0; color: #2c3e50;">{user_mulank}</p>
                        <span style="font-size: 14px; color: #7f8c8d; font-weight: bold;">स्वामी: {mulank_graha}</span>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
            with card_col3:
                st.markdown(
                    f"""
                    <div style="background-color: #fef9e7; padding: 20px; border-radius: 10px; border-left: 5px solid #f1c40f; text-align: center;">
                        <h4 style="color: #d4ac0d; margin: 0;">🚀 आपका भाग्यांक</h4>
                        <p style="font-size: 32px; font-weight: bold; margin: 10px 0; color: #2c3e50;">{user_bhagyank}</p>
                        <span style="font-size: 14px; color: #7f8c8d; font-weight: bold;">स्वामी: {bhagyank_graha}</span>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("🎯 संपूर्ण मोबाइल नंबर संबंध विश्लेषण")
            
            # १. दोनों स्तरों का ग्रहों से संबंध दिखाना
            st.markdown("### 📱 १. पूरे १० अंकों के योग का प्रभाव")
            analyze_planet_relation(digit_sum, user_mulank, user_bhagyank, "संपूर्ण मोबाइल नंबर योग")
            
            st.markdown("### 🔮 २. आखिरी ४ अंकों के योग का प्रभाव")
            analyze_planet_relation(last_4_sum, user_mulank, user_bhagyank, "अंतिम ४ अंकों का विशेष योग")
            # ==============================================================================
        # 🪐 ३. मोबाइल नंबर के बीच बनने वाली ग्रहों की युति (Pairs) स्क्रीन पर दिखाना
        # ==============================================================================
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🔮 ३. मोबाइल नंबर में ग्रहों की विशेष युति का प्रभाव")
        
        found_any_pair_screen = False
        
        # सुरक्षा जांच: क्या pairs_dict कोड में उपलब्ध है
        if 'pairs_dict' in locals():
            for i in range(len(cust_mobile) - 1):
                current_pair = cust_mobile[i:i+2]
                
                # अगर वह जोड़ा हमारी डिक्शनरी में मौजूद है
                if current_pair in pairs_dict:
                    found_any_pair_screen = True
                    pair_info = pairs_dict[current_pair]
                    
                    # दोष या संघर्ष वाले योगों के लिए चेतावनी (Warning Box)
                    if "दोष" in pair_info['title'] or "मतभेद" in pair_info['title'] or "संघर्ष" in pair_info['title'] or "विवाद" in pair_info['title'] or "दुर्घटना" in pair_info['title']:
                        st.warning(f"⚠️ **{pair_info['title']} (अंक {current_pair}):** {pair_info['desc']}")
                    else:
                        # शुभ लक्ष्मी नारायण या चतुर व्यापार योग के लिए (Success Box)
                        st.success(f"✨ **{pair_info['title']} (अंक {current_pair}):** {pair_info['desc']}")
                        
            # अगर पूरे नंबर में कोई भी विशिष्ट युति नहीं मिली
            if not found_any_pair_screen:
                st.info("✨ **अद्भुत योग:** आपके मोबाइल नंबर के बीच में कोई भी नकारात्मक या संघर्षकारी ग्रहों की युति नहीं बन रही है, जो कि आपके लिए बहुत ही उत्तम स्थिति है।")
           # ==============================================================================
# 🧮 १. मुख्य गणितीय गणनाएं (Variables Definition)
# ==============================================================================
if cust_mobile and len(cust_mobile) == 10:
    # पूरे १० अंकों का एकल योग (Single Digit Sum) निकालना
    digit_sum = sum(int(d) for d in cust_mobile if d.isdigit())
    while digit_sum > 9:
        digit_sum = sum(int(d) for d in str(digit_sum))
        
    # आखिरी ४ अंकों का एकल योग निकालना
    last_4_digits = cust_mobile[-4:]
    last_4_sum = sum(int(d) for d in last_4_digits if d.isdigit())
    while last_4_sum > 9:
        last_4_sum = sum(int(d) for d in str(last_4_sum))
else:
    digit_sum = 1
    last_4_sum = 1

# ==============================================================================
# 🚦 २. एसेंडिंग / डिसेंडिंग / न्यूट्रल का वास्तविक गणितीय लॉजिक
# ==============================================================================
is_ascending = False
is_descending = False

if cust_mobile and len(cust_mobile) == 10:
    # गणितीय सटीक जांच
    is_ascending = all(last_4_digits[i] <= last_4_digits[i+1] for i in range(3)) and (last_4_digits[0] < last_4_digits[-1])
    is_descending = all(last_4_digits[i] >= last_4_digits[i+1] for i in range(3)) and (last_4_digits[0] > last_4_digits[-1])

    # 🖥️ स्क्रीन पर क्रम का प्रदर्शन (मूलांक/भाग्यांक के डिब्बों के ठीक नीचे)
    if is_ascending:
        st.success("🟢 **शुभ योग:** आपके मोबाइल के आखिरी अंक बढ़ते क्रम (Ascending Order) में हैं, जो जीवन में निरंतर प्रगति और उन्नति को दर्शाते हैं।")
    elif is_descending:
        st.warning("⚠️ **चेतावनी:** आपके मोबाइल के आखिरी अंक घटते क्रम (Descending Order) में हैं, जो जीवन में संघर्ष को बढ़ा सकते हैं।")
    else:
        st.info("🔵 **सामान्य योग:** आपके मोबाइल के आखिरी अंक मिश्रित क्रम (Neutral/Mixed Order) में हैं। यह जीवन में स्थिरता और उतार-चढ़ाव के बीच संतुलन को दर्शाता है, जो कि एक सामान्य स्थिति है।")
else:
    st.info("📱 कृपया ऊपर अपना १० अंकों का वैध मोबाइल नंबर दर्ज करें ताकि फलादेश की गणना की जा सके।")


# 🪐 (नोट: स्क्रीन पर दोबारा दिखाने वाला 'भाग ३' यहाँ से हटा दिया गया है ताकि डबल न दिखे)


# ==============================================================================
# 🎙️ ४. गुरु रोबोट की आवाज का जादू (Complete Master Audio Block)
# ==============================================================================
if cust_mobile and len(cust_mobile) == 10:
    
    # 👤 यूजर का नाम सुरक्षित रूप से निकालना
    user_name_extracted = st.session_state.get('u_name', '')

    if user_name_extracted:
        speech_script = f"जय श्री राम {user_name_extracted} जी! आपके मोबाइल नंबर का ज्योतिष विश्लेषण इस प्रकार है। "
    else:
        speech_script = "जय श्री राम! आपके मोबाइल नंबर का ज्योतिष विश्लेषण इस प्रकार है। "

    try:
        # १. मूलांक और भाग्यांक की जानकारी जोड़ना
        speech_script += f"आपका मूलांक {user_mulank} है और भाग्यांक {user_bhagyank} है। "

        speech_script += f"आपके पूरे मोबाइल नंबर के कुल अंकों का एकल योग {digit_sum} आता है। "
        
        # मूलांक और भाग्यांक के साथ वास्तविक मित्रता/शत्रुता की जांच
        friendship_matrix = st.session_state.get('friendship_matrix', {})
        m_rel_total = friendship_matrix.get(user_mulank, {}).get("friends", [])
        m_shatru_total = friendship_matrix.get(user_mulank, {}).get("enemies", [])
        
        b_rel_total = friendship_matrix.get(user_bhagyank, {}).get("friends", [])
        b_shatru_total = friendship_matrix.get(user_bhagyank, {}).get("enemies", [])

        # मूलांक से संबंध की सटीक आवाज
        if digit_sum in m_rel_total:
            speech_script += f"यह कुल योग आपके मूलांक {user_mulank} का परम मित्र है, "
        elif digit_sum in m_shatru_total:
            speech_script += f"यह कुल योग आपके मूलांक {user_mulank} का शत्रु अंक है, "
        else:
            speech_script += f"यह कुल योग आपके मूलांक {user_mulank} के साथ सम संबंध रखता है, "

        # भाग्यांक से संबंध की सटीक आवाज
        if digit_sum in b_rel_total:
            speech_script += f"और आपके भाग्यांक {user_bhagyank} का भी मित्र अंक है। "
        elif digit_sum in b_shatru_total:
            speech_script += f"और आपके भाग्यांक {user_bhagyank} का शत्रु अंक होने के कारण रुकावट ला सकता है। "
        else:
            speech_script += f"और आपके भाग्यांक {user_bhagyank} के साथ सामान्य संबंध रखता है। "


        # ==============================================================================
        # 🎙️ ३. आखिरी ४ अंकों के विशेष योग का सटीक फलादेश (रिप्लेसमेंट ब्लॉक)
        # ==============================================================================
        speech_script += f"इसके साथ ही, आपके मोबाइल नंबर के आखिरी चार अंकों का विशेष एकल योग {last_4_sum} आता है। "

        # आखिरी ४ अंकों की मूलांक से जांच
        if last_4_sum in m_rel_total:
            speech_script += f"यह विशेष योग आपके मूलांक {user_mulank} का मित्र है, "
        elif last_4_sum in m_shatru_total:
            speech_script += f"यह विशेष योग आपके मूलांक {user_mulank} का शत्रु होने से दैनिक कार्यों में संघर्ष दे सकता है, "
        else:
            speech_script += f"यह विशेष योग आपके मूलांक {user_mulank} के प्रति न्यूट्रल यानी सामान्य है, "

        # आखिरी ४ अंकों की भाग्यांक से जांच
        if last_4_sum in b_rel_total:
            speech_script += f"और आपके भाग्यांक {user_bhagyank} का मित्र होने से भाग्य उन्नति में सहायक सिद्ध होता है। "
        elif last_4_sum in b_shatru_total:
            speech_script += f"और आपके भाग्यांक {user_bhagyank} का शत्रु अंक है। "
        else:
            speech_script += f"और आपके भाग्यांक {user_bhagyank} के साथ सामान्य संबंध दर्शाता है। "
        # ५. ग्रहों की युति (Pairs Analysis) का फलादेश
        found_any_pair_audio = False
        if 'pairs_dict' in locals():
            for i in range(len(cust_mobile) - 1):
                current_pair = cust_mobile[i:i+2]
                if current_pair in pairs_dict:
                    found_any_pair_audio = True
                    pair_info = pairs_dict[current_pair]
                    clean_desc = pair_info['desc'].replace("***", "")
                    speech_script += f" आपके नंबर में {pair_info['title']} बन रहा है। इसका प्रभाव यह है कि {clean_desc} "

        if not found_any_pair_audio:
            speech_script += " अद्भुत! आपके मोबाइल नंबर के बीच में कोई भी नकारात्मक या शत्रु ग्रहों की युति नहीं है, जो कि एक बहुत अच्छी बात है। "

    except Exception as e:
        if user_name_extracted:
            speech_script = f"जय श्री राम {user_name_extracted} जी! आपके मोबाइल नंबर का विश्लेषण तैयार है। कृपया स्क्रीन पर अपनी रिपोर्ट देखें।"
        else:
            speech_script = "जय श्री राम! आपके मोबाइल नंबर का विश्लेषण तैयार है। कृपया स्क्रीन पर अपनी रिपोर्ट देखें।"
    # 🎙️ गुरु रोबोट की अंतिम सलाह (आवाज के लिए)
        speech_script += " सही मोबाइल नंबर की सटीक जानकारी और उचित चुनाव करने के लिए आप ज्योतिषाचार्य विशाल विक्रम पांडे जी से संपर्क कर सकते हैं। धन्यवाद।"
    # ==============================================================================
    # 🎛️ ५. gTTS ऑडियो प्लेयर जनरेशन
    # ==============================================================================
    st.markdown("---")
    st.markdown("### 🎙️ गुरु मुख से फलादेश सुनें")

    with st.spinner("गुरु आपकी रिपोर्ट तैयार कर रही हैं, कृपया क्षण भर प्रतीक्षा करें..."):
        try:
            tts = gTTS(text=speech_script, lang='hi', slow=False)
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            st.audio(fp, format="audio/mp3")
                
        except Exception as e:
            st.error(f"आवाज तैयार करने में कुछ तकनीकी त्रुटि आई है: {e}")