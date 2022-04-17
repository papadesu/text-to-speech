import os
from google.cloud import texttospeech

import io
import streamlit as st

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'udemy-project-347008-dc24681c4d8c.json'

def synthesize_sppech(text, lang='日本語', gender='defalut'):
    gender_type = {
        'defalut': texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED,
        'male': texttospeech.SsmlVoiceGender.MALE,
        'female': texttospeech.SsmlVoiceGender.FEMALE,
        'neutral': texttospeech.SsmlVoiceGender.NEUTRAL
    }
    lang_code = {
        '英語': 'en-US',
        '日本語': 'ja-JP'
    }


    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code[lang], ssml_gender=gender_type[gender]
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response

st.title('音声出力アプリ')

st.markdown('### データ準備')

input_opthon = st.selectbox(
    '入力データの選択',
    ('直接入力', 'テキストファイル')
)
input_deta = None

if input_opthon == '直接入力':
    input_deta = st.text_area('こちらにテキストを入力して下さい。', 'Cloud Speech-to-Text用のサンプル分になります。')
else:
    uploaded_file = st.file_uploader('テキストファイルをアップロードしてください。', ['txt'])
    if uploaded_file is not None:
        content = uploaded_file.read()
        input_deta = content.decode()

if input_deta is not None:
    st.write('入力データ')
    st.write(input_deta)
    st.markdown('### パラメータ設定')
    st.subheader('言語と話者の性別選択')

    lang = st.selectbox(
        '言語を選択してください',
        ('日本語', '英語')
    )
    gender = st.selectbox(
        '話者の性別を選択してください',
        ('defalut', 'male', 'female', 'neutral')
    )
    st.markdown('### 音声合成')
    st.write('こちらの文章で音声ファイルの生成を行いますか？')
    if st.button('開始'):
        comment = st.empty()
        comment.write('音声出力を開始します')
        response = synthesize_sppech(input_deta, lang, gender=gender)
        st.audio(response.audio_content)
        comment.write('完了しました')