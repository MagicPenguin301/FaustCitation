import streamlit as st
from Citation import Citation

def main():
    # 设置页面标题
    st.title("Faust Citation")

    # 添加两个文本框输入
    input1 = st.text_area("Zitierempfehlung für diesen Artikel", "")
    input2 = st.text_area("Anfang des Artikels", "")

    # 添加按钮
    button_clicked = st.button("生成引用")

    # 在按钮被点击时执行的操作
    if button_clicked:
        wu = Citation()
        wu.parse(input1,input2)
        result = wu
        # 输出文本框
        st.markdown(f"<p style='font-family: Times New Roman; font-size: 12px;'>{result}</p>",
                    unsafe_allow_html=True)


if __name__ == "__main__":
    main()
