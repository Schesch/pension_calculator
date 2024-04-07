import streamlit as st



st.set_page_config(page_title="Portfolio Calculator", page_icon=":chart_with_upwards_trend:", layout="wide")

sprache = st.selectbox(
   "Language",
   ("Deutsch", "Italiano"),
   index=0,
   placeholder="",
)



#### DEFINE FUNCTION FOR METRIC STYLE
def style_metric_cards(
    background_color: str = "#f7ddc3",
    border_size_px: int = 2,
    border_color: str = "#000000",
    border_radius_px: int = 10,
) -> None:
    st.markdown(
        f"""
        <style>
            div[data-testid="stMetric"],
            div[data-testid="metric-container"] {{
                text-align: center;
                background-color: {background_color};
                border: {border_size_px}px solid {border_color};
                padding: 5% 5% 5% 10%;
                border-radius: {border_radius_px}px;
            }}
        </style>
        """,
        unsafe_allow_html=True)

def tilgungsrechner(kreditsumme, laufzeit_in_jahren, jahreszinssatz):
    """
    Berechnet die monatliche Tilgung eines Kredits, die Gesamtzahlung und die gesamte Zinssumme.
    
    :param kreditsumme: Die Gesamtsumme des Kredits.
    :param eigenkapital: Das vom Kreditnehmer eingebrachte Eigenkapital.
    :param laufzeit_in_jahren: Die Laufzeit des Kredits in Jahren.
    :param jahreszinssatz: Der jährliche Zinssatz des Kredits.
    :return: Die monatliche Tilgungsrate, die Gesamtzahlung und die gesamte Zinssumme.
    """
    darlehensbetrag = kreditsumme  # Nettokreditbetrag nach Eigenkapitalabzug
    # Umwandlung des jährlichen Zinssatzes in Dezimalzahl
    zinssatz_dezimal = jahreszinssatz / 100

    # Berechnung der Annuität
    annuitaetenfaktor = (zinssatz_dezimal * (1 + zinssatz_dezimal) ** laufzeit_in_jahren) / ((1 + zinssatz_dezimal) ** laufzeit_in_jahren - 1)
    jaehrliche_annuitaet = kreditsumme * annuitaetenfaktor

    # Berechnung der monatlichen Rate durch Division der jährlichen Annuität durch 12
    monatliche_tilgung = jaehrliche_annuitaet / 12
    
    # Gesamtzahlung des Kredites
    gesamtzahlung = monatliche_tilgung * (laufzeit_in_jahren * 12)
    
    # Gesamte Zinssumme
    gesamte_zinssumme = gesamtzahlung - darlehensbetrag
    
    return monatliche_tilgung, gesamtzahlung, gesamte_zinssumme

