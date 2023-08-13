from google.oauth2 import service_account
from datetime import datetime
from random import randint, shuffle
from pytz import timezone
import streamlit as st
from PIL import Image
import pandas as pd
import gspread
import openai

import streamlit_analytics


def update_spreadsheet(comment, chosen_topic, suggested_review):
    topic_keys = {  '적당' : 0, 
                    '싱싱' : 1, 
                    '신선' : 2, 
                    '(감자)알' : 3,
                    '포슬포슬' : 4,
                    '단단' : 5,
                    '볶음' : 6,
                    '카레' : 7,
                    '가루' : 8,
                    '' : 9}
    
    week = ['MON','TUE','WED','THU','FRI','SAT','SUN']

    now = datetime.now(timezone('Asia/Seoul'))
    weekday = now.weekday()


    if type(comment) == str:
        print(comment)
        l = [   comment, 
                len(comment), 
                chosen_topic,
                topic_keys[chosen_topic], 
                suggested_review,
                week[weekday],
                int(now.year),
                int(now.month),
                int(now.day),
                int(now.hour),
                int(now.minute),
                str(now)
        ]

        print(l)
        sh.append_row(l)


def ChatGPT(keyword = str):
    ''' 
    This function uses the OpenAI API to generate a response to the given 
    user_query using the ChatGPT model
    '''
    query = f'"감자" 에 대한 긍정적인 구매 후기를 "{keyword}" 을 포함해서 한 문장으로 작성해줘'
    completion = openai.Completion.create(
                                  engine = model_engine,
                                  prompt = query,
                                  max_tokens = 128,
                                  n = 1,
                                  temperature = 0.5,
                                )
    response = completion.choices[0].text
    return response.split('\n')[-1]


def ChatGPT_demo(keyword = str, rerun  = False):
   answers = {}
   answers[''] = ['',
                  '',
                  '']
   answers['적당'] = ['감자는 맛있고 적당한 가격에 제공되어 매우 만족스러웠습니다',
                    '감자는 적당한 가격에 신선하고 맛있어서 매우 만족스러웠습니다.',
                    '감자는 맛있고 적당한 가격에 사기에 매우 만족합니다.']
   answers['싱싱'] = ['감자가 싱싱하고 맛있어서 매우 만족합니다!',
                    '감자는 싱싱하고 맛있어서 정말 좋았어요!',
                    '감자가 싱싱하고 맛있어서 매우 만족스러웠어요.']
   answers['신선'] = ['감자는 신선하고 맛있어서 매우 긍정적인 구매 후기를 남겼습니다.',
                    '맛있는 감자로 만든 신선한 음식이 너무 맛있어서 정말 좋았어요!',
                    '감자는 신선하고 맛있어서 매우 만족스러웠어요.']
   answers['알도'] = ['감자는 맛있고 알도 좋았어요!',
                    '알감자는 상처 없이 적당한 크기로 제공되어 신선한 상태를 유지하며, 풍부한 맛과 영양을 안겨줍니다',
                    '싱싱하고 알도 적당한 감자는 요리 과정에서도 그 질감과 맛을 유지하여, 최상의 요리 결과물을 얻을 수 있도록 도와줍니다']
   answers['포슬포슬'] = ['감자는 포슬포슬하고 맛있어서 빨리 다 먹고 싶었어요!',
                    '감자는 포슬포슬하고 맛있어서 매일 먹고 싶어요!',
                    '감자는 포슬포슬하고 맛있어서 먹기 좋았어요!']
   answers['단단'] = ['감자는 단단하고 맛있어서 매우 만족합니다.',
                    '감자는 단단하고 맛있어서 매우 만족스러웠어요.',
                    '감자는 단단하고 맛있어서 정말 좋았어요!']
   answers['볶음'] = ['감자를 볶아먹었는데 맛있고 식감도 좋았어요!',
                    '감자로 만든 볶음이 맛있고 식감이 좋아서 매우 만족스러웠어요!',
                    '감자를 볶아 먹어도 맛있고 식감도 좋아서 정말 좋았어요!']
   answers['카레'] = ['감자 카레는 맛있고 매콤해서 너무 좋아요!',
                    '감자로 만든 카레는 맛있고 식감도 좋았습니다!',
                    '감자가 카레에 너무 잘 어울려서 먹기 좋았습니다!']
   answers['가루'] = ['애호박과 함께 얇게 채 썰어 전분가루로 휘둘러서 바삭하게 부쳐주면 양념장과의 궁합이 정말 끝내줘요. 최고예요^^',
                    '감자를 잘게 채 썰어서 튀김가루에 약간의 소금과 후추로 간을 해서 튀겨먹으면 맛있어요.',
                    '받자마자 감자를 얇게 채 썰어 베이컨을 얇게 자른 후에 치즈가루와 후추로 전 부쳐먹었어요.']
   
   randv = randint(0, len(answers['적당'])-1)
   ans = answers[keyword][randv]
   if rerun == True:
       randv2 = randint(0, len(answers['적당'])-1)
       ans = answers[keyword][randv2]

   return ans
   

