import streamlit as st
from PIL import Image
import pandas as pd
from random import randint

MESSAGES = []
TOPIC1 = ['적당','싱싱', '신선']
TOPIC2 = ['알도','포슬포슬','단단']
TOPIC3 = ['볶음','카레','가루']

<<<<<<< HEAD
model_engine = "text-davinci-003"
openai.api_key = "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" #follow step 4 to get a secret_key


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


def leave_comments(comments = list, keyword = str):
    default = ''
    if keyword == '':
        st.subheader('키워드를 선택하시면 AI가 예시 구매 후기를 보여드려요')
        message = st.text_area(label=f'키워드를 선택해 주세요!', 
                        value= default,
                        max_chars=100, 
                        help='다른 고객분들께 여러분의 구매경험을 나누어 주세요', 
                        height=10)

    else :
        st.subheader("고객님께서 현재 선택하신 키워드는 %s 입니다. " %keyword)
        message = st.text_area(label='예시 구매후기 : '+ChatGPT(keyword), 
                                value=default, 
                                max_chars=100, 
                                help='다른 고객분들께 여러분의 구매경험을 나누어 주세요', 
                                height=10)

=======
>>>>>>> parent of fc7b3c1 (draft : 230713)

def leave_comments(comments = list):
    message = st.text_area(label="댓글을 달아주세요 ", 
                            value="내용을 적어주세요.", 
                            max_chars=100, 
                            help='input message < 100', 
                            height=10)
    
    #등록 버튼 (코멘트가 추가 됨)
    submitted = st.form_submit_button("등록하기")
    if submitted:
        st.balloons()
        if message != "내용을 적어주세요.":
            comments.append(message)   
   

def load_comments(dataframe : pd.DataFrame, to_find : str, num : int) -> list:
    comments = dataframe['리뷰 내용'].tolist()
    include, result = [], []

    for comment in comments:
       if to_find in comment: include.append(comment)
    cnt = len(include)

    for i in range(num):
       result.append(include[randint(0, len(include))])

    return result, cnt



def main() :

<<<<<<< HEAD
    st.title("마켓컬리 구매후기 분석 데모 페이지")
    st.write('이 페이지는 제안을 위한 데모 페이지입니다')
=======
    st.title("마켓컬리 DEMO")
>>>>>>> parent of fc7b3c1 (draft : 230713)

    #--------------------------------- import
    potato_img = Image.open('Potato.PNG')
    wc_img = Image.open('wc.png')
    df = pd.read_csv('hehe.csv')
    

    col1,col2 = st.columns([2,3])
    # 공간을 2:3 으로 분할하여 col1과 col2라는 이름을 가진 컬럼을 생성합니다.
<<<<<<< HEAD
    st.write('  ') #split spaces
    st.write('  ') #split spaces
    st.subheader('구매후기 분석 결과')
=======
    st.subheader('댓글 분석 결과')
>>>>>>> parent of fc7b3c1 (draft : 230713)
    st.write('토픽을 하나만 선택해주세요')
    col3,col4_1, col4_2, col4_3 = st.columns([2,1,1,1])
    # 공간을 2:3 으로 분할하여col3, 4라는 이름을 가진 컬럼을 생성합니다.  

    with col1 :
      #감자 상품 이미지
      st.image(potato_img)
  
    with col2 :
      #감자 상품 정보
      st.header('KF365 감자 1kg')
      st.subheader('4,500원')
      st.write('너 봄 감자가 맛있단다 어쩌구 저쩌구')
      st.write('우리 감자 맛있어요 많이 사드세요 두번 사드세요')
      st.write('감자튀김 감자전 감자수제비 해드시고 카레에도 넣어먹고 된장에도 넣어먹고')
      st.write('배고프다 헤헤 점심은 다들 드셨나요')

    # word cloud image
    with col3 : 
        st.image(wc_img)

    selected_keywords = ['']

    with col4_1:
        st.subheader('TOPIC 1')
        for word in TOPIC1:
          temp = st.checkbox(word)
          if temp :
             selected_keywords.append(word)  

    with col4_2:
       st.subheader('TOPIC 2')
       for word in TOPIC2:
          temp = st.checkbox(word)
          if temp :
             selected_keywords.append(word)

    with col4_3:
       st.subheader('TOPIC 3')
       for word in TOPIC3:
          temp = st.checkbox(word)
          if temp :
             selected_keywords.append(word)

    print(selected_keywords)

    # 데이터 로딩 함수는 여기에!
    comments, cnt = load_comments(df, selected_keywords[-1], 5)
<<<<<<< HEAD
    per = int(cnt*100/(0.2*len(df)))
    if per == 500:
       st.subheader(f'키워드를 선택하시면, 관련 구매후기를 모아보실 수 있어요')
    else:
        st.subheader(f'선택하신 "{selected_keywords[-1]}" 을(를) 포함하는 후기는 {cnt:,}개({int(cnt*100/(0.2*len(df)))}%)예요')
#    print(comments[:5])

=======
    st.subheader(f'선택하신 키워드 "{selected_keywords[-1]}" 를 포함하는 댓글은 {cnt}개로, {int(cnt*100/len(df))}% 입니다')
>>>>>>> parent of fc7b3c1 (draft : 230713)
    for comment in comments:
        st.info(comment)


    st.subheader('선택하신 단어를 참고하여 후기를 작성해 주세요')
    with st.form(key='my_form'):
        leave_comments(MESSAGES)


if __name__ == "__main__" :
    main()
