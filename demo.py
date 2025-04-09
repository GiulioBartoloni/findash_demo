import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import io
import base64
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx

# Titolo dell'app

DATI_RICERCA = [
    "Agilent Technologies, Inc.", "Alcoa Corporation", "Artius II Acquisition Inc.", "ATA Creativity Global", "Ares Acquisition Corporation II",
    "American Airlines Group Inc.", "AA Mission Acquisition Corp.", "Atlantic American Corporation", "Acadian Asset Management Inc.", "Applied Optoelectronics, Inc."
    ]

img = Image.open('FinDash_logo.png')

# Converti in base64
buffered = io.BytesIO()
img.save(buffered, format="PNG")
img_str = base64.b64encode(buffered.getvalue()).decode()

# Mostra nella sidebar con larghezza in %
st.sidebar.markdown(
    f'<img src="data:image/png;base64,{img_str}" style="width:50%; max-width:100%; margin-top: -50px;margin-bottom: 100px">',
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.header("Menu")
opzione = st.sidebar.selectbox(
    "Scegli un'opzione",
    ["Home","Esplora le azioni","Studia le correlazioni"]
)

# Sezione principale
if opzione=="Home":
    st.header("Seleziona una delle opzioni per inziare!")
elif opzione == "Esplora le azioni":
        
    st.title("Stock analytics")
    selected_stock = st.selectbox(
        "Seleziona un'azione da analizzare:", 
        options=[""] + DATI_RICERCA,
        format_func=lambda x: "Seleziona un'azione da analizzare..." if x == "" else x,
        index=0
    )
    data = pd.DataFrame({
    selected_stock: np.random.randn(100),
    "Public opinion": np.random.randn(100)
    })

    # Sezione risultati ricerca
    st.subheader(f"Risultati per: {selected_stock if selected_stock else 'Nessuna ricerca'}")

    # Grafico che si aggiorna in tempo reale
    chart = st.line_chart(data.iloc[:10, [0, 1]])  # Mostra solo i primi
    # Creazione dei 4 blocchi in layout 2x2
    col1, col2 = st.columns(2)  # Prima riga

    with col1:
        with st.container(border=True):  # Blocco 1
            st.subheader("Metrica A")
            st.metric(label="", value="123", delta="+4%")

    with col2:
        with st.container(border=True):  # Blocco 2
            st.subheader("Metrica B")
            st.metric(label="", value="1674", delta="+13%")

    # Seconda riga
    col3, col4 = st.columns(2)

    with col3:
        with st.container(border=True):  # Blocco 3
            st.subheader("Metrica C")
            st.metric(label="", value="634", delta="+9%")
    with col4:
        with st.container(border=True):  # Blocco 4
            st.subheader("Metrica D")
            st.metric(label="", value="74", delta="-17%")

    # Eventuale spazio aggiuntivo
    st.markdown("---")
    st.subheader("Sono stati individuati i seguenti momenti di forte volatilità:")
    # Creazione dei 4 blocchi in layout 2x2
    col1, col2 = st.columns(2)  # Prima riga

    with col1:
        with st.container(border=True):  # Blocco 1
            st.subheader("Spike positivo")
            st.write("14-08-2016")
            with st.expander("Vedi le notizie relative al periodo", expanded=False):
                st.write("Notizia del NYT qui...")


    with col2:
        with st.container(border=True):  # Blocco 2
            st.subheader("Spike negativo")
            st.write("29-12-2022")
            with st.expander("Vedi le notizie relative al periodo", expanded=False):
                st.write("Notizia del NYT qui...")

    # Seconda riga
    col3, col4 = st.columns(2)

    with col3:
        with st.container(border=True):  # Blocco 3
            st.subheader("Spike negativo")
            st.write("14-03-2018")
            with st.expander("Vedi le notizie relative al periodo", expanded=False):
                st.write("Notizia del NYT qui...")


    # Eventuale spazio aggiuntivo
    st.markdown("---")
    
elif opzione == "Studia le correlazioni":
    st.title("Selezione Multipla")

    selected = st.multiselect(
        "Seleziona fino a 5 azioni:",
        DATI_RICERCA,
        default=None,
        placeholder="Cerca o seleziona...",
        max_selections=6  # Disponibile dalla versione 1.31.0
    )
    if st.button("Mostra selezione", type="primary"):
        if not selected:
            st.warning("Nessun elemento selezionato")
        else:
            st.subheader("Elementi selezionati:")
            for i, elemento in enumerate(selected, 1):
                st.write(f"{i}. {elemento}")         
            data = np.random.rand(len(selected),len(selected))
            labels = [f"Var {i+1}" for i in range(len(selected))]
            df = pd.DataFrame(data, columns=labels, index=labels)
            
            fig, ax = plt.subplots()
            sns.heatmap(df.corr(), ax=ax)
            st.write(fig)
            
            G = nx.complete_graph(len(selected))
            for (u, v) in G.edges():
                G.edges[u,v]['weight'] = np.random.randint(-1, 1)   
            pos = nx.circular_layout(G)
            plt.figure(figsize=(8, 8))
            nx.draw(G, pos, with_labels=True, node_size=800, node_color='skyblue', edge_color='gray', width=1.5)
            labels = {i: f"Nodo {i+1}" for i in range(len(selected))}
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_labels(G, pos, labels, font_size=12)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
            st.pyplot(plt)
