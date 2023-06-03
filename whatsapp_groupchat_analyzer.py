import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
##################################################################################################################
def set_dark_theme():
    # Define the CSS styles for the dark theme
    css = """
    <style>
    body {
        color: #FFFFFF;
        background-color: #000000;
    }
    </style>
    """
    # Apply the CSS styles
    st.markdown(css, unsafe_allow_html=True)
    # Set the default background color for Altair charts
    alt.themes.enable('dark')

set_dark_theme()
##################################################################################################################
# Page title
st.title("WhatsApp Group: \"Cousins - Across Borders\"")

st.markdown("""
The legendary family group was created by our legendary <a href="https://wa.me/17744733388" style="color:steelblue" target="_blank">**Neeraj Yellumahanti**</a> on 27-Jun-2013 around 2 AM IST and as they popularly say the rest is history.

I have put together some basic visualizations. I hope you'll like these analytics and strategically reposition yourself within the group to be featured in all key metrics.
""", unsafe_allow_html=True)

##################################################################################################################
df_daily_messages = pd.read_pickle('df_daily_messages.pkl')

# Improving Default Styles using Seaborn
sns.set_style("darkgrid")

# For better readablity;
plt.rcParams['font.size'] = 20
plt.rcParams['figure.figsize'] = (27, 6)      # Same as `plt.figure(figsize = (27, 6))`

# A basic plot
plt.plot(df_daily_messages.date, df_daily_messages.message_count)
plt.title('Messages sent per day over a time period')

# Saving the plots
plt.savefig('msg_plots.svg', format = 'svg')

# Display the plot in Streamlit
# st.pyplot(plt)
##################################################################################################################
df_no_of_messages = pd.read_pickle('df_no_of_messages.pkl')

# Create a new column that will be used for sorting in the chart
df_no_of_messages['sort'] = df_no_of_messages['number_of_msgs'].rank(method='first', ascending=False)

# Add a column 'name_display' to differentiate between 'Top 10' and 'All Others'
df_no_of_messages['name_display'] = df_no_of_messages.apply(
    lambda row: row['name'] if row['sort'] <= 35 else 'All Others',
    axis=1
)

# Group by 'name_display' and sum 'number_of_msgs', preserve 'sort' for the 'Top 10'
df_no_of_messages_grouped = df_no_of_messages.groupby(
    'name_display',
    as_index=False
).agg({'number_of_msgs': 'sum', 'sort': 'min'})

# Create a new column 'name_display_serial' with serial numbers as prefix
df_no_of_messages_grouped['Name'] = df_no_of_messages_grouped['sort'].apply(lambda x: f'{int(x)}. ' if x <= 35 else '') + df_no_of_messages_grouped['name_display']

# Create a horizontal bar chart using Altair
bar_user = alt.Chart(df_no_of_messages_grouped).mark_bar().encode(
    x='number_of_msgs:Q',
    y=alt.Y('Name:N', sort=alt.EncodingSortField(field='sort', op='min')),
    # color=alt.Color('name:N', legend=None)  # Remove if you don't want color
)

# Adjust dy for better text alignment
text_user = bar_user.mark_text(align='left', dx=2, dy=0, color='white').encode(text=alt.Text('number_of_msgs:Q', format=',d'))

chart_user = bar_user + text_user

# Configure the chart to be scrollable
# st.altair_chart(chart_user, use_container_width=True)
##################################################################################################################
df_group_name_org = pd.read_pickle('df_group_name.pkl')
df_group_name = df_group_name_org[['date', 'name', 'group_name']]
df_group_name = df_group_name.rename(columns={
    'date': 'Date',
    'name': 'Changed by',
    'group_name': 'New Group Name',
})

# CSS to hide the row indices in the table
hide_table_row_index = """
    <style>
    thead tr th:first-child {display:none}
    tbody th {display:none}
    </style>
    """
# st.markdown(hide_table_row_index, unsafe_allow_html=True)
# st.set_option('deprecation.showPyplotGlobalUse', False)
# st.table(df_group_name)
##################################################################################################################
# Top 10 days
df_top10days = pd.read_pickle('df_top10days.pkl')

# Convert 'date' to a datetime datatype
df_top10days['date'] = pd.to_datetime(df_top10days['date'])

