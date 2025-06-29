import streamlit as st
import random
import json
import datetime
from typing import Dict, List, Tuple

# Конфигурация страницы
st.set_page_config(
    page_title="🇪🇸 Тренажер испанских глаголов",
    page_icon="🇪🇸",
    layout="centered"
)

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
        'dejar': ['dejo', 'dejas', 'deja', 'dejamos', 'dejáis', 'dejan'],
        'seguir': ['sigo', 'sigues', 'sigue', 'seguimos', 'seguís', 'siguen'],
        'encontrar': ['encuentro', 'encuentras', 'encuentra', 'encontramos', 'encontráis', 'encuentran'],
        'llamar': ['llamo', 'llamas', 'llama', 'llamamos', 'llamáis', 'llaman'],
        'venir': ['vengo', 'vienes', 'viene', 'venimos', 'venís', 'vienen'],
        'pensar': ['pienso', 'piensas', 'piensa', 'pensamos', 'pensáis', 'piensan'],
        'salir': ['salgo', 'sales', 'sale', 'salimos', 'salís', 'salen'],
        'vivir': ['vivo', 'vives', 'vive', 'vivimos', 'vivís', 'viven'],
        'sentir': ['siento', 'sientes', 'siente', 'sentimos', 'sentís', 'sienten'],
        'trabajar': ['trabajo', 'trabajas', 'trabaja', 'trabajamos', 'trabajáis', 'trabajan'],
        'estudiar': ['estudio', 'estudias', 'estudia', 'estudiamos', 'estudiáis', 'estudian']
    },
    'indefinido': {
        'ser': ['fui', 'fuiste', 'fue', 'fuimos', 'fuisteis', 'fueron'],
        'estar': ['estuve', 'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron'],
        'tener': ['tuve', 'tuviste', 'tuvo', 'tuvimos', 'tuvisteis', 'tuvieron'],
        'hacer': ['hice', 'hiciste', 'hizo', 'hicimos', 'hicisteis', 'hicieron'],
        'decir': ['dije', 'dijiste', 'dijo', 'dijimos', 'dijisteis', 'dijeron'],
        'ir': ['fui', 'fuiste', 'fue', 'fuimos', 'fuisteis', 'fueron'],
        'ver': ['vi', 'viste', 'vio', 'vimos', 'visteis', 'vieron'],
        'dar': ['di', 'diste', 'dio', 'dimos', 'disteis', 'dieron'],
        'saber': ['supe', 'supiste', 'supo', 'supimos', 'supisteis', 'supieron'],
        'querer': ['quise', 'quisiste', 'quiso', 'quisimos', 'quisisteis', 'quisieron'],
        'llegar': ['llegué', 'llegaste', 'llegó', 'llegamos', 'llegasteis', 'llegaron'],
        'pasar': ['pasé', 'pasaste', 'pasó', 'pasamos', 'pasasteis', 'pasaron'],
        'deber': ['debí', 'debiste', 'debió', 'debimos', 'debisteis', 'debieron'],
        'poner': ['puse', 'pusiste', 'puso', 'pusimos', 'pusisteis', 'pusieron'],
        'parecer': ['parecí', 'pareciste', 'pareció', 'parecimos', 'parecisteis', 'parecieron'],
        'quedar': ['quedé', 'quedaste', 'quedó', 'quedamos', 'quedasteis', 'quedaron'],
        'creer': ['creí', 'creíste', 'creyó', 'creímos', 'creísteis', 'creyeron'],
        'hablar': ['hablé', 'hablaste', 'habló', 'hablamos', 'hablasteis', 'hablaron'],
        'llevar': ['llevé', 'llevaste', 'llevó', 'llevamos', 'llevasteis', 'llevaron'],
        'dejar': ['dejé', 'dejaste', 'dejó', 'dejamos', 'dejasteis', 'dejaron'],
        'seguir': ['seguí', 'seguiste', 'siguió', 'seguimos', 'seguisteis', 'siguieron'],
        'encontrar': ['encontré', 'encontraste', 'encontró', 'encontramos', 'encontrasteis', 'encontraron'],
        'llamar': ['llamé', 'llamaste', 'llamó', 'llamamos', 'llamasteis', 'llamaron'],
        'venir': ['vine', 'viniste', 'vino', 'vinimos', 'vinisteis', 'vinieron'],
        'pensar': ['pensé', 'pensaste', 'pensó', 'pensamos', 'pensasteis', 'pensaron'],
        'salir': ['salí', 'saliste', 'salió', 'salimos', 'salisteis', 'salieron'],
        'vivir': ['viví', 'viviste', 'vivió', 'vivimos', 'vivisteis', 'vivieron'],
        'sentir': ['sentí', 'sentiste', 'sintió', 'sentimos', 'sentisteis', 'sintieron'],
        'trabajar': ['trabajé', 'trabajaste', 'trabajó', 'trabajamos', 'trabajasteis', 'trabajaron'],
        'estudiar': ['estudié', 'estudiaste', 'estudió', 'estudiamos', 'estudiasteis', 'estudiaron']
    },
    'subjuntivo': {
        'ser': ['sea', 'seas', 'sea', 'seamos', 'seáis', 'sean'],
        'estar': ['esté', 'estés', 'esté', 'estemos', 'estéis', 'estén'],
        'tener': ['tenga', 'tengas', 'tenga', 'tengamos', 'tengáis', 'tengan'],
        'hacer': ['haga', 'hagas', 'haga', 'hagamos', 'hagáis', 'hagan'],
        'decir': ['diga', 'digas', 'diga', 'digamos', 'digáis', 'digan'],
        'ir': ['vaya', 'vayas', 'vaya', 'vayamos', 'vayáis', 'vayan'],
        'ver': ['vea', 'veas', 'vea', 'veamos', 'veáis', 'vean'],
        'dar': ['dé', 'des', 'dé', 'demos', 'deis', 'den'],
        'saber': ['sepa', 'sepas', 'sepa', 'sepamos', 'sepáis', 'sepan'],
        'querer': ['quiera', 'quieras', 'quiera', 'queramos', 'queráis', 'quieran'],
        'llegar': ['llegue', 'llegues', 'llegue', 'lleguemos', 'lleguéis', 'lleguen'],
        'pasar': ['pase', 'pases', 'pase', 'pasemos', 'paséis', 'pasen'],
        'deber': ['deba', 'debas', 'deba', 'debamos', 'debáis', 'deban'],
        'poner': ['ponga', 'pongas', 'ponga', 'pongamos', 'pongáis', 'pongan'],
        'parecer': ['parezca', 'parezcas', 'parezca', 'parezcamos', 'parezcáis', 'parezcan'],
        'quedar': ['quede', 'quedes', 'quede', 'quedemos', 'quedéis', 'queden'],
        'creer': ['crea', 'creas', 'crea', 'creamos', 'creáis', 'crean'],
        'hablar': ['hable', 'hables', 'hable', 'hablemos', 'habléis', 'hablen'],
        'llevar': ['lleve', 'lleves', 'lleve', 'llevemos', 'llevéis', 'lleven'],
        'dejar': ['deje', 'dejes', 'deje', 'dejemos', 'dejéis', 'dejen'],
        'seguir': ['siga', 'sigas', 'siga', 'sigamos', 'sigáis', 'sigan'],
        'encontrar': ['encuentre', 'encuentres', 'encuentre', 'encontremos', 'encontréis', 'encuentren'],
        'llamar': ['llame', 'llames', 'llame', 'llamemos', 'llaméis', 'llamen'],
        'venir': ['venga', 'vengas', 'venga', 'vengamos', 'vengáis', 'vengan'],
        'pensar': ['piense', 'pienses', 'piense', 'pensemos', 'penséis', 'piensen'],
        'salir': ['salga', 'salgas', 'salga', 'salgamos', 'salgáis', 'salgan'],
        'vivir': ['viva', 'vivas', 'viva', 'vivamos', 'viváis', 'vivan'],
        'sentir': ['sienta', 'sientas', 'sienta', 'sintamos', 'sintáis', 'sientan'],
        'trabajar': ['trabaje', 'trabajes', 'trabaje', 'trabajemos', 'trabajéis', 'trabajen'],
        'estudiar': ['estudie', 'estudies', 'estudie', 'estudiemos', 'estudiéis', 'estudien']
    },
    'imperfecto': {
        'ser': ['era', 'eras', 'era', 'éramos', 'erais', 'eran'],
        'estar': ['estaba', 'estabas', 'estaba', 'estábamos', 'estabais', 'estaban'],
        'tener': ['tenía', 'tenías', 'tenía', 'teníamos', 'teníais', 'tenían'],
        'hacer': ['hacía', 'hacías', 'hacía', 'hacíamos', 'hacíais', 'hacían'],
        'decir': ['decía', 'decías', 'decía', 'decíamos', 'decíais', 'decían'],
        'ir': ['iba', 'ibas', 'iba', 'íbamos', 'ibais', 'iban'],
        'ver': ['veía', 'veías', 'veía', 'veíamos', 'veíais', 'veían'],
        'dar': ['daba', 'dabas', 'daba', 'dábamos', 'dabais', 'daban'],
        'saber': ['sabía', 'sabías', 'sabía', 'sabíamos', 'sabíais', 'sabían'],
        'querer': ['quería', 'querías', 'quería', 'queríamos', 'queríais', 'querían'],
        'llegar': ['llegaba', 'llegabas', 'llegaba', 'llegábamos', 'llegabais', 'llegaban'],
        'pasar': ['pasaba', 'pasabas', 'pasaba', 'pasábamos', 'pasabais', 'pasaban'],
        'deber': ['debía', 'debías', 'debía', 'debíamos', 'debíais', 'debían'],
        'poner': ['ponía', 'ponías', 'ponía', 'poníamos', 'poníais', 'ponían'],
        'parecer': ['parecía', 'parecías', 'parecía', 'parecíamos', 'parecíais', 'parecían'],
        'quedar': ['quedaba', 'quedabas', 'quedaba', 'quedábamos', 'quedabais', 'quedaban'],
        'creer': ['creía', 'creías', 'creía', 'creíamos', 'creíais', 'creían'],
        'hablar': ['hablaba', 'hablabas', 'hablaba', 'hablábamos', 'hablabais', 'hablaban'],
        'llevar': ['llevaba', 'llevabas', 'llevaba', 'llevábamos', 'llevabais', 'llevaban'],
        'dejar': ['dejaba', 'dejabas', 'dejaba', 'dejábamos', 'dejabais', 'dejaban'],
        'seguir': ['seguía', 'seguías', 'seguía', 'seguíamos', 'seguíais', 'seguían'],
        'encontrar': ['encontraba', 'encontrabas', 'encontraba', 'encontrábamos', 'encontrabais', 'encontraban'],
        'llamar': ['llamaba', 'llamabas', 'llamaba', 'llamábamos', 'llamabais', 'llamaban'],
        'venir': ['venía', 'venías', 'venía', 'veníamos', 'veníais', 'venían'],
        'pensar': ['pensaba', 'pensabas', 'pensaba', 'pensábamos', 'pensabais', 'pensaban'],
        'salir': ['salía', 'salías', 'salía', 'salíamos', 'salíais', 'salían'],
        'vivir': ['vivía', 'vivías', 'vivía', 'vivíamos', 'vivíais', 'vivían'],
        'sentir': ['sentía', 'sentías', 'sentía', 'sentíamos', 'sentíais', 'sentían'],
        'trabajar': ['trabajaba', 'trabajabas', 'trabajaba', 'trabajábamos', 'trabajabais', 'trabajaban'],
        'estudiar': ['estudiaba', 'estudiabas', 'estudiaba', 'estudiábamos', 'estudíabais', 'estudiaban']
    }
}

