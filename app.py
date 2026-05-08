import streamlit as st
from datetime import date
from gtts import gTTS
import base64
import time
import uuid  
import os    

# १. आवाज़ वाला इंजन
def bol_web(text, part_id):
    try:
        clean_text = text.replace("*", "").replace("#", "").replace("\n", " ")
        tts = gTTS(text=clean_text, lang='hi', tld='co.in')
        
        unique_id = str(uuid.uuid4())[:8]
        filename = f"temp_{part_id}_{unique_id}.mp3"
        tts.save(filename)

        # फाइल को पढ़ना
        with open(filename, "rb") as f:
            audio_bytes = f.read()
        
        # स्क्रीन पर ऑडियो प्लेयर दिखाना
        st.markdown("#### 🎙️ भविष्य रिपोर्ट सुनने के लिए यहाँ नीचे क्लिक करें:")
        st.audio(audio_bytes, format="audio/mp3")

        # पुरानी फाइल डिलीट करना ताकि कंप्यूटर न भरे
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
# २. ग्रहों और उपायों का डेटाबेस (जो मैंने अभी दिया)
remedy_info = {
    1: {
        "grah": "सूर्य (Sun)", 
        "upay": "प्रतिदिन सूर्योदय के समय तांबे के लोटे से जल अर्पित करें। आदित्य हृदय स्तोत्र का पाठ करें और पिता का सम्मान करें। रविवार को गुड़ और गेहूं का दान करना अत्यंत शुभ होगा।"
    },
    2: {
        "grah": "चंद्रमा (Moon)", 
        "upay": "भगवान शिव का दूध से अभिषेक करें। प्रत्येक सोमवार को सफेद वस्तुओं जैसे चावल या दूध का दान करें। माता का आशीर्वाद लें और प्रतिदिन चांदी के पात्र में जल पिएं।"
    },
    3: {
        "grah": "गुरु (Jupiter)", 
        "upay": "गुरुवार को माथे पर केसर या हल्दी का तिलक लगाएं। विष्णु सहस्रनाम का श्रवण करें। चने की दाल और पीले वस्त्रों का दान करें और अपने गुरुजनों की सेवा करें।"
    },
    4: {
        "grah": "राहु (Rahu)", 
        "upay": "भगवान गणेश की आराधना करें और उन्हें दूर्वा अर्पित करें। पक्षियों को सात प्रकार का अनाज (सतनाजा) डालें। अपने पास चांदी का एक चौकोर टुकड़ा रखना आपके लिए कल्याणकारी होगा।"
    },
    5: {
        "grah": "बुध (Mercury)", 
        "upay": "बुधवार को गाय को हरा चारा या पालक खिलाएं। छोटी कन्याओं को उपहार दें। तुलसी के पौधे की नियमित सेवा करें और 'ॐ बुं बुधाय नमः' मंत्र का जाप करें।"
    },
    6: {
        "grah": "शुक्र (Venus)", 
        "upay": "शुक्रवार को सफेद मिठाई या कपूर का दान करें। लक्ष्मी चालीसा का पाठ करें। अपने परिवेश को सुगंधित रखें और इत्र का प्रयोग करें। महिलाओं का सम्मान करना भाग्य जगाएगा।"
    },
    7: {
        "grah": "केतु (Ketu)", 
        "upay": "स्ट्रीट डॉग्स (गलियों के कुत्तों) को मीठी रोटी या बिस्किट खिलाएं। मंदिर के शिखर पर दोरंगी ध्वजा (झंडा) लगाएं। गणेश जी को मोदक का भोग लगाना आपके लिए श्रेष्ठ है।"
    },
    8: {
        "grah": "शनि (Saturn)", 
        "upay": "शनिवार को पीपल के वृक्ष के नीचे सरसों के तेल का दीपक जलाएं। हनुमान चालीसा का पाठ करें। जरूरतमंदों और सफाई कर्मचारियों को काली उड़द या काले वस्त्रों का दान करें।"
    },
    9: {
        "grah": "मंगल (Mars)", 
        "upay": "मंगलवार को हनुमान जी को चोला चढ़ाएं और बूंदी का प्रसाद बांटें। भाइयों के साथ संबंध मधुर रखें। सुंदरकांड का पाठ करना आपके साहस और ऊर्जा में वृद्धि करेगा।"
    }
}
# ५. ऐप इंटरफेस
st.set_page_config(page_title="बजरंगी राम", layout="wide")
st.markdown("<h1 style='text-align: center; color: #E74C3C;'>Ψ बजरंगी राम अंक ज्योतिष केंद्र</h1>", unsafe_allow_html=True)