@st.cache_data
def load_comments(dataframe : pd.DataFrame, to_find : str, num : int) -> list:
    comments = dataframe['리뷰 내용'].tolist()
    score = dataframe['score'].tolist()

    mapped = []
    for i in range(len(comments)):
       mapped.append((comments[i], score[i]))
    mapped.sort(key = lambda x:x[1], reverse = True)
    include, result = [], []

    for comment in mapped:
       if to_find in comment[0]: include.append(comment[0])
    cnt = len(include)

    for i in range(num):
       result.append(include[randint(0, len(include))])
    

    return include[:5], cnt


st.elements.utils._shown_default_value_warning=True

#google auth connect
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info(
    st.secrets['gcp_service_account'],
    scopes = scope
)

gspread_cli = gspread.authorize(credentials)
sheet_title = '2023.08_project_potato_demo_log.comments'
sh = gspread_cli.open(sheet_title).worksheet('default_sheet')
topic_log = gspread_cli.open(sheet_title).worksheet('topic_log')
sati = gspread_cli.open(sheet_title).worksheet('satisfied')

#OpenAI
model_engine = "text-davinci-003"
openai.api_key = ""


def main() :
    streamlit_analytics.start_tracking()

    st.title("마켓컬리 구매후기 분석 데모 페이지")
    st.write('본 서비스는 설문을 위한 Test-시연 페이지입니다 (참고용)')

    #--------------------------------- import
    potato_img = Image.open('resources/Potato.PNG')
    wc1 = Image.open('resources/wc1.png')
    wc2 = Image.open('resources/wc2.png')
    wc3 = Image.open('resources/wc3.png')
    wc4 = Image.open('resources/wc4.png')
    review1 = Image.open('resources/review.png')
    review2 = Image.open('resources/review2.png')
    review3 = Image.open('resources/review3.png')

    wcs = [wc1, wc2, wc3, wc4]
    df = pd.read_csv('./resources/hehe.csv')
    

    col1,col2 = st.columns([2,3])
    # 공간을 2:3 으로 분할하여 col1과 col2라는 이름을 가진 컬럼을 생성합니다.
    st.write('  ') #split spaces
    st.write('  ') #split spaces
    st.subheader('구매후기 분석 결과')
    st.write('주요 등장 단어를 워드클라우드(Word Cloud)로 시각화하여 보여드려요')
    wc_change = st.button('워드클라우드 새로고침')


    with col1 :
      #감자 상품 이미지
      st.image(potato_img)
  
    with col2 :
      #감자 상품 정보
      st.markdown('### KF365 감자 1kg')
      st.markdown('##### ~~4,500원~~ →  :blue[*3,990원* (12%)]')
      st.markdown('---')
      st.markdown('컬리는 국내 농가에서 기른 맛 좋은 감자를 엄선해 문 앞까지\
                  신선하게 전해드릴게요. 취향에 따라 간단하게 찌거나 구워서 즐겨보세요. 볶음, 튀김 등의 요리로 \
                  다채롭게 변신시키면 매일 식탁에 올려도 질리지 않을 거예요.')
      st.markdown("[컬리에서 더보기](https://www.kurly.com/goods/5026448)")
      st.markdown('---')


    # word cloud image
    if wc_change:
        st.image(wcs[randint(1, len(wcs)-1)])
    else:
        st.image(wcs[0])