RULES = {
    'presente': {
        'title': 'Настоящее время (Presente de Indicativo)',
        'content': '''
**Правильные глаголы -AR:**
Основа + -o, -as, -a, -amos, -áis, -an
*Пример: hablar → hablo, hablas, habla, hablamos, habláis, hablan*

**Правильные глаголы -ER:**
Основа + -o, -es, -e, -emos, -éis, -en
*Пример: comer → como, comes, come, comemos, coméis, comen*

**Правильные глаголы -IR:**
Основа + -o, -es, -e, -imos, -ís, -en
*Пример: vivir → vivo, vives, vive, vivimos, vivís, viven*

**Неправильные глаголы** имеют особые формы спряжения, которые нужно запомнить.
        '''
    },
    'indefinido': {
        'title': 'Прошедшее время (Pretérito Indefinido)',
        'content': '''
**Правильные глаголы -AR:**
Основа + -é, -aste, -ó, -amos, -asteis, -aron
*Пример: hablar → hablé, hablaste, habló, hablamos, hablasteis, hablaron*

**Правильные глаголы -ER/-IR:**
Основа + -í, -iste, -ió, -imos, -isteis, -ieron
*Пример: comer → comí, comiste, comió, comimos, comisteis, comieron*
*Пример: vivir → viví, viviste, vivió, vivimos, vivisteis, vivieron*

**Использование:** Завершенные действия в прошлом, конкретные моменты времени.
        '''
    },
    'subjuntivo': {
        'title': 'Сослагательное наклонение (Subjuntivo Presente)',
        'content': '''
**Глаголы -AR:**
Основа + -e, -es, -e, -emos, -éis, -en
*Пример: hablar → hable, hables, hable, hablemos, habléis, hablen*

**Глаголы -ER/-IR:**
Основа + -a, -as, -a, -amos, -áis, -an
*Пример: comer → coma, comas, coma, comamos, comáis, coman*
*Пример: vivir → viva, vivas, viva, vivamos, viváis, vivan*

**Использование:** Сомнения, желания, эмоции, нереальные ситуации. Часто после que, cuando, si.
        '''
    },
    'imperfecto': {
        'title': 'Прошедшее несовершенное время (Pretérito Imperfecto)',
        'content': '''
**Глаголы -AR:**
Основа + -aba, -abas, -aba, -ábamos, -abais, -aban
*Пример: hablar → hablaba, hablabas, hablaba, hablábamos, hablabais, hablaban*

**Глаголы -ER/-IR:**
Основа + -ía, -ías, -ía, -íamos, -íais, -ían
*Пример: comer → comía, comías, comía, comíamos, comíais, comían*
*Пример: vivir → vivía, vivías, vivía, vivíamos, vivíais, vivían*

**Исключения:** ser (era...), ir (iba...), ver (veía...)

**Использование:** Повторяющиеся действия в прошлом, описания, привычки.
        '''
    }
}

