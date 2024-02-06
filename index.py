from flask import Flask, render_template, request, render_template_string
import visuals

app = Flask(__name__, template_folder="template")


@app.route('/')
def index():
    check = visuals.check_file()
    if check == 1:
        plot_dc_html = visuals.date_count_function()
        plot_sc_html = visuals.sender_count_function()
        plot_mt_html = visuals.mails_per_time_intervals()

        return render_template("index.html", plot_dc_html=plot_dc_html, plot_sc_html=plot_sc_html,
                               plot_mt_html=plot_mt_html, data_flag=1)

    else:
        return render_template("index.html", data_flag=0)


@app.route('/generate_report')
def generate_report():
    check = visuals.check_file()
    if check == 1:
        visuals.sweet_viz_report()

        return render_template("REPORT.html")


@app.route('/filter_mail', methods=['GET', 'POST'])
def filter_mail():
    if request.method == 'POST':
        keywords = request.form['emailInput']

        result_df = visuals.filter_record_mails(keywords)

        if result_df is not None and not result_df.empty:
            result_table = result_df.to_html(classes='table table-striped')
        else:
            result_table = '<p>No data found for the given inputs.</p>'

        return render_template_string(result_table=result_table)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
