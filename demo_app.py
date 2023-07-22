from google.oauth2 import service_account
from datetime import datetime
from random import randint
from pytz import timezone
import streamlit as st
from PIL import Image
import pandas as pd
import gspread
import openai


MESSAGES = []
TOPIC1 = ['적당','싱싱', '신선']
TOPIC2 = ['(감자)알','포슬포슬','단단']
TOPIC3 = ['볶음','카레','가루']

#google auth connect
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info(
    st.secrets['gcp_service_account'],
    scopes = scope
)

gspread_cli = gspread.authorize(credentials)
sh = gspread_cli.open('comments').worksheet('default')

#OpenAI
model_engine = "text-davinci-003"
openai.api_key = "" #follow step 4 to get a secret_key


def update_spreadsheet(comment):
    if type(comment) == str:
        l = (comment, len(comment), str(datetime.now(timezone('Asia/Seoul'))))
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


def ChatGPT_demo(keyword = str):
   answers = {}
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
   return answers[keyword][randv]

   


def leave_comments(comments = list, keyword = str):
    default = ''
    if keyword == '':
        st.subheader('키워드를 선택하시면 AI가 예시 구매후기를 보여드려요')
        message = st.text_area(label='위에서 키워드를 선택해 주세요!', 
                        value= default,
                        max_chars=100, 
                        help='다른 고객분들께 여러분의 구매경험을 나누어 주세요', 
                        height=10)

    else :
        st.subheader('고객님께서 현재 선택하신 키워드는 "%s" 입니다.' %keyword)
        message = st.text_area(label='예시 구매후기 : '+ChatGPT_demo(keyword), 
                                value=default, 
                                max_chars=100, 
                                help='다른 고객분들께 여러분의 구매경험을 나누어 주세요', 
                                height=10)


    #등록 버튼 (코멘트가 추가 됨)
    photo = st.form_submit_button("사진 업로드", disabled = True)
    submitted = st.form_submit_button("등록하기")
    if submitted or photo:
        st.balloons()
        st.markdown('##### 작성하신 구매후기가 잘 등록되었습니다! 감사합니다')

        if message != default:
            comments.append(message)   
            return message
   

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



def main() :

    st.title("마켓컬리 구매후기 분석 데모 페이지")
    st.write('본 서비스는 설문을 위한 Test-시연 페이지입니다 (참고용)')

    #--------------------------------- import
    potato_img = Image.open('Potato.PNG')
    wc_img = Image.open('wc.png')
    review1 = Image.open('review.png')
    review2 = Image.open('review2.png')
    review3 = Image.open('review3.png')

    df = pd.read_csv('./resources/hehe.csv')
    

    col1,col2 = st.columns([2,3])
    # 공간을 2:3 으로 분할하여 col1과 col2라는 이름을 가진 컬럼을 생성합니다.
    st.write('  ') #split spaces
    st.write('  ') #split spaces
    st.subheader('구매후기 분석 결과')
    st.write('키워드를 1개 선택해주세요')
    # 공간을 2:3 으로 분할하여col3, 4라는 이름을 가진 컬럼을 생성합니다.  

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
    st.image(wc_img)

    selected_keywords = ['']

    col4_1, col4_2, col4_3 = st.columns([1,1,1])
    with col4_1:
        with st.form('TOPIC 1'):
            for word in TOPIC1:
                submit = st.form_submit_button(word)
                if submit :
                    selected_keywords.append(word)  
        st.image(review1)

    with col4_2:
        with st.form('TOPIC 2'):
            for word in TOPIC2:
                submit = st.form_submit_button(word)
                if submit :
                    if word == '(감자)알':
                        selected_keywords.append('알도')
                    else:
                        selected_keywords.append(word) 
        st.image(review2)

    with col4_3:
        with st.form('TOPIC 3'):
            for word in TOPIC3:
                submit = st.form_submit_button(word)
                if submit :
                    selected_keywords.append(word)  
        st.image(review3)


    print(selected_keywords)

    # 데이터 로딩 함수는 여기에!
    st.write('  ') #split spaces
    st.write('  ') #split spaces

    comments, cnt = load_comments(df, selected_keywords[-1], 5)
    per = int(cnt*100/(0.2*len(df)))
    if per == 500:
       st.markdown('#### 키워드를 선택하시면, 관련 구매후기를 모아보실 수 있어요')
    else:
        keyword = selected_keywords[-1]
        if keyword == '가루':
            ratio = int(cnt*1000/(0.2*len(df)))
        else:
            ratio = int(cnt*100/(0.2*len(df)))
        st.subheader(f'선택하신 "{keyword}" 을(를) 포함하는 후기: {cnt:,}개({ratio}%)')
#    print(comments[:5])

    for comment in comments:
        temp = comment.split('\n')
        header = temp[0]
        if len(temp[0]) < 20 and len(temp) > 1:
           header = ' '.join(temp[:2]) 

        with st.expander(header):
           st.write(comment)

    st.write('  ') #split spaces
    st.write('  ') #split spaces
    with st.form(key='my_form'):
        temp = leave_comments(MESSAGES, selected_keywords[-1])
        update_spreadsheet(comment=temp)

    #copyright
    st.write('Copyright ⓒHGU & CXLab 2023 All Rights Reserved.') #split spaces




if __name__ == "__main__" :
    main()