# Инициализация состояния
def init_session_state():
    if 'current_verb' not in st.session_state:
        st.session_state.current_verb = ''
    if 'current_pronoun_index' not in st.session_state:
        st.session_state.current_pronoun_index = 0
    if 'current_tense' not in st.session_state:
        st.session_state.current_tense = 'presente'
    if 'is_revealed' not in st.session_state:
        st.session_state.is_revealed = False
    if 'stats' not in st.session_state:
        st.session_state.stats = {
            'total': 0,
            'today': 0,
            'last_date': datetime.date.today().isoformat(),
            'combinations': {}
        }
    if 'recent_combinations' not in st.session_state:
        st.session_state.recent_combinations = []

def update_stats():
    today = datetime.date.today().isoformat()
    if st.session_state.stats['last_date'] != today:
        st.session_state.stats['today'] = 0
        st.session_state.stats['last_date'] = today

def get_next_combination():
    attempts = 0
    while attempts < 100:
        verb = random.choice(list(VERBS.keys()))
        pronoun_index = random.randint(0, 5)
        combination = f"{verb}-{pronoun_index}-{st.session_state.current_tense}"
        
        if combination not in st.session_state.recent_combinations or attempts > 50:
            if verb in CONJUGATIONS[st.session_state.current_tense]:
                st.session_state.recent_combinations.append(combination)
                if len(st.session_state.recent_combinations) > 20:
                    st.session_state.recent_combinations.pop(0)
                return verb, pronoun_index
        attempts += 1
    
    # Fallback
    available_verbs = list(CONJUGATIONS[st.session_state.current_tense].keys())
    return available_verbs[0], 0