# Convert date to the 'YYYY-MMM-DD' format
df_top10days['date'] = df_top10days['date'].dt.strftime('%Y-%b-%d')

# Create a new column that will be used for sorting in the chart
df_top10days['sort'] = df_top10days['message_count'].rank(method='first', ascending=False)

# Create a vertical bar chart using Altair
bar_top10 = alt.Chart(df_top10days).mark_bar().encode(
    y='message_count:Q',
    x=alt.X('date:N', sort=alt.EncodingSortField(field='sort', op='min'), axis=alt.Axis(labelAngle=0, labelFontSize=10)),
    # color=alt.Color('name:N', legend=None)  # Remove if you don't want color
).properties(
    width=800  # Increase the width of the chart
)

text_top10 = bar_top10.mark_text(align='center', dx=0, dy=-10, color='white').encode(text=alt.Text('message_count:Q', format=',d'))

chart_top10 = bar_top10 + text_top10

# Configure the chart to be scrollable
# st.altair_chart(chart_top10, use_container_width=True)
##################################################################################################################
df_by_hour = pd.read_pickle('df_by_hour.pkl')

bar_hour = alt.Chart(df_by_hour).mark_bar(color='lightblue').encode(
    y='message_count:Q',
    x=alt.X('hour:N', sort=alt.EncodingSortField(field='sort', op='min'), axis=alt.Axis(labelAngle=0, labelFontSize=10)),
)
text_hour = bar_hour.mark_text(align='center', dx=0, dy=-10, color='white').encode(text=alt.Text('message_count:Q', format=',d'))
chart_hour = bar_hour + text_hour
# st.altair_chart(chart_hour, use_container_width=True)

df_by_day = pd.read_pickle('df_by_day.pkl')

# Specify the correct order for the days of the week
ordered_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# In 'day' chart, sort X-axis by days of the week
bar_day = alt.Chart(df_by_day).mark_bar(color='lightgreen').encode(
    y='message_count:Q',
    x=alt.X('day:N', sort=ordered_days, axis=alt.Axis(labelAngle=0, labelFontSize=10)),
)
text_day = bar_day.mark_text(align='center', dx=0, dy=-10, color='white').encode(text=alt.Text('message_count:Q', format=',d'))
chart_day = bar_day + text_day
# st.altair_chart(chart_day, use_container_width=True)

df_by_month = pd.read_pickle('df_by_month.pkl')

# Specify the correct order for the months of the year
ordered_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# In 'month' chart, sort X-axis by months of the year
bar_month = alt.Chart(df_by_month).mark_bar(color='steelblue').encode(
    y='message_count:Q',
    x=alt.X('month:N', sort=ordered_months, axis=alt.Axis(labelAngle=0, labelFontSize=10)),
)
text_month = bar_month.mark_text(align='center', dx=0, dy=-10, color='white').encode(text=alt.Text('message_count:Q', format=',d'))
chart_month = bar_month + text_month

# Configure the chart to be scrollable
# st.altair_chart(chart_month, use_container_width=True)
##################################################################################################################
# Heatmap Hour & Day
whatsapp_chat_formatted = pd.read_pickle('whatsapp_chat_formatted.pkl')

# Specify the correct order for the days of the week
ordered_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# Create an ordered categorical type with our specified day order
whatsapp_chat_formatted['day'] = pd.Categorical(whatsapp_chat_formatted['day'], ordered_days, ordered=True)

# Count the number of messages per hour and day
message_counts_hd = whatsapp_chat_formatted.groupby(['hour', 'day']).size().reset_index(name='message_count')
message_counts_hd['message_count'] = message_counts_hd['message_count'].astype(float)

# Create Altair chart
chart_heatmap_hd = alt.Chart(message_counts_hd).mark_rect().encode(
    alt.X('hour:O', title='Hour'),
    alt.Y('day:O', sort=ordered_days, title='Day'), # specify the sort order in the encoding
    # alt.Color('message_count:Q', title='Message Count'),
    alt.Color('message_count:Q', scale=alt.Scale(reverse=True), title='Message Count')
    # alt.Color('message_count:Q', scale=alt.Scale(scheme='blueorange', reverse=True), title='Message Count')
)

