import streamlit as st
import altair as alt
import pandas as pd
from vega_datasets import data
from PIL import Image

fideI = Image.open('fider.jpg')
st.image(fideI)

st.title('International Chess Statistics')

st.write('The International Chess Federation or Fédération Internationale des Échecs (FIDE) is the governing body of the sport of chess, and it regulates all international chess competitions.')

st.write('More about FIDE: https://www.fide.com/')

st.write('Highest levels of titles:')
st.write('1. Grandmaster(GM/WGM)')
st.write('2. International Master(IM/WIM)')
st.write('3. FIDE Master(FM/WFM)')
st.write('4. Candidate Master(CM/WCM)')

chessI = Image.open('chesst.jpg')
st.image(chessI)

st.write('The FIDE rating defines the performance of a players. It uses the Elo rating system which is a method for calculating the relative skill levels of players in zero-sum games such as chess. The top ranked players have the highest FIDE ratings.')

playersdf = pd.read_csv('Complete_Players_Database.csv', index_col = 'Name')
statsdf = pd.read_csv('FixedDataset.csv', index_col = '#')

#st.write(playersdf.index[playersdf['FIDE'] == 'unranked/unrated'])
playersdf.drop(playersdf.index[playersdf['FIDE'] == 'unranked/unrated'], inplace=True)
playersdf['FIDE'] = playersdf['FIDE'].astype(float)


statsdf['Men'] = statsdf['Num Players'] - statsdf['Women']
statsdf['MGMs'] = statsdf['GMs'] - statsdf['WGMs']
statsdf['MIMs'] = statsdf['IMs'] - statsdf['WIMs']
statsdf['MFMs'] = statsdf['FMs'] - statsdf['WFMs']
statsdf['% of Men'] = round(100 * (statsdf['Men']/statsdf['Num Players']), 2)
del statsdf['Flag']
statsdf = statsdf.loc[:, ~statsdf.columns.str.contains('^Unnamed')]
statsdf = statsdf[statsdf['Country'].notna()]

statsdf['Total # of Masters'] = statsdf['GMs'] + statsdf['IMs'] + statsdf['FMs']
statsdf = statsdf.reset_index()
playersdf = playersdf.reset_index()


sphere = alt.sphere()
graticule = alt.graticule()
#mapSource = alt.topo_feature(data.world_110m.url, 'countries')
mapSource = alt.topo_feature('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json', 'countries')


topplayers = playersdf.sort_values('FIDE', ascending=False)
number1 = playersdf.loc[playersdf['Country Rank'] == 1]
allGMs = playersdf[playersdf['Title'].isin(['GM', 'WGM'])].sort_values('FIDE', ascending=False)
allIMs = playersdf[playersdf['Title'].isin(['IM', 'WIM'])].sort_values('FIDE', ascending=False)
allFMs = playersdf[playersdf['Title'].isin(['FM', 'WFM'])].sort_values('FIDE', ascending=False)
allCMs = playersdf[playersdf['Title'].isin(['CM', 'WCM'])].sort_values('FIDE', ascending=False)
allUn = playersdf[playersdf['Title'].isin(['unranked/unrated'])].sort_values('FIDE', ascending=False)

statsdf['country_code'] = statsdf['country_code'].fillna(-1)
statsdf['country_code'] = statsdf['country_code'].astype(int)
statsdf['country_code'] = statsdf['country_code'].apply(lambda x: '{0:0>3}'.format(x))


GMbar = alt.Chart(statsdf).mark_bar().encode(
    y='Country:O',
    x='GMs:Q'
).properties(
    title='Grand Masters'
)
GMtext = GMbar.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text='GMs:Q'
)
(GMbar+GMtext).properties(height=3000)

IMbar = alt.Chart(statsdf).mark_bar().encode(
    y='Country:O',
    x='IMs:Q'
).properties(
    title='International Masters'
)
IMtext = IMbar.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text='IMs:Q'
)
(IMbar+IMtext).properties(height=3000)

