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

        emails = sorted_date_counts['Date'].tolist()
        counts = sorted_date_counts['Count'].tolist()

        json_output = []
        for i, j in zip(emails, counts):
            k = {'date': i, 'count': j}
            json_output.append(k)

        return json_output

    # Mail counts per time intervals
    def mails_per_time_intervals(self):
        datetime = pd.to_datetime(self.df['Date'] + ' ' + self.df['Time'], format='%d/%m/%Y %H:%M')

        interval = pd.cut(datetime.dt.hour,
                          bins=[0, 6, 12, 18, 24],
                          labels=['00:00-06:00', '06:00-12:00', '12:00-18:00', '18:00-24:00'],
                          include_lowest=True, right=False)

        interval_counts = interval.value_counts().reset_index()
        interval_counts.columns = ['TimeInterval', 'Count']

        # Convert DataFrame rows to lists
        result_lists = interval_counts.values.tolist()
        print(result_lists)

        json_output = []
        for i in result_lists:
            k = {'value': i[1], 'category': i[0]}
            json_output.append(k)

        return json_output

    # WordCloud using Subject
    def word_cloud(self):
        subject = self.df['Subject'].astype(str)
        text = ' '.join(subject)

        return text
