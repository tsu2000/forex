import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

import xlsxwriter
import base64
import io
import requests
import datetime

from PIL import Image
from streamlit_extras.badges import badge

# Obtaining data from Exchange Rate API
@st.cache_resource
def timeseries_data(start_date, end_date, cur, base_cur):
    # Obtaining up-to-date data for application
    api_url = f'https://api.exchangerate.host/timeseries?start_date={start_date}&end_date={end_date}&symbols={cur}&base={base_cur}'
    data = requests.get(api_url).json()
    
    return data

@st.cache_resource
def latest_data(date, base_cur):
    api_url = f'https://api.exchangerate.host/{date}?base={base_cur}'
    data = requests.get(api_url).json()
    
    return data

def main():
    col1, col2, col3 = st.columns([0.045, 0.265, 0.025])
    
    with col1:
        url = 'https://raw.githubusercontent.com/tsu2000/forex/main/images/exchange.png'
        response = requests.get(url)
        img = Image.open(io.BytesIO(response.content))
        st.image(img, output_format = 'png')

    with col2:
        st.title('&nbsp; Foreign Currency Exchange')

    with col3:
        badge(type = 'github', name = 'tsu2000/forex', url = 'https://github.com/tsu2000/forex')

    full_currency_dict = {'AED - United Arab Emirates (UAE) Dirham': '🇦🇪',
                          'AFN - Afghanistan Afghani': '🇦🇫', 
                          'ALL - Albania Lek': '🇦🇱',
                          'AMD - Armenia Dram': '🇦🇲', 
                          'ANG - Netherlands Antilles Guilder': '🇧🇶', 
                          'AOA - Angola Kwanza': '🇦🇴', 
                          'ARS - Argentina Peso': '🇦🇷', 
                          'AUD - Australia Dollar': '🇦🇺', 
                          'AWG - Aruba Guilder': '🇦🇼', 
                          'AZN - Azerbaijan Manat': '🇦🇿', 
                          'BAM - Bosnia and Herzegovina Convertible Mark': '🇧🇦', 
                          'BBD - Barbados Dollar': '🇧🇧', 
                          'BDT - Bangladesh Taka': '🇧🇩', 
                          'BGN - Bulgaria Lev': '🇧🇬', 
                          'BHD - Bahrain Dinar': '🇧🇭', 
                          'BIF - Burundi Franc': '🇧🇮', 
                          'BMD - Bermuda Dollar': '🇧🇲', 
                          'BND - Brunei Darussalam Dollar': '🇧🇳', 
                          'BOB - Bolivia Bolíviano': '🇧🇴', 
                          'BRL - Brazil Real': '🇧🇷', 
                          'BSD - Bahamas Dollar': '🇧🇸', 
                          'BTC - Bitcoin': '₿', 
                          'BTN - Bhutan Ngultrum': '🇧🇹', 
                          'BWP - Botswana Pula': '🇧🇼', 
                          'BYN - Belarus Ruble': '🇧🇾', 
                          'BZD - Belize Dollar': '🇧🇿', 
                          'CAD - Canada Dollar': '🇨🇦', 
                          'CDF - Congo/Kinshasa Franc': '🇨🇩', 
                          'CHF - Switzerland Franc': '🇨🇭', 
                          'CLF - Chile Unit of Account (UF)': '🇨🇱', 
                          'CLP - Chile Peso': '🇨🇱', 
                          'CNH - China Yuan (Offshore)': '🇨🇳', 
                          'CNY - China Yuan Renminbi (RMB)': '🇨🇳', 
                          'COP - Colombia Peso': '🇨🇴', 
                          'CRC - Costa Rica Colon': '🇨🇷', 
                          'CUC - Cuba Convertible Peso': '🇨🇺', 
                          'CUP - Cuba Peso': '🇨🇺', 
                          'CVE - Cape Verde Escudo': '🇨🇻', 
                          'CZK - Czech Republic Koruna': '🇨🇿', 
                          'DJF - Djibouti Franc': '🇩🇯', 
                          'DKK - Denmark Krone': '🇩🇰', 
                          'DOP - Dominican Republic Peso': '🇩🇴', 
                          'DZD - Algeria Dinar': '🇩🇿', 
                          'EGP - Egypt Pound': '🇪🇬', 
                          'ERN - Eritrea Nakfa': '🇪🇷', 
                          'ETB - Ethiopia Birr': '🇪🇹', 
                          'EUR - Euro': '🇪🇺', 
                          'FJD - Fiji Dollar': '🇫🇯', 
                          'FKP - Falkland Islands (Malvinas) Pound': '🇫🇰', 
                          'GBP - United Kingdom (UK) Pound': '🇬🇧', 
                          'GEL - Georgia Lari': '🇬🇪', 
                          'GGP - Guernsey Pound': '🇬🇬', 
                          'GHS - Ghana Cedi': '🇬🇭', 
                          'GIP - Gibraltar Pound': '🇬🇮', 
                          'GMD - Gambia Dalasi': '🇬🇲', 
                          'GNF - Guinea Franc': '🇬🇳', 
                          'GTQ - Guatemala Quetzal': '🇬🇹', 
                          'GYD - Guyana Dollar': '🇬🇾', 
                          'HKD - Hong Kong (HK) Dollar': '🇭🇰', 
                          'HNL - Honduras Lempira': '🇭🇳', 
                          'HRK - Croatia Kuna': '🇭🇷', 
                          'HTG - Haiti Gourde': '🇭🇹', 
                          'HUF - Hungary Forint': '🇭🇺', 
                          'IDR - Indonesia Rupiah': '🇮🇩', 
                          'ILS - Israel New Shekel': '🇮🇱', 
                          'IMP - Isle of Man Pound': '🇮🇲', 
                          'INR - India Rupee': '🇮🇳', 
                          'IQD - Iraq Dinar': '🇮🇶', 
                          'IRR - Iran Rial': '🇮🇷', 
                          'ISK - Iceland Krona': '🇮🇸', 
                          'JEP - Jersey Pound': '🇯🇪', 
                          'JMD - Jamaica Dollar': '🇯🇲', 
                          'JOD - Jordan Dinar': '🇯🇴', 
                          'JPY - Japan Yen': '🇯🇵', 
                          'KES - Kenya Shilling': '🇰🇪', 
                          'KGS - Kyrgyzstan Som': '🇰🇬', 
                          'KHR - Cambodia Riel': '🇰🇭', 
                          'KMF - Comoros Franc': '🇰🇲', 
                          'KPW - North Korea (NK) Won': '🇰🇵', 
                          'KRW - South Korea (SK) Won': '🇰🇷', 
                          'KWD - Kuwait Dinar': '🇰🇼', 
                          'KYD - Cayman Islands Dollar': '🇰🇾', 
                          'KZT - Kazakhstan Tenge': '🇰🇿', 
                          'LAK - Laos Kip': '🇱🇦', 
                          'LBP - Lebanon Pound': '🇱🇧', 
                          'LKR - Sri Lanka Rupee': '🇱🇰', 
                          'LRD - Liberia Dollar': '🇱🇷', 
                          'LSL - Lesotho Loti': '🇱🇸', 
                          'LYD - Libya Dinar': '🇱🇾', 
                          'MAD - Morocco Dirham': '🇲🇦', 
                          'MDL - Moldova Leu': '🇲🇩', 
                          'MGA - Madagascar Ariary': '🇲🇬', 
                          'MKD - Macedonia Denar': '🇲🇰', 
                          'MMK - Myanmar (Burma) Kyat': '🇲🇲', 
                          'MNT - Mongolia Tughrik': '🇲🇳', 
                          'MOP - Macau Pataca': '🇲🇴', 
                          'MRU - Mauritania Ouguiya': '🇲🇷', 
                          'MUR - Mauritius Rupee': '🇲🇺', 
                          'MVR - Maldives Rufiyaa': '🇲🇻', 
                          'MWK - Malawi Kwacha': '🇲🇼', 
                          'MXN - Mexico Peso': '🇲🇽', 
                          'MYR - Malaysia Ringgit': '🇲🇾', 
                          'MZN - Mozambique Metical': '🇲🇿', 
                          'NAD - Namibia Dollar': '🇳🇦', 
                          'NGN - Nigeria Naira': '🇳🇬', 
                          'NIO - Nicaragua Cordoba': '🇳🇮', 
                          'NOK - Norway Krone': '🇳🇴', 
                          'NPR - Nepal Rupee': '🇳🇵', 
                          'NZD - New Zealand Dollar': '🇳🇿',
                          'OMR - Oman Rial': '🇴🇲', 
                          'PAB - Panama Balboa': '🇵🇦', 
                          'PEN - Peru Sol': '🇵🇪', 
                          'PGK - Papua New Guinea Kina': '🇵🇬', 
                          'PHP - Philippines Peso': '🇵🇭', 
                          'PKR - Pakistan Rupee': '🇵🇰', 
                          'PLN - Poland Zloty': '🇵🇱', 
                          'PYG - Paraguay Guarani': '🇵🇾', 
                          'QAR - Qatar Riyal': '🇶🇦', 
                          'RON - Romania Leu': '🇷🇴', 
                          'RSD - Serbia Dinar': '🇷🇸', 
                          'RUB - Russia Ruble': '🇷🇺', 
                          'RWF - Rwanda Franc': '🇷🇼', 
                          'SAR - Saudi Arabia Riyal': '🇸🇦', 
                          'SBD - Solomon Islands Dollar': '🇸🇧', 
                          'SCR - Seychelles Rupee': '🇸🇨', 
                          'SDG - Sudan Pound': '🇸🇩', 
                          'SEK - Sweden Krona': '🇸🇪', 
                          'SGD - Singapore Dollar': '🇸🇬', 
                          'SHP - Saint Helena Pound': '🇸🇭', 
                          'SLL - Sierra Leone Leone': '🇸🇱', 
                          'SOS - Somalia Shilling': '🇸🇴', 
                          'SRD - Suriname Dollar': '🇸🇷', 
                          'SSP - South Sudan Pound': '🇸🇸', 
                          'STD - São Tomé and Príncipe Dobra (Pre-2018)': '🇸🇹', 
                          'STN - São Tomé and Príncipe Dobra': '🇸🇹', 
                          'SVC - El Salvador Colon': '🇸🇻', 
                          'SYP - Syria Pound': '🇸🇾', 
                          'SZL - eSwatini Lilangeni': '🇸🇿', 
                          'THB - Thailand Baht': '🇹🇭', 
                          'TJS - Tajikistan Somoni': '🇹🇯', 
                          'TMT - Turkmenistan Manat': '🇹🇲', 
                          'TND - Tunisia Dinar': '🇹🇳', 
                          'TOP - Tonga Pa\'anga': '🇹🇴', 
                          'TRY - Turkey Lira': '🇹🇷', 
                          'TTD - Trinidad and Tobago Dollar': '🇹🇹', 
                          'TWD - Taiwan New Dollar': '🇹🇼', 
                          'TZS - Tanzania Shilling': '🇹🇿', 
                          'UAH - Ukraine Hryvnia': '🇺🇦', 
                          'UGX - Uganda Shilling': '🇺🇬', 
                          'USD - United States (US) Dollar': '🇺🇸', 
                          'UYU - Uruguay Peso': '🇺🇾', 
                          'UZS - Uzbekistan Som': '🇺🇿', 
                          'VES - Venezuela Bolívar': '🇻🇪', 
                          'VND - Vietnam Dong': '🇻🇳', 
                          'VUV - Vanuatu Vatu': '🇻🇺', 
                          'WST - Samoa Tala': '🇼🇸', 
                          'XAF - Communauté Financière Africaine (BEAC) CFA Franc': '🇨🇫', 
                          'XAG - Silver Ounce': '🥈', 
                          'XAU - Gold Ounce': '🥇', 
                          'XCD - East Caribbean Dollar': '🇦🇬', 
                          'XDR - Int\'l Monetary Fund (IMF) Special Drawing Rights': '💰', 
                          'XOF - Communauté Financière Africaine (BCEAO) Franc': '🇨🇮', 
                          'XPD - Palladium Ounce': '🔧', 
                          'XPF - Comptoirs Français du Pacifique (CFP) Franc': '🇵🇫', 
                          'XPT - Platinum Ounce': '🤍', 
                          'YER - Yemen Rial': '🇾🇪', 
                          'ZAR - South Africa Rand': '🇿🇦', 
                          'ZMW - Zambia Kwacha': '🇿🇲', 
                          'ZWL - Zimbabwe Dollar': '🇿🇼'}

    st.markdown('### 💱 &nbsp; Foreign Currency Exchange Rates (FOREX) App')

    st.markdown('A simple foreign currency conversion web application. Users can view the current exchange rates by selecting a base currency, and historical exchange rates between 2 currencies from 2 selected dates beginning from 1999. **Disclaimer:** Not all data shown may be accurate or available. (API used: [**Source**](<https://exchangerate.host/#/>))')

    opt = st.selectbox('Select a feature:', ['Historical Exchange Rate Data', 'Current Exchange Rates'])

    st.markdown('---')

    if opt == 'Historical Exchange Rate Data':
        timeseries(full_currency_list = list(full_currency_dict.keys()))

    elif opt == 'Current Exchange Rates':
        latest(full_currency_dict = full_currency_dict)

    
