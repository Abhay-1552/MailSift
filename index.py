from flask import Flask, render_template
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
