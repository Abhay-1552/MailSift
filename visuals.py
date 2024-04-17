import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import sweetviz as sw
import os


class Graph:
    def __init__(self, json_data):
        self.df = pd.DataFrame(json_data)
        print(self.df)

    # SweetViz report
    def sweet_viz_report(self):
        report_path = 'A:/Projects/MailSift/template/REPORT.html'
        if os.path.exists(report_path):
            pass
        else:
            report = sw.analyze(self.df)
            report.show_html(filepath='A:/Projects/MailSift/template/REPORT.html')

    # Dashboard
    # Total number of mails by individual senders
    def sender_count_function(self):
        sender_counts = self.df['SenderEmail'].value_counts().reset_index()
        sender_counts.columns = ['SenderEmail', 'Count']
        sorted_sender_counts = sender_counts.sort_values(by='Count', ascending=False).head(10)

        color_scale = px.colors.qualitative.Plotly
        fig = px.bar(sorted_sender_counts, x='SenderEmail', y='Count', title='Top 10 Sender Counts - Bar Graph',
                     hover_data={'SenderEmail': True, 'Count': True}, color='Count', color_continuous_scale=color_scale)

        fig.update_xaxes(categoryorder='total descending')
        fig.update_layout(height=500, width=1000)

        plot_sc_html = fig.to_html(full_html=False)

        return plot_sc_html

    # Mail counts on individual date
    def date_count_function(self):
        date_counts = self.df['Date'].value_counts().reset_index()
        date_counts.columns = ['Date', 'Count']
        sorted_date_counts = date_counts.sort_values(by='Date', ascending=True)

        color_scale = px.colors.qualitative.Plotly
        fig = px.bar(sorted_date_counts, x='Date', y='Count', title='Date Counts - Bar Graph', color='Count',
                     color_continuous_scale=color_scale)

        fig.update_xaxes(categoryorder='category ascending')
        fig.update_layout(height=500, width=1200)

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
        fig.update_layout(height=500, width=600)

        plot_mt_html = fig.to_html(full_html=False)

        return plot_mt_html

    # WordCloud using Subject
    def word_cloud(self):
        subject = self.df['Subject'].astype(str)
        text = ' '.join(subject)

        wordcloud = WordCloud(width=1200, height=600, background_color='white').generate(text)
        fig = go.Figure(go.Image(z=wordcloud.to_array()))

        # Remove axes
        fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False))
        fig.update_layout(height=500, width=600)

        plot_wc_html = fig.to_html(full_html=False)

        return plot_wc_html