def timeseries(full_currency_list):
    # Initialise defaultexchange rates
    if 'baseCurr' not in st.session_state:
        st.session_state['baseCurr'] = 'SGD - Singapore Dollar'

    if 'convertedCurr' not in st.session_state:
        st.session_state['convertedCurr'] = 'MYR - Malaysia Ringgit'

    left_col, right_col = st.columns([0.1, 0.018])

    with left_col:
        st.markdown('### ⌛ &nbsp; Historical Exchange Rate Data')

    with right_col:
        swap_rates = st.button('Swap rates')
        if swap_rates:
             st.session_state['baseCurr'], st.session_state['convertedCurr'] = st.session_state['convertedCurr'], st.session_state['baseCurr']

    base_full = st.selectbox('Choose the base currency:', 
                             full_currency_list, 
                             full_currency_list.index(st.session_state['baseCurr']))

    cur_full = st.selectbox('Choose the currency to convert from:', 
                            full_currency_list, 
                            full_currency_list.index(st.session_state['convertedCurr']))

    st.session_state['baseCurr'] = base_full
    st.session_state['convertedCurr'] = cur_full

    base_code, cur_code = base_full[:3], cur_full[:3]

    # Select date range to view exchange rate data for:
    col_left, col_right = st.columns(2)

    with col_left:
        start_choice = st.date_input('Select start date (YYYY/MM/DD):', 
                                     datetime.date(2022, 1, 1), 
                                     min_value = datetime.date(1999, 1, 1),
                                     max_value = datetime.date.today())

    with col_right:
        end_choice = st.date_input('Select end date (YYYY/MM/DD):',
                                   datetime.date(2022, 12, 31), 
                                   min_value = start_choice,
                                   max_value = datetime.date.today())

    # Final initialisation of DataFrame
    st.write(start_choice > end_choice)
    days_timedelta = end_choice - start_choice
    days_left = days_timedelta.days

    if days_left < 0:
        st.error("End date cannot be earlier than start date.")
        st.stop()

    if days_left > 365:
        dict_alldays = {}
        while days_left > 365:
            dict_alldays.update(timeseries_data(start_choice, start_choice + datetime.timedelta(days = 365), cur_code, base_code)['rates'])
            days_left -= 365
            start_choice += datetime.timedelta(days = 365)
        dict_alldays.update(timeseries_data(start_choice, end_choice, cur_code, base_code)['rates'])
        
        res = pd.DataFrame(dict_alldays)

    else:
        res = pd.DataFrame(timeseries_data(start_choice, end_choice, cur_code, base_code)['rates'])

    df = res.T.reset_index(names = 'Date')

    # Differentiated charts between daily and monthly averages
    interval_type = st.radio('Choose chart type:', ['Daily Average', 'Monthly Average'])

    if interval_type == 'Daily Average':
        alt_line_chart = alt.Chart(df).mark_line(
            point = alt.OverlayMarkDef(color = 'green', shape = 'circle')
        ).encode(
            x = 'Date:T',
            y = alt.Y(f'{cur_code}:Q', title = f'Qty of {cur_code} to 1 {base_code}'),
            color = alt.value('green'),
        ).properties(
            title = f'Quantity of {cur_code} equivalent to 1 unit of {base_code}',
            width = 700,
            height = 350
        ).configure_title(
            fontSize = 16,
            offset = 14
        ).interactive()

    elif interval_type == 'Monthly Average':
        alt_line_chart = alt.Chart(df).mark_line(
            point = alt.OverlayMarkDef(color = 'blue', shape = 'circle')
        ).encode(
            x = alt.X('yearmonth(Date):T', title = 'Date (Month-Year)'),
            y = alt.Y(f'mean({df.columns[1]}):Q', title = f'Monthly Avg Qty of {cur_code} to 1 {base_code}'),
            color = alt.value('blue'),
        ).properties(
            title = f'Monthly average of {cur_code} equivalent to 1 unit of {base_code}',
            width = 700,
            height = 350
        ).configure_title(
            fontSize = 16,
            offset = 14
        ).interactive()        

    # Display selected chart
    st.altair_chart(alt_line_chart, use_container_width = True, theme = None)

    st.markdown('---')

    # Download data to Excel file
    def to_excel(df):
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine = 'xlsxwriter')

        df.to_excel(writer, sheet_name = f'{cur_code} to {base_code}', index = False)
        worksheet = writer.sheets[f'{cur_code} to {base_code}']

        # Adjust width of columns
        worksheet.set_column('A:A', 15)

        # Saving and returning data
        writer.close()
        processed_data = output.getvalue()

        return processed_data

    def get_table_download_link(df, freq):
        """Generates a link allowing the data in a given Pandas DataFrame to be downloaded
        in:  dataframe
        out: href string
        """
        val = to_excel(df)
        b64 = base64.b64encode(val)

        return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{freq}_Rates: {cur_code} to {base_code}.xlsx">:inbox_tray: Download (.xlsx)</a>' 

    col_1, col_2 = st.columns([0.1, 0.0254])

    with col_1:
        st.markdown('Download exchange rates to an Excel file **(Daily rates)**:')
        st.markdown('Download exchange rates to an Excel file **(Monthly rates)**:')

    with col_2:
        st.markdown(get_table_download_link(df, 'Daily'), unsafe_allow_html = True)

        # Group by year and month
        df['Month'] = df['Date'].str.slice(0, 7)
        df_monthly = df.groupby('Month').mean().reset_index()

        st.markdown(get_table_download_link(df_monthly, 'Monthly'), unsafe_allow_html = True)