FMbar = alt.Chart(statsdf).mark_bar().encode(
    y='Country:O',
    x='FMs:Q'
).properties(
    title='FIDE Masters'
)
FMtext = FMbar.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text='FMs:Q'
)
(FMbar+FMtext).properties(height=3000)

FIDEbar = alt.Chart(statsdf).mark_bar().encode(
    y='Country:O',
    x='FIDE Average:Q'
).properties(
    title='FIDE Averages'
)
FIDEtext = FIDEbar.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text='FIDE Average:Q'
)
(FIDEbar+FIDEtext).properties(height=3000)

Mbar = alt.Chart(statsdf).mark_bar().encode(
    y='Country:O',
    x='Total # of Masters:Q'
).properties(
    title='Total # of Masters'
)
Mtext = Mbar.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text='Total # of Masters:Q'
)
(Mbar+Mtext).properties(height=3000)


if st.sidebar.checkbox('Who is the top player?'):
    st.markdown("## The top ranked player")
    st.write(playersdf[playersdf.FIDE == playersdf.FIDE.max()])
    st.write("The players witht the higest FIDE average is the top ranked player")
    
if st.sidebar.checkbox('Show #1 ranked players of each country'):
    st.markdown("## All players ranked #1 from their country")
    st.write(number1)
    
if st.sidebar.checkbox('Show all highest ranked players'):
    st.markdown("## All players ranked")
    st.write(topplayers)
    
if st.sidebar.checkbox('Show the top 10 highest ranked players'):
    st.markdown("## Top 10")
    st.write(topplayers.head(10))
    
if st.sidebar.checkbox('Show all Grandmasters'):
    st.markdown("## Grandmasters")
    st.write(allGMs)

if st.sidebar.checkbox('Show all International Masters'):
    st.markdown("## International Masters")
    st.write(allIMs)

if st.sidebar.checkbox('Show all FIDE Masters'):
    st.markdown("## FIDE Masters")
    st.write(allFMs)

if st.sidebar.checkbox('Show all Candidate Masters'):
    st.markdown("## Candidate Masters")
    st.write(allCMs)

if st.sidebar.checkbox('Show all players with no title'):
    st.markdown("## Unrated Players")
    st.write(allUn)
    

mapFIDE = alt.layer(
    alt.Chart(sphere).mark_geoshape(fill='lightblue'),
    alt.Chart(graticule).mark_geoshape(stroke='white', strokeWidth=0.5),
    alt.Chart(mapSource).mark_geoshape(stroke = 'white').encode(
        color=alt.Color('FIDE Average:Q', scale=alt.Scale(scheme='turbo')),
        tooltip=['#:Q', 'properties.name:O', 'FIDE Average:Q', 'country_code:Q']
    ).transform_lookup(
        lookup = 'id',
        default="0",
        from_ = alt.LookupData(statsdf, key='country_code', fields=['#','FIDE Average', 'country_code'])
    )
).project(
    type='naturalEarth1'
).properties(
    width=900,
    height=500,
    title='World Map of Chess Competitors'
)

mapMasters = alt.layer(
    alt.Chart(sphere).mark_geoshape(fill='lightblue'),
    alt.Chart(graticule).mark_geoshape(stroke='white', strokeWidth=0.5),
    alt.Chart(mapSource).mark_geoshape(stroke = 'white').encode(
        color=alt.Color('Total # of Masters:Q', scale=alt.Scale(scheme='turbo')),
        tooltip=['#:Q', 'properties.name:O', 'Total # of Masters:Q', 'country_code:Q']
    ).transform_lookup(
        lookup = 'id',
        default="0",
        from_ = alt.LookupData(statsdf, key='country_code', fields=['#','Total # of Masters', 'country_code'])
    )
).project(
    type='naturalEarth1'
).properties(
    width=900,
    height=500,
    title='World Map of Chess Competitors'
)

