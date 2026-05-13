import streamlit as st
from datetime import date
from gtts import gTTS
import base64
import time
import uuid  
import os    
from io import BytesIO
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
       
        active_rajyog = []
        # चेक करने के लिए सभी ८ कॉम्बिनेशन
        planes = [
            ([4, 9, 2], "4-9-2"), ([3, 5, 7], "3-5-7"), ([8, 1, 6], "8-1-6"), # Horizontal
            ([4, 3, 8], "4-3-8"), ([9, 5, 1], "9-5-1"), ([2, 7, 6], "2-7-6"), # Vertical
            ([4, 5, 6], "4-5-6"), ([2, 5, 8], "2-5-8")                       # Diagonal
        ]
         
        rajyog_fal = {
        "मानसिक शक्ति राजयोग (4-9-2)": " 4  आपकी सोचने की शक्ति और मेमोरी बहुत तेज है। आप मानसिक कार्यों में बहुत सफल होते हैं।",
        "इच्छा शक्ति राजयोग (3-5-7)": "आपकी संकल्प शक्ति बहुत मजबूत है। आप जो ठान लेते हैं, उसे पूरा करके ही दम लेते हैं।",
        "कर्म शक्ति राजयोग (8-1-6)": "आप अत्यंत परिश्रमी हैं। आपका कर्म ही आपकी सफलता का मुख्य आधार बनता है।",
        "विचार शक्ति राजयोग (4-3-8)": "आप योजना बनाने में माहिर हैं। आपकी दूरदर्शिता आपको व्यापार और करियर में लाभ दिलाती है।",
        "सफलता राजयोग (9-5-1)": "यह एक अत्यंत शुभ योग है जो जीवन के हर क्षेत्र में नाम, प्रसिद्धि और सफलता दिलाता है।",
        "संतान और संपन्नता (2-7-6)": "यह योग सुखी पारिवारिक जीवन, अच्छी संतान और भौतिक सुख-सुविधाओं का संकेत देता है।",
        "गोल्डन राजयोग (4-5-6)": "यह लो-शू ग्रिड का सबसे शक्तिशाली योग है, जो अपार धन और भाग्य लेकर आता है।",
        "सिल्वर राजयोग (2-5-8)": "यह योग संपत्ति और जमीन-जायदाद के मामले में बहुत शुभ फल प्रदान करता है।"
        }

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

            # Ab aapke purane tabs yahan se shuru honge
        tab1, tab2, tab3 = st.tabs(["📑 मूलांक-भाग्यांक फल", "🔮 नाम-भाग्य विचार", "🎡 ग्रिड एवं उपाय"])      
                    

        with tab1:
            # १. डेटा को सुरक्षित रूप से निकालें
            m_data = grah_deta.get(mulank, {})
            b_data = grah_deta.get(bhagyank, {})

            # २. पहले से डिफाइन करें ताकि NameError न आए
            tab1_audio = f"नमस्ते {u_name} जी। आपके मूलांक और भाग्यांक का विश्लेषण तैयार है।"

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
                <h3 style="text-align: center; color: #1a508b; margin-top: 0;">🌟 आपके शुभ पैरामीटर्स</h3>
                <div class="flex-box">
                    <div class="info-col m-bg">
                        <h4 style="color: #1976d2; margin-top: 0;">मूलांक: {mulank} (स्वभाव)</h4>
                        <p><span class="label">🪐 ग्रह:</span> {m_data.get('grah', 'N/A')}</p>
                        <p><span class="label">📅 दिन:</span> {m_data.get('day', 'N/A')}</p>
                        <p><span class="label">🎨 रंग:</span> {m_data.get('color', 'N/A')}</p>
                        <p style="font-size: 12px; color: #666; font-style: italic;">उपयोग: दैनिक शांति व आत्मविश्वास हेतु।</p>
                    </div>
                    <div class="info-col b-bg">
                        <h4 style="color: #7b1fa2; margin-top: 0;">भाग्यांक: {bhagyank} (भाग्य)</h4>
                        <p><span class="label">🪐 ग्रह:</span> {b_data.get('grah', 'N/A')}</p>
                        <p><span class="label">📅 दिन:</span> {b_data.get('day', 'N/A')}</p>
                        <p><span class="label">🎨 रंग:</span> {b_data.get('color', 'N/A')}</p>
                        <p style="font-size: 12px; color: #666; font-style: italic;">उपयोग: करियर व बड़ी सफलताओं हेतु।</p>
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

            # ५. व्यक्तित्व का मुख्य आधार सेक्शन
            st.markdown("---")
            st.markdown(f"### 🌟 आपके व्यक्तित्व का मुख्य आधार")
            st.write(f"मूलांक **{mulank}** और भाग्यांक **{bhagyank}** का यह मेल आपके जीवन की दिशा तय करता है।")

            # ६. ऑडियो को कॉल करें (अगर bol_web फंक्शन बना हुआ है)
            bol_web(tab1_audio, "graha_voice")
               
        with tab2:
            st.header("🔮 गुरु का वैज्ञानिक परामर्श")
            
            # name_sum ko define karna taaki peeli line hat jaye
            if 'name_sum' not in locals() and 'name_sum' not in globals():
                name_sum = name_num 

            def get_g_n(n):
                return grah_deta.get(int(n), {}).get('grah', 'अंक')

            # Mulank aur Bhagyank ke liye grah ka naam
            n_g, m_g, b_g = get_g_n(name_num), get_g_n(mulank), get_g_n(bhagyank)
            t2_audio = f"Namaste! Aapka namank {name_num} hai jo {n_g} ka ank hai. "

            # 1. Sanyukt Namank ka Phal (Compound Number Logic)
            if name_sum > 9:
                st.subheader(f"🔢 संयुक्त नामांक {name_sum} का फल")
                f_d, s_d = int(str(name_sum)[0]), int(str(name_sum)[1])
                g1, g2 = get_g_n(f_d), get_g_n(s_d)
                
                # Sanyukt ank ke aapas ka sambandh
                rel = "मित्र" if s_d in friendship_logic.get(f_d, {}).get('friends', []) else "शत्रु" if s_d in friendship_logic.get(f_d, {}).get('enemies', []) else "सम"
                inf_msg = f"आपका संयुक्त नामांक {name_sum}, {g1} ({f_d}) और {g2} ({s_d}) के योग से बना है। ये आपस में {rel} हैं।"
                st.info(inf_msg)
                t2_audio += f"Aapka sanyukt namank {name_sum}, {g1} aur {g2} ke yog se bana hai, jo aapas mein {rel} hain. "
                
                c_f = compound_master_81.get(int(name_sum), "यह विशिष्ट ऊर्जा वाला अंक है।")
                st.success(f"**फल:** {c_f}")
                t2_audio += f"Iska phal hai: {c_f}. "

            st.write("---")

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
                t2_audio += f"{msg} "
            else:
                msg = f"नामांक {name_num} ({n_g}) आपके {' और '.join(shatru_list)} का शत्रु है।"
                st.error(f"❌ {msg}")
                t2_audio += f"{msg} "

            st.write("---")

            # 3. Rajyog Logic (Mangal 9 ko prathmikta)
            st.subheader("💡 गुरु का विशेष राजयोग सुझाव")
            priorities = [
                {'t': 9, 'others': [3, 6], 'name': "आध्यात्मिक प्लेन (3-6-9)"},
                {'t': 4, 'others': [5, 6], 'name': "गोल्डन राजयोग (4-5-6)"}
            ]

            for p in priorities:
                target = p['t']
                if target in missing_nums and all(x in grid_pos for x in p['others']):
                    t_grah = get_g_n(target)
                    # Check if it's safe (not enemy of mulank or bhagyank)
                    if target not in m_en and target not in b_en:
                        msg = f"{p['name']} पूरा करने हेतु {target} ({t_grah}) अपनाएं, यह आपके मूलांक {mulank} और भाग्यांक {bhagyank} का मित्र है।"
                        st.success(f"🌟 {msg}")
                        t2_audio += f"Sujhav hai ki {msg} "
                        break
                    else:
                        shatru_of = "मूलांक" if target in m_en else "भाग्यांक"
                        msg = f"अंक {target} ({t_grah}) {p['name']} बना सकता है, पर यह आपके {shatru_of} का शत्रु है, अतः न अपनाएं।"
                        st.warning(f"⚠️ {msg}")
                        t2_audio += f"Chetavni! {msg} "
                # ३. ऑडियो प्ले करना
                    if 'bol_web' in locals():
                        bol_web(tab1_audio, "graha_voice")
            # Contact Info [cite: 2025-06-12]
            st.write("---")
            contact_msg = "सुक्ष्म गाडना हेतु Vishal Vikram Pandey ji se संपर्क करे ."
            st.info(f"📍 {contact_msg}")
            t2_audio += f" {contact_msg}"
            
            bol_web(t2_audio, "tab2_voice")
            st.markdown("<p style='text-align: center; color: gray;'>आचार्य विशाल विक्रम पांडे</p>", unsafe_allow_html=True)

     
        with tab3:
            st.markdown("### 🌟 लो-शू ग्रिड और विस्तृत भविष्य फल")
            
            # 1. सबसे पहले ऑडियो वेरिएबल को परिभाषित (Define) करें
            tab3_audio = "प्रणाम! आपके चार्ट का विशेष विश्लेषण यहाँ दिया गया है। "

            # 2. अब grid_counts को परिभाषित करें ताकि पिछला Error न आए
            from collections import Counter
            grid_counts = Counter(dob_digits)
            for num in [mulank, bhagyank, name_num, kua]:
                grid_counts[num] += 1

            # 3. अब राजयोग की गणना (Calculation)
            active_rajyog = []
            planes = [
                ([4, 9, 2], "मानसिक शक्ति राजयोग (4-9-2)"),
                ([3, 5, 7], "इच्छा शक्ति राजयोग (3-5-7)"),
                ([8, 1, 6], "कर्म शक्ति राजयोग (8-1-6)"),
                ([4, 5, 6], "गोल्डन राजयोग (4-5-6)"),
                ([2, 5, 8], "सिल्वर राजयोग (2-5-8)")
            ]

            for plane_nums, plane_name in planes:
                if all(grid_counts.get(num, 0) > 0 for num in plane_nums):
                    active_rajyog.append(plane_name)

            # 4. अब आपका पुराना ऑडियो वाला हिस्सा (जो फोटो fe7396e7 में है)
            if active_rajyog:
                tab3_audio += "सबसे पहले आपके चार्ट के राजयोगों की बात करते हैं। "
                for ry in active_rajyog:
                    st.success(f"✅ {ry}")
                    tab3_audio += f"{ry}. "
            # 1. Sabse pehle audio variable ko start karein (Taki Error na aaye)
            tab3_audio = "प्रणाम! आपके चार्ट का विशेष विश्लेषण यहाँ दिया गया है। "

            # 2. Missing Numbers ki list taiyaar karein
            all_present_nums = set(dob_digits) | {mulank, bhagyank, name_num, kua}
            missing_nums = [n for n in range(1, 10) if n not in all_present_nums]

            # 3. Rajyog ka logic (Jo humne pehle discuss kiya tha)
            active_rajyog = []
            # ... (Yahan aapka planes wala loop rahega)

            # 4. Missing Numbers ka Audio aur Display
            if missing_nums:
                tab3_audio += "अब आपके चार्ट में मौजूद मिसिंग नंबरों के उपायों की चर्चा करते हैं। "
                for n in missing_nums:
                    if n in remedy_info:
                        g = remedy_info[n]['grah']
                        u = remedy_info[n]['upay']
                        st.info(f"🚩 **अंक {n} ({g}):** {u}") # Screen par dikhane ke liye
                        tab3_audio += f"अंक {n} जो {g} का है, उसके लिए उपाय है: {u}। " # Audio mein jodne ke liye        
                                
            # ३. उपायों को ऑडियो में जोड़ना
            if 'missing_nums' in locals():
                tab3_audio += "अब missing number के उपायों की चर्चा करते हैं। "
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
                