def berechne_gesamtrate_und_zinsen(kredit1_betrag, kredit1_zinssatz, kredit1_laufzeit, kredit2_betrag, kredit2_zinssatz, kredit2_laufzeit):
    """
    Berechnet die monatliche Rate, die Gesamtzahlung und die gesamte Zinssumme für zwei Kredite mit unterschiedlichen Laufzeiten und Zinssätzen.
    
    :param kredit1_betrag: Betrag des ersten Kredits.
    :param kredit1_zinssatz: Jahreszinssatz des ersten Kredits.
    :param kredit1_laufzeit: Laufzeit des ersten Kredits in Jahren.
    :param kredit2_betrag: Betrag des zweiten Kredits.
    :param kredit2_zinssatz: Jahreszinssatz des zweiten Kredits.
    :param kredit2_laufzeit: Laufzeit des zweiten Kredits in Jahren.
    :return: Die monatliche Rate für die ersten Jahre, die Rate für die restlichen Jahre, die Gesamtzahlung und die gesamte Zinssumme beider Kredite.
    """
    # ANNUITÄT FÜR DEN BANKENKREDIT
    zinssatz_dezimal_kredit1 = kredit1_zinssatz / 100
    annuitaetenfaktor_kredit1 = (zinssatz_dezimal_kredit1 * (1 + zinssatz_dezimal_kredit1) ** kredit1_laufzeit) / ((1 + zinssatz_dezimal_kredit1) ** kredit1_laufzeit - 1)
    jaehrliche_annuitaet_kredit1 = kredit1_betrag * annuitaetenfaktor_kredit1

    # Berechnung der monatlichen Rate durch Division der jährlichen Annuität durch 12
    monatliche_rate_kredit1 = jaehrliche_annuitaet_kredit1 / 12

    # ANNUITÄT FÜR BAUSPAR DARLEHEN
    zinssatz_dezimal_kredit2 = kredit2_zinssatz / 100
    annuitaetenfaktor_kredit2 = (zinssatz_dezimal_kredit2 * (1 + zinssatz_dezimal_kredit2) ** kredit2_laufzeit) / ((1 + zinssatz_dezimal_kredit2) ** kredit2_laufzeit - 1)
    jaehrliche_annuitaet_kredit2 = kredit2_betrag * annuitaetenfaktor_kredit2

    # Berechnung der monatlichen Rate durch Division der jährlichen Annuität durch 12
    monatliche_rate_kredit1 = jaehrliche_annuitaet_kredit1 / 12
    monatliche_rate_kredit2 = jaehrliche_annuitaet_kredit2 / 12
    
    # Gesamtzahlungen und Zinssummen berechnen
    gesamtzahlung_kredit1 = monatliche_rate_kredit1 * (kredit1_laufzeit * 12)
    gesamtzahlung_kredit2 = monatliche_rate_kredit2 * (kredit2_laufzeit * 12)
    gesamte_zinssumme_kredit1 = gesamtzahlung_kredit1 - kredit1_betrag
    gesamte_zinssumme_kredit2 = gesamtzahlung_kredit2 - kredit2_betrag
    
    gesamtzahlung = gesamtzahlung_kredit1 + gesamtzahlung_kredit2
    gesamte_zinssumme = gesamte_zinssumme_kredit1 + gesamte_zinssumme_kredit2
    
    # Gesamtrate für die ersten Jahre berechnen
    gesamtrate_erste_jahre = monatliche_rate_kredit1 + monatliche_rate_kredit2
    
    # Rate für die restlichen Jahre, nachdem Kredit 1 abbezahlt ist
    if kredit1_laufzeit < kredit2_laufzeit:
        rate_restliche_jahre = monatliche_rate_kredit2
    elif kredit2_laufzeit < kredit1_laufzeit:
        rate_restliche_jahre = monatliche_rate_kredit1
    
    return gesamtrate_erste_jahre, rate_restliche_jahre, gesamtzahlung, gesamte_zinssumme

def format_eu(zahl):
    """
    Formatieren einer Zahl im europäischen Format mit Tausendertrennzeichen und zwei Dezimalstellen.

    :param zahl: Die zu formatierende Zahl.
    :return: Die formatierte Zahl als String.
    """
    return "{:,.1f}".format(zahl).replace(",", "X").replace(".", ",").replace("X", ".")




