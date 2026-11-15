from pathlib import Path
from html import escape
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='ROADSAFE | Road Safety Intelligence', page_icon='🛡️', layout='wide', initial_sidebar_state='expanded')
ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
if not DATA.exists():
    DATA = ROOT / 'ROADSAFE_3_Datasets'

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
:root{--ink:#eaf2ff;--muted:#9aafcb;--line:#263a54}
html,body,[class*="css"],.stApp{font-family:'DM Sans',sans-serif}
.stApp{background:radial-gradient(ellipse at 80% -10%,#11223d 0%,#09111f 47%,#080f1c 100%);color:var(--ink)}
[data-testid="stSidebar"]{background:#0c1728;border-right:1px solid #263950}
[data-testid="stSidebar"] .block-container{padding-top:2rem}
.block-container{max-width:1580px;padding:2.5rem 3rem 4rem}
#MainMenu,footer{visibility:hidden}
h1,h2,h3{font-family:'DM Sans',sans-serif;letter-spacing:-.035em}
h1{font-size:2.7rem!important;font-weight:800!important}
h3{font-weight:750!important}
.brand{font-size:24px;font-weight:800;letter-spacing:-.8px;color:#f4f8ff}.brand span{color:#56d6eb}
.brand-sub,.eyebrow,.section-index,.source-line{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:1.5px;color:#7fa2c7}
.brand-sub{margin-top:4px}.side-rule{height:1px;background:#263950;margin:27px 0}
.hero{position:relative;overflow:hidden;background:linear-gradient(105deg,#14344d 0%,#172747 56%,#302043 100%);border:1px solid #33516e;border-radius:22px;padding:30px 34px;min-height:148px;margin:15px 0 20px;box-shadow:0 14px 42px #0002}
.hero:before,.hero:after{content:'';position:absolute;border:1px solid #407aa14d;border-radius:50%;width:420px;height:420px;right:-55px;top:-310px;pointer-events:none}.hero:after{width:310px;height:310px;right:2px;top:-250px}
.hero-title{font-size:23px;font-weight:800;color:white;margin-bottom:9px;position:relative}.hero-desc{font-size:15px;color:#bcd2ea;max-width:780px;line-height:1.7;position:relative}
.hero-chip{display:inline-block;background:#0f434a;border:1px solid #277b79;border-radius:30px;padding:7px 12px;font-size:10px;letter-spacing:1px;font-weight:800;color:#7cf3d2;margin-top:15px}
.kpi{background:linear-gradient(150deg,#15263e,#101c2f);border:1px solid #2b405c;border-radius:17px;padding:20px;min-height:139px;box-shadow:0 10px 25px #0002}
.kpi-label{font-size:11px;letter-spacing:1.2px;color:#a5bce0;font-weight:650;white-space:nowrap}
.kpi-value{font-size:clamp(23px,2.2vw,34px);font-weight:750;letter-spacing:-1px;color:#dceaff;margin:11px 0 8px;white-space:nowrap}
.kpi-note{font-size:11px;color:#76dfc1;line-height:1.3}
.section-top{border-top:1px solid #263b55;padding-top:29px;margin-top:26px}
.section-index{color:#83a6d3;margin-bottom:9px}.section-title{font-size:21px;font-weight:750;color:#edf4ff;margin:0 0 17px}
.chart-title{font-size:14px;font-weight:700;color:#e6f0ff;margin:6px 0 12px}
[data-testid="stPlotlyChart"]{border:1px solid #2b415b;background:#101d30;border-radius:17px;padding:6px;overflow:hidden}
[data-testid="stPlotlyChart"]>div{width:100%}
[data-testid="stDataFrame"]{border:1px solid #2b415b;border-radius:12px}
[data-testid="stSidebar"] label{font-size:13px;font-weight:650}
.stButton button,.stDownloadButton button{border-radius:11px;border:1px solid #36546e;background:#16283f;color:#e9f5ff}
.source-line{margin:18px 0 6px;text-align:right;letter-spacing:.3px}
@media(max-width:1100px){.block-container{padding:1.5rem 1rem}.kpi{min-height:118px;padding:14px}.kpi-label{white-space:normal}.kpi-value{font-size:23px}}
</style>''', unsafe_allow_html=True)

FILES = {'State Accidents':'road_accidents.csv','State Fatalities':'state_fatalities.csv','Monthly Trends':'monthly_accidents.csv','Road Categories':'road_types.csv','Road Users':'road_user_fatalities.csv','Collisions':'collision_types.csv','Safety Devices':'safety_device_totals.csv','Junctions':'junction_types_2019.csv','Vehicle Context':'historical_vehicle_context.csv'}
@st.cache_data
def read_csv(filename):
    path = DATA / filename
    if not path.exists(): return pd.DataFrame()
    try:
        d = pd.read_csv(path)
        d.columns = d.columns.str.strip()
        for col in ('Year','Accidents','Fatalities','Injured','Month_Number'):
            if col in d: d[col] = pd.to_numeric(d[col],errors='coerce')
        return d
    except (OSError, ValueError, pd.errors.ParserError) as exc:
        st.warning(f'Unable to load {filename}: {exc}')
        return pd.DataFrame()
D = {name:read_csv(filename) for name,filename in FILES.items()}
if all(d.empty for d in D.values()):
    st.error('No datasets found. Put all nine CSV files in the data folder beside app.py.')
    st.stop()

CYAN='#51d5ed'; PURPLE='#9294ff'; GOLD='#ffbd70'; GREEN='#64d9b0'
PALETTE=[CYAN,PURPLE,GOLD,GREEN,'#ee80bc','#7eabef','#c0df80']
PAPER='#101d30'; GRID='#263951'
def valid(df,*cols): return not df.empty and all(c in df.columns for c in cols)
def figure(fig,height=340):
    fig.update_layout(template='plotly_dark',paper_bgcolor=PAPER,plot_bgcolor=PAPER,height=height,
        font=dict(family='DM Sans',color='#dbe8fb',size=12),margin=dict(l=24,r=17,t=30,b=26),
        legend=dict(orientation='h',y=1.13,x=0,font=dict(size=11)),coloraxis_showscale=False)
    fig.update_xaxes(gridcolor=GRID,zerolinecolor=GRID,automargin=True)
    fig.update_yaxes(gridcolor=GRID,zerolinecolor=GRID,automargin=True)
    st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
def kpi(label,value,note):
    st.markdown(f'<div class="kpi"><div class="kpi-label">{escape(str(label))}</div><div class="kpi-value">{escape(str(value))}</div><div class="kpi-note">{escape(str(note))}</div></div>',unsafe_allow_html=True)
def section(n,tag,title):
    st.markdown(f'<div class="section-top"><div class="section-index">{n:02d} / {escape(tag.upper())}</div><div class="section-title">{escape(title)}</div></div>',unsafe_allow_html=True)
def heading(text): st.markdown(f'<div class="chart-title">{escape(text)}</div>',unsafe_allow_html=True)
def year_filter(df,year): return df[df.Year.eq(year)].copy() if valid(df,'Year') else pd.DataFrame()

# SIDEBAR
st.sidebar.markdown('<div class="brand">◈ ROAD<span>SAFE</span></div><div class="brand-sub">ROAD OPERATIONS / ANALYTICS</div><div class="side-rule"></div>',unsafe_allow_html=True)
st.sidebar.markdown('### Filters')
years=sorted({int(y) for d in D.values() if 'Year' in d for y in d.Year.dropna().unique()},reverse=True)
year=st.sidebar.selectbox('Reporting year',years)
metric=st.sidebar.selectbox('Trend metric',['Accidents','Fatalities'])
state_names=sorted(set(D['State Accidents'].get('State',pd.Series(dtype=str)).dropna().astype(str))|set(D['State Fatalities'].get('State',pd.Series(dtype=str)).dropna().astype(str)))
states=st.sidebar.multiselect('States / UTs',state_names,placeholder='All states / UTs')
st.sidebar.markdown('<div class="side-rule"></div>',unsafe_allow_html=True)
st.sidebar.markdown('### Data source')
st.sidebar.markdown('<span class="hero-chip">● OFFICIAL HISTORICAL DATA</span>',unsafe_allow_html=True)
st.sidebar.caption(f'{sum(not d.empty for d in D.values())} of 9 datasets loaded')
st.sidebar.caption('MoRTH Road Accidents in India 2023 and supplied CSV files')
st.sidebar.caption('State selection affects state charts only. National charts use national data.')

monthly=D['Monthly Trends']; fatalities=D['State Fatalities']; accidents=D['State Accidents']; roads=D['Road Categories']; users=D['Road Users']; collisions=D['Collisions']; safety=D['Safety Devices']; junctions=D['Junctions']; vehicles=D['Vehicle Context']
m=year_filter(monthly,year); f=year_filter(fatalities,year); a=year_filter(accidents,year); r=year_filter(roads,year); u=year_filter(users,year); c=year_filter(collisions,year); s=year_filter(safety,year); j=year_filter(junctions,year)

# HEADER AND KPIS
st.title('Road Safety Intelligence')
st.markdown('<div class="hero"><div class="hero-title">Road operations at a glance</div><div class="hero-desc">Understand when accidents rise, which roads report the most incidents, and where safety outcomes deserve attention.</div><span class="hero-chip">● NATIONAL ROAD SAFETY DATA</span></div>',unsafe_allow_html=True)
cols=st.columns(4,gap='medium')
values=[('TOTAL ACCIDENTS',f'{int(m.Accidents.sum()):,}' if valid(m,'Accidents') else '—','Monthly total · '+str(year)),('ROAD FATALITIES',f'{int(m.Fatalities.sum()):,}' if valid(m,'Fatalities') else '—','Monthly total · '+str(year)),('REPORTING STATES',str(f.State.nunique()) if valid(f,'State') else '—','Fatality records · '+str(year)),('ROAD CATEGORIES',str(r.Road_Type.nunique()) if valid(r,'Road_Type') else '—','National classification · '+str(year))]
for col,details in zip(cols,values):
    with col:kpi(*details)
st.markdown(f'<div class="source-line">REPORTING YEAR {year} &nbsp; / &nbsp; HISTORICAL DATA, NOT LIVE INCIDENTS</div>',unsafe_allow_html=True)

# 01 and 02
section(1,'Accident trajectory','National accident trends')
left,right=st.columns([1.45,1],gap='large')
with left:
    heading('Accidents and fatalities over time')
    if valid(monthly,'Year',metric):
        annual=monthly.groupby('Year',as_index=False)[['Accidents','Fatalities']].sum()
        fig=px.area(annual,x='Year',y=metric,markers=True,color_discrete_sequence=[CYAN])
        fig.update_traces(line_width=3,fillcolor='rgba(81,213,237,.16)');fig.update_xaxes(dtick=1)
        figure(fig,360)
    else:st.info('National monthly trend data unavailable.')
with right:
    heading('Accident share by road type')
    if valid(r,'Road_Type','Accidents'):
        fig=px.pie(r,names='Road_Type',values='Accidents',hole=.68,color_discrete_sequence=PALETTE)
        fig.update_traces(textposition='outside',textinfo='percent',hovertemplate='%{label}: %{value:,}<extra></extra>')
        fig.add_annotation(text='<b>ROAD MIX</b>',x=.5,y=.5,showarrow=False,font=dict(size=15,color='#eaf4ff'))
        figure(fig,360)
    else:st.info('Road category figures available for 2021–2023.')

section(2,'Seasonal intelligence','Monthly accident patterns')
left,right=st.columns([1.45,1],gap='large')
with left:
    heading(f'Monthly {metric.lower()} · {year}')
    if valid(m,'Month_Number','Month',metric):
        mm=m.sort_values('Month_Number')
        fig=px.line(mm,x='Month',y=metric,markers=True,color_discrete_sequence=[CYAN]);fig.update_traces(line_width=3,marker_size=8)
        figure(fig,340)
    else:st.info('Monthly data available for 2019–2023.')
with right:
    heading('Accident intensity heatmap')
    if valid(monthly,'Year','Month_Number','Accidents'):
        pivot=monthly.pivot_table(index='Year',columns='Month_Number',values='Accidents',aggfunc='sum')
        fig=px.imshow(pivot,aspect='auto',color_continuous_scale=['#172941','#206b87','#55d9eb'],labels=dict(x='Month',y='Year',color='Accidents'))
        figure(fig,340)

# 03
section(3,'Road infrastructure','Road category comparison')
left,right=st.columns([1.4,1],gap='large')
with left:
    heading('Accidents, fatalities and injuries')
    if valid(r,'Road_Type','Accidents','Fatalities','Injured'):
        fig=px.bar(r,x='Road_Type',y=['Accidents','Fatalities','Injured'],barmode='group',color_discrete_sequence=PALETTE)
        figure(fig,365)
    else:st.info('Road category data available for 2021–2023.')
with right:
    heading('Fatalities by road category')
    if valid(r,'Road_Type','Fatalities'):
        fig=px.bar(r.sort_values('Fatalities'),x='Fatalities',y='Road_Type',orientation='h',color='Road_Type',color_discrete_sequence=PALETTE)
        fig.update_layout(showlegend=False);figure(fig,365)
    else:st.info('No road category data for this year.')

# 04
section(4,'Regional intelligence','State-level accident and fatality analysis')
left,right=st.columns([1.4,1],gap='large')
with left:
    heading('State fatalities over time')
    if valid(fatalities,'State','Year','Fatalities'):
        df=fatalities[fatalities.State.isin(states)] if states else fatalities
        if not states:
            top=df[df.Year.eq(df.Year.max())].nlargest(8,'Fatalities').State
            df=df[df.State.isin(top)]
        fig=px.line(df,x='Year',y='Fatalities',color='State',markers=True,color_discrete_sequence=PALETTE)
        fig.update_xaxes(dtick=1);figure(fig,400)
    else:st.info('State fatality data unavailable.')
with right:
    heading(f'State fatalities · {year}')
    ff=f[f.State.isin(states)] if states and valid(f,'State') else f
    if valid(ff,'State','Fatalities'):
        top=ff.nlargest(12,'Fatalities').sort_values('Fatalities')
        fig=px.bar(top,x='Fatalities',y='State',orientation='h',color='Fatalities',color_continuous_scale=['#1b4967','#4fd4eb'])
        figure(fig,400)
    else:st.info('State fatality data available for 2019–2023.')

section(5,'Regional distribution','State accident distribution')
left,right=st.columns([1.4,1],gap='large')
aa=a[a.State.isin(states)] if states and valid(a,'State') else a
with left:
    heading(f'Highest accident counts · {year}')
    if valid(aa,'State','Accidents'):
        top=aa.nlargest(15,'Accidents').sort_values('Accidents')
        fig=px.bar(top,x='Accidents',y='State',orientation='h',color='Accidents',color_continuous_scale=['#1a425f','#5ad7ed'])
        figure(fig,400)
    else:st.info('State accident counts are available for 2016–2019.')
with right:
    heading('State accident treemap')
    if valid(aa,'State','Accidents'):
        fig=px.treemap(aa,path=['State'],values='Accidents',color='Accidents',color_continuous_scale=['#183753','#317fa6','#9a95ff'])
        figure(fig,400)
    else:st.info('Choose a year from 2016–2019.')

# 06
section(6,'People and road users','Road-user fatality intelligence')
left,right=st.columns([1.4,1],gap='large')
with left:
    heading('Fatalities by road-user category')
    if valid(u,'Road_User_Category','Fatalities'):
        fig=px.bar(u.sort_values('Fatalities'),x='Fatalities',y='Road_User_Category',orientation='h',color='Fatalities',color_continuous_scale=['#193f5c','#5cdbeb'])
        figure(fig,400)
    else:st.info('Road-user fatality data available for 2022–2023.')
with right:
    heading('Share of road-user fatalities')
    if valid(u,'Road_User_Category','Fatalities'):
        fig=px.pie(u,names='Road_User_Category',values='Fatalities',hole=.62,color_discrete_sequence=PALETTE)
        fig.update_traces(textinfo='percent',textposition='inside');figure(fig,400)
    else:st.info('Choose 2022 or 2023.')
st.caption('Road-user categories describe victims, not the vehicles responsible for crashes.')

# 07
section(7,'Collision intelligence','Collision patterns')
left,right=st.columns([1.4,1],gap='large')
with left:
    heading('Accidents by collision type')
    if valid(c,'Collision_Type','Accidents'):
        fig=px.bar(c.sort_values('Accidents'),x='Accidents',y='Collision_Type',orientation='h',color='Accidents',color_continuous_scale=['#292852','#9b95ff'])
        figure(fig,385)
    else:st.info('Collision data available for 2022–2023.')
with right:
    heading('Collision composition')
    if valid(c,'Collision_Type','Accidents'):
        fig=px.treemap(c,path=['Collision_Type'],values='Accidents',color='Accidents',color_continuous_scale=['#183753','#347da4','#a89dff'])
        figure(fig,385)
    else:st.info('No collision figures for this year.')

# 08
section(8,'Preventive safety','Helmet and seat-belt outcomes')
left,right=st.columns([1.4,1],gap='large')
with left:
    heading('Recorded fatalities and injuries')
    if valid(s,'Safety_Device_Not_Used','Fatalities','Injured'):
        fig=px.bar(s,x='Safety_Device_Not_Used',y=['Fatalities','Injured'],barmode='group',color_discrete_sequence=[CYAN,PURPLE])
        figure(fig,350)
    else:st.info('Safety-device figures are available for 2023 only.')
with right:
    heading('Fatalities by safety device not used')
    if valid(s,'Safety_Device_Not_Used','Fatalities'):
        fig=px.pie(s,names='Safety_Device_Not_Used',values='Fatalities',hole=.65,color_discrete_sequence=[CYAN,PURPLE])
        figure(fig,350)
    else:st.info('Choose 2023.')

# 09
section(9,'Junction analysis','Accidents by junction design')
if valid(j,'State','Junction_Type','Accidents'):
    location=st.selectbox('Select reporting location',sorted(j.State.dropna().unique()))
    jj=j[j.State.eq(location)]
    left,right=st.columns([1.4,1],gap='large')
    with left:
        heading('Accidents by junction type')
        fig=px.bar(jj,x='Accidents',y='Junction_Type',orientation='h',color='Accidents',color_continuous_scale=['#1c4461','#54d4eb'])
        figure(fig,345)
    with right:
        heading('Junction mix')
        fig=px.pie(jj,names='Junction_Type',values='Accidents',hole=.60,color_discrete_sequence=PALETTE)
        figure(fig,345)
    st.caption('Source labels in the State field represent reporting locations/cities in this junction table.')
else:st.info('Junction analysis available for 2019 only.')

# 10
section(10,'Historical context','Vehicle and accident trends')
left,right=st.columns([1.45,1],gap='large')
with left:
    heading('National historical counts (thousands, rounded)')
    if valid(vehicles,'Year','Accidents_Thousands_Rounded','Deaths_Thousands_Rounded'):
        fig=px.line(vehicles,x='Year',y=['Accidents_Thousands_Rounded','Deaths_Thousands_Rounded'],markers=True,color_discrete_sequence=[CYAN,PURPLE])
        figure(fig,350)
    else:st.info('Historical vehicle context unavailable.')
with right:
    heading('Deaths per 10,000 registered vehicles')
    if valid(vehicles,'Year','Deaths_Per_10000_Vehicles'):
        fig=px.area(vehicles,x='Year',y='Deaths_Per_10000_Vehicles',markers=True,color_discrete_sequence=[GOLD])
        fig.update_traces(fillcolor='rgba(255,189,112,.16)');figure(fig,350)
    else:st.info('Vehicle rate data unavailable.')

# 11
section(11,'Automated findings','Key findings from selected year')
findings=[]
if valid(m,'Accidents','Month'):
    peak=m.loc[m.Accidents.idxmax()];findings.append(f"Peak accident month: {peak['Month']} ({int(peak['Accidents']):,} accidents).")
if valid(r,'Road_Type','Accidents'):
    peak=r.loc[r.Accidents.idxmax()];findings.append(f"Largest road category by recorded accidents: {peak['Road_Type']} ({int(peak['Accidents']):,}).")
if valid(f,'State','Fatalities'):
    peak=f.loc[f.Fatalities.idxmax()];findings.append(f"Highest state/UT fatality count: {peak['State']} ({int(peak['Fatalities']):,}).")
if valid(c,'Collision_Type','Accidents'):
    peak=c.loc[c.Accidents.idxmax()];findings.append(f"Most recorded collision type: {peak['Collision_Type']}.")
if findings:
    for item in findings:st.info(item)
else:st.info('Choose a year with supported datasets to see findings.')
st.caption('These are descriptive comparisons of counts, not evidence of causes or population-adjusted risk.')

# 12
section(12,'Data explorer','Explore and export source tables')
selected=st.selectbox('Choose dataset',list(FILES))
df=D[selected]
if not df.empty:
    st.dataframe(df,use_container_width=True,hide_index=True)
    st.download_button('Download selected CSV',df.to_csv(index=False).encode('utf-8'),file_name=FILES[selected],mime='text/csv')
else:st.warning('This file was not found in the data directory.')
with st.expander('Source notes and coverage'):
    st.markdown('''Data sources: MoRTH Road Accidents in India 2023 and the supplied historical tables. State accidents cover 2016–2019; state fatalities 2019–2023; national monthly totals 2019–2023; road types 2021–2023; road users and collisions 2022–2023; safety devices 2023; junctions 2019; vehicle context 2012–2023. National charts are not state-filtered. The 2021 monthly accident records sum to 412,632 whereas the published annual total is 412,432; original monthly entries are retained. Vehicle context counts are rounded to thousands. Never sum fatalities from different breakdowns.''')
st.divider()
st.caption('ROADSAFE 3.0  /  SMART ROAD SAFETY INTELLIGENCE  /  HISTORICAL REPORT DATA')