st.header("📋 विवरण भरें")
import datetime

# --- इनपुट विभाग (Input Section) ---

# १. नाम के लिए (Placeholder के साथ)
u_name = st.text_input("आपका शुभ नाम", placeholder="यहाँ अपना पूरा नाम भरें...")

# २. आज की तारीख और रेंज सेट करना
today = datetime.date.today()
hundred_years_ago = today.year - 100
hundred_years_ahead = today.year + 100

# ३. डेट पिकर (१०० साल पीछे और १०० साल आगे की रेंज के साथ)
u_dob = st.date_input(
    "अपनी जन्म तिथि चुनें",
    value=today, # डिफ़ॉल्ट रूप से आज की तारीख दिखाएगा
    min_value=datetime.date(hundred_years_ago, 1, 1), # १०० साल पीछे
    max_value=datetime.date(hundred_years_ahead, 12, 31) # १०० साल आगे
)

u_gender = st.selectbox("लिंग", ["Male", "Female"])
submit = st.button("कुंडली देखें")

if submit:
    
    st.balloons()
    placeholder = st.empty()
    welcome_text = f"🚩 जय श्री राम {u_name} जी! आपकी ज्योतिषीय गणना की जा रही है..."
    typed = ""
    for char in welcome_text:
        typed += char
        placeholder.markdown(f"<div style='background-color: #FDEDEC; padding: 15px; border-radius: 10px; border: 1px solid #E74C3C; text-align: center;'><h3>{typed}</h3></div>", unsafe_allow_html=True)
        time.sleep(0.02)

        # --- स्टेज २: गणना (Calculations) ---
    d, m, y = u_dob.day, u_dob.month, u_dob.year
    mulank = get_single_digit(d)
    bhagyank = get_single_digit(d + m + y)
    name_val = sum(chaldean_table.get(c.upper(), 0) for c in u_name if c.isalpha())
    name_num = get_single_digit(name_val)
    
    y_sum = get_single_digit(y)
    kua = get_single_digit(11 - y_sum) if u_gender == "Male" else get_single_digit(y_sum + 4)

