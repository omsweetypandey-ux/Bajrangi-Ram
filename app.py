import streamlit as st
# नीचे वाला कोड यहाँ पेस्ट करें:
hide_streamlit_style = """
              <style>
              #MainMenu {visibility: hidden;}
              footer {visibility: hidden;}
              header {visibility: hidden;}
              </style>
              """
import datetime  
from gtts import gTTS
from elevenlabs.client import ElevenLabs
import base64
import time
import uuid  
import os
#import json
#import firebase_admin
#from firebase_admin import credentials, db

# Firebase को कनेक्ट करें
#if not firebase_admin._apps:
   # cred = credentials.Certificate('firebase_key.json')
   # firebase_admin.initialize_app(cred, {
       # 'databaseURL': 'https://bajrangiram-jyotish-kendra-default-rtdb.firebaseio.com/'
   # })

# 📸 नया बैनर यहाँ से शुरू है
st.image("banner.png", use_container_width=True)
from io import BytesIO

# ✨ प्रीमियम हेडर: चमकते पीले बटन्स और ब्लैक स्टाइलिंग
st.markdown("""
    <style>
    div.stButton > button[key="search_popup_btn"],
    div.stButton > button[key="menu_category_btn"] {
        background-color: #000000 !important;
        color: #FFEB3B !important;
        font-weight: bold !important;
        border: 2px solid #FFEB3B !important;
        border-radius: 8px !important;
        width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #FFEB3B !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# हेडर टाइटल (अब इसे नया लुक दिया है)
# नया लेआउट: एक कॉलम में टाइटल, दूसरे में मेन्यू
col_title, col_menu = st.columns([3, 1])

with col_title:
    st.markdown("<h3 style='color:#8B0000; margin-top:0;'>ψ अंक में छिपा आपका भविष्य </h3>", unsafe_allow_html=True)

with col_menu:
    st.markdown("""
    <style>
    /* एक्सपेंडर को ट्रांसपेरेंट और सुंदर बनाएं */
    .stExpander { 
        background-color: #f0f2f6 !important; 
        border: 1px solid #ccc !important; 
        border-radius: 8px !important; 
        color: #333 !important;
    }
    
    /* टेक्स्ट का रंग काला करें ताकि साफ़ दिखे */
    .stRadio label {
        color: #333 !important;
        font-weight: 500;
    }
    
    /* मेन्यू हेडर का रंग */
    .streamlit-expanderHeader {
        color: #8B0000 !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)
    
    # 2. मेनू बार को एक्सपेंडर (बटन) में बदलें
# with col_menu:
#     with st.expander("☰ मेन्यू"):
        
#         menu_choice = st.radio("विकल्प चुनें", ["होम", "नामांक गणना", "मूलांक-भाग्यांक", "राजयोग", "मोबाइल विश्लेषण", "अबाउट अस"])
# # हेडर के ठीक नीचे एक सुंदर पतली विभाजक रेखा
# st.markdown("<hr style='margin-top:10px; margin-bottom:20px; border:1px solid #ddd;'>", unsafe_allow_html=True)



# --- यहाँ से आपका मेनू कंट्रोलर शुरू होता है ---

# if menu_choice == "होम":
#     st.write("बजरंगी राम अंक ज्योतिष केंद्र में आपका स्वागत है।")
#     # यहाँ अपना होम पेज का कंटेंट रखें

# elif menu_choice == "नामांक गणना":
#     st.subheader("नामांक गणना")
#     # यहाँ अपना नामांक वाला सारा कोड (इनपुट/बटन) पेस्ट कर दें

# elif menu_choice == "मूलांक-भाग्यांक":
#     st.subheader("मूलांक-भाग्यांक फल")
#     # यहाँ अपना मूलांक वाला सारा कोड पेस्ट कर दें

# elif menu_choice == "राजयोग":
#     st.subheader("राजयोग विश्लेषण")
#     # यहाँ राजयोग वाला कोड पेस्ट करें

# elif menu_choice == "मोबाइल विश्लेषण":
#     st.subheader("मोबाइल नंबर विश्लेषण")
#     # यहाँ मोबाइल एनालिसिस वाला कोड पेस्ट करें

# elif menu_choice == "अबाउट अस":
#     st.subheader("हमारे बारे में")
#     st.write("यह ऐप ज्योतिष शास्त्र की गणना में सहायता के लिए बनाया गया है।")

    # टैब का निर्माण (जैसा आपने फोटो में चाहा था)
# tab_1, tab_2 = st.tabs(["📂 Search", "➕ New"])

# with tab_1:
#     st.subheader("🔍 ग्राहक खोजें")
    
#     # Firebase से डेटा सर्च करने का नया तरीका
#     query = st.text_input("नाम या मोबाइल से खोजें...", key="search_bar")
    
#     if query:
#         try:
#             # Firebase से सारा डेटा लाएं
#             #ref = db.reference('/')
#             all_users = ref.get()
            
#             if all_users:
#                 # सर्च लॉजिक (नाम या मोबाइल के आधार पर)
#                 results = [user for user in all_users.values() if 
#                            query.lower() in str(user.get('name', '')).lower() or 
#                            query in str(user.get('mobile', ''))]
                
#                 if results:
#                     for entry in results:
#                         btn_label = f"👤 {entry.get('name')} | {entry.get('mobile')}"
#                         if st.button(btn_label, key=f"btn_{entry.get('mobile')}"):
#                             st.session_state['u_name'] = entry.get('name')
#                             st.session_state['u_phone'] = entry.get('mobile')
#                             st.rerun()
#                 else:
#                     st.warning("कोई रिकॉर्ड नहीं मिला।")
#             else:
#                 st.info("डेटाबेस अभी खाली है।")
#         except Exception as e:
#             st.error(f"सर्च करने में समस्या: {e}")
# with tab_2:
#     st.subheader("➕ नया विवरण भरें")
    
#     # Reset बटन का लॉजिक
# if st.button("🔄 नया फॉर्म साफ़ करें (Reset)"):
    # सभी कीज़ को खाली करें
    # st.session_state['u_name'] = ""
    # st.session_state['u_phone'] = ""
    # st.session_state['u_dob'] = datetime.date(2000, 1, 1) # डिफ़ॉल्ट तारीख
    # st.session_state['u_gender'] = "Male"
    
    # # पेज को री-रन करें
    # st.rerun()

    # इसके बाद आपका पुराना फॉर्म वाला कोड (नाम, जन्मतिथि, आदि) जारी रहेगा
    # सुनिश्चित करें कि आपके इनपुट फील्ड्स में key='u_name', key='u_phone' आदि दिए हुए हैं।
def bol_web(text, part_id):
    try:
        # 1. टेक्स्ट को साफ़ करना
        clean_text = text.replace("*", "").replace("#", "")
        
        # 2. ElevenLabs API सेट करना
        client = ElevenLabs(api_key="sk_1725e586c5ab003998eb1112c392b1f9b67d363fe0299bb8")
        
        # 3. Shivank की आवाज़ से ऑडियो बनाना (नया अपडेटेड मेथड)
        audio_stream = client.text_to_speech.convert(
            text=clean_text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2"
        )
        
        audio_bytes = b"".join(audio_stream)
        
        # 4. ऑडियो प्ले करना
        st.markdown("#### 🗣️ भविष्य रिपोर्ट सुनने के लिए यहाँ नीचे क्लिक करें:")
        st.audio(audio_bytes, format="audio/mp3")
        
    except Exception as e:
        st.error(f"ऑडियो जनरेट करने में समस्या आई: {e}")
# =====================================================================
# 🗄️ ग्राहकों का विवरण हमेशा के लिए सेव रखने का तिजोरी लॉजिक (JSON Database)
# =====================================================================
DB_FILE = "kundli_database.json"

        # फाइल में वापस सेव करें
# नया फंक्शन: डेटा को Firebase Realtime Database में सेव करने के लिए
import datetime # यह import सुनिश्चित करें कि फाइल में सबसे ऊपर हो

# def save_to_database(mobile, name, dob, gender):
#     # आज की तारीख निकालें
#     today_date = datetime.date.today().strftime("%d-%m-%Y")
    
#     # डेटा तैयार करें (तारीख के साथ)
#     user_data = {
#         'name': str(name),
#         'dob': str(dob),
#         'gender': str(gender),
#         'date': today_date  # यह लाइन आपके एडमिन पैनल का आधार बनेगी
#     }
    
#     # Firebase में सेव करें
#     #3ref = db.reference('users')
#     ref.child(str(mobile)).set(user_data)
def get_single_digit(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

 # यहाँ अपना नया सर्च फंक्शन पेस्ट करें
# def search_by_name(target_name):
#     # Firebase से डेटा लाने के लिए
#     #ref = db.reference('users')
#     all_users = ref.get() 
    
#     if all_users:
#         results = []
#         for mobile, details in all_users.items():
#             # अगर नाम मिलता है, तो उसे रिजल्ट में जोड़ें
#             if target_name.lower() in details.get('name', '').lower():
#                 details['mobile'] = mobile # मोबाइल नंबर भी साथ जोड़ दें
#                 results.append(details)
#         return results if results else "❌ कोई रिकॉर्ड नहीं मिला!"
#     return "❌ डेटाबेस खाली है!"
 

chaldean_table = {'A':1,'I':1,'J':1,'Q':1,'Y':1,'B':2,'K':2,'R':2,'C':3,'G':3,'L':3,'S':3,'D':4,'M':4,'T':4,'E':5,'H':5,'N':5,'X':5,'U':6,'V':6,'W':6,'O':7,'Z':7,'F':8,'P':8}
# ४. ८१ कॉम्बिनेशन (उदाहरण के लिए)
faladesh_dict = {
    "1-1": " 1 no. jo surya ka hai, Surya aur Surya ka yog. Aap ek janmjaat neta hain. Shasan aur prashasan mein safalta mile. समाज में प्रतिष्ठा बढ़ती है और लोग आपकी बात मानते हैं।करियर में सफलता: सरकारी नौकरी के योग बनते हैं और नौकरी-व्यवसाय में उच्च पद की प्राप्ति होती है।",
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
    "9-6": "Mangal aur Shukra. Akarshan aur junoon. Media ya luxury mein safal. मूलांक 9 के कारण आप निर्भीक, साहसी और ऊर्जा से भरपूर हैं।आकर्षक और कलात्मक: भाग्यांक 6 आपको रचनात्मक, कलात्मक और लोगों को आकर्षित करने वाला व्यक्तित्व देता है। आप दूसरों की मदद करने के लिए हमेशा तत्पर रहते हैं और मानवतावादी दृष्टिकोण रखते हैं।",
    "9-7": "Mangal aur Ketu. Doctor ya Engineer banne ke yog. Sahas bahut zyada.",
    "9-8": "Mangal aur Shani. Sangharsh ke baad sthayi safalta. Property mein labh.",
    "9-9": "Double Mangal. Aseem urja. Hanuman ji ki bhakti se sab safal hoga."
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
st.header("📋 विवरण भरें")
import datetime
# --- इनपुट विभाग (Input Section) ---

# १. नाम के लिए (Placeholder के साथ)
u_name = st.text_input("आपका शुभ नाम", key="u_name")
# २. आज की तारीख और रेंज सेट करना
today = datetime.date.today()
hundred_years_ago = today.year - 100
hundred_years_ahead = today.year + 100

# इसे पेस्ट करें (लाइन 401-406 की जगह):
u_dob = st.date_input("अपनी जन्मतिथि चुनें", key="u_dob", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())

u_gender = st.selectbox("लिंग", ["Male", "Female"], key="u_gender")


# 📱 मोबाइल नंबर इनपुट बॉक्स (पुराने रिकॉर्ड से डेटा लोड करने की क्षमता के साथ)
# यहाँ से पेस्ट करना शुरू करें:
# मोबाइल नंबर का इनपुट फील्ड
# नंबर के लिए नया और सटीक इनपुट फील्ड
if 'u_phone' not in st.session_state:
    st.session_state.u_phone = ""

import re

u_phone = st.text_input("अपना पंजीकृत मोबाइल नंबर भरें...", key="phone_key")

# अब पूरे कोड में जहाँ भी मोबाइल नंबर की ज़रूरत हो, 
# वहां st.session_state.u_phone का उपयोग करें।

# === विवरण सुरक्षित करने का बटन ===
# विवरण सुरक्षित करने का बटन


#     # विवरण सुरक्षित करने का बटन
# if st.button("अपना विवरण सुरक्षित करें"):
#     if u_name and u_phone:
#         try:
#             # Firebase में डेटा सेव करें (मोबाइल नंबर को ID की तरह उपयोग करें)
#             ref = db.reference(f'/{u_phone}')
#             ref.set({
#                 'name': u_name,
#                 'dob': str(u_dob),
#                 'gender': u_gender,
#                 'mobile': u_phone
#             })
#             st.success(f"{u_name} का विवरण सफलतापूर्वक सुरक्षित कर लिया गया है!")
#             st.balloons()
#             import time
#             time.sleep(2)
#             st.rerun()
#         except Exception as e:
#             st.error(f"डेटा सेव करने में समस्या: {e}")
#     else:
#         st.warning("कृपया नाम और मोबाइल नंबर जरूर भरें।")
# ====================================================================
col1, col2 = st.columns([1, 1])

with col1:
    # 2. विवरण देखें सबमिट बटन
    submit = st.button("👁️ विवरण देखें", use_container_width=True)

with col2:
    my_contact_number = "+916392311093" # यहाँ अपना 10 अंकों का नंबर लिखें

    call_html = f'''
    <a href="tel:{my_contact_number}" style="text-decoration: none;">
        <button style="
            width: 100%;
            background-color: #FF4B4B;
            color: white;
            border: none;
            padding: 0.8rem;
            border-radius: 0.5rem;
            cursor: pointer;
            font-weight: bold;
            font-size: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;">
            📞 सूक्ष्म गणना हेतु Call Now
        </button>
    </a>
    '''
    st.markdown(call_html, unsafe_allow_html=True)

if submit:
    # 1. सीधे इनपुट बॉक्स (u_phone) से ऑटो-फ़िल वाली वैल्यू उठाएं
    raw_val = str(u_phone) if u_phone else ""
    
    # 2. केवल 0-9 डिजिट्स निकालें (स्पेस, +91 या ब्रैकेट हटाएँ)
    cleaned_phone = re.sub(r'\D', '', raw_val)
    
    # 3. अगर 10 से ज़्यादा अंक हैं तो आख़िरी 10 अंक लें
    if len(cleaned_phone) > 10:
        cleaned_phone = cleaned_phone[-10:]
        
    # 4. साफ़ किया हुआ नंबर सेशन स्टेट में सेव करें
    st.session_state.u_phone = cleaned_phone

    # 5. अगर 10 अंक नहीं हैं तो एरर दिखाएं
    if len(cleaned_phone) != 10:
        st.error("⚠️ कृपया गणना के लिए 10 अंकों का सही मोबाइल नंबर भरें।")
    else:
        st.balloons()
        placeholder = st.empty()
        welcome_text = f"🚩 जय श्री राम {u_name} जी! आपकी ज्योतिषीय गणना की जा रही है..."
        typed = ""
        for char in welcome_text:
            typed += char
            placeholder.markdown(f"<div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; font-size: 18px; font-weight: bold; text-align: center; color: #1e3d59;'>{typed}</div>", unsafe_allow_html=True)
            time.sleep(0.02)
        d, m, y = u_dob.day, u_dob.month, u_dob.year
        mulank = get_single_digit(d)
        bhagyank = get_single_digit(d + m + y)
        name_val = sum(chaldean_table.get(c.upper(), 0) for c in u_name if c.isalpha())
        name_num = get_single_digit(name_val)
        
        y_sum = get_single_digit(y)
        kua = get_single_digit(11 - y_sum) if u_gender == "Male" else get_single_digit(y_sum + 4)
            # पहले पेज की गणना के तुरंत बाद इसे मेमोरी (Session State) में सेव करें
        st.session_state['user_logged_in'] = True
        st.session_state['app_mulank'] = mulank
        st.session_state['app_bhagyank'] = bhagyank
        st.session_state['app_user_name'] = u_name
        
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
        # 1. ग्रहों की जानकारी (रंग और दिन)
        grah_deta = {
            1: {"grah": "सूर्य", "day": "रविवार", "color": "नारंगी या सुनहरा"},
            2: {"grah": "चंद्रमा", "day": "सोमवार", "color": "सफेद या सिल्वर"},
            3: {"grah": "गुरु", "day": "गुरुवार", "color": "पीला"},
            4: {"grah": "राहु", "day": "शनिवार", "color": "नीला या भूरा"},
            5: {"grah": "बुध", "day": "बुधवार", "color": "हरा"},
            6: {"grah": "शुक्र", "day": "शुक्रवार", "color": "चमकीला सफेद या गुलाबी"},
            7: {"grah": "केतु", "day": "मंगलवार", "color": "चितकबरा या स्लेटी"},
            8: {"grah": "शनि", "day": "शनिवार", "color": "काला या गहरा नीला"},
            9: {"grah": "मंगल", "day": "मंगलवार", "color": "लाल"}
        }
        # मूलांक और भाग्यांक का संबंध निकालना
        m_rel = friendship_logic.get(mulank, {}).get('friends', [])
        m_enm = friendship_logic.get(mulank, {}).get('enemies', [])    
        # --- Yeh lines bilkul shuruat se likhi honi chahiye (0 spaces) ---
        # डुप्लिकेट्स को संभालने के लिए लिस्ट का उपयोग
        dob_digits = [int(n) for n in u_dob.strftime('%d%m%Y') if n != '0']
    
        col1, col2 = st.columns([1, 1])

        # --- बायाँ कॉलम (कॉलम 1): मूलांक, भाग्यांक आदि कार्ड ---
        with col1:
            st.markdown(f"""
                <div style='background-color: #f0f2f6; padding: 12px; border-radius: 10px; border-left: 4px solid #E74C3C;'>
                    <h5 style='margin: 0; color: #E74C3C; font-size: 15px;'>मूलांक: {mulank}</h5>
                    <h5 style='margin: 6px 0; color: #1E90FF; font-size: 15px;'>भाग्यांक: {bhagyank}</h5>
                    <h5 style='margin: 6px 0; color: #2ECC71; font-size: 15px;'>नामांक: {name_num}</h5>
                    <h5 style='margin: 6px 0 0 0; color: #8E44AD; font-size: 15px;'>कुआं नंबर: {kua}</h5>
                </div>
            """, unsafe_allow_html=True)

        # --- ग्रिड मैपिंग और लॉजिक ---
        grid_pos = {4:(0,0), 9:(0,1), 2:(0,2), 3:(1,0), 5:(1,1), 7:(1,2), 8:(2,0), 1:(2,1), 6:(2,2)}
        display_grid = [[[] for _ in range(3)] for _ in range(3)]

        # १. DOB के नंबर (Black)
        for n in dob_digits:
            if n in grid_pos:
                r, c = grid_pos[n]
                display_grid[r][c].append(f"<span style='color:black;'>{n}</span>")

        # २. विशेष नंबरों को जोड़ना (Colors)
        special_nums = [(mulank, "#E74C3C"), (bhagyank, "#1E90FF"), (name_num, "#2ECC71"), (kua, "#8E44AD")]
        for num, color in special_nums:
            if num in grid_pos:
                r, c = grid_pos[num]
                display_grid[r][c].append(f"<span style='color:{color};'>{num}</span>")

        # --- दायाँ कॉलम (कॉलम 2): लो-शू ग्रिड टेबल ---
        with col2:
            st.markdown("##### 🗓️ लो-शू ग्रिड")
            
            grid_rows_html = ""
            for row in display_grid:
                grid_rows_html += "<tr style='height:40px;'>"
                for cell_list in row:
                    content = " ".join(cell_list) if cell_list else "&nbsp;"
                    grid_rows_html += f"<td style='border:2px solid #E74C3C; width:33%; height:40px; background-color:#FFFDF0; font-size:16px; font-weight:bold; text-align:center; vertical-align:middle;'>{content}</td>"
                grid_rows_html += "</tr>"

            html_grid = f"""
            <table style="width:100%; height:130px; border-collapse:collapse; margin-top:5px; background-color:#FFFDF0;">
                {grid_rows_html}
            </table>
            """
            st.markdown(html_grid, unsafe_allow_html=True)
                
            # १. ८१ कॉम्बिनेशन का फल निकालना
            comb_key = f"{mulank}-{bhagyank}"
            comb_fal = faladesh_dict.get(comb_key, "आपके मूलांक और भाग्यांक का तालमेल उत्तम है।")

            # २. मिसिंग नंबर और उपाय
            all_present_nums = set(dob_digits) | {mulank, bhagyank, name_num, kua}
            missing_nums = [n for n in range(1, 10) if n not in all_present_nums]
    # --- राजयोग चेक करने का लॉजिक ---
        
            active_rajyog = []
            # चेक करने के लिए सभी ८ कॉम्बिनेशन
            planes = [
                ([4, 9, 2], "4-9-2"), ([3, 5, 7], "3-5-7"), ([8, 1, 6], "8-1-6"), # Horizontal
                ([4, 3, 8], "4-3-8"), ([9, 5, 1], "9-5-1"), ([2, 7, 6], "2-7-6"), # Vertical
                ([4, 5, 6], "4-5-6"), ([2, 5, 8], "2-5-8")                       # Diagonal
            ]
            
            rajyog_fal = {
            "मानसिक शक्ति राजयोग (4-9-2)": "अंक ज्योतिष (Numerology) में 'मानसिक राजयोग' या 'राजयोग' का अर्थ जन्मतिथि के उन दुर्लभ और शक्तिशाली संयोजनों से है जो व्यक्ति को बिना अत्यधिक संघर्ष के अपार सफलता, धन, पद और मानसिक शांति प्रदान करते हैं। आपकी सोचने की शक्ति और मेमोरी बहुत तेज है। आप मानसिक कार्यों में बहुत सफल होते हैं।",
            "इच्छा शक्ति राजयोग (3-5-7)": "अंक ज्योतिष में इच्छा शक्ति का सीधा संबंध व्यक्ति के मानसिक बल और लक्ष्यों के प्रति दृढ़ संकल्प से होता है। आपकी संकल्प शक्ति बहुत मजबूत है। आप जो ठान लेते हैं, उसे पूरा करके ही दम लेते हैं।",
            "कर्म शक्ति राजयोग (8-1-6)": "आप अत्यंत परिश्रमी हैं। आपका कर्म ही आपकी सफलता का मुख्य आधार बनता है। ऐसे लोगों को अपने जीवन में बड़ी उपलब्धियां प्राप्त होती हैं।  इस राजयोग के प्रभाव से व्यक्ति में अद्भुत निर्णय लेने की शक्ति और नेतृत्व का गुण आता है। समाज में मान-सम्मान और अत्यधिक प्रसिद्धि मिलने का यह एक प्रमुख अंक ज्योतिषीय योग है।s",
            "विचार शक्ति राजयोग (4-3-8)": "आप योजना बनाने में माहिर हैं। आपकी दूरदर्शिता आपको व्यापार और करियर में लाभ दिलाती है।",
            "सफलता राजयोग (9-5-1)": "यह एक अत्यंत शुभ योग है जो जीवन के हर क्षेत्र में नाम, प्रसिद्धि और सफलता दिलाता है।",
            "संतान और संपन्नता (2-7-6)": "यह योग सुखी पारिवारिक जीवन, अच्छी संतान और भौतिक सुख-सुविधाओं का संकेत देता है।",
            "गोल्डन राजयोग (4-5-6)": "यह लो-शू ग्रिड का सबसे शक्तिशाली योग है, जो अपार धन और भाग्य लेकर आता है।",
            "सिल्वर राजयोग (2-5-8)": "यह योग संपत्ति और जमीन-जायदाद के मामले में बहुत शुभ फल प्रदान करता है।"
            }

            report_parts = [
                f"✨ जय बजरंगी! स्वागत है **{u_name}** जी। आपका बजरङ्गिराम अंक ज्योतिष में स्वागत है ",
                f"✨ जय बजरंगी! स्वागत है **{u_name}** जी। आपका बजरङ्गिराम अंक ज्योतिष में स्वागत है ",
                f"🔸 आपका **मूलांक {mulank}** और **भाग्यांक {bhagyank}** है।",
                f"🔸 आपका **नामांक {name_num}** और **कुआ नंबर {kua}** है।",
                f"🔮 **विशेष फल:** {comb_fal}"
                    ]
            # ४. राजयोग का फल जोड़ना
                    # टैब्स को मोबाइल फ्रेंडली और सुंदर बनाने के लिए नया CSS
            
               
                            
            # ६. 🎤 ऑडियो स्क्रिप्ट (जो सब कुछ बोलकर बताएगा)
            audio_script = f"जय बजरंगबली {u_name} जी। आपका बजरङ्गिराम अंक ज्योतिष में स्वागत है  "
            audio_script += f"आपका मूलांक {mulank} और भाग्यांक {bhagyank} है। "
            audio_script += f"नामांक {name_num} और कुआ नंबर {kua} है। "
            audio_script += f"आपके ग्रहों का फल कहता है कि {comb_fal}। "
            if active_rajyog:
                audio_script += " आपके ग्रिड में विशेष राजयोग भी बन रहे हैं। "
                for ry in active_rajyog:
                    audio_script += f"{ry} "
                    # --- यहाँ रखें st.session_state वाला हिस्सा ---
                st.session_state['u_name'] = u_name
                st.session_state['dob_digits'] = dob_digits
                st.session_state['missing_nums'] = missing_nums
                st.session_state['name_num'] = name_num

        # ====================================================
            # 🎯 हेडर + एनिमेटेड एरो कोड
            # ====================================================
            कैटेगरी_हेडर_एचटीएमएल = """
            <style>
            @keyframes colorChangeHeader {
                0% { color: #dc2626; text-shadow: 0 0 10px rgba(220, 38, 38, 0.4); }
                33% { color: #d97706; text-shadow: 0 0 10px rgba(217, 119, 6, 0.4); }
                66% { color: #2563eb; text-shadow: 0 0 10px rgba(37, 99, 235, 0.4); }
                100% { color: #16a34a; text-shadow: 0 0 10px rgba(22, 163, 74, 0.4); }
            }
            .category-header-text {
                font-size: 26px !important;
                font-weight: 900 !important;
                text-align: center !important;
                animation: colorChangeHeader 4s infinite alternate !important;
                margin-bottom: 2px !important;
                letter-spacing: 0.5px !important;
            }
            @keyframes bounceUpDown {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(8px); }
            }
            .bouncing-arrow {
                display: inline-block !important;
                font-size: 22px !important;
                animation: bounceUpDown 1.2s infinite ease-in-out !important;
            }
            </style>

            <div style="text-align: center; margin-bottom: 8px;">
                <div class="category-header-text">✨ अपनी कैटेगरी चुनें ✨</div>
                <div class="bouncing-arrow">👇</div>
            </div>
            """
            st.markdown(कैटेगरी_हेडर_एचटीएमएल, unsafe_allow_html=True)

                        # ====================================================
            # 🌟 लाइट, आकर्षक एवं लाइव रंग बदलने वाला प्रीमियम CSS
            # ====================================================
            जादुई_कैटेगरी_स्टाइल = """
            <style>
            /* १. मुख्य बाहरी डिब्बा (२-२ बटनों के लिए ग्रिड) */
            .stTabs [data-baseweb="tab-list"] {
                display: flex !important;
                flex-wrap: wrap !important;
                gap: 10px !important;
                width: 100% !important;
                justify-content: space-between !important;
                background: transparent !important;
                padding: 5px 0px !important;
                border: none !important;
            }

            /* २. एनिमेटेड अन-सिलेक्टेड कैटेगरी बटन्स */
            .stTabs [data-baseweb="tab"] {
                flex: 1 1 calc(50% - 10px) !important;
                min-width: 140px !important;
                min-height: 55px !important;
                background: #ffffff !important;
                border: 2px solid #3b82f6 !important;
                border-radius: 12px !important;
                box-shadow: 0px 4px 12px rgba(59, 130, 246, 0.15) !important;
                transition: all 0.3s ease-in-out !important;
                padding: 8px 6px !important;
                justify-content: center !important;
                animation: pulseGlow 2.5s infinite alternate !important; /* बटन्स के लिए एनिमेशन */
            }

            /* बटन्स के लिए ग्लोइंग एनिमेशन प्रभाव */
            @keyframes pulseGlow {
                0% {
                    border-color: #3b82f6;
                    box-shadow: 0px 2px 8px rgba(59, 130, 246, 0.2);
                    transform: scale(0.99);
                }
                50% {
                    border-color: #ec4899;
                    box-shadow: 0px 4px 15px rgba(236, 72, 153, 0.4);
                    transform: scale(1.02);
                }
                100% {
                    border-color: #8b5cf6;
                    box-shadow: 0px 2px 8px rgba(139, 92, 246, 0.2);
                    transform: scale(0.99);
                }
            }

            /* ३. बटनों के अक्षरों का डिज़ाइन (मोटा, बड़ा और स्पष्ट फ़ॉन्ट) */
            .stTabs [data-baseweb="tab"] div,
            .stTabs [data-baseweb="tab"] p,
            .stTabs [data-baseweb="tab"] span {
                color: #1e293b !important;
                font-weight: 800 !important;
                font-size: 16px !important;
                white-space: normal !important;
                text-align: center !important;
                line-height: 1.2 !important;
            }

            /* ४. जो टैब सिलेक्ट होगा (Active Tab) - वो और भी ज़्यादा चमकेगा */
            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
                border: 2px solid #ffffff !important;
                animation: activeGlow 1.8s infinite alternate !important;
            }

            .stTabs [aria-selected="true"] div,
            .stTabs [aria-selected="true"] p,
            .stTabs [aria-selected="true"] span {
                color: #ffffff !important;
                text-shadow: 0px 1px 3px rgba(0, 0, 0, 0.3) !important;
            }

            @keyframes activeGlow {
                0% { box-shadow: 0 0 8px #2563eb; }
                100% { box-shadow: 0 0 18px #2563eb, 0 0 8px #ec4899; }
            }

            /* ५. नीचे की पतली रेड लाइन हटाना */
            .stTabs [data-baseweb="tab-highlight"] {
                display: none !important;
            }

            /* ६. बटनों का साइज़ और अक्षरों को बड़ा करना (Large Tabs) */
            .stTabs [data-baseweb="tab"] {
                min-height: 65px !important;
                padding: 12px 10px !important;
            }

            .stTabs [data-baseweb="tab"] div,
            .stTabs [data-baseweb="tab"] p,
            .stTabs [data-baseweb="tab"] span {
                font-size: 19px !important;
                font-weight: 900 !important;
            }
            </style>
            """

            st.markdown(जादुई_कैटेगरी_स्टाइल, unsafe_allow_html=True)
                        # Ab aapke purane tabs yahan se shuru honge
                    # यहाँ हमने चौथा टैब "📱 मोबाइल नंबर विचार" नाम से जोड़ दिया है
                    # 'key="current_active_tab"' जोड़ने से स्ट्रीमलिट याद रखेगा कि यूजर किस टैब पर था
            
            tab1, tab2, tab3, tab4 = st.tabs(["⬜ मूलांक-भाग्यांक फल", "👤 नाम-भाग्य विचार", "🔳 ग्रिड एवं उपाय", "📱 मोबाइल नंबर विचार"], key="active_numerology_tab")

        

            with tab1:

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
            with tab2:
                st.subheader("🔮 गुरु का वैज्ञानिक परामर्श")
                
                # name_sum ko define karna taaki peeli line hat jaye
                if 'name_sum' not in locals() and 'name_sum' not in globals():
                    name_sum = name_num 

                def get_g_n(n):
                    return grah_deta.get(int(n), {}).get('grah', 'अंक')

                # Mulank aur Bhagyank ke liye grah ka naam
                n_g, m_g, b_g = get_g_n(name_num), get_g_n(mulank), get_g_n(bhagyank)
                tab2_audio = f"Namaste! Aapka namank {name_num} hai jo {n_g} ka ank hai. "

                # 1. Sanyukt Namank ka Phal (Compound Number Logic)
                if name_sum > 1:
                    # === ३.५ कम्पाउंड नंबर (Compound Number) का फलकथन और ऑडियो स्क्रिप्ट ===
                    st.markdown("<p style='font-size: 22px; font-weight: bold; color: #1F618D;'>🔢 Compound Number (संयुक्त अंक) का फल</p>", unsafe_allow_html=True)
                    # 'name_val' वेरिएबल से नाम का कुल योग लेकर कम्पाउंड फल निकालना
                    compound_num = name_val
                    compound_fal = compound_master_81.get(compound_num, "इस संयुक्त अंक का फल अभी उपलब्ध नहीं है।")
                    
                    # स्क्रीन पर दिखाना
                    st.info(f"**आपका संयुक्त अंक {compound_num} है:** {compound_fal}")
                    
                    # ऑडियो स्क्रिप्ट तैयार करना (ताकि अंत में गुरु इसे बोलकर सुनाएं)
                    # लाइन नंबर 734 को ऐसा बदलें:
                    compound_audio_text = f"{u_name} जी, आपके नाम के अक्षरों का कुल योग, यानी आपका संयुक्त..."
                    
                    # इसे टैब ३ के मुख्य ऑडियो वेरिएबल में जोड़ना (बिना पुराना डेटा हटाए)
                    tab2_audio += compound_audio_text

                    st.divider()
                    
                    # 2. Maitree Analysis (Grah aur Ank ke Naam ke Saath)
                    st.subheader(f"📊 अंक मैत्री विवरण: {name_num} ({n_g})")
                    m_en = friendship_logic.get(int(mulank), {}).get('enemies', [])
                    b_en = friendship_logic.get(int(bhagyank), {}).get('enemies', [])

                    shatru_list = []
                    if name_num in m_en: shatru_list.append(f"मूलांक {mulank} ({m_g})")
                    if name_num in b_en: shatru_list.append(f"भाग्यांक {bhagyank} ({b_g})")

                    if not shatru_list:
                        msg = f"नामांक {name_num} ({n_g}), मूलांक {mulank} ({m_g}) और भाग्यांक {bhagyank} ({b_g}) दोनों का मित्र है।"
                        st.success(f"✅ {msg}")
                        tab2_audio += f"{msg} "
                    else:
                        msg = f"नामांक {name_num} ({n_g}) आपके {' और '.join(shatru_list)} का शत्रु है।"
                        st.error(f"❌ {msg}")
                        tab2_audio += f"{msg} "

                    st.write("---")

                    # 3. Rajyog Logic (Mangal 9 ko prathmikta)
                    st.subheader("💡 गुरु का विशेष राजयोग सुझाव")
                    # यहाँ हम यूज़र के सभी शुद्ध अंकों को एक साथ मिला रहे हैं
                    शुद्ध_अंक_स्ट्रिंग = str(mulank) + str(bhagyank) + str(name_num)
                    
                    # यदि आपने कुआ नंबर भी ग्रिड में जोड़ा है, तो उसे भी यहाँ शामिल कर लें:
                    if 'kua_num' in locals() or 'kua_num' in globals():
                        शुद्ध_अंक_स्ट्रिंग += str(kua)
                        
                    # अगर आपके पास जन्मतिथि के अंकों की कोई शुद्ध स्ट्रिंग (जैसे 'dob_digits') है, तो उसे भी जोड़ सकते हैं:
                    if 'dob_digits' in locals() or 'dob_digits' in globals():
                        शुद्ध_अंक_स्ट्रिंग += str(dob_digits)
                    # यूज़र के पास जितने भी असली अंक मौजूद हैं, उनकी एक शुद्ध लिस्ट
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
                
                    st.subheader("⚠️ अत्यधिक पुनरावृत्ति एवं ऊर्जा असंतुलन")
                    
                    has_overactive = False
                    
                    # १ से ९ तक के सभी अंकों की बिल्कुल शुद्ध और सटीक जांच
                    for num in range(1, 10):
                        count_in_grid = शुद्ध_अंक_स्ट्रिंग.count(str(num))
                        
                        # यदि कोई अंक २ से अधिक बार आया है (३ या उससे ज़्यादा बार)
                        if count_in_grid > 2:
                            has_overactive = True
                            grah_name = get_g_n(num)
                            
                            # पूर्णतः हिंदी में चेतावनी बॉक्स
                            st.warning(f"✨ **अंक {num} ({grah_name})** आपकी ग्रिड में **{count_in_grid} बार** आया है।")
                            
                            # पूर्णतः हिंदी में असंतुलन का विवरण
                            st.write(
                                f"लो-शू ग्रिड में दो से अधिक बार मौजूद होने के कारण **{grah_name}** की शक्ति अत्यधिक बढ़ गई है, "
                                f"जिससे आपकी **ऊर्जा असंतुलित हो रही है**। इसे संतुलित करने के लिए कृपया विशेष ज्योतिषीय उपाय अपनाएं।"
                            )
                            
                            # ऑडियो स्क्रिप्ट (बैकएंड में गुरु के बोलने के लिए)
                            overactive_audio = f"Aapki grid mein ank {num} do se adhik baar aaya hai, jisse {grah_name} ki oorja asantulit ho rahi hai. Kripya is grah ke vishesh upaye karein. "
                            tab2_audio += overactive_audio

                    if not has_overactive:
                        # पूर्णतः हिंदी में सफलता का संदेश
                        st.success("🎯 आपकी ग्रिड में सभी ग्रहों की ऊर्जा संतुलित है। कोई भी ग्रह दो से अधिक बार नहीं आया है।")
                        tab2_audio += "Aapki grid mein sabhi grahon ki oorja santulit hai. "
                    # ==========================================
                    
                    # ३. ऑडियो प्ले करना
                    st.write("---")
                    contact_msg = "सुक्ष्म गाडना हेतु Vishal Vikram Pandey ji se संपर्क करे ."
                    st.info(f"📍 {contact_msg}")
                    tab2_audio += f" {contact_msg}"
                    bol_web(tab2_audio, "tab2_voice")
                    st.markdown("<p style='text-align: center; color: gray;'>आचार्य विशाल विक्रम पांडे</p>", unsafe_allow_html=True)

            with tab3:
                # १. ऑडियो वेरिएबल को शुरू करें
                tab3_audio = "प्रणाम! आपके चार्ट का विशेष विश्लेषण यहाँ दिया गया है। "

                # २. राजयोग की गणना (Calculation)
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

                # चेक करें कि कौन से राजयोग बन रहे हैं
                for p_nums, p_name in planes:
                    if all(num in all_present_nums for num in p_nums):
                        active_rajyog.append(p_name)

                # ३. राजयोग का फल दिखाना (Display)
                st.subheader("✨ आपके लो-शू ग्रिड के राजयोग")
                if active_rajyog:
                    tab3_audio += "सबसे पहले आपके चार्ट के राजयोगों की बात करते हैं। "
                    for ry in active_rajyog:
                        # डिक्शनरी से फल उठाना
                        fal = rajyog_fal.get(ry, "यह एक अत्यंत शुभ राजयोग है जो जीवन में प्रगति लाता है।")
                        
                        # स्क्रीन पर दिखाना
                        st.success(f"✅ **{ry}**")
                        st.info(f"📜 **फल:** {fal}")
                        
                        # ऑडियो में जोड़ना
                        tab3_audio += f"{ry}. {fal} "
                else:
                    st.write("वर्तमान ग्रिड में कोई पूर्ण राजयोग नहीं बन रहा है।")

                st.divider()

                # ४. मिसिंग नंबर्स (Missing Numbers) की गणना और उपाय
                st.subheader("🔍 मिसिंग नंबर्स और उपाय")
                
                # वर्तमान में मौजूद अंकों की लिस्ट
                all_present_nums = set(dob_digits) | {mulank, bhagyank, name_num, kua}
                missing_nums = [n for n in range(1, 10) if n not in all_present_nums]

                if missing_nums:
                    tab3_audio += "अब आपके चार्ट में मौजूद मिसिंग नंबरों के उपायों की चर्चा करते हैं। "
                    for n in missing_nums:
                        if n in remedy_info:
                            g = remedy_info[n]['grah']
                            u = remedy_info[n]['upay']
                            
                            # स्क्रीन पर दिखाना
                            st.warning(f"अंक {n} ({g}) अनुपस्थित है")
                            st.write(f"💡 **उपाय:** {u}")
                            
                            # ऑडियो में जोड़ना
                            tab3_audio += f"अंक {n} जो {g} का है, उसके लिए उपाय है: {u}। "

    # ५. अंत में ऑडियो प्लेयर (Optional)
        # st.audio(generate_audio(tab3_audio))
                if tab3_audio:
                    st.write("---")
                    # केवल एक स्लाइडर बनेगा जो राजयोग और उपाय दोनों बोलेगा
                    bol_web(tab3_audio, "graha_voice")
            import streamlit as st
    # ------------------ WITH TAB4 SECTION ------------------
        with tab4:
            st.header("📱 मोबाइल नंबर ज्योतिष विश्लेषण")
            st.write("अपने मोबाइल नंबर के भाग्य और अनुकूलता की गहरी जांच के लिए नीचे दिए गए बटन पर क्लिक करके विशेष विश्लेषण स्क्रीन पर जाएं।")
            
            # यह बटन सीधे 'pages' फोल्डर के अंदर रखी फाइल पर भेज देगा
            st.page_link("pages/mobile_jyotish.py", label="👉 मोबाइल नंबर विश्लेषण पेज पर जाएं", icon="📱")
                
        import streamlit as st

    # यह कोड आपके एडमिन पैनल या सेटिंग्स टैब के लिए है
    def admin_control_board():
        st.markdown("---")
        st.markdown("<h3 style='color: #ff6f00;'>⚙️ गुरु एडमिन कंट्रोल बोर्ड (Admin Panel)</h3>", unsafe_allow_html=True)
        
        # १. प्रति मिनट दर सेट करने का विकल्प
        st.subheader("1. कॉलिंग रेट मैनेजमेंट")
        if 'call_rate' not in st.session_state:
            st.session_state['call_rate'] = 21.00  # डिफ़ॉल्ट दर: 21 रुपये प्रति मिनट

        new_rate = st.number_input(
            "प्रति मिनट बातचीत की दर (INR / Minute) तय करें:", 
            min_value=1.0, 
            max_value=500.0, 
            value=float(st.session_state['call_rate']),
            step=1.0
        )
        st.session_state['call_rate'] = new_rate
        st.success(f"वर्तमान कॉलिंग दर: ₹{st.session_state['call_rate']}/मिनट सेट है।")

        st.markdown("---")

        # २. मैन्युअल रिचार्ज और मिनट कैलकुलेटर बोर्ड
        st.subheader("2. ग्राहक वॉलेट रिचार्ज केंद्र (Manual Entry)")
        
        # इनपुट फ़ील्ड्स
        cust_phone = st.text_input("ग्राहक का मोबाइल नंबर दर्ज करें:")
        recharge_amount = st.number_input("प्राप्त हुआ रिचार्ज अमाउंट (₹):", min_value=0, step=10)
        
        # गणना (Calculations)
        if recharge_amount > 0:
            # मिनट की गणना = राशि / प्रति मिनट दर
            available_minutes = int(recharge_amount / st.session_state['call_rate'])
            
            st.info(f"💡 **गणना:** ₹{recharge_amount} के रिचार्ज पर ग्राहक को **{available_minutes} मिनट** का टॉक-टाइम मिलेगा।")
            
            # रिचार्ज कन्फर्म करने का बटन
            if st.button("वॉलेट में मिनट जोड़ें और एक्टिवेट करें"):
                if cust_phone and len(cust_phone) == 10:
                    # १. एक ग्लोबल डिक्शनरी (तिजोरी) बनाना ताकि ऐप रिफ्रेश होने पर डेटा सुरक्षित रहे
                    if 'user_wallets' not in st.session_state:
                        st.session_state['user_wallets'] = {}
                    
                    # २. इस विशिष्ट मोबाइल नंबर के खाते में रिचार्ज राशि को सेव करना
                    st.session_state['user_wallets'][cust_phone] = float(recharge_amount)
                    
                    # ३. ग्राहक के मुख्य पेज के वेरिएबल (wallet_balance) में पैसे को ट्रांसफर करना
                    st.session_state['wallet_balance'] = float(recharge_amount)
                    
                    st.balloons()
                    st.success(f"सफलतापूर्वक! ग्राहक {cust_phone} का वॉलेट एक्टिव कर दिया गया है। कुल समय: {available_minutes} मिनट।")
                else:
                    st.error("कृपया पहले ग्राहक का 10 अंकों का सही मोबाइल नंबर दर्ज करें।")
    # मुख्य ऐप में इसे देखने के लिए बस इस फंक्शन को कॉल करें:
    # admin_control_board()
    # # Sidebar mein Admin Panel ka ek gupt option (sirf aapke liye)
    st.sidebar.markdown("---")
    show_admin = st.sidebar.checkbox("🔒 गुरु एडमिन लॉगिन (Admin View)")

    # Agar aap check-box par click karenge, tabhi dashboard screen par sabse niche khulega
    if show_admin:
        admin_control_board()