if sprache == "Deutsch":
    st.title("Tilgungsrechner mit und ohne Bausparen")
    url_ra = "https://www.pensplan.com/de/bausparen.asp"
    st.markdown("Die Provinz Bozen hat mit dem Bausparmodell eine Möglichkeit geschaffen, um den Bau, den Kauf oder die Wiedergewinnung der eigenen vier Wände zu finanzieren. Weitere Informationen finden Sie hier: [Pensplan](%s)" % url_ra)
    st.markdown("""Folgende Voraussetzungen müssen gegeben sein:""")
    st.markdown(
            """
                    * Einschreibung in einem Rentenfonds, der dem Bausparmodell beigetreten ist
                    * Seit mindestens 5 Jahren kontinuierlich in der Autonomen Provinz Bozen ansässig
                    * Nicht älter als 65 Jahre
                    * Seit mindestens 8 Jahren in einem Zusatzrentenfonds eingeschrieben
                    * Persönliche Zusatzrentenfondsposition von mindestens 15.000 Euro frei von Lasten, Verbindlichkeiten, Bindungen und Auflagen
                    * Die Erstwohnung befindet sich in Südtirol
                    """
        )
    st.markdown("""Das Darlehen für das Bausparmodell hat einen fixen Zinssatz von **1 Prozent**. Für eine Einzelperson kann das Darlehen vom Bausparmodell max. 150.000 € betragen und für einen Haushalt 250.000 €. In der folgenden Berechnung wird die Zinsersparnis mit einem Bauspardarlehen berechnet für eine Einzelperson. Bei der Berechnung wird die Annuitätenmethode verwendet.""")



    st.subheader("Bedingungen des Bankdarlehens")
    col1, col2, col3 = st.columns(3)
    # Place each widget in its respective column
    with col1:
        kreditsumme = st.number_input('Summe des Darlehens', format='%.0f', placeholder= "", value = float(300000), step = float(10000))
    with col2:
        jahreszinssatz = st.number_input('Zinssatz des Darlehens (%)', format='%.2f', placeholder= "", value = float(4.50), step = float(0.10))
    with col3:
        laufzeit_in_jahren = st.number_input('Laufzeit des Darlehens in Jahren', format='%.0f', placeholder= "", value = float(30), step = float(1))




    st.subheader("Bedingungen des Bauspardarlehens")
    spar1, spar2, spar3 = st.columns(3)
    # Place each widget in its respective column
    with spar1:
        rentenposition = st.number_input('Angespartes Kapital im Rentenfonds', format='%.0f', placeholder= "", value = float(15000), step = float(1000))
    with spar2:
        kredit2_laufzeit = st.number_input('Laufzeit Bauspardarlehen in Jahren', format='%.0f', placeholder= "", value = float(20), step = float(1))
    with spar3:
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
        anstellung = st.radio(
        "Öffentlicher Angestellter in einem kollektivvertraglichen Rentenfonds?",
        ["Nein", "Ja"])

    if anstellung == "Ja":
        faktor = 3
    elif anstellung == "Nein":
        faktor = 2



    resultate_1 = tilgungsrechner(kreditsumme, laufzeit_in_jahren, jahreszinssatz)

    st.subheader("Tilgung ohne Bausparen")
    col1, col2, col3 = st.columns(3)
    col1.metric(f"Monatliche Rate für {laufzeit_in_jahren:.0f} Jahre", f"{format_eu(resultate_1[0])} €")
    col2.metric("Gesamtzahlung", f"{format_eu(resultate_1[1])} €")
    col3.metric("Gesamte Zinsen", f"{format_eu(resultate_1[2])} €")


    style_metric_cards()


    # Beispiel: Ein Aufruf der Funktion
    sparsumme = rentenposition * faktor
    if sparsumme > 150000:
        sparsumme = 150000

    kredit1_betrag = kreditsumme - sparsumme
    kredit1_zinssatz = jahreszinssatz
    kredit1_laufzeit = laufzeit_in_jahren


    kredit2_betrag = sparsumme
    kredit2_zinssatz = 1.0

    resultate_2 = berechne_gesamtrate_und_zinsen(kredit1_betrag, kredit1_zinssatz, kredit1_laufzeit, kredit2_betrag, kredit2_zinssatz, kredit2_laufzeit)

    st.subheader("Tilgung mit Bausparen")
    col1, col2 = st.columns(2)
    col1.metric(f"Monatliche Rate für die ersten {min(kredit1_laufzeit, kredit2_laufzeit):.0f} Jahre", f"{format_eu(resultate_2[0])} €")
    col2.metric(f"Monatliche Rate für die restlichen {max(kredit1_laufzeit, kredit2_laufzeit) - min(kredit1_laufzeit, kredit2_laufzeit):.0f} Jahre", f"{format_eu(resultate_2[1])} €")

    style_metric_cards()

    col1, col2 = st.columns(2)
    col1.metric("Gesamtzahlung", f"{format_eu(resultate_2[2])} €")
    col2.metric("Gesamte Zinsen", f"{format_eu(resultate_2[3])} €")

    style_metric_cards()


    zinsersparnis = resultate_1[2] - resultate_2[3]

    st.subheader("Ersparnis der Zinsen")
    st.markdown(f"Gesamte Zinsersparnis mit dem Bausparmodell beträgt: **{format_eu(zinsersparnis)} €**")


      





