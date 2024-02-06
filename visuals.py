import pandas as pd
import plotly.express as px
import sweetviz as sw
import os

# Assuming 'Date' is the column in your Excel file
try:
    df = pd.read_csv(r"mail.csv")
except Exception as e:
    print(f"Error: {e}")
    df = None


def check_file():
    if df is not None and not df.empty:
        return 1  # DataFrame exists and is not empty
    else:
        return 0  # DataFrame does not exist or is empty


def date_count_function():
    date_counts = df['Date'].value_counts().reset_index()

    date_counts.columns = ['Date', 'Count']
    sorted_date_counts = date_counts.sort_values(by='Date', ascending=False)

    color_scale = px.colors.qualitative.Plotly
    fig = px.bar(sorted_date_counts, x='Date', y='Count', title='Date Counts - Bar Graph', color='Count',
                 color_continuous_scale=color_scale)

    fig.update_xaxes(categoryorder='category ascending')
    fig.update_layout(height=500, width=1200)

    plot_dc_html = fig.to_html(full_html=False)

    return plot_dc_html


def sender_count_function():
    date_counts = df['SenderEmail'].value_counts().reset_index()

    date_counts.columns = ['SenderEmail', 'Count']
    sorted_date_counts = date_counts.sort_values(by='Count', ascending=False).head(8)

    color_scale = px.colors.qualitative.Plotly
    fig = px.bar(sorted_date_counts, x='SenderEmail', y='Count', title='Top 10 Sender Counts - Bar Graph',
                 hover_data={'SenderEmail': True, 'Count': True}, color='Count', color_continuous_scale=color_scale)

    fig.update_xaxes(categoryorder='total descending')
    fig.update_layout(height=500, width=1000)

    plot_sc_html = fig.to_html(full_html=False)

    return plot_sc_html


def mails_per_time_intervals():
    datetime = pd.to_datetime(df['Date'] + ' ' + df['Time'])

    interval = pd.cut(datetime.dt.hour,
                      bins=[0, 6, 12, 18, 24],
                      labels=['00:00-06:00', '06:00-12:00', '12:00-18:00', '18:00-24:00'],
                      include_lowest=True, right=False)

    # Count occurrences of mails in each time interval
    interval_counts = interval.value_counts().reset_index()
    interval_counts.columns = ['TimeInterval', 'Count']

    # Create a pie chart using Plotly Express
    fig = px.pie(interval_counts, names='TimeInterval', values='Count', title='Mail Counts by Time Interval')
    fig.update_layout(height=400, width=800)

    plot_mt_html = fig.to_html(full_html=False)

    return plot_mt_html


def sweet_viz_report():
    report_path = 'A:/Projects/MailSift/template/REPORT.html'
    if os.path.exists(report_path):
        pass
    else:
        report = sw.analyze(df)
        report.show_html(filepath='A:/Projects/MailSift/template/REPORT.html')


def filter_record_mails(keywords):
    filtered_rows = df[df['Payload'].str.contains('|'.join(keywords))]
    merged_df = pd.DataFrame(filtered_rows)

    return merged_df