# Add text labels
text_heatmap_hd = chart_heatmap_hd.mark_text(baseline='middle', align='center').encode(
    text=alt.Text('message_count:Q', format='.0f'),
    color=alt.condition(
        alt.datum.message_count == message_counts_hd['message_count'].max(),
        alt.value('black'),
        alt.value('black')
    )
)

chart_heatmap_hd = chart_heatmap_hd + text_heatmap_hd

# st.altair_chart(chart_heatmap_hd)

# Find top 3 message counts
heatmap_hd_top_3 = message_counts_hd.sort_values('message_count', ascending=False).head(3)
heatmap_hd_top_3['message_count'] = heatmap_hd_top_3['message_count'].astype(int)

# Find bottom 3 message counts
heatmap_hd_bottom_3 = message_counts_hd.sort_values('message_count', ascending=True).head(3)
heatmap_hd_bottom_3['message_count'] = heatmap_hd_bottom_3['message_count'].astype(int)

##################################################################################################################
# Heatmap Day & Month
whatsapp_chat_formatted = pd.read_pickle('whatsapp_chat_formatted.pkl')

# Specify the correct order for the days of the week
ordered_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
ordered_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Create an ordered categorical type with our specified day order
whatsapp_chat_formatted['day'] = pd.Categorical(whatsapp_chat_formatted['day'], ordered_days, ordered=True)
whatsapp_chat_formatted['month'] = pd.Categorical(whatsapp_chat_formatted['month'], ordered_months, ordered=True)

# Count the number of messages per hour and day
message_counts_dm = whatsapp_chat_formatted.groupby(['day', 'month']).size().reset_index(name='message_count')
message_counts_dm['message_count'] = message_counts_dm['message_count'].astype(float)

# Create Altair chart
chart_heatmap_dm = alt.Chart(message_counts_dm).mark_rect().encode(
    alt.X('month:O', sort=ordered_months, title='Month'),
    alt.Y('day:O', sort=ordered_days, title='Day'), # specify the sort order in the encoding
    # alt.Color('message_count:Q', title='Message Count'),
    alt.Color('message_count:Q', scale=alt.Scale(reverse=True), title='Message Count')
    # alt.Color('message_count:Q', scale=alt.Scale(scheme='blueorange', reverse=True), title='Message Count')
)

# Add text labels
text_heatmap_dm = chart_heatmap_dm.mark_text(baseline='middle', align='center').encode(
    text=alt.Text('message_count:Q', format='.0f'),
    color=alt.condition(
        alt.datum.message_count == message_counts_dm['message_count'].max(),
        alt.value('black'),
        alt.value('black')
    )
)

chart_heatmap_dm = chart_heatmap_dm + text_heatmap_dm

# st.altair_chart(chart_heatmap_hd)

# Find top 3 message counts
heatmap_dm_top_3 = message_counts_dm.sort_values('message_count', ascending=False).head(3)
heatmap_dm_top_3['message_count'] = heatmap_dm_top_3['message_count'].astype(int)

# Find bottom 3 message counts
heatmap_dm_bottom_3 = message_counts_dm.sort_values('message_count', ascending=True).head(3)
heatmap_dm_bottom_3['message_count'] = heatmap_dm_bottom_3['message_count'].astype(int)

##################################################################################################################
# Heatmap Month & Year
whatsapp_chat_formatted = pd.read_pickle('whatsapp_chat_formatted.pkl')

# Specify the correct order for the days of the week
ordered_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Create an ordered categorical type with our specified day order
whatsapp_chat_formatted['month'] = pd.Categorical(whatsapp_chat_formatted['month'], ordered_months, ordered=True)

# Count the number of messages per hour and day
message_counts_my = whatsapp_chat_formatted.groupby(['month', 'year']).size().reset_index(name='message_count')
message_counts_my['message_count'] = message_counts_my['message_count'].astype(float)

# Create Altair chart
chart_heatmap_my = alt.Chart(message_counts_my).mark_rect().encode(
    alt.X('year:O', title='Year'),
    alt.Y('month:O', sort=ordered_months, title='Month'), # specify the sort order in the encoding
    # alt.Color('message_count:Q', title='Message Count'),
    alt.Color('message_count:Q', scale=alt.Scale(reverse=True), title='Message Count')
    # alt.Color('message_count:Q', scale=alt.Scale(scheme='blueorange', reverse=True), title='Message Count')
)