mapPlayers = alt.layer(
    alt.Chart(sphere).mark_geoshape(fill='lightblue'),
    alt.Chart(graticule).mark_geoshape(stroke='white', strokeWidth=0.5),
    alt.Chart(mapSource).mark_geoshape(stroke = 'white').encode(
        color=alt.Color('Num Players:Q', scale=alt.Scale(scheme='turbo')),
        tooltip=['#:Q', 'properties.name:O', 'Num Players:Q', 'country_code:Q']
    ).transform_lookup(
        lookup = 'id',
        default="0",
        from_ = alt.LookupData(statsdf, key='country_code', fields=['#','Num Players', 'country_code'])
    )
).project(
    type='naturalEarth1'
).properties(
    width=900,
    height=500,
    title='World Map of Chess Competitors'
)

mapWomen = alt.layer(
    alt.Chart(sphere).mark_geoshape(fill='lightblue'),
    alt.Chart(graticule).mark_geoshape(stroke='white', strokeWidth=0.5),
    alt.Chart(mapSource).mark_geoshape(stroke = 'white').encode(
        color=alt.Color('% of Women:Q', scale=alt.Scale(scheme='turbo')),
        tooltip=['#:Q', 'properties.name:O', '% of Women:Q', 'country_code:Q']
    ).transform_lookup(
        lookup = 'id',
        default="0",
        from_ = alt.LookupData(statsdf, key='country_code', fields=['#','% of Women', 'country_code'])
    )
).project(
    type='naturalEarth1'
).properties(
    width=900,
    height=500,
    title='World Map of Chess Competitors'
)

mapMen = alt.layer(
    alt.Chart(sphere).mark_geoshape(fill='lightblue'),
    alt.Chart(graticule).mark_geoshape(stroke='white', strokeWidth=0.5),
    alt.Chart(mapSource).mark_geoshape(stroke = 'white').encode(
        color=alt.Color('% of Men:Q', scale=alt.Scale(scheme='turbo')),
        tooltip=['#:Q', 'properties.name:O', '% of Men:Q', 'country_code:Q']
    ).transform_lookup(
        lookup = 'id',
        default="0",
        from_ = alt.LookupData(statsdf, key='country_code', fields=['#','% of Men', 'country_code'])
    )
).project(
    type='naturalEarth1'
).properties(
    width=900,
    height=500,
    title='World Map of Chess Competitors'
)
    
    
map_expander = st.expander(label='Show a Map')

with map_expander:
    mapping = st.radio("What do you want to map?", ('FIDE Averages', 'Masters', 'All Num Players', '% of Women', '% of Men'))

    if mapping == 'FIDE Averages':
        st.write(mapFIDE)
    elif mapping == 'All Num Players':
        st.write(mapPlayers)
        st.write("It seems that Russia leads the way for the most number of masters and number of players, considering the fact that it's the top ranked country, way ahead of the others.")
    elif mapping == '% of Women':
        st.write(mapWomen)
        st.write("Vietnam seems to have the highest percentage in women players, along with Mongolia and Mozambique")
    elif mapping == '% of Men':
        st.write(mapMen)
        st.write("In most countries, more men compete than women")
    else:
        st.write(mapMasters)
        st.write("It seems that Russia leads the way for the most number of masters and number of players, considering the fact that it's the top ranked country, way ahead of the others.")
        st.write("It can also be inferred that most European and some Asian countries lead the way in having the most number of masters and being placed in the higher ranks.")

        
bar_expander = st.expander(label='Show a Bar Chart of all Countries')

with bar_expander:
    bar = st.radio("Select an option", ('All Grandmasters', 'All International Masters', 'All FIDE Masters', 'Total # of Masters', 'All FIDE Averages'))
    
    if bar == 'All Grandmasters':
        st.markdown("## Grandmasters by Country")
        st.write(GMbar+GMtext)
        st.write("Russia also leads the way for having the most masters of every type (GMs, IMs, FMs).")
    elif bar == 'All International Masters':
        st.markdown("## International Masters by Country")
        st.write(IMbar+IMtext)
        st.write("Russia also leads the way for having the most masters of every type (GMs, IMs, FMs).")
    elif bar == 'All FIDE Masters':
        st.markdown("## FIDE Masters by Country")
        st.write(FMbar+FMtext)
        st.write("Russia also leads the way for having the most masters of every type (GMs, IMs, FMs).")
    elif bar == 'Total # of Masters':
        st.markdown("## Total Masters by Country")
        st.write(Mbar+Mtext)
    else:
        st.markdown("## FIDE Averages by Country")
        st.write(FIDEbar+FIDEtext)
        
    
