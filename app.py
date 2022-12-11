import os
import argparse
import openai
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.urandom(32)

def getsong(artist):
    """ get possible songtext based on parameter artist """
    prompt_text = f"Artist: {artist}\n\nLyrics:\n"
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt_text,
        temperature=0.7,
        max_tokens=256,
        frequency_penalty=0.5
    )
    return prompt_text + response['choices'][0]['text']

# forms
class ArtistForm(FlaskForm):
    artist = StringField(label='Artist', render_kw={"placeholder": "Artist"})
    submit = SubmitField("submit")

@app.route('/', methods=['GET', 'POST'])
def index(song=None):
    form = ArtistForm()
    if form.submit.data:
        song = getsong(form.artist.data)
    return render_template('home.html', form=form, song=song)

if __name__ == '__main__':
   app.run()
