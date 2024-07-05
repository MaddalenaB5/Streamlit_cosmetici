import streamlit as st
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import re
from PyPDF2 import PdfReader
from io import BytesIO


# Funzione per scaricare il PDF. Utilizziamo BytesIO per convertire il pdf in binario
def scarica_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        if 'application/pdf' in response.headers.get('Content-Type', ''):
            contenuto_pdf_binario = BytesIO(response.content)
            return contenuto_pdf_binario
        else:
            st.error(f"Il contenuto scaricato da {url} non è un PDF.")
            return None
    else:
        st.error(f"Impossibile scaricare il PDF da {url}.")
        return None


# Funzione per estrarre tutto il testo dal PDF
def estrai_testo_pdf(contenuto_pdf_binario):
    try:
        reader = PdfReader(contenuto_pdf_binario)
        lunghezza_pdf = len(reader.pages)
        testo_estratto = ""
        for pagina in range(lunghezza_pdf):
            oggetto_pagina = reader.pages[pagina]
            testo_estratto += oggetto_pagina.extract_text()
        return testo_estratto
    except Exception as e:
        st.warning(f"Questo PDF non è analizzabile: {e}")
        return None


# Funzione per estrarre il contesto attorno a una parola chiave
def estrai_contesto(testo_estratto, keyword, context_lines=2):
    if testo_estratto is None:
        return []

    righe = testo_estratto.split('\n')
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)  # permette di trovare la parola chiave comunque sia scritta

    risultati = []
    for i, riga in enumerate(righe):
        if pattern.search(riga):
            start = max(0, i - context_lines)
            end = min(len(righe), i + context_lines + 1)
            contesto = "\n".join(righe[start:end])
            # Evidenziamo la parola chiave in grassetto
            contesto = pattern.sub(f"**{keyword}**", contesto)
            risultati.append(contesto)
    return risultati


# Funzione per verificare se un URL è valido
def is_valid_url(url):
    return url.startswith('http://') or url.startswith('https://')


# Funzione principale per l'applicazione Streamlit
def main():
    st.title("Ingredient analysis")

    with open('Cir.html', encoding='utf-8') as fp1:
        soup = BeautifulSoup(fp1, "html.parser")

    tabella = soup.find('table', class_='table')
    url_sito = 'https://cir-reports.cir-safety.org/'

    nomi_links = []
    for el in tabella.find_all('a'):
        href = el.get('href')
        nome_ingrediente = el.get_text()
        if href:
            url_completo = urljoin(url_sito, href)
            nomi_links.append((nome_ingrediente, url_completo))

    # Rimuovi duplicati
    nomi_links_univoci = []
    visti = set()
    for n_ingr, l_ingr in nomi_links:
        if (n_ingr, l_ingr) not in visti:
            nomi_links_univoci.append((n_ingr, l_ingr))
            visti.add((n_ingr, l_ingr))

    # Input dell'utente
    richiesta_utente = st.text_input("Inserisci il nome di un ingrediente:").lower()

    if richiesta_utente:
        ingredienti = []
        for n_ingr, l_ingr in nomi_links_univoci:
            if richiesta_utente in n_ingr.lower():
                ingredienti.append((n_ingr, l_ingr))

        if ingredienti:
            for nome, url_ingrediente in ingredienti:
                st.sidebar.markdown(f"## {nome}")
                response = requests.get(url_ingrediente)
                soup = BeautifulSoup(response.content, 'html.parser')
                tabella_pdf = soup.find('table', class_='table')

                links_ingrediente = []
                for el in tabella_pdf.find_all('a'):
                    href1 = el.get('href')
                    if href1:
                        url_completo_ingrediente = urljoin(url_sito, href1)
                        links_ingrediente.append(url_completo_ingrediente)

                # Filtra i link non validi
                links_ingrediente_validi = []
                for url in links_ingrediente:
                  if is_valid_url(url):
                    links_ingrediente_validi.append(url)

                for pdf_url in links_ingrediente_validi:
                    st.write(f"Dati estratti dal PDF per {nome}: {pdf_url}")
                    contenuto_pdf_binario = scarica_pdf(pdf_url)
                    if contenuto_pdf_binario:
                        testo = estrai_testo_pdf(contenuto_pdf_binario)
                        if testo:
                            keywords_noael = ["NOAEL"]
                            keywords_ld50 = ["LD₅₀", "LD50", "LD 50", "Ld50", "Ld₅₀"]

                            contesti_noael = []
                            for keyword in keywords_noael:
                                contesti_noael.extend(estrai_contesto(testo, keyword))

                            contesti_LD50 = []
                            for keyword in keywords_ld50:
                                contesti_LD50.extend(estrai_contesto(testo, keyword))

                            with st.expander(f"Dettagli NOAEL per {nome}"):
                                if contesti_noael:
                                    for cont in contesti_noael:
                                        st.write(cont)
                                        st.write("\n" + "=" * 80 + "\n")
                                else:
                                    st.write("Nessun dato NOAEL trovato.")

                            with st.expander(f"Dettagli LD50 per {nome}"):
                                if contesti_LD50:
                                    for cont in contesti_LD50:
                                        st.write(cont)
                                        st.write("\n" + "=" * 80 + "\n")
                                else:
                                    st.write("Nessun dato LD50 trovato.")
                        else:
                            st.warning(
                                f"Il PDF non è analizzabile. Visita il link per maggiori informazioni: {pdf_url}")
        else:
            st.error("Spiacente, l'ingrediente da te selezionato non è stato trovato.")


if __name__ == "__main__":
    main()
