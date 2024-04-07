import streamlit as st


st.set_page_config(page_title="Pension Calculator", page_icon=":bar_chart:", layout="wide")

sprache = st.selectbox(
   "Language",
   ("Deutsch", "Italiano"),
   index=0,
   placeholder="",
)


if sprache == "Deutsch":

    st.title("Herzlich Willkommen")
    st.subheader("zum Online Tool zur Berechnung der Beitragsentwicklung für die regionalen Zusatzrentenfonds in Trentino-Südtirol")

    st.markdown("Dieser Online Rechner ermöglich es Ihnen die Pensionsfonds in der Region Trentino Südtirol und die Performance der einzelnen Investitionslinien zu vergleichen.")
    st.markdown("Auf der linken Seite können Sie zu dem jeweiligen Fond wechseln und die Parameter für die Berechnung bestimmen.")
    st.markdown("Aufgrund der Veröffentlichungspflicht der Rentenfonds konnten die Daten von den Webseiten der jeweiligen Pensionsfonds selbst entnommen werden.")
    st.markdown("Dieses Projekt steht in keiner Verbindung zu den Institutionen der Zusatzrente, sondern wurde von einer Privatperson selbst erstellt. Es wird keine Garantie für die Richtigkeit der Informationen gewährt, da die Daten kopiert wurden.")
    st.markdown(
        """Entwickelt von **Alex Laimer**"""
    )
elif sprache == "Italiano":
    st.title("Benvenuto")
    st.subheader("al dashboard online per il calcolo dell'evoluzione dei contributi per i fondi pensione complementari regionali in Trentino-Alto Adige.")

    st.markdown("Questo calcolatrice online vi permette di confrontare i fondi pensione nella regione Trentino Alto Adige e la performance delle singole linee di investimento.")
    st.markdown("Sul lato sinistro, è possibile passare al fondo corrispondente e determinare i parametri per il calcolo.")
    st.markdown("A causa dell'obbligo di pubblicazione dei fondi pensione, i dati sono stati prelevati direttamente dai siti web dei rispettivi fondi pensione.")
    st.markdown("Questo progetto non è collegato alle istituzioni della pensione complementare, ma è stato creato da un privato autonomamente. Non viene garantita l'accuratezza delle informazioni poiché i dati sono stati copiati..")
    st.markdown(
        """Sviluppato da **Alex Laimer**"""
    )

