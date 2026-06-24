import streamlit as st
from firebase_admin import db

def admin_page():
    st.title("🛡️ एडमिन पैनल - बजरंगी राम ज्योतिष केंद्र")
    
    # सर्च बार
    search_query = st.text_input("🔍 नाम से खोजें...")
    
    try:
        ref = db.reference('/')
        data = ref.get()
        
        if data:
            users = data.items()
            
            # फिल्टरिंग लॉजिक
            filtered_users = [u for u in users if search_query.lower() in u[1].get('name', '').lower()]
            
            st.subheader(f"कुल पंजीकृत ग्राहक: {len(filtered_users)}")
            
            for phone, info in filtered_users:
                with st.expander(f"👤 {info.get('name')} | {phone}"):
                    # एडिट फॉर्म
                    new_name = st.text_input("नाम", value=info.get('name'), key=f"n_{phone}")
                    new_dob = st.text_input("जन्मतिथि (YYYY-MM-DD)", value=info.get('dob'), key=f"d_{phone}")
                    
                    if st.button("💾 अपडेट करें", key=f"upd_{phone}"):
                        db.reference(f'/{phone}').update({'name': new_name, 'dob': new_dob})
                        st.success("अपडेट हो गया!")
                        st.rerun()
                        
                    if st.button("🗑️ डिलीट करें", key=f"del_{phone}"):
                        db.reference(f'/{phone}').delete()
                        st.warning("रिकॉर्ड हटा दिया गया!")
                        st.rerun()
        else:
            st.info("डेटाबेस खाली है।")
    except Exception as e:
        st.error(f"त्रुटि: {e}")

admin_page()