from telnetlib import theNULL
import streamlit as st
from datetime import datetime, timedelta, date
from dateutil import relativedelta 

st.set_page_config(
    page_title='RiteHealth',
    page_icon=':heart:'#,
#    layout='wide'
)

if 'member_details_submit' in st.session_state.keys():
    member_details_submit = st.session_state['member_details_submit']
else:
    member_details_submit = False
    st.session_state['member_details_submit'] = False

if 'medical_cond_submit' in st.session_state.keys():
    medical_cond_submit = st.session_state['medical_cond_submit']
else:
    medical_cond_submit = False
    st.session_state['medical_cond_submit'] = False
    st.session_state['medical_cond'] = []

#st.write(st.session_state)
#st.write(medical_cond_submit)

def update_session(key_list):
    for key, value in key_list.items():
        if key not in st.session_state:
            st.session_state[key] = value

update_session({'member_dob':date(date.today().year-25, 1, 1), 'member_height':180.0, 'member_weight':75.0})

def get_value(id, ifmissing=None):
    if id in st.session_state.keys():
        return st.session_state[id]
    else:
        return ifmissing

def member_details_toggle():
    global member_details_submit
    member_details_submit = not member_details_submit
    st.session_state['member_details_submit'] = member_details_submit
    if member_details_submit:
        st.session_state['member_dob'] = st.session_state['member_dob_value']
        st.session_state['member_height'] = st.session_state['member_height_value']
        st.session_state['member_weight'] = st.session_state['member_weight_value']

def medical_cond_toggle():
    global medical_cond_submit
    if 'medical_cond_value' in st.session_state.keys():
        if len(st.session_state['medical_cond_value']) > 0:
            medical_cond_submit = not medical_cond_submit
            if medical_cond_submit:
                st.session_state['medical_cond'] = st.session_state['medical_cond_value']
        else:
            with med_cond_warning:
                st.warning("Select at least one medical contition.")
                if 'medical_cond' in st.session_state.keys():
                    del st.session_state['medical_cond']
    else:
        medical_cond_submit = False

    st.session_state['medical_cond_submit'] = medical_cond_submit

    
#st.write(st.session_state)

css_style = """
<style>

/* Restore label font sizes*/
label {
    font-size: 1rem !important;
} 

/* to remove the ugly top padding */
.css-18e3th9 {
    padding-top: 3rem !important;
} 

/* to remove the padding and border around forms
.css-12ttj6m {
    border: 0px solid rgba(49, 51, 63, 0.2) !important;
    padding: 0;
}*/
</style>
"""

def render_member_details_form():
    with st.form('member_details'):
        st.session_state['member_dob_value'] = st.session_state['member_dob']
        st.session_state['member_height_value'] = st.session_state['member_height']
        st.session_state['member_weight_value'] = st.session_state['member_weight']

        member_dob=st.date_input('Date of Birth: ', max_value=date.today(), min_value=date(date.today().year-100, 1, 1), key='member_dob_value')
        member_height=st.number_input('Height (in cm): ', min_value=1.0, max_value=250.0, step=1.0, format="%.1f", key='member_height_value')
        member_weight=st.number_input('Weight (in kg): ', min_value=1.0, max_value=250.0, step=1.0 , format="%.1f", key='member_weight_value')
        st.form_submit_button('Next', on_click=member_details_toggle)

def render_member_details_submitted():
    member_age = relativedelta.relativedelta(date.today(), st.session_state['member_dob']).years
    member_bmi = st.session_state['member_weight'] / ((st.session_state['member_height']/100) ** 2)
    st.session_state['member_age'] = member_age
    st.session_state['member_bmi'] = member_bmi
    st.button('Edit Member Details', on_click=member_details_toggle, key='member_details_button')
    st.markdown('Date of Birth:')
    st.markdown('**{0:%d %b %Y}**'.format(st.session_state['member_dob']))
    st.markdown('Height (in cm):')
    st.markdown('**{0:0.1f}**'.format(st.session_state['member_height']))
    st.markdown('Weight (in kg):')
    st.markdown('**{0:0.1f}**'.format(st.session_state['member_weight']))
    st.markdown('Member Age:')
    st.markdown('**{0}**'.format(member_age))
    st.markdown('Body Mass Index:')
    st.markdown('**{0:0.1f}**'.format(member_bmi))

def render_medical_conditions_form():
    with st.form('medical_conditions'):
        if 'medical_cond' in st.session_state.keys():
            st.session_state['medical_cond_value'] = st.session_state['medical_cond']
        st.multiselect(label='Select medical conditions:', options=['Diabetis', 'Asthma', 'Cancer', 'Others'], key='medical_cond_value')
        global med_cond_warning
        med_cond_warning = st.container()
        with med_cond_warning:
            st.write("")
        st.form_submit_button('Next', on_click=medical_cond_toggle)

def render_medical_conditions_submitted():
    st.button('Edit Medical Conditions', on_click=medical_cond_toggle, key='medical_cond_button')
    st.subheader("Selected Medical Conditions:")
    st.markdown("* " + "\n* ".join(st.session_state['medical_cond']))
    st.subheader("Required Documents:")
    st.markdown("* Documents for " + "\n* Documents for ".join(st.session_state['medical_cond']))

st.markdown(css_style,unsafe_allow_html=True)
st.title('RiteHealth')
st.header("Member Details")
if not member_details_submit:
    render_member_details_form()   
else:
    render_member_details_submitted()
    st.markdown('----')
    st.header("Medical Conditions")
    if not medical_cond_submit:
        render_medical_conditions_form()
    else:
        render_medical_conditions_submitted()

#st.write(st.session_state)
