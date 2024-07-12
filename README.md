# CIR Ingredient Search
Questa web app è stata sviluppata per soddisfare le esigenze di un biologo cosmetologo, al fine di velocizzare e ottimizzare la ricerca dei valori di tossicità 'NOAEL' e 'LD50' sul sito "CIR", che valuta la sicurezza degli ingredienti nei prodotti cosmetici.

## Funzionalità della web app
1. Ricercare parzialmente il nome di un ingrediente nella barra di ricerca
2. Selezionare un ingrediente corrispondente alla ricerca dal menù a tendina

Una volta selezionato un ingrediente sarà possibile:
- Consultare direttamente i pdf associati cliccando il link
- Aprire i menù a tendina in cui vengono mostrati tutti i valori di 'NOAEL' e 'LD50' presenti nel pdf con il relativo contesto.

https://github.com/user-attachments/assets/370d3192-74c7-4eaa-8427-1d42246689b1


## Link alla web app
Tramite questo link è possibile utilizzare direttamente la nostra web app 
https://appcosmetici-n4ziichyt7vc4o7k3t7sxs.streamlit.app/


## Caratteristiche principali e panoramica del codice
**1. Ricerca di un Ingrediente**
- Gli utenti possono inserire il nome di un ingrediente nel campo di testo fornito.
- L'applicazione cerca nel file HTML pre-caricato (Cir.html) per trovare i nomi degli ingredienti corrispondenti e i relativi link.


**2. Visualizzazione degli Ingredienti**
- Se l'input corrisponde a uno dei nomi degli ingredienti, apparirà un menu a tendina per consentire all'utente di scegliere l'ingrediente specifico.


**3. Download e Analisi dei PDF**
- Dopo aver selezionato un ingrediente, l'applicazione recupera tutti i link ai PDF correlati.
- Valida ogni link per assicurarsi che siano URL corretti.
- Scarica i file PDF da questi link.


**4. Estrazione delle Informazioni dai PDF**
- L'applicazione estrae il contenuto testuale dai PDF scaricati.
- Cerca parole chiave specifiche (NOAEL e LD50) all'interno del testo.
- Visualizza il contesto attorno a queste parole chiave, evidenziandole per una facile identificazione.


## Panoramica delle Funzioni
**1. scarica_pdf(url)**
- Scarica un PDF dall'URL fornito e lo converte in formato binario utilizzando BytesIO.


**3. estrai_testo_pdf(contenuto_pdf_binario)**
- Estrae e restituisce il contenuto testuale dal contenuto PDF binario fornito.


**4. estrai_contesto(testo_estratto, keyword, context_lines=2)**
- Trova e restituisce il contesto attorno a una data parola chiave all'interno del testo estratto. Evidenzia la parola chiave per una migliore visibilità.


**5. controllo_validita_url(url)**
- Verifica se l'URL fornito è valido (cioè, inizia con http:// o https://).


**6. main()**
- La funzione principale che inizializza e esegue l'applicazione Streamlit. Gestisce gli input degli utenti, visualizza le opzioni, scarica i PDF ed estrae le informazioni rilevanti.


## Installazione
1. Clona la repository nel tuo pc
2. Crea e attiva il virtual environment
3. Installa le librerie necessarie, utilizza il file 'requirements.txt'
4. Assicurati che il file 'Cir.html' sia presente nella directory del tuo script
5. Utilizzando il terminale esegui l'applicazione streamlit

```cmd
streamlit run Ingredient_main.py
```


## Note
Questa web app si basa sulla struttura html e sui pdf del sito 'Cosmetic Ingredient Review'. Ogni modifica alla struttura di questi elementi comporta la necessità di modificare il codice per permettere il corretto funzionamento della web app

## Autori
@alexandraazzena
@MaddalenaB5
@giannoneaurora


