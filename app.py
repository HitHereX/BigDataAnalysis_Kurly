import streamlit as st
from PIL import Image

def main() :

    st.title("마켓컬리 Demo")

    Potato_img = Image.open('Potato.PNG')
    col1,col2 = st.columns([2,3])
    # 공간을 2:3 으로 분할하여 col1과 col2라는 이름을 가진 컬럼을 생성합니다.  
    col3,col4,col5,col6 = st.columns([1,1,1,1])

    with col1 :
      # column 1 에 담을 내용
      #감자 상품 이미지
      st.image(Potato_img)
    with col2 :
      # column 2 에 담을 내용
      #감자 상품 정보
      st.subheader('KF365 감자 1kg')
      st.subheader('4,500원')


    # with 구문 말고 다르게 사용 가능 
    #리뷰 Text input (title:제목, message: 리뷰 내용)
    title = st.text_input(label="후기 쓰기", value="제목을 적어주세요.", max_chars=10, help='input message < 10')
    message = st.text_area(label="내용 ", value="내용을 적어주세요.", max_chars=100, help='input message < 100', height=10)
    

    multi_select = st.multiselect('Please select somethings in multi selectbox!',
                                    ['구매동기', '맛', '상태', '배송'])
      
    st.write('You selected:', multi_select)

    #도움돼요 버튼
    st.button("👍")
    st.button("👎")

    #등록 버튼
    if st.button("등록하기"):
      st.write("Data Loading..")
      # 데이터 로딩 함수는 여기에!

    with col3 : 
      # column 3 에 담을 내용 (만족도)
      #사용자 평점
      st.subheader('사용자 평점')
    with col4 :
      # column 4 에 담을 내용
      #사용자 평점
      st.subheader('맛있어요')
      values = st.slider('75%가 만족했어요', 0.0, 100.0, (0.0, 75.0))
      
      
    with col5 :
      # column 5 에 담을 내용
      st.subheader('배달')
      values = st.slider('60%가 배달이 빨라요!', 0.0, 100.0, (0.0, 60.0))
      
    with col6 :
      # column 6 에 담을 내용

      st.subheader('포장')
      


if __name__ == "__main__" :
    main()