def next_verb():
    verb, pronoun_index = get_next_combination()
    st.session_state.current_verb = verb
    st.session_state.current_pronoun_index = pronoun_index
    st.session_state.is_revealed = False

def reveal_answer():
    if not st.session_state.is_revealed:
        st.session_state.is_revealed = True
        
        # Обновляем статистику
        st.session_state.stats['total'] += 1
        st.session_state.stats['today'] += 1
        
        combination = f"{st.session_state.current_verb}-{st.session_state.current_pronoun_index}-{st.session_state.current_tense}"
        if combination not in st.session_state.stats['combinations']:
            st.session_state.stats['combinations'][combination] = 0
        st.session_state.stats['combinations'][combination] += 1

def reset_progress():
    st.session_state.stats = {
        'total': 0,
        'today': 0,
        'last_date': datetime.date.today().isoformat(),
        'combinations': {}
    }
    st.session_state.recent_combinations = []

# Основное приложение
def main():
    init_session_state()
    update_stats()
    
    # Заголовок
    st.title("🇪🇸 Тренажер спряжений испанских глаголов")
    
    # Статистика
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Всего изучено", st.session_state.stats['total'])
    with col2:
        st.metric("Сегодня", st.session_state.stats['today'])
    with col3:
        unique_combinations = len(st.session_state.stats['combinations'])
        st.metric("Уникальных комбинаций", unique_combinations)
    
    # Управление
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Сбросить прогресс"):
            reset_progress()
            st.success("Прогресс сброшен!")
            st.rerun()
    
    with col2:
        if st.button("📊 Экспорт данных"):
            data = {
                'stats': st.session_state.stats,
                'export_date': datetime.datetime.now().isoformat(),
                'total_cards': st.session_state.stats['total'],
                'unique_combinations': len(st.session_state.stats['combinations'])
            }
            st.download_button(
                label="💾 Скачать JSON",
                data=json.dumps(data, indent=2, ensure_ascii=False),
                file_name=f"spanish_verbs_{datetime.date.today()}.json",
                mime="application/json"
            )
    
    with col3:
        if st.button("🎯 Следующий глагол", key="next_main"):
            next_verb()
            st.rerun()
    
    # Выбор времени
    st.subheader("Выберите время:")
    tense_names = {
        'presente': 'Presente',
        'indefinido': 'Pretérito Indefinido', 
        'subjuntivo': 'Subjuntivo Presente',
        'imperfecto': 'Pretérito Imperfecto'
    }
    
    selected_tense = st.selectbox(
        "Время:",
        options=list(tense_names.keys()),
        format_func=lambda x: tense_names[x],
        index=list(tense_names.keys()).index(st.session_state.current_tense)
    )
    
    if selected_tense != st.session_state.current_tense:
        st.session_state.current_tense = selected_tense
        next_verb()
        st.rerun()
    
    # Инициализируем глагол если нужно
    if not st.session_state.current_verb:
        next_verb()
    
    # Карточка с глаголом
    st.markdown("---")
    
    # Проверяем что глагол существует в выбранном времени
    if (st.session_state.current_verb in CONJUGATIONS[st.session_state.current_tense] and
        st.session_state.current_verb in VERBS):
        
        verb_info = VERBS[st.session_state.current_verb]
        
        # Отображение глагола
        st.markdown(f"### 🎯 {st.session_state.current_verb}")
        st.markdown(f"*{verb_info['translation']}*")
        st.markdown(f"**Время:** {tense_names[st.session_state.current_tense]}")
        
        # Местоимение
        pronoun = PRONOUNS[st.session_state.current_pronoun_index]
        st.markdown(f"### 👤 {pronoun}")
        
        # Кнопка для показа ответа
        if not st.session_state.is_revealed:
            if st.button("🔍 Показать ответ", key="reveal", use_container_width=True):
                reveal_answer()
                st.rerun()
        else:
            # Показываем ответ
            conjugation = CONJUGATIONS[st.session_state.current_tense][st.session_state.current_verb][st.session_state.current_pronoun_index]
            st.success(f"### ✅ {conjugation}")
            
            # Кнопка следующего глагола
            if st.button("➡️ Следующий глагол", key="next_after_reveal", use_container_width=True):
                next_verb()
                st.rerun()
    else:
        st.error("Ошибка: глагол не найден в базе данных")
        if st.button("🔄 Получить новый глагол"):
            next_verb()
            st.rerun()
    
    # Правила спряжения
    st.markdown("---")
    with st.expander("📚 Правила спряжения"):
        rule = RULES[st.session_state.current_tense]
        st.markdown(f"## {rule['title']}")
        st.markdown(rule['content'])
    
    # Инструкции по использованию
    with st.expander("ℹ️ Как пользоваться"):
        st.markdown("""
        1. **Выберите время** для изучения
        2. **Посмотрите на глагол** и местоимение
        3. **Подумайте о правильном спряжении**
        4. **Нажмите "Показать ответ"** для проверки
        5. **Переходите к следующему глаголу**
        
        **Горячие клавиши:**
        - `Ctrl + Enter` - показать ответ / следующий глагол
        - `R` - сбросить прогресс (при фокусе на странице)
        """)

if __name__ == "__main__":
    main()