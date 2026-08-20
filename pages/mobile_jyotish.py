import streamlit as st
import json
import os
import re
import asyncio
import edge_tts

# =========================================================
# 1. एडमिन कॉन्फ़िग लोड करना
# =========================================================
CONFIG_FILE = "config.json"

def load_admin_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "rule_friendship": True,
        "rule_ascending": True,
        "rule_anti_digits": True,
        "custom_notice_text": "कृपया अपने मूलांक और भाग्यांक के अनुकूल ही लकी मोबाइल नंबर का चयन करें।",
        "custom_banner_url": ""
    }

config = load_admin_config()

# =========================================================
# 2. Edge-TTS वॉइस फ़ंक्शन
# =========================================================
async def generate_speech(text, output_file="output_mobile.mp3"):
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural") # या आपकी पसंदीदा वॉइस
    await communicate.save(output_file)

def speak_text(text, filename="output_mobile.mp3"):
    asyncio.run(generate_speech(text, filename))
    if os.path.exists(filename):
        st.audio(filename, format="audio/mp3", autoplay=True)

# =========================================================
# 3. पेज कॉन्फ़िगरेशन व स्टाइलिंग
# =========================================================
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; }
    .stAlert { border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

if config.get("custom_banner_url"):
    st.image(config.get("custom_banner_url"), use_column_width=True)

if config.get("custom_notice_text"):
    st.info(f"📌 **विशेष निर्देश:** {config.get('custom_notice_text')}")

st.title("📱 मोबाइल ज्योतिष विश्लेषण एवं लकी नंबर")

# =========================================================
# 4. इनपुट फ़ील्ड व टैब संरचना
# =========================================================
cust_mobile = st.text_input("Enter your 10 digits no", max_chars=10, key="cust_mob_input")

tab1, tab2 = st.tabs(["Check Your No", "My Lucky No"])

# =========================================================
# 5. अंक ज्योतिष डेटाबेस
# =========================================================
FRIENDSHIP_TABLE = {
    1: {"friends": [1, 2, 3, 5, 9], "enemies": [8], "neutral": [4, 6, 7]},
    2: {"friends": [1, 2, 3, 5], "enemies": [4, 8, 9], "neutral": [6, 7]},
    3: {"friends": [1, 2, 3, 5, 9], "enemies": [6], "neutral": [4, 7, 8]},
    4: {"friends": [5, 6, 7, 8], "enemies": [1, 2, 9], "neutral": [3]},
    5: {"friends": [1, 2, 3, 5, 6, 8], "enemies": [], "neutral": [4, 7, 9]},
    6: {"friends": [4, 5, 6, 7, 8], "enemies": [3], "neutral": [1, 2, 9]},
    7: {"friends": [4, 6, 9], "enemies": [1, 2], "neutral": [3, 5, 7, 8]},
    8: {"friends": [4, 5, 6], "enemies": [1, 2, 9], "neutral": [3, 7, 8]},
    9: {"friends": [1, 2, 3, 7], "enemies": [4, 8], "neutral": [5, 6, 9]}
}

def check_friendship_status(user_num, target_num):
    f_info = FRIENDSHIP_TABLE.get(user_num, {})
    friends = f_info.get("friends", [])
    enemies = f_info.get("enemies", [])
    if target_num in friends:
        return "मित्र 🟢"
    elif target_num in enemies:
        return "शत्रु 🔴"
    return "सम 🟠"

PLANET_PAIRS = {
    "11": "सूर्य-सूर्य: अत्यधिक आत्म-विश्वास, नेतृत्व क्षमता में वृद्धि, किंतु अहंकार का खतरा।",
    "12": "सूर्य-चंद्र: राजयोग कारक युति, समाज में मान-सम्मान और प्रशासनिक कार्यों में सफलता।",
    "13": "सूर्य-गुरु: ज्ञान, आध्यात्मिक उन्नति, उच्च पद और प्रतिष्ठा का योग।",
    "14": "सूर्य-राहु: ग्रहण योग, मानसिक भ्रम, पिता से विचार-भेद या अचानक बाधाएं।",
    "15": "सूर्य-बुध: बुधादित्य योग, तीक्ष्ण बुद्धि, वाक्पटुता और व्यापार में भारी लाभ।",
    "16": "सूर्य-शुक्र: कलात्मक रुचि, किंतु सौंदर्य और विलासिता में अधिक व्यय।",
    "17": "सूर्य-केतु: आध्यात्मिक दृष्टि, गूढ़ विद्याओं में रुचि, यदा-कदा अलगाव।",
    "18": "सूर्य-शनि: पिता-पुत्र में वैचारिक दूरी, कार्यों में विलंब व कड़ा संघर्ष।",
    "19": "सूर्य-मंगल: अत्यधिक साहसी स्वभाव, ऊर्जावान, किंतु क्रोध पर नियंत्रण आवश्यक।",
    "22": "चंद्र-चंद्र: अत्यधिक भावुकता, कल्पनाशक्ति, मन की चंचलता और यात्रा योग।",
    "23": "चंद्र-गुरु: गजकेसरी योग का प्रभाव, मानसिक शांति, समृद्धि और सम्मान।",
    "24": "चंद्र-राहु: ग्रहण दोष, अकारण चिंता, तनाव और मानसिक अशंति।",
    "25": "चंद्र-बुध: तीक्ष्ण याददाश्त, व्यापारिक सूझ-बूझ और मिलनसार व्यक्तित्व।",
    "26": "चंद्र-शुक्र: कला, संगीत और सौंदर्य के प्रति विशेष रुझान, सुख-सुविधाएं।",
    "27": "चंद्र-केतु: अति-संवेदनशील मन, अंतर्ज्ञान शक्ति में वृद्धि।",
    "28": "चंद्र-शनि: विष योग प्रभाव, कार्यों में मानसिक दबाव और उतावलापन।",
    "29": "चंद्र-मंगल: महालक्ष्मी योग प्रभाव, साहसी निर्णय और आर्थिक प्रगति।",
    "33": "गुरु-गुरु: अपार ज्ञान, धार्मिकता, शिक्षण व मार्गदर्शन में विशेष सफलता।",
    "34": "गुरु-राहु: गुरु-चांडाल योग प्रभाव, अपरंपरागत विचार, निर्णयों में सतर्कता रखें।",
    "35": "गुरु-बुध: ज्ञान और बुद्धि का उत्तम मेल, शिक्षण, लेखन व कंसल्टेंसी में सफलता।",
    "36": "गुरु-शुक्र: दो महान ग्रहों का योग, ज्ञान और भौतिक सुखों का अनूठा संगम।",
    "37": "गुरु-केतु: परम आध्यात्मिक योग, शोध और अध्यात्म में सफलता।",
    "38": "गुरु-शनि: न्यायप्रियता, गंभीर सोच और दीर्घकालिक सफलता।",
    "39": "गुरु-मंगल: धर्म-ज्ञान और पराक्रम का मेल, साहसी और न्यायप्रिय नेतृत्व।",
    "44": "राहु-राहु: अत्यधिक महत्वाकांक्षा, डिजिटल व अचानक सफलता का योग।",
    "45": "राहु-बुध: अत्यंत चतुर बुद्धि, शेयर मार्केट व तकनीक में त्वरित सफलता।",
    "46": "राहु-शुक्र: आकर्षण, मीडिया, ग्लैमर और भौतिक सुख-सुविधाओं की प्राप्ति।",
    "47": "राहु-केतु: रहस्यमयी सोच, जीवन में अचानक बड़े बदलाव।",
    "48": "राहु-शनि: कड़ा संघर्ष, तकनीकी क्षेत्र में सफलता, कानूनी मामलों में सतर्कता।",
    "49": "राहु-मंगल: अंगारक योग प्रभाव, अत्यधिक आक्रामकता, निर्णयों में जल्दबाजी से बचें।",
    "55": "बुध-बुध: व्यापारिक कुशलता, हिसाब-किताब में निपुणता और उत्तम वाणी।",
    "56": "बुध-शुक्र: लक्ष्मी-नारायण योग, सुंदर अभिव्यक्ति, मीडिया व कला में सफलता।",
    "57": "बुध-केतु: विश्लेषणात्मक बुद्धि, कोडिंग व रिसर्च में सफलता।",
    "58": "बुध-शनि: व्यावहारिक सोच, अनुशासन और सीए/अकाउंट्स में तरक्की।",
    "59": "बुध-मंगल: त्वरित निर्णय क्षमता, तर्क-वितर्क में निपुणता।",
    "66": "शुक्र-शुक्र: लक्जरी जीवन, वाहन, आभूषण और उत्तम जीवनशैली।",
    "67": "शुक्र-केतु: कला में गहराई, किंतु संबंधों में वैराग्य या उदासीनता।",
    "68": "शुक्र-शनि: प्रॉपर्टी व रियल्टी क्षेत्र में लाभ, धीरे-धीरे स्थायी सुख।",
    "69": "शुक्र-मंगल: आकर्षण, अत्यधिक ऊर्जा और रोमांटिक स्वभाव।",
    "77": "केतु-केतु: शोधत्मक सोच, गूढ़ विद्याओं और योग-ध्यान में सफलता।",
    "78": "केतु-शनि: एकांतप्रियता, कड़ा परिश्रम और गूढ़ विषयों में ज्ञान।",
    "79": "केतु-मंगल: साहसी, सर्जिकल या तकनीकी कार्यों में विशेष निपुणता।",
    "88": "शनि-शनि: अत्यधिक अनुशासन, कड़ा संघर्ष और जीवन के उत्तरार्ध में स्थायी सफलता।",
    "89": "शनि-मंगल: लोहा, मशीनरी, कंस्ट्रक्शन में सफलता, दुर्घटनाओं से सावधान।",
    "99": "मंगल-मंगल: अपार साहस, भूमि-भवन लाभ, आक्रामकता पर नियंत्रण आवश्यक।"
}

# =========================================================
# 6. हेल्पिंग फ़ंक्शंस
# =========================================================
def calculate_single_digit(num_str):
    total = sum(int(d) for d in str(num_str) if d.isdigit())
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total

def check_ascending_descending(last_4_str):
    digits = [int(d) for d in last_4_str if d.isdigit()]
    if len(digits) < 4:
        return False, False
    is_asc = all(digits[i] <= digits[i+1] for i in range(len(digits)-1))
    is_desc = all(digits[i] >= digits[i+1] for i in range(len(digits)-1))
    return is_asc, is_desc

# शुद्ध लो-शू ग्रिड: केवल जन्मतिथि, मूलांक, भाग्यांक, नामांक और कुआं नंबर
def render_pure_lo_shu_grid(dob_list, mulank, bhagyank, namank, kua):
    grid_pos = {4:(0,0), 9:(0,1), 2:(0,2), 3:(1,0), 5:(1,1), 7:(1,2), 8:(2,0), 1:(2,1), 6:(2,2)}
    display_grid = [[[] for _ in range(3)] for _ in range(3)]

    # 1. DOB के नंबर (Black)
    for n in dob_list:
        if n in grid_pos:
            r, c = grid_pos[n]
            display_grid[r][c].append(f"<span style='color:black; font-weight:bold;'>{n}</span>")

    # 2. विशेष नंबरों को जोड़ना (Colors)
    special_nums = [
        (mulank, c),
        (bhagyank, "#0055B8"),
        (namank, "#008000"),
        (kua, "#800080")
    ]
    
    for num, color in special_nums:
        if num in grid_pos:
            r, c = grid_pos[num]
            display_grid[r][c].append(f"<span style='color:{color}; font-weight:bold;'>{num}</span>")

    # 3. HTML टेबल बनाना
    grid_rows_html = ""
    for row in display_grid:
        grid_rows_html += "<tr style='height:45px;'>"
        for cell_list in row:
            content = "".join(cell_list) if cell_list else "&nbsp;"
            grid_rows_html += f"<td style='border:1px solid #d3d3d3; font-size:18px; text-align:center;'>{content}</td>"
        grid_rows_html += "</tr>"

    return f"<table style='width:100%; border-collapse:collapse; background-color:#fffdfa;'>{grid_rows_html}</table>"
# =========================================================
# [टैब 1] Check Your No
# =========================================================
with tab1:
       # Session State से मान प्राप्त करना (मुख्य app.py की Keys से 100% सिंक)
    user_m = st.session_state.get("app_mulank", 1)
    user_b = st.session_state.get("app_bhagyank", 1)
    user_n = st.session_state.get("app_namank", 1)
    user_k = st.session_state.get("app_kua", 1)

    dob_digits = st.session_state.get("app_dob_digits", [1, 9, 8, 6, 4, 1, 8])

    # 1. शुद्ध लो-शू ग्रिड डिस्प्ले (केवल मूल अंक)
    c_head1, c_head2 = st.columns([1, 1])
    with c_head1:
        st.markdown(f"""
            <div style="background-color:#fef8f5; padding:15px; border-radius:8px; border-left:4px solid #8B0000;">
                <p style="margin:2px; color:#8B0000; font-weight:bold;">मूलांक: {user_m}</p>
                <p style="margin:2px; color:#0055B8; font-weight:bold;">भाग्यांक: {user_b}</p>
                <p style="margin:2px; color:#008000; font-weight:bold;">नामांक: {user_n}</p>
                <p style="margin:2px; color:#800080; font-weight:bold;">कुआं नंबर: {user_k}</p>
            </div>
        """, unsafe_allow_html=True)

    with c_head2:
        st.markdown("📅 **लो-शू ग्रिड**", unsafe_allow_html=True)
        grid_html = render_pure_lo_shu_grid(dob_digits, user_m, user_b, user_n, user_k)
        st.markdown(grid_html, unsafe_allow_html=True)

    # 2. केवल मिसिंग नंबरों की गणना करना (बिना मोबाइल नंबर को ग्रिड में डाले)
    birth_present = set(dob_digits + [user_m, user_b, user_n, user_k])
    missing_digits = [n for n in range(1, 10) if n not in birth_present]
    st.session_state["missing_numbers"] = missing_digits

    # 225 नंबर लाइन की जगह यह कोड डालें
    missing_str = ', '.join(map(str, missing_digits)) if missing_digits else "कोई नहीं"
    
    st.markdown(f"""
        <div style="background-color: #f8f9fa; border-left: 5px solid #d9534f; padding: 12px 18px; border-radius: 8px; margin-top: 10px; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <p style="font-size: 19px; font-weight: 600; color: #2c3e50; margin: 0;">
                🔍 ग्रिड में अनुपस्थित (मिसिंग) अंक: 
                <span style="font-size: 24px; color: #d9534f; font-weight: bold; margin-left: 5px;">{missing_str}</span>
            </p>
            <p style="font-size: 18px; color: #8B0000; margin-top: 8px; margin-bottom: 0px; font-style: italic;">
                नोट: लो-शू ग्रिड में जो अंकअनुपस्थित हैं, उन्हें मोबाइल नंबर में जोड़ कर ग्रहों को संतुलित किया जा सकता है|
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # 3. मोबाइल नंबर का पृथक विश्लेषण
    if cust_mobile and len(cust_mobile) == 10 and cust_mobile.isdigit():
        st.subheader(f"📱 मोबाइल नंबर: {cust_mobile} का विश्लेषण")

        tot_sum = calculate_single_digit(cust_mobile)
        l4_sum = calculate_single_digit(cust_mobile[-4:])
        is_asc, is_desc = check_ascending_descending(cust_mobile[-4:])

        m_status = check_friendship_status(user_m, tot_sum)
        b_status = check_friendship_status(user_b, tot_sum)

        l4_m_status = check_friendship_status(user_m, l4_sum)
        l4_b_status = check_friendship_status(user_b, l4_sum)

        # देखना कि यह मोबाइल नंबर मिसिंग अंकों को पूरा कर रहा है या नहीं
        mob_digits = set(int(d) for d in cust_mobile if d != '0')
        covered_missing = [d for d in missing_digits if d in mob_digits]

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("10 अंकों का कुल योग (Total Single Digit)", f"{tot_sum}")
            st.write(f"• मूलांक ({user_m}) से संबंध: **{m_status}**")
            st.write(f"• भाग्यांक ({user_b}) से संबंध: **{b_status}**")

        with col_m2:
            st.metric("अंतिम 4 अंकों का योग (Last 4 Digit Sum)", f"{l4_sum}")
            st.write(f"• मूलांक ({user_m}) से संबंध: **{l4_m_status}**")
            st.write(f"• भाग्यांक ({user_b}) से संबंध: **{l4_b_status}**")

        st.info(f"✨ **यह मोबाइल नंबर आपके मिसिंग अंकों की पूर्ति करता है:** {', '.join(map(str, covered_missing)) if covered_missing else 'कोई नहीं'}")

        st.divider()

        st.subheader("📈 अंतिम 4 अंकों का क्रम (Order Analysis)")
        if is_asc:
            st.success("🟢 अंतिम 4 अंक बढ़ते क्रम (Ascending Order) में हैं! यह उन्नति का संकेत है।")
        elif is_desc:
            st.error("🔴 अंतिम 4 अंक घटते क्रम (Descending Order) में हैं! यह संघर्ष का संकेत है।")
        else:
            st.warning("🟠 अंतिम 4 अंक मिश्रित क्रम में हैं। जीवन में उतर चढाव बना रहेगा")

        st.divider()

        st.subheader("🔮 मोबाइल नंबर के दो-अंकों के संयोजन (युति फलादेश)")
        found_pairs = False
        for i in range(len(cust_mobile) - 1):
            pair = cust_mobile[i:i+2]
            if pair in PLANET_PAIRS:
                found_pairs = True
                st.write(f"• **{pair}**: {PLANET_PAIRS[pair]}")
        if not found_pairs:
            st.write("कोई विशेष ग्रहीय युति नहीं पाई गई।")

        # -------------------------------------------------------------
            # वॉयस ऑटो-प्ले एवं कॉल/WhatsApp संपर्क बटन्स
            # -------------------------------------------------------------
            st.divider()

            # 1. सेफ वेरिएबल चेकिंग (येलो लाइन पूरी तरह हटाने के लिए)
        u_missing = locals().get('user_missing_digits', st.session_state.get('missing_numbers', []))
        t_sum = locals().get('total_sum', '')
        l4_sum = locals().get('last_4_sum', '')

        missing_str = ", ".join(map(str, u_missing)) if u_missing else "कोई नहीं"
        covered_str = ", ".join(map(str, covered_missing)) if 'covered_missing' in locals() and covered_missing else "कोई नहीं"

        order_text = "बढ़ते क्रम" if 'is_asc' in locals() and is_asc else ("घटते क्रम" if 'is_desc' in locals() and is_desc else "मिश्रित क्रम")

        # 2. वॉइस स्क्रिप्ट तैयार करना
        analysis_voice_script = f"""
        मोबाइल ज्योतिष विश्लेषण में आपका स्वागत है।
        आपके लो शू ग्रिड में अनुपस्थित यानी मिसिंग अंक हैं: {missing_str}।
        नोट: लो शू ग्रिड में जो अंक अनुपस्थित हैं, उन्हें मोबाइल नंबर में जोड़कर ग्रहों को संतुलित किया जा सकता है।

        आपके मोबाइल नंबर का 10 अंकों का कुल योग {t_sum} है।
        अंतिम 4 अंकों का योग {l4_sum} है।
        यह मोबाइल नंबर आपके मिसिंग अंक {covered_str} की पूर्ति करता है।
        अंतिम 4 अंक {order_text} में हैं।

        मोबाइल नंबर की अधिक जानकारी के लिए आप ऊपर माय लकी नंबर पर क्लिक कर सकते हैं, अन्यथा विशाल विक्रम पांडे जी से कॉल करके बात कर सकते हैं।
        """.strip()

        # 3. वॉइस जनरेट करना और बजना
        try:
            speak_text(analysis_voice_script, "output_mobile.mp3")
        except Exception as e:
            pass

        # 4. कॉल व WhatsApp संपर्क बटन्स
        st.info("💡 **मोबाइल नंबर की अधिक जानकारी के लिए आप ऊपर 'My Lucky No' पर क्लिक कर सकते हैं अन्यथा विशाल विक्रम पांडे से आप कॉल करके बात कर सकते हैं।**")

        phone_number = "919838123456" # यहाँ अपना सही व्हाट्सएप/कॉलिंग नंबर डालें
        whatsapp_msg = "जय श्री राम विशाल जी, मुझे अपने मोबाइल नंबर के ज्योतिष विश्लेषण और लकी नंबर के बारे में जानकारी चाहिए।"

        col_call, col_wa = st.columns(2)
        with col_call:
            st.markdown(f'''
                <a href="tel:+{phone_number}" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #0d6efd; color: white; text-align: center; padding: 12px; border-radius: 8px; font-weight: bold; font-size: 15px;">
                        📞 विशाल जी को कॉल करें
                    </div>
                </a>
            ''', unsafe_allow_html=True)

        with col_wa:
            st.markdown(f'''
                <a href="https://wa.me/{6392311093}?text={whatsapp_msg}" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #25d366; color: white; text-align: center; padding: 12px; border-radius: 8px; font-weight: bold; font-size: 15px;">
                        💬 WhatsApp पर बात करें
                    </div>
                </a>
            ''', unsafe_allow_html=True)

    else:
        st.warning("कृपया ऊपर 10 अंकों का सही मोबाइल नंबर दर्ज करें।")

   
# =========================================================
# [टैब 2] My Lucky No
# =========================================================
with tab2:
    st.header("✨ आपके लिए सबसे सटीक लकी मोबाइल नंबर")

    user_m = st.session_state.get("app_mulank") or st.session_state.get("user_mulank") or 8
    user_b = st.session_state.get("app_bhagyank") or st.session_state.get("user_bhagyank") or 4
    user_missing_digits = st.session_state.get("missing_numbers", [2, 3, 7])

    c_inf1, c_inf2, c_inf3 = st.columns(3)
    with c_inf1:
        st.info(f"👤 **आपका मूलांक:** {user_m}")
    with c_inf2:
        st.info(f"🌟 **आपका भाग्यांक:** {user_b}")
    with c_inf3:
        st.warning(f"🔍 **मिसिंग अंक:** {', '.join(map(str, user_missing_digits))}")

    if "show_lucky_btn" not in st.session_state:
        st.session_state["show_lucky_btn"] = False

    if st.button("सर्वश्रेष्ठ लकी नंबर खोजें", type="primary"):
        st.session_state["show_lucky_btn"] = True

    if st.session_state["show_lucky_btn"]:
        m_friends = FRIENDSHIP_TABLE.get(user_m, {}).get("friends", [1, 2, 3, 5, 9])
        b_friends = FRIENDSHIP_TABLE.get(user_b, {}).get("friends", [5, 6, 7, 8])
        common_friends = list(set(m_friends).intersection(set(b_friends)))

       # अलग-अलग सीरीज (Prefixes) और सफिक्स से डायनामिक नंबर पूल तैयार करना
        prefixes = [
            "9838", "9919", "9792", "9450", "9651", "9889", 
            "8887", "8707", "8574", "7007", "7275", "7388",
            "9935", "9140", "9559", "8004", "7800", "6386"
        ]
        
        suffixes = [
            "123456", "234567", "345678", "456789", "567890",
            "578123", "578345", "878523", "357812", "357822",
            "157823", "835781", "385782", "578111", "578222"
        ]

        raw_number_pool = []
        for p in prefixes:
            for s in suffixes:
                raw_number_pool.append(p + s)

        evaluated_numbers = []

        for num in raw_number_pool:
            total_sum = calculate_single_digit(num)
            last_4_sum = calculate_single_digit(num[-4:])
            is_asc, _ = check_ascending_descending(num[-4:])

            is_total_friendly = (total_sum in common_friends) or (total_sum in m_friends)
            is_last4_friendly = (last_4_sum in common_friends) or (last_4_sum in m_friends)

            num_digits = set(int(d) for d in num if d != '0')
            covered_missing = [d for d in user_missing_digits if d in num_digits]
            missing_count = len(covered_missing)

            if is_asc and missing_count >= 3:
                tag = "⭐ सर्वोत्तम (आरोही + 3+ मिसिंग अंक)"
            elif is_asc and missing_count >= 2:
                tag = "🥇 बहुत बढ़िया (आरोही + 2 मिसिंग अंक)"
            elif is_asc:
                tag = "🥈 उत्तम (आरोही क्रम)"
            else:
                tag = "👍 अनुकूल विकल्प"

            evaluated_numbers.append({
                "श्रेणी": tag,
                "मोबाइल नंबर": num,
                "10 अंकों का कुल योग": f"{total_sum} ({'🟢 मित्र' if is_total_friendly else '🟠 सामान्य'})",
                "अंतिम 4 अंकों का योग": f"{last_4_sum} ({'🟢 मित्र' if is_last4_friendly else '🟠 सामान्य'})",
                "कवर हुए मिसिंग अंक": f"{', '.join(map(str, covered_missing)) if covered_missing else 'कोई नहीं'}",
                "आरोही क्रम": "हाँ 📈" if is_asc else "सामान्य",
                "asc_score": 1 if is_asc else 0,
                "missing_score": missing_count,
                "friend_score": (1 if is_total_friendly else 0) + (1 if is_last4_friendly else 0)
            })

        evaluated_numbers.sort(
            key=lambda x: (x["asc_score"], x["missing_score"], x["friend_score"]),
            reverse=True
        )

        st.subheader("📋 आपके लिए अनुशंसित लकी नंबरों की प्राथमिकता सूची:")
        st.dataframe(evaluated_numbers[:10], use_container_width=True)