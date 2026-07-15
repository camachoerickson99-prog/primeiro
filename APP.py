import streamlit as st

st.set_page_config(page_title="Semáforo 3x4")

SIMBOLOS = {
    "vazio": " ",
    "verde": "verde","🟢"
    "amarelo": "amarelo","🟡"
    "vermelho": "vermelho","🔴"
}

PROXIMA_COR = {
    "vazio": "verde",
    "verde": "amarelo",
    "amarelo": "vermelho",
    "vermelho": "vermelho",
}

LINHAS_VENCEDORAS = [
    # Horizontais
    (0, 1, 2), (1, 2, 3),
    (4, 5, 6), (5, 6, 7),
    (8, 9, 10), (9, 10, 11),

    # Verticais
    (0, 4, 8),
    (1, 5, 9),
    (2, 6, 10),
    (3, 7, 11),

    # Diagonais
    (0, 5, 10),
    (1, 6, 11),
    (2, 5, 8),
    (3, 6, 9),
]


def iniciar_jogo():
    st.session_state.tabuleiro = ["vazio"] * 12
    st.session_state.jogador = 1
    st.session_state.vencedor = None
    st.session_state.mensagem = None


def garantir_estado_inicial():
    if "tabuleiro" not in st.session_state:
        iniciar_jogo()
    st.session_state.setdefault("mensagem", None)


def verificar_vencedor():
    for a, b, c in LINHAS_VENCEDORAS:
        cor = st.session_state.tabuleiro[a]

        if (
            cor != "vazio"
            and cor == st.session_state.tabuleiro[b]
            and cor == st.session_state.tabuleiro[c]
        ):
            return st.session_state.jogador

    return None


def jogar(posicao):
    if st.session_state.vencedor is not None:
        return

    cor_atual = st.session_state.tabuleiro[posicao]

    if cor_atual == "vermelho":
        st.session_state.mensagem = (
            f"A célula {posicao + 1} está bloqueada. Escolha outra."
        )
        return

    st.session_state.mensagem = None
    st.session_state.tabuleiro[posicao] = PROXIMA_COR[cor_atual]

    vencedor = verificar_vencedor()

    if vencedor is not None:
        st.session_state.vencedor = vencedor
        return

    if st.session_state.jogador == 1:
        st.session_state.jogador = 2
    else:
        st.session_state.jogador = 1


garantir_estado_inicial()

st.title("Jogo do Semáforo 3x4")
st.write("Clique numa célula para mudar a cor: vazio → verde → amarelo → vermelho.")
st.write("Vence quem formar três células iguais, não vazias, numa linha, coluna ou diagonal.")

if st.session_state.vencedor is None:
    st.info(f"Vez do Jogador {st.session_state.jogador}")
else:
    st.success(f"Jogador {st.session_state.vencedor} venceu!")

if st.session_state.mensagem:
    st.warning(st.session_state.mensagem)

indice = 0
for _ in range(3):
    colunas = st.columns(4)
    for coluna in colunas:
        with coluna:
            st.button(
                SIMBOLOS[st.session_state.tabuleiro[indice]],
                key=f"celula_{indice}",
                on_click=jogar,
                args=(indice,),
                use_container_width=True,
            )
        indice += 1

st.button("Novo jogo", on_click=iniciar_jogo)