#    st.image(wc_img)

    selected_keywords = ['']



    st.write('마음에 드는 키워드를 1개 선택해주세요')

    select_topic = {
        '🚛 적당, 싱싱, 신선': [['적당', '싱싱', '신선'], 
                            review1],
        '🥔 (감자)알, 포슬포슬, 단단': [['(감자)알', '포슬포슬', '단단'],
                                    review2],
        '🍽 볶음, 카레, 가루': [['볶음', '카레', '가루'], 
                            review3]

    }


    tabs = list(select_topic.keys())
    shuffle(tabs)

    st_tabs = st.tabs(tabs)
    for tab, key_tab in zip(st_tabs, tabs):
        with tab:
            cp_key_tab = select_topic[key_tab][0]
            shuffle(cp_key_tab)

            st.image(select_topic[key_tab][1])
            for atopic in cp_key_tab:
                t = st.checkbox(atopic)
                if t:
                    if atopic == '(감자)알' : selected_keywords.append('알도')
                    else: selected_keywords.append(atopic)
    print('selected keywords', selected_keywords)
    

    prev_selected = topic_log.col_values(1)
    if len(selected_keywords) > 1 and selected_keywords[1] != prev_selected[-1]:
        topic_log.append_row([str(selected_keywords[1]), 
                              str(datetime.now(timezone('Asia/Seoul')))])
        prev_selected = selected_keywords[1]


    # split spaces
    st.write('  ')
    st.write('  ')

    kwd_value = ''
    if len(selected_keywords) > 1:
        kwd_value = selected_keywords[1]

    comments, cnt = load_comments(df, kwd_value, 5)
    per = int(cnt*100/(0.2*len(df)))
    if per == 500:
       st.markdown('#### 키워드를 선택하시면, 관련 구매후기를 모아보실 수 있어요')
    else:
        keyword = kwd_value
        if keyword == '가루':
            ratio = int(cnt*1000/(0.2*len(df)))
        else:
            ratio = int(cnt*100/(0.2*len(df)))
        st.subheader(f'선택하신 "{keyword}" 을(를) 포함하는 후기: {cnt:,}개({ratio}%)')

    for comment in comments:
        temp = comment.split('\n')
        header = temp[0]
        if len(temp[0]) < 20 and len(temp) > 1:
           header = ' '.join(temp[:2]) 

        with st.expander(header):
           st.write(comment)

    st.write('  ') #split spaces
    st.write('  ') #split spaces
    st.write('  ') #split spaces



    ex = ChatGPT_demo(kwd_value)
    label = '위에서 키워드를 선택해 주세요!'
    subh = '키워드를 선택하시면 AI가 예시 구매후기를 보여드려요'
    if kwd_value != '':
        label = '예시 후기 : '+ex
        subh = '고객님께서 현재 선택하신 키워드는 ' + kwd_value + '입니다.'

    if 'ui' not in st.session_state:
        st.session_state['ui'] = ''

    st.subheader(subh)
    cp = st.button('예시 후기 복사하기', key = 'copy')

    if cp:
        st.session_state.ui = ex

    msg = st.text_area(label = label,
                       value = st.session_state.ui,
                       key = 'ui',
                       height = 10)       
    regen = st.button('후기 다시 제안받기')

    if regen:
        if len(selected_keywords) <= 1:
            st.markdown('##### :blue[키워드를 선택하시면 관련 문장을 생성해 드려요]')

        else:
            ex = ChatGPT_demo(kwd_value, rerun= True)

    submit = st.button('등록하기', type = 'primary')

    if submit and msg != '':
        st.balloons()
        st.markdown('##### 작성하신 구매후기가 잘 등록되었습니다! 감사합니다')
        update_spreadsheet(msg, kwd_value, ex)

    st.write('  ') #split spaces
    st.write('  ') #split spaces
    st.write('  ')

    satisfy = ['전혀 불만족','불만족','다소 불만족','보통','다소 만족','만족','매우 만족']
    st.subheader('본 페이지에 대한 만족도를 알려주세요')
    satisfied = st.select_slider('본 페이지에 대한 만족도 조사',
                     options = satisfy,
                     value = '보통',
                     label_visibility = 'collapsed')
    sati_submit = st.button('만족도 등록하기')
    if sati_submit:
        sati.append_row([satisfied, str(datetime.now(timezone('Asia/Seoul')))])
        st.markdown('##### :blue[만족도 평가가 잘 등록되었습니다. 감사합니다. 데모 시연 페이지를 종료해 주세요]')

    

    st.write('  ') #split spaces
    st.write('  ') #split spaces
    st.write('  ') #split spaces
    st.write('  ') #split spaces

    st.markdown('#### 참고.다른 분들의 후기도 확인해보세요')
    site_comments = sh.col_values(1)
    displayed_site_comments = []
    displayed_site_cnt = 0
    site_comments_addr = -1
    while True:
        if displayed_site_cnt == 5 or site_comments_addr == abs(len(site_comments)):
            break
        cmt = site_comments[site_comments_addr]
        if cmt not in displayed_site_comments:
            st.info(cmt)
            displayed_site_cnt += 1
        site_comments_addr += 1

#    for cmt in site_comments[:-6:-1]:
#        st.info(cmt)

    #copyright
    st.write('  ') #split spaces
    st.write('  ') #split spaces
    st.write('Copyright ⓒHGU & CXLab 2023 All Rights Reserved.') #split spaces

    streamlit_analytics.stop_tracking()



if __name__ == "__main__" :
    main()