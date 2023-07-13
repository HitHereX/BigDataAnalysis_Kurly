import streamlit as st
from PIL import Image
import pandas as pd
from random import randint
import openai


MESSAGES = []
TOPIC1 = ['적당','싱싱', '신선']
TOPIC2 = ['알도','포슬포슬','단단']
TOPIC3 = ['볶음','카레','가루']

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
        st.subheader('키워드를 선택하시면 AI가 예시 댓글을 보여드려요')
        message = st.text_area(label=f'키워드를 선택해 주세요!', 
                        value= default,
                        max_chars=100, 
                        help='예시 문장을 참고하여 댓글을 입력해 주세요', 
                        height=10)

    else :
        st.subheader("고객님께서 현재 선택하신 키워드는 %s 입니다. " %keyword)
        message = st.text_area(label='예시 댓글 : '+ChatGPT(keyword), 
                                value=default, 
                                max_chars=100, 
                                help='다른 고객분들께 여러분의 구매 경험을 나누어 주세요', 
                                height=10)


    #등록 버튼 (코멘트가 추가 됨)
    submitted = st.form_submit_button("등록하기")
    if submitted:
        st.balloons()
        if message != default:
            comments.append(message)   
   

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

    st.title("마켓컬리 댓글 분석 데모 페이지")
    st.write('이 페이지는 제안을 위한 데모 페이지입니다')

    #--------------------------------- import
    potato_img = Image.open('Potato.PNG')
    wc_img = Image.open('wc.png')
    review1 = Image.open('review.png')
    review2 = Image.open('review2.png')
    review3 = Image.open('review3.png')

    df = pd.read_csv('hehe.csv')
    

    col1,col2 = st.columns([2,3])
    # 공간을 2:3 으로 분할하여 col1과 col2라는 이름을 가진 컬럼을 생성합니다.
    st.write('  ') #split spaces
    st.write('  ') #split spaces
    st.subheader('댓글 분석 결과')
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
      st.markdown('---')
      st.markdown('컬리는 국내 농가에서 기른 맛 좋은 감자를 엄선해 문 앞까지\
                  신선하게 전해드릴게요. 취향에 따라 간단하게 찌거나 구워서 즐겨보세요. 볶음, 튀김 등의 요리로 \
                  다채롭게 변신시키면 매일 식탁에 올려도 질리지 않을 거예요.    \
                  [컬리 페이지 링크](https://www.kurly.com/goods/5026448)')
      st.markdown('---')


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
        st.image(review1)

    with col4_2:
       st.subheader('TOPIC 2')
       for word in TOPIC2:
          temp = st.checkbox(word)
          if temp :
             selected_keywords.append(word)
       st.image(review2)

    with col4_3:
       st.subheader('TOPIC 3')
       for word in TOPIC3:
          temp = st.checkbox(word)
          if temp :
             selected_keywords.append(word)
       st.image(review3)


#    print(selected_keywords)

    # 데이터 로딩 함수는 여기에!
    st.write('  ') #split spaces
    st.write('  ') #split spaces

    comments, cnt = load_comments(df, selected_keywords[-1], 5)
    per = int(cnt*100/(0.2*len(df)))
    if per == 500:
       st.subheader(f'키워드를 선택하시면, 관련 댓글을 모아보실 수 있어요')
    else:
        st.subheader(f'선택하신 "{selected_keywords[-1]}" 을(를) 포함하는 댓글은 {cnt:,}개({int(cnt*100/(0.2*len(df)))}%)예요')
#    print(comments[:5])

    for comment in comments:
        temp = comment.split('\n')
        with st.expander(temp[0]):
           st.write(comment)

    st.write('  ') #split spaces
    st.write('  ') #split spaces
    with st.form(key='my_form'):
        leave_comments(MESSAGES, selected_keywords[-1])


if __name__ == "__main__" :
    main()