def latest(full_currency_dict):
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

    st.markdown('### 📅 &nbsp; Current Exchange Rates')

    base = st.selectbox('Select base currency:', list(full_currency_dict.keys()))
    basecode = base[:3]

    units = st.number_input('Choose quantity of monetary units for the currency:', 
                            value = 1.000000,
                            min_value = 0.000000,
                            max_value = 10000000000.000000,
                            step = 0.000001,
                            format = '%0.6f')

    try:
        today = latest_data(datetime.date.today(), basecode)['rates']
        yesterday = latest_data(datetime.date.today() - datetime.timedelta(days = 1), basecode)['rates']
    except KeyError:
        st.error('Oops! Current exchange rate data is currently unavailable. Please check back later for updates.', icon = '🚨')
        st.stop()

    # # Check if missing keys:
    # st.write('Equal no. of list values:', len([base[:3] for base in list(full_currency_dict.values())]) == len(today.keys()))
    # for i in set(today.keys()):
    #     if i not in set([base[:3] for base in list(full_currency_dict.keys())]):
    #         st.write(i)

    curr_list = list(full_currency_dict.keys())
    emoji_list = list(full_currency_dict.values())
    today_list = list(today.values())
    yesterday_list = list(yesterday.values())

    # Create final DataFrame:
    df = pd.DataFrame(list(zip(curr_list, emoji_list, today_list, yesterday_list)),
                      columns = ['Currency', 'Emoji', 'Today', 'Yesterday'])
    df['Percent Change'] = (df['Today'] - df['Yesterday']) / df['Yesterday'] * 100
    df['Today'] *= units
    df = df.set_index('Currency')
    df = df.round({'Percent Change': 4, 'Today': 6})

    currs = st.multiselect('Select the currencies you wish to view the exchange rate (and daily change in %) for:', 
                           list(full_currency_dict.keys()),
                           default = ['USD - United States (US) Dollar',
                                      'EUR - Euro',
                                      'GBP - United Kingdom (UK) Pound',
                                      'JPY - Japan Yen',
                                      'CHF - Switzerland Franc',
                                      'CNY - China Yuan Renminbi (RMB)',
                                      'HKD - Hong Kong (HK) Dollar',
                                      'SGD - Singapore Dollar'],
                           max_selections = 30)

    st.markdown('---')
    st.markdown(f'##### :blue[{units}] Unit(s) of :blue[{base}] is equal to:')

    def create_metric(currSpec):
        return st.metric(f"{df.loc[currSpec]['Emoji']} {currSpec}", 
                         df.loc[currSpec]['Today'],
                         f"{df.loc[currSpec]['Percent Change']}%")

    col1, col2 = st.columns(2)
    with col1:
        for curr in currs[0::2]:
            create_metric(curr)
    with col2:
        for curr in currs[1::2]:
            create_metric(curr)
    
    st.markdown('---')


if __name__ == "__main__":
    st.set_page_config(page_title = 'FOREX Rates', page_icon = '💱')
    main()
