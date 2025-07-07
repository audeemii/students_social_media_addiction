import pandas as pd
import plotly.express as px
import streamlit as st

## Carga el dataset en la misma carpeta
df = pd.read_csv('students_social_media_addiction.csv')

## Pasa todos los strings a minusculas (columnas y datos)
df.columns = df.columns.str.lower()

df['gender'] = df['gender'].str.lower()
df['academic_level'] = df['academic_level'].str.lower()
df['country'] = df['country'].str.lower()
df['most_used_platform'] = df['most_used_platform'].str.lower()
df['affects_academic_performance'] = df['affects_academic_performance'].str.lower()
df['relationship_status'] = df['relationship_status'].str.lower()

## Cambia tipo de datos de 'student_id' a 'str'
df['student_id'] = df['student_id'].astype('str')

## Renombra algunas columnas por versiones mas cortas
colums_name = {
    'avg_daily_usage_hours':'daily_usage',
    'most_used_platform':'platform',
    'affects_academic_performance':'performance',
    'sleep_hours_per_night':'spleep_hours',
    'mental_health_score':'mental_health',
    'relationship_status':'rel_status',
    'conflicts_over_social_media':'conflicts'
    }
df = df.rename( columns=colums_name )

## Streamlit
st.title("Student's Social Media Addiction")

about_data = '''## [About Dataset](https://www.kaggle.com/datasets/adilshamim8/social-media-addiction-vs-relationships)

The Student Social Media & Relationships dataset contains anonymized records of students social‐media behaviors and related life outcomes. It spans multiple countries and academic levels, focusing on key dimensions such as usage intensity, platform preferences, and relationship dynamics. Each row represents one student’s survey response, offering a cross‐sectional snapshot suitable for statistical analysis and machine‐learning applications.

- Population: Students aged 16–25 enrolled in high school, undergraduate, or graduate programs.
- Geography: Multi‐country coverage (e.g., Bangladesh, India, USA, UK, Canada, Australia, Germany, Brazil, Japan, South Korea).
- Timeframe: Data collected via a one‐time online survey administered in Q1 2025.
- Volume: Configurable sample sizes (e.g., 100, 500, 1,000 records) based on research needs.

#### About columns

| Variable | Type | Description |
|---|---|---|
| Student_ID | Integer | Unique respondent identifier |
| Age | Integer | Age in years |
| Gender | Categorical | “Male” or “Female” |
| Academic_Level | Categorical | High School / Undergraduate / Graduate |
| Country | Categorical | Country of residence |
| Avg_Daily_Usage_Hours | Float | Average hours per day on social media |
| Most_Used_Platform | Categorical | Instagram, Facebook, TikTok, etc. |
| Affects_Academic_Performance | Boolean | Self‐reported impact on academics (Yes/No) |
| Sleep_Hours_Per_Night | Float | Average nightly sleep hours |
| Mental_Health_Score | Integer | Self‐rated mental health (1 = poor to 10 = excellent) |
| Relationship_Status | Categorical | Single / In Relationship / Complicated |
| Relationship_Status | Categorical | Single / In Relationship / Complicated |
| Conflicts_Over_Social_Media | Integer | Number of relationship conflicts due to social media |
| Addicted_Score | Integer | Social Media Addiction Score (1 = low to 10 = high) |

'''

st.markdown(about_data)

st.markdown('## Data analysis')

st.markdown('#### Data sample')
st.write(df.sample(5))

st.markdown('#### Top 5 platforms')
top_platform = df.groupby('platform')['platform'].count().sort_values(ascending=False)[:5]
mean_top_platform = df[ df['platform'].isin(top_platform.index) ].groupby('platform')['daily_usage'].mean().sort_values(ascending=False)
st.dataframe(mean_top_platform, width=400)

## ----------------------------- daily usage -------------------------------------

daily_usage_txt = '''#### Daily usage

- The most important benchmark is time spent on social media, or "daily_usage," measured in hours. This amount is an average daily value estimated by users, a reference weight that users place on social media use relative to other activities during the day. It is not a rigorously measured amount or directly measured from any device.

- The most used platforms are Instagram, TikTok, Facebook, WhatsApp, and Twitter.

- On average, more than 6 hours are spent on WhatsApp, more than 5 hours on TikTok, and more than 4 hours on the rest of the top platforms.

- Average daily usage is used as the reference parameter to measure how it affects other parameters.
'''

st.markdown(daily_usage_txt)

with st.expander('Show / Hide'):
    fig = px.histogram(df[ df['platform'].isin(top_platform.index) ], x="daily_usage", color='platform', facet_col='platform',title='Mean daily usage by top platforms')
    st.write(fig)


## ----------------------------- addicted score -------------------------------------

addicted_score_txt = '''#### Relation between daily usage and addicted score

- There is a clear correlation between students' average daily usage and their self-assigned addiction score.

- Users who perceive that social media use has not affected their academic performance are those who spend the least amount of time on it. Those who perceive that it has affected their academic performance are those who spend the most time on it.
'''

st.markdown(addicted_score_txt)

with st.expander('Show / Hide'):
    fig = px.scatter(df, x="daily_usage", y='addicted_score', color='performance', title='Scatter of daily_usage and addicted_score')
    st.write(fig)


## ----------------------------- sleep hours -------------------------------------

sleep_hours_txt = '''#### Relation between daily usage and sleep hours

- The respondent's average nightly sleep duration in hours, provided to investigate correlations between screen time and sleep quality/quantity.

- Since they increase the amount of time spent on social media, it's expected to affect the amount of time spent on other areas. In this case, a strong negative correlation is observed between daily use and sleep hours.
'''

st.markdown(sleep_hours_txt)

with st.expander('Show / Hide'):
    fig = px.scatter(df[ df['platform'].isin(top_platform.index) ], x="daily_usage", y='spleep_hours', color='platform', title='Scatter of daily_usage and sleep_hours')
    st.write(fig)


## ----------------------------- mental health -------------------------------------

mental_health_txt = '''#### Relation between daily usage and mental health

- A self-rated integer from 1 (poor) to 10 (excellent) indicating overall mental well-being, allowing assessment of potential associations with social media habits.

- There is a negative correlation between social media use and self-perceived mental health. Of course, there is also a strong correlation between perceived mental health and sleep hours.

- Students who perceive themselves as having better mental health are also those who give themselves lower social media addiction scores. They are the ones who sleep more.

- There is no distinction in the time used for the different relationship statuses.
'''

st.markdown(mental_health_txt)

with st.expander('Show / Hide'):

    fig = px.scatter(df[ df['platform'].isin(top_platform.index) ], x="daily_usage", y='mental_health', title='Scatter of daily_usage and mental_health')

    left_mental, middle_mental, right_mental = st.columns(3)
    if left_mental.button("Relationship status", key='left_mental', use_container_width=True):
        fig = px.scatter(df[ df['platform'].isin(top_platform.index) ], x="daily_usage", y='mental_health', color='rel_status', title='Scatter of daily_usage and mental_health')
    if middle_mental.button("Gender", key='middle_mental', use_container_width=True):
        fig = px.scatter(df[ df['platform'].isin(top_platform.index) ], x="daily_usage", y='mental_health', color='gender', title='Scatter of daily_usage and mental_health')
    if right_mental.button("None", key='right_mental', use_container_width=True):
        fig = px.scatter(df[ df['platform'].isin(top_platform.index) ], x="daily_usage", y='mental_health', title='Scatter of daily_usage and mental_health')

    st.write(fig)