multi_expander = st.expander(label='Multiselect Countries')

with multi_expander:
    options = st.multiselect('What countries do you want to display?', (statsdf['Country'].tolist()))
    testdf = statsdf[statsdf['Country'].isin(options)]
    st.write(testdf)
    
    selMbar = alt.Chart(testdf).transform_fold(
        ['GMs', 'IMs', 'FMs'],
        as_=['column', 'value']
    ).mark_bar().encode(
        y='Country:N',
        x='value:Q',
        color='column:N',
        tooltip=['#:O', 'Country:O', 'FMs:Q', 'GMs:Q', 'IMs:Q', 'Total # of Masters:Q']
    ).properties(
        title='Total Masters'
    ).interactive()
    st.write(selMbar)
    
    selallMbar = alt.Chart(testdf).transform_fold(
        ['MGMs', 'MIMs', 'MFMs', 'WGMs', 'WIMs', 'WFMs'],
        as_=['column', 'value']
    ).mark_bar().encode(
        y='Country:N',
        x='value:Q',
        color='column:N',
        tooltip=['#:O', 'Country:O', 'MFMs:Q', 'MGMs:Q', 'MIMs:Q', 'WFMs:Q', 'WGMs:Q', 'WIMs:Q', 'Total # of Masters:Q']
    ).properties(
        title='Total Masters by All Type'
    ).interactive()
    st.write(selallMbar)
    
    selGender = alt.Chart(testdf).transform_fold(
        ['Women', 'Men'],
        as_=['column', 'Total Players']
    ).mark_bar().encode(
        y='Country:N',
        x='Total Players:Q',
        color='column:N',
        tooltip=['Country:O', 'Men:Q', 'Women:Q', 'Num Players:Q']
    ).properties(
        title='Players'
    ).interactive()
    st.write(selGender)
    
    selFIDE = alt.Chart(testdf).mark_bar().encode(
        y='Country:O',
        x='FIDE Average:Q'
    ).properties(
        title='FIDE Averages'
    )
    selFIDEtext = selFIDE.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='FIDE Average:Q'
    )
    (selFIDE+selFIDEtext).properties(height=3000)
    st.write(selFIDE+selFIDEtext)
    
    

single_expander = st.expander(label='Single Select Countries')

