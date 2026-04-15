import streamlit as st
from datetime import date
from gtts import gTTS
import base64
import time
import uuid
import os
# यह कोड उस छोटे तीर (Arrow) को बड़ा और लाल कर देगा
st.markdown("""
    <style>
    /* तीर वाले बटन को बड़ा और रंगीन बनाने के लिए */
    [data-testid="sidebar-expand-back"], [aria-label="Open sidebar"] {
        background-color: #FF4B4B !important;
        color: white !important;
        width: 60px !important;
        height: 60px !important;
        border-radius: 50% !important;
        position: fixed !important;
        top: 20px !important;
        left: 10px !important;
        z-index: 999999 !important;
        box-shadow: 0px 0px 15px rgba(255, 75, 75, 0.8) !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    /* तीर के पास निर्देश दिखाने के लिए */
    [aria-label="Open sidebar"]::after {
        content: "👈 Click for Details";
        position: absolute;
        left: 70px;
        background: #FF4B4B;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 12px;
        white-space: nowrap;
    }
    </style>
""", unsafe_allow_html=True)
# १. आवाज़ वाला इंजन
def bol_web(text, part_id):
    try:
        clean_text = text.replace("*", "").replace("#", "").replace("\n", " ")
        tts = gTTS(text=clean_text, lang='hi', tld='co.in')
        
        unique_id = str(uuid.uuid4())[:8] 
        filename = f"temp_{part_id}_{unique_id}.mp3"
        tts.save(filename)
        
        with open(filename, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            
        # --- बिल्कुल यही HTML कोड इस्तेमाल करें ---
        audio_html = f"""
            <div style="margin: 20px 0; padding: 15px; background: #f1f3f4; border-radius: 10px; border-left: 5px solid #1a73e8;">
                <p style="margin: 0 0 10px 0; font-weight: bold; color: #1a73e8;">🎤 रिपोर्ट ऑडियो:</p>
                <button onclick="var a=document.getElementById('aud_{unique_id}'); a.paused?a.play():a.pause()" 
                    style="background:#1a73e8; color:white; border:none; padding:8px 16px; border-radius:5px; cursor:pointer; margin-right:5px;">
                    ⏯️ बजाएं / रोकें
                </button>
                <button onclick="var a=document.getElementById('aud_{unique_id}'); a.currentTime=0; a.play()" 
                    style="background:#5f6368; color:white; border:none; padding:8px 16px; border-radius:5px; cursor:pointer;">
                    🔄 फिर से सुनें
                </button>
                <audio id="aud_{unique_id}" autoplay>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            </div>
        """
        # ध्यान दें: यह लाइन सबसे जरूरी है
        st.markdown(audio_html, unsafe_allow_html=True)
        
        if os.path.exists(filename):
            os.remove(filename)

    except Exception as e:
        st.error(f"ऑडियो में समस्या: {e}")
    
def get_single_digit(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

chaldean_table = {'A':1,'I':1,'J':1,'Q':1,'Y':1,'B':2,'K':2,'R':2,'C':3,'G':3,'L':3,'S':3,'D':4,'M':4,'T':4,'E':5,'H':5,'N':5,'X':5,'U':6,'V':6,'W':6,'O':7,'Z':7,'F':8,'P':8}
# ४. ८१ कॉम्बिनेशन (उदाहरण के लिए)
faladesh_dict = {
    "1-1": " 1 no. jo surya ka hai, Surya aur Surya ka yog. Aap ek janmjaat neta hain. Shasan aur prashasan mein safalta milegi.",
    "1-2": "Surya aur Chandra. Creative kshamatayein achhi hain, par mann thoda chanchal reh sakta hai.",
    "1-3": "Surya aur Guru. Yeh gyaan aur adhikaar ka adbhut sangam hai. Aap ek achhe shikshak ban sakte hain.",
    "1-4": "Surya aur Rahu. Sangharsh ke baad badi safalta milti hai. Rajneeti mein ruchi ho sakti hai.",
    "1-5": "Surya aur Budh. Yeh 'Budhaditya' yog jaisa hai. Vyapar aur buddhi mein aap nipun hain.",
    "1-6": "Surya aur Shukra. Luxury aur sukh-suvidhaon wala jeevan rahega, par parivarik zimmedari badhengi.",
    "1-7": "Surya aur Ketu. Adhyatmik ruchi aur gahri soch. Aap parde ke peeche rehkar kaam karna pasand karenge.",
    "1-8": "Surya aur Shani. Pita se matbhed ho sakte hain, par kadi mehnat se aap uncha pad payenge.",
    "1-9": "Surya aur Mangal. Sabse shaktishali yog. Sena, police ya prashasan mein uchh pad milta hai.",
    "2-1": "Chandra aur Surya. Maa ka sahyog milega. Aap sensitive hain par naitrutva kar sakte hain.",
    "2-2": "Double Chandra. Ati-shilp aur bhavukta. Kala aur sangeet mein ruchi ho sakti hai.",
    "2-3": "Chandra aur Guru. Gaj-kesari yog jaisa fal. Dhan aur maan-samman ki prapti hogi.",
    "2-4": "Chandra aur Rahu. Mansik tanav reh sakta hai. Meditaiton aur shiv upasna karein.",
    "2-5": "Chandra aur Budh. Bolne mein nipun aur chatur. Marketing mein safalta milegi.",
    "2-6": "Chandra aur Shukra. Akarshak vyaktitv aur sukhad parivarik jeevan.",
    "2-7": "Chandra aur Ketu. Intuition power bahut tej hai. Sapne sach ho sakte hain.",
    "2-8": "Chandra aur Shani. Vish yog ka prabhav. Jeevan mein vailamb aur sangharsh rahega.",
    "2-9": "Chandra aur Mangal. Laxmi yog. Dhan ki kabhi kami nahi hogi, par gussa jald aayega.",
    "3-1": "Guru aur Surya. Gyaani aur prabhavshali. Samaj mein badi pratishtha milti hai.",
    "3-2": "Guru aur Chandra. Shanti aur gyaan ka mel. Log aapke paas salah lene aayenge.",
    "3-3": "Double Guru. Gyaan ka bhandaar. Shiksha aur dharmik kshetra mein bade kaam karenge.",
    "3-4": "Guru aur Rahu. Chanakya jaisi buddhi. Aap mushkil se mushkil raasta nikal lenge.",
    "3-5": "Guru aur Budh. Shikshan aur vyapar dono mein safal. Communication bahut achha hai.",
    "3-6": "Guru aur Shukra. Gyaan aur luxury ka mel. Thoda kharchila swabhav ho sakta hai.",
    "3-7": "Guru aur Ketu. Brahm-gyaan aur moksh ki raah. Gehra chintan aapki shakti hai.",
    "3-8": "Guru aur Shani. Kadi mehnat se gyaan ka vistar. Law ya justice mein safalta.",
    "3-9": "Guru aur Mangal. Shashtra aur Shaastra dono ka gyaan. Suraksha ya coaching mein best.",
    "4-1": "Rahu aur Surya. Rajneetik chaturai. Achanak bhagya uday hoga.",
    "4-2": "Rahu aur Chandra. Kalpana-shakti tej par mann ashant. Shiv ji ki puja karein.",
    "4-3": "Rahu aur Guru. Guru-Chandal yog ka prabhav. Buddhi bahut tej par dharam par vishwas kam.",
    "4-4": "Double Rahu. Bhramit ho sakte hain, par technical field mein kamaal karenge.",
    "4-5": "Rahu aur Budh. IT aur calculation mein maharat. Smart work karne mein expert.",
    "4-6": "Rahu aur Shukra. Glamour aur dikhawe ki duniya mein ruchi. Kharchon par dhyan dein.",
    "4-7": "Rahu aur Ketu. Jeevan mein kai utaar-chadaav, par adhyatmik ant.",
    "4-8": "Rahu aur Shani. Bahut kadi mehnat aur sangharsh, par ant mein sthayi safalta.",
    "4-9": "Rahu aur Mangal. Angarak yog jaisa prabhav. Gusse se bachein, technical kaam karein.",
    "5-1": "Budh aur Surya. Business minded aur prabhavshali. Sarkaari labh mil sakta hai.",
    "5-2": "Budh aur Chandra. Creative business idea. Mood swings ka dhyan rakhein.",
    "5-3": "Budh aur Guru. Advisor ya Consultant ke roop mein bade safal honge.",
    "5-4": "Budh aur Rahu. Share market aur research mein maharat. Achannak labh.",
    "5-5": "Double Budh. Ati-chatur aur vyaparik buddhi. Hisab-kitab mein expert.",
    "5-6": "Budh aur Shukra. Entertainment aur media mein safalta. Shaukeen mizaj.",
    "5-7": "Budh aur Ketu. Writing aur research mein best. Akant mein kaam karna pasand.",
    "5-8": "Budh aur Shani. Sthayi vyapar aur dheere-dheere tarakki. Dhairya rakhein.",
    "5-9": "Budh aur Mangal. Real Estate aur zameen ke kaamon mein safalta.",
    "6-1": "Shukra aur Surya. Luxury life par thoda ego problem ho sakta hai.",
    "6-2": "Shukra aur Chandra. Romance aur kala mein ruchi. Sundar vyaktitv.",
    "6-3": "Shukra aur Guru. Sansarik aur adhyatmik sukhon santulan.",
    "6-4": "Shukra aur Rahu. Achannak dhangaman. Fashion aur tech mein ruchi.",
    "6-5": "Shukra aur Budh. Media, Acting ya Business mein badi safalta.",
    "6-6": "Double Shukra. Ati-vilasita. Parivar aur prem mein samarpit.",
    "6-7": "Shukra aur Ketu. Prem mein dhokha mil sakta hai, par adhyatma mein unchai.",
    "6-8": "Shukra aur Shani. Dheere-dheere sampatti banegi. Purani cheezon se labh.",
    "6-9": "Shukra aur Mangal. Junoon aur sahas. Sports ya construction mein labh.",
    "7-1": "Ketu aur Surya. Government se thoda doori, par research mein unchai.",
    "7-2": "Ketu aur Chandra. Ati-samvedansheel. Gahri neend mein samasya ho sakti hai.",
    "7-3": "Ketu aur Guru. Param gyaani. Astrology aur occult mein maharat.",
    "7-4": "Ketu aur Rahu. Achannak ghatnayein. Research field mein best.",
    "7-5": "Ketu aur Budh. Analytical dimaag. Writing aur occult mein safal.",
    "7-6": "Ketu aur Shukra. Prem mein virakti. Adhyatmik prem ki talash.",
    "7-7": "Double Ketu. Bahut zyada adhyatmik. Duniya se thoda alag rehne ki aadat.",
    "7-8": "Ketu aur Shani. Rahasyamayi aur kadi mehnat karne wala vyaktitv.",
    "7-9": "Ketu aur Mangal. Surgery ya technical field mein bade doctor ya engineer.",
    "8-1": "Shani aur Surya. Sangharsh purn prarambh, par ant mein bada pad.",
    "8-2": "Shani aur Chandra. Vish yog ka dhyan rakhein. Dheere badhein.",
    "8-3": "Shani aur Guru. Dharma aur Nyay ke raste par chalne se bhagya uday.",
    "8-4": "Shani aur Rahu. Shrapit dosh jaisa prabhav, par technical field mein king.",
    "8-5": "Shani aur Budh. Corporate sector aur finance mein badi safalta.",
    "8-6": "Shani aur Shukra. Dheere-dheere ameeri. Purani cheezon se labh.",
    "8-7": "Shani aur Ketu. Akantpriya aur adhyatmik. Gehra shodhkarta.",
    "8-8": "Double Shani. Bahut adhik kadi mehnat. Jeevan ke uttarardh mein vijay.",
    "8-9": "Shani aur Mangal. Technical maharat. Construction ya factory mein safal.",
    "9-1": "yaha mulank 9 tatha bhagyank 1, Mangal aur Surya. Maha-shaktishali. Naitrutva aapke khoon mein hai.",
    "9-2": "Mangal aur Chandra. Laxmi yog. Dhanwan aur saahasi.",
    "9-3": "Mangal aur Guru. Gyaan aur shakti ka mel. Ek mahan margdarshak.",
    "9-4": "Mangal aur Rahu. Angarak yog. Gusse se bachein, urja ko sahi jagah lagayein.",
    "9-5": "Mangal aur Budh. Zameen aur hisab-kitab mein nipun.",
    "9-6": "Mangal aur Shukra. Akarshan aur junoon. Media ya luxury mein safal.",
    "9-7": "Mangal aur Ketu. Doctor ya Engineer banne ke yog. Sahas bahut zyada.",
    "9-8": "Mangal aur Shani. Sangharsh ke baad sthayi safalta. Property mein labh.",
    "9-9": "Double Mangal. Aseem urja. Hanuman ji ki bhakti se sab safal hoga."
}
remedies_dict = {
    1: "Surya ko jal chadhayein.", 2: "Chandi ka glass istemal karein.",
    3: "Kesar ka tilak lagayein.", 4: "Tulsi ka paudha lagayein.",
    5: "Gai ko hara chara khilayein.", 6: "Itr (perfume) lagayein.",
    7: "Kutte ko roti khilayein.", 8: "Shani dev ki puja karein.",
    9: "Hanuman Chalisa ka paath karein."
}

# ५. ऐप इंटरफेस
st.set_page_config(page_title="बजरंगी राम", layout="wide")
st.markdown("<h1 style='text-align: center; color: #E74C3C;'>Ψ बजरंगी राम अंक ज्योतिष केंद्र</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 विवरण भरें")
    u_name = st.text_input("पूरा नाम", "vishal")
    u_dob = st.date_input("जन्म तिथि", date(1986, 4, 18))
    u_gender = st.selectbox("लिंग", ["Male", "Female"])
    submit = st.button("कुंडली देखें")

if submit:
    d, m, y = u_dob.day, u_dob.month, u_dob.year
    mulank = get_single_digit(d)
    bhagyank = get_single_digit(d + m + y)
    name_val = sum(chaldean_table.get(c.upper(), 0) for c in u_name if c.isalpha())
    name_num = get_single_digit(name_val)
    
    y_sum = get_single_digit(y)
    kua = get_single_digit(11 - y_sum) if u_gender == "Male" else get_single_digit(y_sum + 4)

    # डुप्लिकेट्स को संभालने के लिए लिस्ट का उपयोग
    dob_digits = [int(n) for n in u_dob.strftime('%d%m%Y') if n != '0']
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #E74C3C;'>
                <h3 style='margin:0; color:#E74C3C;'>मूलांक: {mulank}</h3>
                <h3 style='margin:5px 0; color:#1E90FF;'>भाग्यांक: {bhagyank}</h3>
                <h3 style='margin:5px 0; color:#2ECC71;'>नामांक: {name_num}</h3>
                <h3 style='margin:10px 0; color:#8E44AD;'>कुआ नंबर: {kua}</h3>
            </div>
        """, unsafe_allow_html=True)

        st.subheader("🗓️ लो-शू ग्रिड (Multi-Number View)")
        
        # ग्रिड मैपिंग
        grid_pos = {4:(0,0), 9:(0,1), 2:(0,2), 3:(1,0), 5:(1,1), 7:(1,2), 8:(2,0), 1:(2,1), 6:(2,2)}
        display_grid = [[[] for _ in range(3)] for _ in range(3)]

        # १. DOB के नंबर (Black)
        for n in dob_digits:
            if n in grid_pos:
                r, c = grid_pos[n]
                display_grid[r][c].append(f"<span style='color:black;'>{n}</span>")
        
        # २. विशेष नंबरों को जोड़ना (Colors)
        special_nums = [(mulank, "#E74C3C"), (bhagyank, "#1E90FF"), (name_num, "#2ECC71"), (kua, "#8E44AD")]
        for num, color in special_nums:
            r, c = grid_pos[num]
            display_grid[r][c].append(f"<span style='color:{color};'>{num}</span>")

        # ग्रिड बनाना
        html_grid = "<table style='width:100%; border-collapse: collapse; text-align:center; font-size:24px; font-weight:bold;'>"
        for row in display_grid:
            html_grid += "<tr style='height:110px;'>"
            for cell_list in row:
                content = " ".join(cell_list) if cell_list else ""
                html_grid += f"<td style='border:2px solid #E74C3C; width:33%; background-color:#FFF9F0;'>{content}</td>"
            html_grid += "</tr>"
        html_grid += "</table>"
        st.markdown(html_grid, unsafe_allow_html=True)

    with col2:
        st.subheader("📜 भविष्य रिपोर्ट एवं उपाय")
        
        # १. ८१ कॉम्बिनेशन का फल निकालना
        comb_key = f"{mulank}-{bhagyank}"
        comb_fal = faladesh_dict.get(comb_key, "आपके मूलांक और भाग्यांक का तालमेल उत्तम है।")

        # २. मिसिंग नंबर और उपाय
        all_present_nums = set(dob_digits) | {mulank, bhagyank, name_num, kua}
        missing_nums = [n for n in range(1, 10) if n not in all_present_nums]
# --- राजयोग चेक करने का लॉजिक ---
        rajyog_dict = {
            "4-9-2": "Mental Plane (मानसिक शक्ति): आपकी याददाश्त और योजना बनाने की शक्ति गजब की है।",
            "3-5-7": "Emotional Plane (भावनात्मक शक्ति): आप बहुत दयालु हैं और आपकी अंतरात्मा की आवाज़ बहुत सटीक होती है।",
            "8-1-6": "Practical Plane (व्यावहारिक शक्ति): आप मेहनत और काम करने में विश्वास रखते हैं, सफलता कदम चूमेगी।",
            "4-3-8": "Thought Plane (विचार शक्ति): आप किसी भी काम को शुरू करने से पहले उसकी गहराई तक जाते हैं।",
            "9-5-1": "Will Power Plane (इच्छा शक्ति): आपकी संकल्प शक्ति बहुत मजबूत है, आप जो ठान लेते हैं वो पूरा करते हैं।",
            "2-7-6": "Action Plane (कर्म शक्ति): आप बोलने से ज्यादा करने में विश्वास रखते हैं।",
            "4-5-6": "Golden Rajyog (स्वर्ण राजयोग): यह सबसे बड़ा राजयोग है, आपको जीवन में धन और सफलता दोनों मिलेगी।",
            "2-5-8": "Silver Rajyog (रजत राजयोग): आपके पास अपनी प्रॉपर्टी और घर होने के प्रबल योग हैं।"
        }

        active_rajyog = []
        # चेक करने के लिए सभी ८ कॉम्बिनेशन
        planes = [
            ([4, 9, 2], "4-9-2"), ([3, 5, 7], "3-5-7"), ([8, 1, 6], "8-1-6"), # Horizontal
            ([4, 3, 8], "4-3-8"), ([9, 5, 1], "9-5-1"), ([2, 7, 6], "2-7-6"), # Vertical
            ([4, 5, 6], "4-5-6"), ([2, 5, 8], "2-5-8")                       # Diagonal
        ]

        for p_nums, p_key in planes:
            if all(num in all_present_nums for num in p_nums):
                active_rajyog.append(rajyog_dict[p_key])
        # ३. रिपोर्ट तैयार करना (स्क्रीन पर दिखाने के लिए)
        report_parts = [
            f"✨ जय बजरंगी! स्वागत है **{u_name}** जी। आपका बजरङ्गिराम अंक ज्योतिष में स्वागत है ",
            f"🔸 आपका **मूलांक {mulank}** और **भाग्यांक {bhagyank}** है।",
            f"🔸 आपका **नामांक {name_num}** और **कुआ नंबर {kua}** है।",
            f"🔮 **विशेष फल:** {comb_fal}"
        ]
# ४. राजयोग का फल जोड़ना
        if active_rajyog:
            report_parts.append("\n👑 **आपके ग्रिड के राजयोग:**")
            for ry in active_rajyog:
                report_parts.append(f"⭐ {ry}")
        # 5. उपाय जोड़ना
        if missing_nums:
            report_parts.append("\n🛠️ **मिसिंग नंबर के उपाय:**")
            for n in missing_nums:
                upay = remedies_dict.get(n, "इस अंक की ऊर्जा बढ़ाएं।")
                report_parts.append(f"- अंक {n}: {upay}")

        # ५. स्क्रीन पर पूरी रिपोर्ट दिखाना
        full_display_text = "\n\n".join(report_parts)
        st.info(full_display_text)

        # ६. 🎤 ऑडियो स्क्रिप्ट (जो सब कुछ बोलकर बताएगा)
        audio_script = f"जय बजरंगबली {u_name} जी। आपका बजरङ्गिराम अंक ज्योतिष में स्वागत है  "
        audio_script += f"आपका मूलांक {mulank} और भाग्यांक {bhagyank} है। "
        audio_script += f"नामांक {name_num} और कुआ नंबर {kua} है। "
        audio_script += f"आपके ग्रहों का फल कहता है कि {comb_fal}। "
        if active_rajyog:
            audio_script += " आपके ग्रिड में विशेष राजयोग भी बन रहे हैं। "
            for ry in active_rajyog:
                audio_script += f"{ry} "
        if missing_nums:
            audio_script += " आपके ग्रिड में कुछ अंक कम हैं, जिनके उपाय रिपोर्ट में दिए गए हैं। कृपया उन्हें देखें।"

        # ७. आवाज़ चालू करना (Collapse Fix के साथ)
        bol_web(audio_script, "full_report_vFinal")