elif sprache == "Italiano":
    st.title("Calcolatore con e senza Mutuo Risparmio Casa")
    url_ra = "https://www.pensplan.com/de/bausparen.asp"
    st.markdown("La provincia di Bolzano ha creato con il modello Mutuo Risparmio Casa un'opportunità per finanziare la costruzione, l'acquisto o il recupero della propria casa. Ulteriori informazioni sono disponibili qui: [Pensplan](%s)" % url_ra)
    st.markdown("""Le seguenti condizioni devono essere soddisfatte:""")
    st.markdown(
            """
                    * Iscrizione ad un fondo pensione aderente al modello Risparmio Casa
                    * Almeno 5 anni di residenza continuativa nella Provincia Autonoma di Bolzano
                    * Età anagrafica non superiore ai 65 anni
                    * Anzianità di iscrizione alla previdenza complementare pari ad almeno 8 anni
                    * Posizione previdenzale complementare pari ad almeno 15.000,00 € libera da pesi, oneri, vincoli o gravami di ogni genere
                    * Ubicazione della prima casa di abitazione nel territorio della Provincia di Bolzano
                    """
        )
    st.markdown("""Il prestito per il modello di risparmio edilizio ha un tasso di interesse fisso dell'**1 percento**. Per una singola persona, il prestito dal modello di risparmio edilizio può essere al massimo di 150.000 € e per una famiglia 250.000 €. Nel seguente calcolo verrà calcolato il risparmio di interessi con un prestito di risparmio edilizio per una singola persona. Il calcolo utilizza il metodo dell'annuità.""")



    st.subheader("Condizioni del prestito bancario")
    col1, col2, col3 = st.columns(3)
    # Place each widget in its respective column
    with col1:
        kreditsumme = st.number_input('Somma del Prestito', format='%.0f', placeholder= "", value = float(300000), step = float(10000))
    with col2:
        jahreszinssatz = st.number_input('Tasso di interesse del prestito (%)', format='%.2f', placeholder= "", value = float(4.50), step = float(0.10))
    with col3:
        laufzeit_in_jahren = st.number_input('Durata del prestito in anno', format='%.0f', placeholder= "", value = float(30), step = float(1))




    st.subheader("Condizioni del Mutuo Risparmio Casa")
    spar1, spar2, spar3 = st.columns(3)
    # Place each widget in its respective column
    with spar1:
        rentenposition = st.number_input('Capitale accumulato nel fondo pensione', format='%.0f', placeholder= "", value = float(15000), step = float(1000))
    with spar2:
        kredit2_laufzeit = st.number_input('Durata Mutuo Risparmio Casa in anni', format='%.0f', placeholder= "", value = float(20), step = float(1))
    with spar3:
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
        anstellung = st.radio(
        "Impiegato pubblico in un fondo pensione contrattuale?",
        ["No", "Si"])

    if anstellung == "Si":
        faktor = 3
    elif anstellung == "No":
        faktor = 2



    resultate_1 = tilgungsrechner(kreditsumme, laufzeit_in_jahren, jahreszinssatz)

    st.subheader("Ammortamento senza Mutuo Risparmio Casa")
    col1, col2, col3 = st.columns(3)
    col1.metric(f"Rata Mensile per {laufzeit_in_jahren:.0f} anni", f"{format_eu(resultate_1[0])} €")
    col2.metric("Pagamento Total", f"{format_eu(resultate_1[1])} €")
    col3.metric("Interessi Totali", f"{format_eu(resultate_1[2])} €")


    style_metric_cards()


    # Beispiel: Ein Aufruf der Funktion
    sparsumme = rentenposition * faktor
    if sparsumme > 150000:
        sparsumme = 150000

    kredit1_betrag = kreditsumme - sparsumme
    kredit1_zinssatz = jahreszinssatz
    kredit1_laufzeit = laufzeit_in_jahren


    kredit2_betrag = sparsumme
    kredit2_zinssatz = 1.0

    resultate_2 = berechne_gesamtrate_und_zinsen(kredit1_betrag, kredit1_zinssatz, kredit1_laufzeit, kredit2_betrag, kredit2_zinssatz, kredit2_laufzeit)

    st.subheader("Ammortamento con Mutuo Risparmio Casa")
    col1, col2 = st.columns(2)
    col1.metric(f"Rata Mensile per i primi {min(kredit1_laufzeit, kredit2_laufzeit):.0f} anni", f"{format_eu(resultate_2[0])} €")
    col2.metric(f"Rata Mensile per i seguenti {max(kredit1_laufzeit, kredit2_laufzeit) - min(kredit1_laufzeit, kredit2_laufzeit):.0f} anni", f"{format_eu(resultate_2[1])} €")

    style_metric_cards()

    col1, col2 = st.columns(2)
    col1.metric("Pagamento Totale", f"{format_eu(resultate_2[2])} €")
    col2.metric("Interessi Totali", f"{format_eu(resultate_2[3])} €")

    style_metric_cards()


    zinsersparnis = resultate_1[2] - resultate_2[3]

    st.subheader("Risparmio degli Interessi")
    st.markdown(f"Il risparmio totale sugli interessi con il modello di Mutuo Risparmio Casa ammonta a: **{format_eu(zinsersparnis)} €**")
