import streamlit as st
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive


@st.cache(show_spinner=False)
def get_exoplanet_data_by_astroquery():
    parameters = 'hostname,pl_name,pl_orbper,pl_orbsmax,pl_bmasse,pl_rade'
    exoplanet_data = NasaExoplanetArchive.query_criteria(table='pscomppars', select=parameters)
    exoplanet_data = exoplanet_data.to_pandas()
    exoplanet_data = exoplanet_data.sort_values(
        by=['hostname'], ignore_index=True
    )
    renamed_columns_dict = {
        'hostname': '母恆星名稱',
        'pl_name': '行星名稱',
        'pl_orbper': '行星軌道週期',
        'pl_orbsmax': '行星軌道半長軸',
        'pl_bmasse': '行星質量',
        'pl_rade': '行星半徑',
    }
    exoplanet_data = exoplanet_data.rename(columns=renamed_columns_dict)

    return exoplanet_data


st.set_page_config(layout="wide")
st.title('用NASA太陽系外行星資料庫的資料驗證[克卜勒第三定律](https://zh.wikipedia.org/zh-tw/%E5%BC%80%E6%99%AE%E5%8B%92%E5%AE%9A%E5%BE%8B#%E5%BC%80%E6%99%AE%E5%8B%92%E7%AC%AC%E4%B8%89%E5%AE%9A%E5%BE%8B)')
st.info('克卜勒第三定律為各個行星繞其母恆星公轉週期的平方及其橢圓軌道的半長軸的立方成正比，本教材以NASA太陽系外行星資料庫的資料來驗證此定律。')

with st.spinner('從[NASA太陽系外行星資料庫](https://exoplanetarchive.ipac.caltech.edu/)載入資料中，請稍候...'):
    exoplanet_data = get_exoplanet_data_by_astroquery()
    hostname_list = list(exoplanet_data['母恆星名稱'].unique())
    st.header('太陽系外行星資料表')
    st.dataframe(exoplanet_data)

hostname = st.sidebar.text_input('輸入母恆星名稱', hostname_list[0])

if hostname in hostname_list:
    selected_exoplanets = exoplanet_data[
        exoplanet_data['母恆星名稱'] == hostname].reset_index(drop=True)

    st.header(f'{hostname}系統中的行星')
    st.table(selected_exoplanets)

    pl_name_list = selected_exoplanets['行星名稱'].tolist()
    period_list = selected_exoplanets['行星軌道週期'].tolist()
    semi_major_axis_list = selected_exoplanets['行星軌道半長軸'].tolist()

    for index, pl_name in enumerate(pl_name_list):
        period = period_list[index]
        semi_major_axis = semi_major_axis_list[index]
        k = period ** 2 / semi_major_axis ** 3
        st.success(f"行星{pl_name}的「軌道週期平方除以軌道半長軸的立方」為{k}")

else:
    st.error('輸入的母恆星名稱並沒有在資料庫中')