# --- अंक ज्योतिष मैत्री गणना (1 से 9 अंक) ---
    friendship_logic = {
            1: {'friends': [2, 3, 5, 9], 'enemies': [8], 'neutral': [4, 6, 7]},
            2: {'friends': [1, 3, 5], 'enemies': [4, 8, 9], 'neutral': [6, 7]},
            3: {'friends': [1, 2, 5, 7, 9], 'enemies': [6], 'neutral': [4, 8]},
            4: {'friends': [5, 6, 7, 8], 'enemies': [1, 2, 9], 'neutral': [3]},
            5: {'friends': [1, 2, 3, 4, 6, 7, 8, 9], 'enemies': [], 'neutral': []},
            6: {'friends': [4, 5, 7, 8], 'enemies': [3], 'neutral': [1, 2, 9]},
            7: {'friends': [3, 4, 5, 6], 'enemies': [1, 2, 9], 'neutral': [8]},
            8: {'friends': [4, 5, 6, 7], 'enemies': [1, 2, 9], 'neutral': [3]},
            9: {'friends': [1, 2, 3, 5], 'enemies': [4, 7, 8], 'neutral': [6]}
        }

        # मूलांक और भाग्यांक का संबंध निकालना
    m_rel = friendship_logic.get(mulank, {}).get('friends', [])
    m_enm = friendship_logic.get(mulank, {}).get('enemies', [])    

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
        st.subheader("📜 click bellow to chooes  category")
        
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
                # टैब्स को मोबाइल फ्रेंडली और सुंदर बनाने के लिए नया CSS
        st.markdown("""
        <style>
            /* टैब्स के पूरे कंटेनर को मोबाइल स्क्रीन पर फिट करना */
            .stTabs [data-baseweb="tab-list"] {
                display: flex;
                flex-wrap: wrap; /* यह लाइन मोबाइल पर टैब्स को टूटने से बचाएगी */
                gap: 8px;
                width: 100%;
                justify-content: center;
            }

            /* हर टैब बटन का स्टाइल */
            .stTabs [data-baseweb="tab"] {
                flex: 1 1 auto; /* टैब नाम के हिसाब से अपनी चौड़ाई लेगा */
                min-width: 80px; 
                height: auto; /* फिक्स हाइट हटा दी ताकि मोबाइल पर समस्या न हो */
                padding: 8px 12px;
                background-color: #F0F2F6;
                border-radius: 10px 10px 0px 0px;
                font-weight: bold;
                font-size: 14px; /* मोबाइल के लिए सही साइज */
                color: #2C3E50;
            }

            /* जब कोई टैब सिलेक्ट हो (Active Tab) */
            .stTabs [aria-selected="true"] {
                background-color: #E74C3C !important; /* बजरंग लाल रंग */
                color: white !important;
                border-bottom: 3px solid #FFD700 !important;
            }
        </style>
        """, unsafe_allow_html=True)
            # Ab aapke purane tabs yahan se shuru honge
        tab1, tab2, tab3 = st.tabs(["📑 मूलांक-भाग्यांक फल", "🔮 नाम-भाग्य विचार", "🎡 ग्रिड एवं उपाय"])      
                    

        with tab1:
            st.markdown("### 🌟 आपके व्यक्तित्व का मुख्य आधार")
            
            # मूलांक और भाग्यांक को सुंदर कार्ड में दिखाना
            st.markdown(f"""
            <div style="background-color: #fdf2e9; padding: 20px; border-radius: 15px; border-left: 8px solid #e67e22; margin-bottom: 20px;">
                <h4 style="color: #e67e22; margin: 0;">मूलांक: {mulank} | भाग्यांक: {bhagyank}</h4>
                <p style="color: #6e2c00; font-size: 16px; margin-top: 10px;">
                आपका <b>मूलांक</b> आपकी आंतरिक शक्ति है, और <b>भाग्यांक</b> आपका कर्म मार्ग।
                </p>
            </div>
            """, unsafe_allow_html=True)

            # 2. Audio script ki shuruat karein
            tab1_audio = f"Namaste! Aapka Mulaank {mulank} hai aur Bhagyaank {bhagyank} hai. "
        # मैत्री लॉजिक का परिणाम दिखाना
            if bhagyank in m_rel:
                st.success(f"✔️ **Aapka sambandh:** Mulaank {mulank} aur Bhagyaank {bhagyank} ke beech sambandh **Mitravat (Friendly)** hai.")
                tab1_audio += f"In dono ke beech bahut hi mitravat sambandh hai, jo aapko har kaam mein safalta dilayega."
            elif bhagyank in m_enm:
                st.warning(f"⚠️ **Aapka sambandh:** Mulaank {mulank} aur Bhagyaank {bhagyank} ke beech sambandh **Shatruvat (Enemy)** hai.")
                tab1_audio += f"In dono ke beech shatruvat sambandh hone ke karan, aapko thoda sangharsh karna pad sakta hai."
            else:
                st.info(f"ℹ️ **Aapka sambandh:** Mulaank {mulank} aur Bhagyaank {bhagyank} ke beech sambandh **Sam (Neutral)** hai.")
                tab1_audio += f"In dono ke beech sam sambandh hai, jo aapke jeevan ko santulit banaye rakhega."

            # 3. Tab 1 ke liye audio button (Sabse niche lagayein)
            if tab1_audio:
                st.write("---")
                # केवल एक स्लाइडर बनेगा जो राजयोग और उपाय दोनों बोलेगा
                bol_web(tab1_audio, "graha_voice")
            
        with tab2:
            st.markdown("### ⚖️ नामांक (Name Number) विश्लेषण एवं परामर्श")
            
            # नामांक कार्ड
            st.markdown(f"""
            <div style="background-color: #ebf5fb; padding: 20px; border-radius: 15px; border-left: 8px solid #2e86c1; margin-bottom: 20px; text-align: center;">
                <h2 style="color: #2e86c1; margin: 0;">आपका नामांक: {name_num}</h2>
                <p style="color: #1b4f72; font-size: 16px; margin-top: 10px;">
                (चूकि आपका नाम '{u_name}' है, जिसका अंक ज्योतिष मूल्य {name_num} आता है)
                </p>
            </div>
            """, unsafe_allow_html=True)

            # --- क्रांतिकारी परामर्श लॉजिक (The Revolutionary Logic) ---
            
            # १. चेक करें कि क्या नामांक पहले से ग्रिड में मौजूद है?
            # 'all_present_nums' वह सेट है जिसमें DOB के अंक शामिल हैं
            count_in_dob = dob_digits.count(name_num)
            
            if count_in_dob >= 1:
                # चेतावनी: अगर अंक पहले से मौजूद है
                st.error(f"⚠️ **अंकों की अति (Overload) की चेतावनी!**")
                st.write(f"आपका नामांक **{name_num}** आपकी जन्मतिथि में पहले से ही मौजूद है। नाम के माध्यम से इस अंक की पुनरावृत्ति हो रही है, जो इस ग्रह की ऊर्जा को 'असंतुलित' कर सकती है।")
                
                st.markdown("---")
                st.subheader("💡 गुरु का परामर्श (Name Correction Suggestion)")
                st.info("बेहतर सफलता और राजयोग के लिए आपको अपना नाम उस अंक पर लाना चाहिए जो आपके ग्रिड में अनुपस्थित (Missing) है।")

                # २. राजयोग के लिए सबसे बेहतर सुझाव ढूंढना
                suggestions = []
                if 5 in missing_nums:
                    suggestions.append(("5 (बुध)", "यह आपके 'स्वर्ण राजयोग' (4-5-6) को पूर्ण करेगा। व्यापार और संवाद में जबरदस्त सफलता मिलेगी।"))
                elif 6 in missing_nums:
                    suggestions.append(("6 (शुक्र)", "यह सुख-समृद्धि और पारिवारिक सुख के द्वार खोलेगा।"))
                elif 1 in missing_nums:
                    suggestions.append(("1 (सूर्य)", "यह सरकारी लाभ और मान-सम्मान में वृद्धि करेगा।"))
                
                if suggestions:
                    for title, desc in suggestions:
                        st.success(f"✅ **सुझाव: नाम को अंक {title} पर ले जाएं।**")
                        st.write(f"👉 {desc}")
                else:
                    # यदि ऊपर वाले मुख्य अंक नहीं हैं, तो कोई भी पहला मिसिंग नंबर बताएं
                    st.success(f"✅ **सुझाव:** अपने नाम को अंक **{missing_nums[0]}** पर सेट करना आपके लिए हितकारी होगा।")

            elif name_num in missing_nums:
                # यदि नामांक किसी कमी को पूरा कर रहा है
                st.success(f"✨ **शुभ योग:** आपका वर्तमान नामांक **{name_num}** आपके ग्रिड की एक कमी को पूरा कर रहा है। यह आपके लिए बहुत ही अनुकूल और प्रगतिशील है।")
            
            st.markdown("---")
            st.warning("📣 **विशेष सलाह:** नाम की स्पेलिंग में बदलाव करने से पहले **विशाल विक्रम पांडे जी** से परामर्श अवश्य लें ताकि सूक्ष्म गणना सही हो सके। mo. 6392311093")
            # --- टैब २ के लिए आवाज़ का हिस्सा ---
            # पहले एक स्क्रिप्ट तैयार करते हैं
            tab2_audio = f"नामांक विश्लेषण के अनुसार, आपका नामांक {name_num} है। "
            
            if count_in_dob >= 1:
                tab2_audio = f"नमस्कार {u_name} जी। नामांक विश्लेषण के अनुसार, आपका नामांक {name_num} है। "

            if count_in_dob >= 1:
                tab2_audio += f"सावधान! आपका नामांक {name_num} आपकी जन्मतिथि के अंकों के साथ रिपीट हो रहा है। "
    
    # राजयोग की गणना (अंक ५ या ६ के आधार पर)
            if 5 in missing_nums:
                tab2_audio += "गुरु का परामर्श है कि आप अपना नाम अंक 5 पर लाने का प्रयास करें। इससे स्वर्ण राजयोग बनेगा। "
            elif 6 in missing_nums:
                tab2_audio += "बेहतर होगा कि आप अपना नाम अंक 6 पर ले जाएं, जिससे संपत्ति राजयोग की प्राप्ति होगी। "
            else:
                tab2_audio += f"सुझाव है कि आप अपने नाम को अंक {missing_nums[0] if missing_nums else 1} पर सेट करें। "
            