text_heatmap_my = chart_heatmap_my.mark_text(baseline='middle', align='center').encode(
    text=alt.Text('message_count:Q', format='.0f'),
    color=alt.condition(
        alt.datum.message_count == message_counts_my['message_count'].max(),
        alt.value('black'),
        alt.value('black')
    )
)

chart_heatmap_my = chart_heatmap_my + text_heatmap_my

# Find top 3 message counts
heatmap_my_top_3 = message_counts_my.sort_values('message_count', ascending=False).head(3)
heatmap_my_top_3['message_count'] = heatmap_my_top_3['message_count'].astype(int)

# Find bottom 3 message counts
heatmap_my_bottom_3 = message_counts_my.sort_values('message_count', ascending=True).head(3)
heatmap_my_bottom_3['message_count'] = heatmap_my_bottom_3['message_count'].astype(int)

##################################################################################################################
whatsapp_chat_formatted = pd.read_pickle('whatsapp_chat_formatted.pkl')

STOPWORDS.update(['group', 'link', 'invite', 'joined', 'message', 'deleted', 'yeah', 
                  'hai', 'yes', 'okay', 'ok', 'will', 'use', 'using', 'one', 'know', 
                  'guy', 'group', 'media', 'omitted'])
stopwords = STOPWORDS

# Generate comment_words using a generator expression and str.join()
comment_words = ' '.join(word for message in whatsapp_chat_formatted.message for word in str(message).lower().split())

wordcloud = WordCloud(width = 800, height = 400, 
                background_color ='white', 
                stopwords = stopwords, 
                min_font_size = 10).generate(comment_words)

# st.image(wordcloud.to_image())
##################################################################################################################
# Container with 1 column
with st.container():
    st.subheader("Messages Over Time")
    st.pyplot(plt) 

st.markdown('---')

with st.container():
    st.subheader("Users Chart")
    st.altair_chart(chart_user, use_container_width=True) 

st.markdown('---')

with st.container():
    st.subheader("Most used words")
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.table(df_group_name)

st.markdown('---')

with st.container():
    st.subheader("Top 10 days with most conversations")
    # st.altair_chart(chart_top10, use_container_width=True) 
    st.image(wordcloud.to_image()) 

st.markdown('---')

with st.container():
    st.subheader("Top 10 days with most conversations")
    st.altair_chart(chart_top10, use_container_width=True)  

st.markdown('---')

with st.container():
    st.subheader("Messages by Hour")
    st.altair_chart(chart_hour, use_container_width=True)

with st.container():
    st.subheader("Messages by Day")
    st.altair_chart(chart_day, use_container_width=True)

with st.container():
    st.subheader("Messages by Month")
    st.altair_chart(chart_month, use_container_width=True)

st.markdown('---')

with st.container():
    st.subheader("Heatmap of # of Messages by Hour & Weekday")
    st.altair_chart(chart_heatmap_hd, use_container_width=True)

# Container with 2 columns
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 3")
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        # st.set_option('deprecation.showPyplotGlobalUse', False)
        st.table(heatmap_hd_top_3)

    with col2:
        st.subheader("Bottom 3")
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        # st.set_option('deprecation.showPyplotGlobalUse', False)
        st.table(heatmap_hd_bottom_3)

st.markdown('---')

with st.container():
    st.subheader("Heatmap of # of Messages by Weekday & Month")
    st.altair_chart(chart_heatmap_dm, use_container_width=True)

# Container with 2 columns
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 3")
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        # st.set_option('deprecation.showPyplotGlobalUse', False)
        st.table(heatmap_dm_top_3)

    with col2:
        st.subheader("Bottom 3")
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        # st.set_option('deprecation.showPyplotGlobalUse', False)
        st.table(heatmap_dm_bottom_3)

st.markdown('---')

with st.container():
    st.subheader("Heatmap of # of Messages by Month & Year")
    st.altair_chart(chart_heatmap_my, use_container_width=True)

# Container with 2 columns
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 3")
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        # st.set_option('deprecation.showPyplotGlobalUse', False)
        st.table(heatmap_my_top_3)

    with col2:
        st.subheader("Bottom 3")
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        # st.set_option('deprecation.showPyplotGlobalUse', False)
        st.table(heatmap_my_bottom_3)
##################################################################################################################
