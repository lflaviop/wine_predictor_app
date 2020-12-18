import joblib
import os

from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import FloatField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY']='wP4xQ8hUljJ5oI1c'
bootstrap = Bootstrap(app)

class InputForm(FlaskForm):
	alcohol  = FloatField('Álcool:', validators=[DataRequired()])
	malic_acid = FloatField('Ácido málico:', validators=[DataRequired()])
	total_phenols = FloatField('Fenóis totais:', validators=[DataRequired()])
	flavanoids = FloatField('Fenóis flavonóides:', validators=[DataRequired()])
	nonflav_phenols = FloatField('Fenóis não-flavonóides:', validators=[DataRequired()])
	proanthocyanins = FloatField('Proantocianino:', validators=[DataRequired()])
	color = FloatField('Intensidade de cor:', validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
	form = InputForm(request.form)
	specie = 'No-image'
	
	if form.validate_on_submit():
		x = [[form.alcohol.data, form.malic_acid.data, form.total_phenols.data, form.flavanoids.data, form.nonflav_phenols.data, form.proanthocyanins.data, form.color.data]]
		specie = str(make_prediction(x))
	
	return render_template('index.html', form=form, specie=specie)

def make_prediction(x):
	filename = os.path.join('model', 'finalized_model.sav')
	model = joblib.load(filename)
	return model.predict(x)[0]
