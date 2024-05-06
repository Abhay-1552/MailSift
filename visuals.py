import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import json


class Graph:
    def __init__(self, json_data):
        self.df = pd.DataFrame(json_data)

    # Dashboard
    # Total number of mails by individual senders
    def sender_count_to_lists(self):
        sender_counts = self.df['SenderEmail'].value_counts().reset_index()
        sender_counts.columns = ['SenderEmail', 'Count']
        sorted_sender_counts = sender_counts.sort_values(by='Count', ascending=False).head(10)

        # Extract email and count data
        emails = sorted_sender_counts['SenderEmail'].tolist()
        counts = sorted_sender_counts['Count'].tolist()

        json_output = []
        for i, j in zip(emails, counts):
            k = {'email': i, 'count': j}
            json_output.append(k)

        return json_output

    # Mail counts on individual date
    def date_count_function(self):
        date_counts = self.df['Date'].value_counts().reset_index()
        date_counts.columns = ['Date', 'Count']
        sorted_date_counts = date_counts.sort_values(by='Date', ascending=True)

        color_scale = px.colors.qualitative.Plotly
        fig = px.bar(sorted_date_counts, x='Date', y='Count', title='Date Counts - Bar Graph', color='Count',
                     color_continuous_scale=color_scale)

        fig.update_xaxes(categoryorder='category ascending')
        fig.update_layout(height=450, width=700)

        plot_dc_html = fig.to_html(full_html=False)

        return plot_dc_html

    # Mail counts per time intervals
    def mails_per_time_intervals(self):
        datetime = pd.to_datetime(self.df['Date'] + ' ' + self.df['Time'], format='%d/%m/%Y %H:%M')

        interval = pd.cut(datetime.dt.hour,
                          bins=[0, 6, 12, 18, 24],
                          labels=['00:00-06:00', '06:00-12:00', '12:00-18:00', '18:00-24:00'],
                          include_lowest=True, right=False)

        interval_counts = interval.value_counts().reset_index()
        interval_counts.columns = ['TimeInterval', 'Count']

        # Create a pie chart using Plotly Express
        fig = px.pie(interval_counts, names='TimeInterval', values='Count', title='Mail Counts by Time Interval')
        fig.update_layout(height=450, width=500)

        plot_mt_html = fig.to_html(full_html=False)

        return plot_mt_html

    # WordCloud using Subject
    def word_cloud(self):
        subject = self.df['Subject'].astype(str)
        text = ' '.join(subject)

        return text