with single_expander:
    selCountry = st.selectbox('Select a Country to Show Stats', (statsdf['Country'].tolist()))
    
    selectedCountry = statsdf[statsdf['Country'].isin([selCountry])]
    st.write(selectedCountry)
    st.markdown("**Country:** " + selectedCountry['Country'].to_string(index=False))
    st.markdown("**Country Rank:** #" + selectedCountry['#'].to_string(index=False))
    st.markdown("**Number of Players:** " + selectedCountry['Num Players'].to_string(index=False))
    st.markdown("**Men:** " + selectedCountry['Men'].to_string(index=False))
    st.markdown("**Women:** " + selectedCountry['Women'].to_string(index=False))
    st.markdown("**FIDE Average:** " + selectedCountry['FIDE Average'].to_string(index=False))
    st.markdown("**Grandmasters:** " + selectedCountry['GMs'].to_string(index=False))
    st.markdown("**International Masters:** " + selectedCountry['IMs'].to_string(index=False))
    st.markdown("**FIDE Masters:** " + selectedCountry['FMs'].to_string(index=False))
    st.markdown("**Total Masters:** " + selectedCountry['Total # of Masters'].to_string(index=False))
    st.markdown("**Age Average:** " + selectedCountry['Age Avg'].to_string(index=False))
    
    selPlayers = playersdf[playersdf['Country'].isin([selCountry])]
    st.markdown('#### All the Players')
    st.write(selPlayers)
    
    countryPlay = alt.Chart(selPlayers).mark_point().encode(
        x=alt.X('Country Rank'),
        y='FIDE',
        color = 'Title',
        tooltip=['Name', 'Country Rank', 'FIDE', 'Title']
        #color=alt.condition(brush, 'FIDE Average:Q', alt.value('lightgray'))
    ).properties(
        title = 'FIDE and Player Rank Correlation',
        width = 750,
        height = 750
    ).interactive()
    st.write(countryPlay)
    
    agePlay = alt.Chart(selPlayers).mark_point().encode(
        x='Age',
        y='FIDE',
        color = 'Title',
        tooltip=['Name', 'Country Rank', 'Title', 'Age']
        #color=alt.condition(brush, 'FIDE Average:Q', alt.value('lightgray'))
    ).properties(
        title = 'FIDE and Age Correlation',
        width = 750,
        height = 750
    ).interactive()
    st.write(agePlay)
    st.write("It seems that most middle-aged players (25-50) tend to have the highest FIDE averages of their country most of the time.")
    
    gensource = pd.DataFrame(
        {"category": ["Men", "Women"], "value": [selectedCountry.iloc[0]["Men"], selectedCountry.iloc[0]["Women"]]}
    )
    
    genderPie = alt.Chart(gensource).mark_arc().encode(
        theta=alt.Theta(field="value", type="quantitative", stack=True),
        radius=alt.Radius("value", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
        color=alt.Color(field="category", type="nominal")
    ).properties(
        title = "Players by Gender"
    )
    
    genpietext = genderPie.mark_text(radiusOffset=10).encode(text="value:Q")
    st.write(genderPie+genpietext)
    
    
    mastersource = pd.DataFrame(
        {"category": ["GMs", "IMs", "FMs"], "value": [selectedCountry.iloc[0]["GMs"], selectedCountry.iloc[0]["IMs"], selectedCountry.iloc[0]["FMs"]]}
    )
    
    masterPie = alt.Chart(mastersource).mark_arc().encode(
        theta=alt.Theta(field="value", type="quantitative", stack=True),
        radius=alt.Radius("value", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
        color=alt.Color(field="category", type="nominal")
    ).properties(
        title = "Players by Master"
    )
    
    maspietext = masterPie.mark_text(radiusOffset=10).encode(text="value:Q")
    st.write(masterPie+maspietext)
    
    gmsource = pd.DataFrame(
        {"category": ["MGMs", "WGMs"], "value": [selectedCountry.iloc[0]["MGMs"], selectedCountry.iloc[0]["WGMs"]]}
    )
    
    masterGM = alt.Chart(gmsource).mark_arc().encode(
        theta=alt.Theta(field="value", type="quantitative", stack=True),
        radius=alt.Radius("value", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
        color=alt.Color(field="category", type="nominal")
    ).properties(
        title = "Players by Grandmaster"
    )
    gmtext = masterGM.mark_text(radiusOffset=10).encode(text="value:Q")
    st.write(masterGM+gmtext)
    
    imsource = pd.DataFrame(
        {"category": ["MIMs", "WIMs"], "value": [selectedCountry.iloc[0]["MIMs"], selectedCountry.iloc[0]["WIMs"]]}
    )
    
    masterIM = alt.Chart(imsource).mark_arc().encode(
        theta=alt.Theta(field="value", type="quantitative", stack=True),
        radius=alt.Radius("value", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
        color=alt.Color(field="category", type="nominal")
    ).properties(
        title = "Players by International Master"
    )
    imtext = masterIM.mark_text(radiusOffset=10).encode(text="value:Q")
    st.write(masterIM+imtext)
    
    fmsource = pd.DataFrame(
        {"category": ["MFMs", "WFMs"], "value": [selectedCountry.iloc[0]["MFMs"], selectedCountry.iloc[0]["WFMs"]]}
    )
    masterFM = alt.Chart(fmsource).mark_arc().encode(
        theta=alt.Theta(field="value", type="quantitative", stack=True),
        radius=alt.Radius("value", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
        color=alt.Color(field="category", type="nominal")
    ).properties(
        title = "Players by FIDE Master"
    )
    fmtext = masterFM.mark_text(radiusOffset=10).encode(text="value:Q")
    st.write(masterFM+fmtext)


scatter_expander = st.expander(label='Create Your Own Correlation')

with scatter_expander:
    col = ['Num Players', 'Men', 'Women', '% of Women', '% of Men', 'FIDE Average', 'GMs', 'IMs', 'FMs', 'WGMs', 'WIMs', 'WFMs', 'MGMs', 'MIMs', 'MFMs', 'Total # of Masters', 'Age Avg']
    
    option = st.selectbox(
        'Choose an x-axis',
        (col))
    
    option2 = st.selectbox(
        'Choose a y-axis',
        (col))
    
    selAxis = alt.Chart(statsdf).mark_point().encode(
        x=option,
        y=option2,
        #size = 'FIDE Average',
        tooltip=['Country', 'Num Players', 'FIDE Average', 'Total # of Masters']
        #color=alt.condition(brush, 'FIDE Average:Q', alt.value('lightgray'))
    ).properties(
        title = 'Correlation',
        width = 500,
        height = 500
    ).interactive()
    st.write(selAxis)    

    
    
key_expander = st.expander(label='Key Insights')

with key_expander:
    st.write("It seems that Russia leads the way for the most number of masters and number of players, considering the fact that it's the top ranked country, way ahead of the others.")
    st.write("Russia also leads the way for having the most masters of every type (GMs, IMs, FMs).")
    st.write("It can also be inferred that most European and some Asian countries lead the way in having the most number of masters and being placed in the higher ranks.")
    st.write("The players witht the higest FIDE average is the top ranked player")
    st.write("The top ranked players of all time is currently Magnus Carlsen with an FIDE average of 2,864")
    st.write("The higher number of players could mean that there would be more players being titled as masters")
    st.write("The higher age average could mean a higher overall FIDE average of the country.")
    st.write("Doesn't look like there is much of a correlation between the number of players competing and the overall FIDE average.")
    st.write("Vietnam seems to have the highest percentage in women players, along with Mongolia and Mozambique")
    st.write("Cambodia seems to have the highest FIDE average, but that because it has a small number of players with many of them having a high FIDE rating.")
    
    
Mplay = alt.Chart(statsdf).mark_point().encode(
    x='Num Players',
    y='Total # of Masters',
    color = 'FIDE Average',
    tooltip=['Country', 'Num Players', 'FIDE Average', 'Total # of Masters']
    #color=alt.condition(brush, 'FIDE Average:Q', alt.value('lightgray'))
).properties(
    title = 'Master and Player Correlation',
    width = 500,
    height = 500
).interactive()


rankFIDE = alt.Chart(statsdf).mark_point().encode(
    x='Num Players',
    y='FIDE Average',
    color = 'Age Avg',
    tooltip=['Country', 'Num Players', 'FIDE Average']
).properties(
    title = 'FIDE and # of Players Correlation',
    width = 500,
    height = 500
).interactive()


ageFIDE = alt.Chart(statsdf).mark_point().encode(
    x='Age Avg',
    y='FIDE Average',
    tooltip=['Country', 'Age Avg', 'FIDE Average']
).properties(
    title = 'Age and FIDE Correlation',
    width = 500,
    height = 500
).interactive()

st.write(Mplay)
st.write("The higher number of players could mean that there would be more players being titled as masters")

st.write(ageFIDE)
st.write("The higher age average could mean a higher overall FIDE average of the country.")

st.write(rankFIDE)
st.write("Doesn't look like there is much of a correlation between the number of players competing and the overall FIDE average.")