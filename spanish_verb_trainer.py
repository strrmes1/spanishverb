import streamlit as st
import random
import json
import datetime
from typing import Dict, List, Tuple

# Конфигурация страницы
st.set_page_config(
    page_title="🇪🇸 Тренажер испанских глаголов",
    page_icon="🇪🇸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS для мобильной адаптивности
st.markdown("""
<style>
    /* Общие стили для мобильных устройств */
    @media (max-width: 768px) {
        .main > div {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        /* Увеличиваем размер кнопок на мобильных */
        .stButton > button {
            height: 3rem;
            font-size: 1.1rem;
        }
        
        /* Улучшаем отображение метрик */
        [data-testid="metric-container"] {
            border: 1px solid #e0e0e0;
            padding: 0.5rem;
            border-radius: 0.5rem;
            margin-bottom: 0.5rem;
        }
        
        /* Стили для карточек глаголов */
        .verb-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 1rem;
            border-radius: 1rem;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .verb-title {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .verb-translation {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 1rem;
        }
        
        .pronoun-display {
            font-size: 1.8rem;
            font-weight: bold;
            margin: 1rem 0;
            background: rgba(255,255,255,0.2);
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            display: inline-block;
        }
        
        .answer-display {
            font-size: 2rem;
            font-weight: bold;
            background: rgba(255,255,255,0.9);
            color: #2d5e3e;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
    }
    
    /* Для больших экранов */
    @media (min-width: 769px) {
        .verb-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2rem;
            border-radius: 1rem;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        }
        
        .verb-title {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .verb-translation {
            font-size: 1.4rem;
            opacity: 0.9;
            margin-bottom: 1.5rem;
        }
        
        .pronoun-display {
            font-size: 2rem;
            font-weight: bold;
            margin: 1.5rem 0;
            background: rgba(255,255,255,0.2);
            padding: 0.8rem 1.5rem;
            border-radius: 0.5rem;
            display: inline-block;
        }
        
        .answer-display {
            font-size: 2.5rem;
            font-weight: bold;
            background: rgba(255,255,255,0.9);
            color: #2d5e3e;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 1.5rem 0;
        }
    }
    
    /* Скрытие стандартных элементов Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Улучшение отображения selectbox на мобильных */
    .stSelectbox > div > div {
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Данные глаголов
VERBS = {
    'ser': {'translation': 'быть, являться', 'type': 'irregular'},
    'estar': {'translation': 'находиться, быть', 'type': 'irregular'},
    'tener': {'translation': 'иметь', 'type': 'irregular'},
    'hacer': {'translation': 'делать', 'type': 'irregular'},
    'decir': {'translation': 'говорить, сказать', 'type': 'irregular'},
    'ir': {'translation': 'идти, ехать', 'type': 'irregular'},
    'ver': {'translation': 'видеть', 'type': 'irregular'},
    'dar': {'translation': 'давать', 'type': 'irregular'},
    'saber': {'translation': 'знать', 'type': 'irregular'},
    'querer': {'translation': 'хотеть, любить', 'type': 'irregular'},
    'llegar': {'translation': 'прибывать, приходить', 'type': 'regular-ar'},
    'pasar': {'translation': 'проходить, проводить', 'type': 'regular-ar'},
    'deber': {'translation': 'быть должным', 'type': 'regular-er'},
    'poner': {'translation': 'класть, ставить', 'type': 'irregular'},
    'parecer': {'translation': 'казаться', 'type': 'irregular'},
    'quedar': {'translation': 'оставаться', 'type': 'regular-ar'},
    'creer': {'translation': 'верить, считать', 'type': 'regular-er'},
    'hablar': {'translation': 'говорить', 'type': 'regular-ar'},
    'llevar': {'translation': 'носить, нести', 'type': 'regular-ar'},
    'dejar': {'translation': 'оставлять', 'type': 'regular-ar'},
    'seguir': {'translation': 'следовать, продолжать', 'type': 'irregular'},
    'encontrar': {'translation': 'находить, встречать', 'type': 'irregular'},
    'llamar': {'translation': 'звать, называть', 'type': 'regular-ar'},
    'venir': {'translation': 'приходить', 'type': 'irregular'},
    'pensar': {'translation': 'думать', 'type': 'irregular'},
    'salir': {'translation': 'выходить', 'type': 'irregular'},
    'vivir': {'translation': 'жить', 'type': 'regular-ir'},
    'sentir': {'translation': 'чувствовать', 'type': 'irregular'},
    'trabajar': {'translation': 'работать', 'type': 'regular-ar'},
    'estudiar': {'translation': 'изучать', 'type': 'regular-ar'}
}

PRONOUNS = ['yo', 'tú', 'él/ella', 'nosotros', 'vosotros', 'ellos/ellas']

CONJUGATIONS = {
    'presente': {
        'ser': ['soy', 'eres', 'es', 'somos', 'sois', 'son'],
        'estar': ['estoy', 'estás', 'está', 'estamos', 'estáis', 'están'],
        'tener': ['tengo', 'tienes', 'tiene', 'tenemos', 'tenéis', 'tienen'],
        'hacer': ['hago', 'haces', 'hace', 'hacemos', 'hacéis', 'hacen'],
        'decir': ['digo', 'dices', 'dice', 'decimos', 'decís', 'dicen'],
        'ir': ['voy', 'vas', 'va', 'vamos', 'vais', 'van'],
        'ver': ['veo', 'ves', 've', 'vemos', 'veis', 'ven'],
        'dar': ['doy', 'das', 'da', 'damos', 'dais', 'dan'],
        'saber': ['sé', 'sabes', 'sabe', 'sabemos', 'sabéis', 'saben'],
        'querer': ['quiero', 'quieres', 'quiere', 'queremos', 'queréis', 'quieren'],
        'llegar': ['llego', 'llegas', 'llega', 'llegamos', 'llegáis', 'llegan'],
        'pasar': ['paso', 'pasas', 'pasa', 'pasamos', 'pasáis', 'pasan'],
        'deber': ['debo', 'debes', 'debe', 'debemos', 'debéis', 'deben'],
        'poner': ['pongo', 'pones', 'pone', 'ponemos', 'ponéis', 'ponen'],
        'parecer': ['parezco', 'pareces', 'parece', 'parecemos', 'parecéis', 'parecen'],
        'quedar': ['quedo', 'quedas', 'queda', 'quedamos', 'quedáis', 'quedan'],
        'creer': ['creo', 'crees', 'cree', 'creemos', 'creéis', 'creen'],
        'hablar': ['hablo', 'hablas', 'habla', 'hablamos', 'habláis', 'hablan'],
        'llevar': ['llevo', 'llevas', 'lleva', 'llevamos', 'lleváis', 'llevan'],
        'dejar': ['dejo', 'dejas', '