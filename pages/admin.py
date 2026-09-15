import streamlit as st
import sqlite3

# साइडबार को पूरी तरह गायब रखने का कोड
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

def admin_page():
    st.title("🛡️ गुरु एडमिन कंट्रोल बोर्ड")
    st.write("---")
    
    # आपका 4 अंकों का टिपिकल पिन (इसे अपनी पसंद से बदल लें)
    ADMIN_PIN = "8953"  
    
    # सीधे पिन इनपुट
    pin_input = st.text_input("🔐 4 अंकों का एडमिन पिन दर्ज करें:", type="password", key="admin_pin_only")
    
    if pin_input == ADMIN_PIN:
        st.success("🎉 पिन सत्यापित! एडमिन पैनल में आपका स्वागत है।")
        st.write("---")
        
        # मुख्य पेज पर वापस जाने का बटन
        if st.button("⬅️ वापस मुख्य ऐप पर जाएँ"):
            st.switch_page("app.py")
            
        st.subheader("📋 बुक किए गए अपॉइंटमेंट की सूची")
        
        # सर्च बार
        search_query = st.text_input("🔍 नाम या मोबाइल नंबर से खोजें...")
        
        try:
            conn = sqlite3.connect("appointments.db")
            cursor = conn.cursor()
            
            if search_query:
                cursor.execute('''
                    SELECT name, dob, gender, phone, created_at 
                    FROM appointments 
                    WHERE name LIKE ? OR phone LIKE ? 
                    ORDER BY id DESC
                ''', (f'%{search_query}%', f'%{search_query}%'))
            else:
                cursor.execute('''
                    SELECT name, dob, gender, phone, created_at 
                    FROM appointments 
                    ORDER BY id DESC
                ''')
                
            rows = cursor.fetchall()
            conn.close()
            
            if rows:
                st.info(f"कुल दर्ज अपॉइंटमेंट: {len(rows)}")
                for row in rows:
                    name, dob, gender, phone, created_at = row
                    with st.expander(f"👤 {name} | 📞 {phone}"):
                        st.write(f"**नाम:** {name}")
                        st.write(f"**जन्मतिथि:** {dob}")
                        st.write(f"**लिंग:** {gender}")
                        st.write(f"**मोबाइल नंबर:** {phone}")
                        st.write(f"**बुकिंग समय:** {created_at}")
            else:
                st.info("अभी तक कोई अपॉइंटमेंट दर्ज नहीं हुआ है।")
                
        except Exception as e:
            st.error(f"⚠️ डेटाबेस पढ़ने में त्रुटि: {e}")
            
    elif pin_input != "":
        st.error("❌ गलत पिन! कृपया सही पिन दर्ज करें।")

admin_page()