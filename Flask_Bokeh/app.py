import pandas as pd
import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import csv
import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.embed import file_html
from bokeh.resources import CDN
from bokeh.embed import components
# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from bokeh.models import Panel
from scripts.matrix import matrix_tab

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
ALLOWED_EXTENSIONS = {'csv', 'txt'}

app = Flask(__name__)
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    var1 = "uploads/" + filename
    myDataFrame = pd.read_csv(var1)
    author_list = myDataFrame.iloc[:, 0]

    m = [None] * (author_list.size)
    author = [None] * (author_list.size)
    i = 0
    while i < author_list.size:
        m[i] = author_list[i].split(";")
        i += 1

    i = 0
    while i < (author_list.size):
        n = m[i][1:-1]
        author[i] = m[i][0]
        m[i] = n
        i += 1

    i = 0
    while i < author_list.size:
        j = 0
        while j < author_list.size:
            m[i][j] = float(m[i][j])
            j += 1
        i += 1

    arrayM = np.array(m)
    p = figure(x_range=(0, 2), y_range=(0, 2))
    ds = ColumnDataSource(data=dict(image=[arrayM]))
    p.image(image='image', x=0, y=0, dw=2, dh=2, source=ds, palette="Spectral11")

    dfM = pd.DataFrame(m)
    dfM['sum'] = dfM[list(dfM.columns)].sum(axis=1)

    minimum = 100
    maximum = 150

    dfMFilter = dfM[(dfM['sum'] >= minimum) & (dfM['sum'] <= maximum)]

    dfM = dfM.sort_values(by='sum', ascending=0)
    del dfM['sum']
    del dfMFilter['sum']

    dfM = dfM.reindex(columns=dfM.index)
    mReorder = dfM.as_matrix(columns=None)
    arrayMReorder = np.array(mReorder)

    dfMFilter = dfMFilter.reindex(columns=dfMFilter.index)
    mFilterReorder = dfMFilter.as_matrix(columns=None)
    arrayMFilterReorder = np.array(mFilterReorder)

    pReorder = figure(x_range=(0, 2), y_range=(0, 2))
    pReorder.image(image=[arrayMReorder], x=0, y=0, dw=2, dh=2, palette="Spectral11")

    # script, div = components(p)
    # tab = Panel(child=p, title='Matrix')
    # curdoc().add_root(tab)
    # return render_template('upload.html', var1=var1, tab=tab)
    script, div = components(p)
    script_2, div_2 = components(pReorder)
    return render_template('upload.html',  var1=var1, script=script, div=div, script2=script_2, div2=div_2)
    # return render_template('upload.html', tab=tab)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)