# --- आपकी पर्ची वाली विशेष सलाह जोड़ना ---
                tab2_audio += "विशेष सलाह: नाम की स्पेलिंग में बदलाव करने हेतु और सूक्ष्म गणना के लिए विशाल विक्रम पाण्डेय जी से संपर्क करें। धन्यवाद। जय श्री राम।"
            bol_web(tab2_audio, "tab2_advice_voice")
            # अब मशीन को बोलने का आदेश दें
            st.markdown("---")
            st.write("🎙️ **गुरु का परामर्श सुनें:**")
           
        with tab3:
            

            # २. लो-शु ग्रिड दिखाना (फोटो 478cc4f2 के वेरिएबल्स के अनुसार)
            st.markdown("### 🔮 लो-शू ग्रिड और विस्तृत भविष्य फल")
            st.write("### 🔲 आपका लो-शू ग्रिड चार्ट")
            
            
            # १. ऑडियो स्क्रिप्ट को यहाँ एक बार शुरू करें
            tab3_audio = "प्रणाम! आपके चार्ट का विशेष विश्लेषण यहाँ दिया गया है। "

            # २. राजयोगों को ऑडियो में जोड़ना
            if 'active_rajyog' in locals() and active_rajyog:
                tab3_audio += "सबसे पहले आपके चार्ट के राजयोगों की बात करते हैं। आपके चार्ट में ये विशेष राजयोग बन रहे हैं: "
                for ry in active_rajyog:
                    st.success(f"✔️ {ry}") # स्क्रीन पर दिखाएँ
                    tab3_audio += f"{ry}। " # ऑडियो में जोड़ें
            else:
                st.info("फिलहाल इस चार्ट में कोई विशेष राजयोग नहीं बन रहा है।")
                tab3_audio += "फिलहाल इस चार्ट में कोई विशेष राजयोग नहीं है। "

            st.write("---")

            # ३. उपायों को ऑडियो में जोड़ना
            if 'missing_nums' in locals():
                tab3_audio += "अब लुप्त अंकों के उपायों की चर्चा करते हैं। "
                for n in missing_nums:
                    if n in remedy_info:
                        g = remedy_info[n]["grah"]
                        u = remedy_info[n]["upay"]
                        
                        st.info(f"**अंक {n} ({g}):** {u}") # स्क्रीन पर दिखाएँ
                        # ऑडियो स्क्रिप्ट में जोड़ें
                        tab3_audio += f"अंक {n} जो {g} का है, उसके लिए उपाय है: {u}। "

            # ४. मुख्य सुधार: बोल_वेब (bol_web) को लूप के बिल्कुल बाहर रखें
            if tab3_audio:
                st.write("---")
                # केवल एक स्लाइडर बनेगा जो राजयोग और उपाय दोनों बोलेगा
                bol_web(tab3_audio, "graha_voice")
