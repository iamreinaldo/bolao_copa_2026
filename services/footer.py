import streamlit as st


def mostrar_rodape():
    st.markdown(
        """
        <div style='text-align:center;
                    color:gray;
                    font-size:12px;
                    margin-top:50px;'>
            Desenvolvido por Reitinik - versão 2.0.1
        </div>
        """,
        unsafe_allow_html=True
    )