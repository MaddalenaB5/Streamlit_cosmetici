import streamlit as st
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from functions import scarica_pdf, estrai_testo_pdf, estrai_contesto, controllo_validita_url


def main():
    st.title("SafeCosmetic")

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

    #Rimozione degli eventuali duplicati
    nomi_links_univoci = []
    visti = set()
    for n_ingr, l_ingr in nomi_links:
        if (n_ingr, l_ingr) not in visti:
            nomi_links_univoci.append((n_ingr, l_ingr))
            visti.add((n_ingr, l_ingr))

    #Ingrediente inserito dall'utente
    richiesta_utente = st.text_input("Inserisci il nome di un ingrediente: ").lower()

    if richiesta_utente:
        ingredienti = []
        for n_ingr, l_ingr in nomi_links_univoci:
            if richiesta_utente in n_ingr.lower():
                ingredienti.append(n_ingr)

        if ingredienti:
            ingrediente_scelto = st.selectbox("Scegli un ingrediente: ", ingredienti)

            if ingrediente_scelto:
                url_ingrediente = ""
                for n_ingr, l_ingr in nomi_links_univoci:
                    if n_ingr == ingrediente_scelto:
                        url_ingrediente = l_ingr

                st.sidebar.markdown(f"## {ingrediente_scelto}")
                response = requests.get(url_ingrediente)
                soup = BeautifulSoup(response.content, 'html.parser')
                tabella_pdf = soup.find('table', class_='table')

                links_ingrediente = []
                for el in tabella_pdf.find_all('a'):
                    href1 = el.get('href')
                    if href1:
                        url_completo_ingrediente = urljoin(url_sito, href1)
                        links_ingrediente.append(url_completo_ingrediente)

                #Filtra gli eventuali link non validi
                links_ingrediente_validi = []
                for url in links_ingrediente:
                    if controllo_validita_url(url):
                        links_ingrediente_validi.append(url)

                for pdf_url in links_ingrediente_validi:
                    st.write(f"Dati estratti dal PDF per {ingrediente_scelto}: [Download pdf]({pdf_url})")
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

                            with st.expander(f"Dettagli NOAEL per {ingrediente_scelto}"):
                                if contesti_noael:
                                    for cont in contesti_noael:
                                        st.write(cont)
                                        st.write("\n" + "=" * 80 + "\n")
                                else:
                                    st.write("Nessun valore NOAEL trovato.")

                            with st.expander(f"Dettagli LD50 per {ingrediente_scelto}"):
                                if contesti_LD50:
                                    for cont in contesti_LD50:
                                        st.write(cont)
                                        st.write("\n" + "=" * 80 + "\n")
                                else:
                                    st.write("Nessun valore LD50 trovato.")
                        else:
                            st.warning(f"Il PDF non è analizzabile. Visita il link per maggiori informazioni: {pdf_url}")
        else:
            st.error("L'ingrediente da te selezionato non è stato trovato.")


if __name__ == "__main__":
    main()
