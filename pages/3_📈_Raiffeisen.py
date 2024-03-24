import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



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
            unsafe_allow_html=True,
        )


if sprache == "Deutsch":


    st.title("Zusatzrentenfonds Rechner - Raiffeisen")



    st.markdown("Dieser Rechner ermöglich es Ihnen die Entwicklung Ihrer Beiträge im Zusatzrentenfonds zu visualisieren.")
    st.markdown("Sie können die Investitionslinie und Beitragsbeginn für die Simulation bestimmen, welche vom Raiffeisen Offener Pensionsfonds angeboten werden.")
    st.markdown(
        """ 
                * Investitionslinie **Guaranty**: Geringes Risiko
                * Investitionslinie **Safe**: Geringes bis mittleres Risiko
                * Investitionslinie **Activitiy**: Mittleres bis hohes Risiko
                * Investitionslinie **Dynamic**: Hohes Risiko
                """
    )
    url_ra = "https://www.raiffeisenpensionsfonds.it/de/index.html"
    st.markdown("Weitere Informationen finden Sie hier: [Raiffeisen Offener Pensionsfonds](%s)" % url_ra)


    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  


    st.subheader("Simulieren Sie die Portfolio Entwicklung")
    st.markdown("In dieser Berechnung werden die öffentlich zugänglichen Daten des jeweiligen Pensionsfonds verwendet. Alle Pensionsfonds sind verpflichtet den Wert aller Investitionslinien zu veröffentlichen. Dabei wird der sogennante Net Asset Value verwendet, bei welchem jegliche Verwaltungskosten (bis auf Mitgliedsgebühr) bereits abgezogen sind.")

    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)

    st.subheader("1. Schritt: Wählen Sie die Art der Beiträge aus")
    typ = st.selectbox(
    "Bitte definieren Sie ob Ihre Beiträge auf kollektivvertraglicher oder individueller Basis eingezahlt werden",
    ("Kollektivvertraglich", "Individuell"),
    index = 0,
    placeholder="Einzahlungsart",
    )
    st.markdown("**Kollektivvertraglich:** Die Höhe der Beiträge ist in den jeweiligen Arbeitskollektivverträgen festgelegt. Der Arbeitnehmerbeitrag kann zudem erhöht werden. Sie werden monatlich vom Gehalt einbehalten und auf das Bruttoeinkommen berechnet. Anschließend werden sie direkt vom Arbeitgeber vierteljährlich an den Zusatzrentenfonds überwiesen und in der Einheitlichen Bescheinigung (CU) festgehalten.")
    st.markdown("**Individuell:** Erfolgt der Beitritt auf individueller Basis, kann das Mitglied selbst die Höhe und Regelmäßigkeit der Beitragszahlung bestimmen, indem es direkt in den Zusatzrentenfonds einzahlt und diese Beträge in der Steuererklärung angibt. So kann es die Beiträge von der Einkommenssteuer abziehen.")


    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)



    st.subheader("2. Schritt: Wählen Sie die Investitionslinie aus")
    line = st.selectbox(
    "Wählen Sie eine der Investitionslinien aus",
    ("Guaranty", "Safe", "Activitiy", "Dynamic"),
    index=3,
    placeholder="Ihre Linie",
    )

    if line == "Guaranty":
        fund_name = "RA_GAR"
    elif line == "Safe":
        fund_name = "RA_SAF"
    elif line == "Dynamic":
        fund_name = "RA_DYN"
    elif line == "Activitiy":
        fund_name = "RA_ACT"



    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  # Adds 100px of space



    st.subheader("3. Schritt: Definieren Sie Ihren Beitrag")

    if typ == "Kollektivvertraglich":
        # Create three columns
        col1, col2, col3 = st.columns(3)
        # Place each widget in its respective column
        with col1:
            income = st.number_input('Jahreseinkommen Brutto', format='%.0f', placeholder= "Geben Sie Ihr Einkommen an", value = float(30000), step = float(1000))
        with col2:
            an_beitrag = st.slider('Arbeitnehmer Beitrag', float(0), float(10), float(1), format='%.2f', step=0.1)
        with col3:
            ag_beitrag = st.slider('Arbeitgeber Beitrag', float(0), float(10), float(1), format='%.2f', step=float(0.1))
    elif typ == "Individuell":
        col1, col2 = st.columns(2)
        # Place each widget in its respective column
        with col1:
            beitrag = st.number_input('Beitragszahlung', format='%.0f', placeholder= "", value = float(250), step = float(50))
        with col2:
            intervall = st.selectbox(
    "Bestimmen Sie das Intervall der Einzahlungen",
    ("Monatlich", "Vierteljährlich", "Halbjährlich", "Jährlich"),
    index=0,
    placeholder="Ihre Linie",
    )



    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  # Adds 100px of space

    # Determine the start year based on the fund_name
    if fund_name == "RA_GAR":
        start_year = 2019
    elif fund_name == "RA_DYN":
        start_year = 2007
    elif fund_name == "RA_ACT":
        start_year = 2005
    elif fund_name == "RA_SAF":
        start_year = 2005


    st.subheader("4. Schritt: Bestimmen Sie den Startpunkt der Einzahlung")
    if typ == "Kollektivvertraglich":
        # Create three columns
        date1, date2 = st.columns(2)
        # Place each widget in its respective column
        with date1:
            quartal = st.selectbox(
        "Startpunkt Einzahlungen Quartal",
        ("Q1", "Q2", "Q3", "Q4"),
        index=0,
        placeholder="",
        )
        with date2:
            jahr = st.slider('Startpunkt Einzahlungen Jahr', start_year, int(2023), int(2020), format='%.0f', step=int(1))
    elif typ == "Individuell":
        # Create three columns
        date1, date2 = st.columns(2)
        # Place each widget in its respective column
        with date1:
            monat = st.selectbox(
        "Startpunkt Monat",
        (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
        index=5,
        placeholder="",
        )
        with date2:
            jahr = st.slider('Startpunkt Einzahlungen Jahr', start_year, int(2023), int(2010), format='%.0f', step=int(1))



    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  # Adds 100px of space




    excel_path = 'https://raw.githubusercontent.com/Schesch/pension_calculator/main/data/Raiffeisen.xlsx'

    # Read Excel file
    df = pd.read_excel(excel_path, sheet_name=fund_name)

    if typ == "Kollektivvertraglich":
        einzahlung = round((income * ((an_beitrag/100) + (ag_beitrag/100))) / 4 ,2)
    elif typ == "Individuell":
        einzahlung = beitrag

    try:
        if intervall == "Monatlich":
            filter_range = 1
        elif intervall == "Vierteljährlich":
            filter_range = 3
        elif intervall == "Halbjährlich":
            filter_range = 6
        elif intervall == "Jährlich":
            filter_range = 12
    except NameError:
        pass


    st.subheader("Auswahl der Parameter")

    if typ == "Kollektivvertraglich":
        try:
            start_idx = df[(df['Quartal'] == quartal) & (df['Jahr'] == jahr)].index[0]
            df_filtered = df.iloc[start_idx:]
            df_filtered = df_filtered.groupby(['Quartal', 'Jahr']).tail(1)
            st.markdown(
                f"""
        Sie haben folgende Parameter für die Berechnung ausgewählt:
        * Investitionslinie: {line}
        * Einkommen: {income}€
        * Arbeitnehmer Beitrag: {an_beitrag}%
        * Arbeitgeber Beitrag: {ag_beitrag}%
        * Einzahlung pro Quartal: {einzahlung}€
        * Erstes Quartal Einzahlung: {quartal}
        * Erstes Jahr Einzahlung: {jahr}
                """
            )
        except IndexError:
            st.markdown(
                """
        Die Simulation kann nicht zu Ihrem angegeben Zeiptunkt nicht gestartet werden, da die Daten nicht verfügbar sind.
        Überprüfen Sie, ob Sie einen gültigen Startpunkt gewählt haben.
        * Für die Linie Guaranty: ab Q1 2019
        * Für die Linie Safe: ab Q4 2005
        * Für die Linie Activity: ab Q4 2005
        * Für die Linie Dynamic: ab Q1 2007
                """
            )
    elif typ == "Individuell":
        try:
            start_idx = df[(df['Monat'] == monat) & (df['Jahr'] == jahr)].index[0]
            df_filtered = df.iloc[start_idx::filter_range]
            st.markdown(
                f"""
        Sie haben folgende Parameter für die Berechnung ausgewählt:
        * Investitionslinie: {line}
        * Summe Einzahlung: {einzahlung}€
        * Intervall der Einzahlung: {intervall}
        * Erstes Monat Einzahlung: {monat}
        * Erstes Jahr Einzahlung: {jahr}
                """
            )
        except IndexError:
            st.markdown(
                """
        Die Simulation kann nicht zu Ihrem angegeben Zeiptunkt nicht gestartet werden, da die Daten nicht verfügbar sind.
        Überprüfen Sie, ob Sie einen gültigen Startpunkt gewählt haben.
        * Für die Linie Guaranty: ab Januar 2019
        * Für die Linie Safe: ab November 2005
        * Für die Linie Activity: ab November 2005
        * Für die Linie Dynamic: ab Januar 2007
                """
            )


    portfolio_value = 0
    total_contributions = 0
    shares_owned = 0
    portfolio_values = []
    dates = []
    contribution = einzahlung

    for index, row in df_filtered.iterrows():
        total_contributions += contribution
        nav_per_share = row['NAV']
        
        # Buy shares with the new contributions
        shares_bought = contribution / nav_per_share
        shares_owned += shares_bought
        
        # Update portfolio value to include new shares
        portfolio_value = shares_owned * nav_per_share
        
        portfolio_values.append(portfolio_value)
        dates.append(row['Datum'])
    profit = portfolio_value - total_contributions
    profit_percent = (profit/total_contributions) * 100

    st.markdown("<div style='margin: 75px;'></div>", unsafe_allow_html=True)  # Adds 100px of space

    first_date = min(df_filtered["Datum"]).strftime("%d/%m/%Y")
    last_date = max(df_filtered["Datum"]).strftime("%d/%m/%Y")


    col1, col2 = st.columns(2)
    col1.metric("Beiträge vom " + first_date + " bis zum " + last_date, f"{round(total_contributions, 1):,}€")
    col2.metric("Portfolio Wert am " + last_date, f"{round(portfolio_value, 1):,}€")
        
    col3, col4 = st.columns(2)
    col3.metric("Gewinn am " + last_date, f"{round(profit, 1):,}€")
    col4.metric("Performance vom " + first_date + " bis zum " + last_date, f"{round(profit_percent, 1):,}%")

    style_metric_cards()





    st.markdown("<div style='margin: 50px;'></div>", unsafe_allow_html=True)  # Adds 100px of space



    plt.figure(figsize=(10, 5))
    plt.plot(dates, portfolio_values, marker='o', linestyle='-', markersize=4, color='blue')
    plt.title('Entwicklung der Gesamtposition im Verlauf der Zeit')
    plt.xlabel('Zeitraum (Monat/Jahr)', fontsize = 10)
    plt.ylabel('Wert des Portfolios in €', fontsize = 10)

    # Determine quarters and years for all dates
    months = [date.month for date in dates]
    years = [date.year for date in dates]

    # Function to check if observations are sequential months
    def are_sequential_months(months):
        for i in range(1, len(months)):
            # Check if the current month is either the next month of the previous or it's January following December
            if not ((months[i] == (months[i-1] % 12) + 1)):
                return False
        return True

    is_monthly = are_sequential_months(months)

    # Now, you can continue with setting up custom labels and positions based on 'is_monthly'
    custom_labels = []
    custom_positions = []

    if is_monthly:
        # If monthly, add every third month to labels and positions
        for i in range(0, len(dates), 3):
            month = dates[i].month
            year = dates[i].year
            custom_labels.append(f"{month}/{year}")
            custom_positions.append(dates[i])
    else:
        # If not monthly (e.g., quarterly, bi-annually), add all observations
        custom_labels = [f"{dates[i].month}/{dates[i].year}" for i in range(len(dates))]
        custom_positions = dates

    # Set custom ticks and labels
    plt.xticks(ticks=custom_positions, labels=custom_labels, rotation=90, fontsize = 7)
    # Set font size for y-axis tick labels
    plt.yticks(fontsize=8)

    vertical_offset = 10  # Adjust this value as needed for appropriate spacing

    # Label the first and last points with their values, adding vertical_offset for spacing
    plt.text(dates[0], portfolio_values[0] + vertical_offset, f"{portfolio_values[0]:.0f}€", color="black", ha="center", va="bottom", fontsize="small")
    plt.text(dates[-1], portfolio_values[-1] + vertical_offset, f"{portfolio_values[-1]:.0f}€", color="black", ha="center", va="bottom", fontsize="small")

    # Enable grid lines on the y-axis only, with custom color and linewidth
    plt.grid(axis='y', color='#c7c3c3', linestyle='-', linewidth=0.7)
    plt.tight_layout()
    # Display the plot in Streamlit
    st.pyplot(plt)

    st.markdown(
        """Entwickelt von **Alex Laimer**"""
    )




elif sprache == "Italiano":


    st.title("Calcolatore del fondo pensione complementare - Raiffeisen")



    st.markdown("Questa calcolatrice le permette di visualizzare lo sviluppo dei suoi contributi nel fondo pensione complementare.")
    st.markdown("Può scegliere tra le linee di investimento, offerte dal Fondo Pensione Aperto Raiffeisen, e determinare l'inizio dei contributi per la simulazione.")
    st.markdown(
        """ 
                * Linea di Investimento **Guaranty**: Rischio basso
                * Linea di Investimento **Safe**: Rischio da basso a medio
                * Linea di Investimento **Activitiy**: Rischio da medio ad alto
                * Linea di Investimento **Dynamic**: Rischio alto
                """
    )
    url_ra = "https://www.raiffeisenpensionsfonds.it/de/index.html"
    st.markdown("Per ulteriori informazioni, consultare qui: [Fondo Pensione Aperto Raiffeisen](%s)" % url_ra)


    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  


    st.subheader("Simuli lo sviluppo del portafoglio")
    st.markdown("In questo calcolo vengono utilizzati i dati pubblicamente accessibili del rispettivo fondo pensione. Tutti i fondi pensione sono obbligati a pubblicare il valore di tutte le linee di investimento. Si utilizza il cosiddetto Valore Patrimoniale Netto, dal quale sono già detratti tutti i costi di gestione (esclusa la quota associativa).")

    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)

    st.subheader("1° Passo: Scegliere il tipo di contributi")
    typ = st.selectbox(
    "Si prega di definire se i suoi contributi vengono versati su base collettiva o individuale",
    ("Base Collettiva", "Individuale"),
    index = 0,
    placeholder="Tipo di contributo",
    )
    st.markdown("**Base Collettiva:** L'importo dei contributi è stabilito nei rispettivi contratti collettivi di lavoro. Il contributo del lavoratore può inoltre essere aumentato. Vengono trattenuti mensilmente dallo stipendio e calcolati sul reddito lordo. Successivamente, vengono versati direttamente dall'azienda al fondo pensione complementare su base trimestrale e registrati nella Certificazione Unica (CU).")
    st.markdown("**Individuale:** Se l'adesione avviene su base individuale, il membro può determinare autonomamente l'ammontare e la regolarità dei versamenti dei contributi, effettuando i pagamenti direttamente al fondo pensione complementare e dichiarando tali importi nella dichiarazione dei redditi. In questo modo, è possibile dedurre i contributi dall'imposta sul reddito.")


    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)



    st.subheader("2° Passo: Scegliere la linea di investimento")
    line = st.selectbox(
    "Selezionare una linea di investimento",
    ("Guaranty", "Safe", "Activitiy", "Dynamic"),
    index=3,
    placeholder="La sua linea",
    )

    if line == "Guaranty":
        fund_name = "RA_GAR"
    elif line == "Safe":
        fund_name = "RA_SAF"
    elif line == "Dynamic":
        fund_name = "RA_DYN"
    elif line == "Activitiy":
        fund_name = "RA_ACT"



    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  # Adds 100px of space



    st.subheader("3° Passo: Determinare il suo contributo")

    if typ == "Base Collettiva":
        # Create three columns
        col1, col2, col3 = st.columns(3)
        # Place each widget in its respective column
        with col1:
            income = st.number_input('Reddito annuo lordo', format='%.0f', placeholder= "Geben Sie Ihr Einkommen an", value = float(30000), step = float(1000))
        with col2:
            an_beitrag = st.slider('Contributo del lavoratore', float(0), float(10), float(1), format='%.2f', step=0.1)
        with col3:
            ag_beitrag = st.slider('Contributo del datore di lavoro', float(0), float(10), float(1), format='%.2f', step=float(0.1))
    elif typ == "Individuale":
        col1, col2 = st.columns(2)
        # Place each widget in its respective column
        with col1:
            beitrag = st.number_input('Contributo', format='%.0f', placeholder= "", value = float(250), step = float(50))
        with col2:
            intervall = st.selectbox(
    "Determinare l'intervallo dei versamenti",
    ("Mensile", "Trimestrale", "Semestrale", "Annuale"),
    index=0,
    placeholder="La sua linea",
    )



    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  # Adds 100px of space

    # Determine the start year based on the fund_name
    if fund_name == "RA_GAR":
        start_year = 2019
    elif fund_name == "RA_DYN":
        start_year = 2007
    elif fund_name == "RA_ACT":
        start_year = 2005
    elif fund_name == "RA_SAF":
        start_year = 2005


    st.subheader("4° Passo: Determinare il punto di inizio del versamento")
    if typ == "Base Collettiva":
        # Create three columns
        date1, date2 = st.columns(2)
        # Place each widget in its respective column
        with date1:
            quartal = st.selectbox(
        "Inizio dei versamenti trimestrale",
        ("Q1", "Q2", "Q3", "Q4"),
        index=0,
        placeholder="",
        )
        with date2:
            jahr = st.slider('Anno di inizio dei versamenti', start_year, int(2023), int(2020), format='%.0f', step=int(1))
    elif typ == "Individuale":
        # Create three columns
        date1, date2 = st.columns(2)
        # Place each widget in its respective column
        with date1:
            monat = st.selectbox(
        "Inizio Mese",
        (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
        index=5,
        placeholder="",
        )
        with date2:
            jahr = st.slider('Anno di inizio dei versamenti', start_year, int(2023), int(2010), format='%.0f', step=int(1))



    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  # Adds 100px of space




    excel_path = 'https://raw.githubusercontent.com/Schesch/pension_calculator/main/data/Raiffeisen.xlsx'

    # Read Excel file
    df = pd.read_excel(excel_path, sheet_name=fund_name)

    if typ == "Base Collettiva":
        einzahlung = round((income * ((an_beitrag/100) + (ag_beitrag/100))) / 4 ,2)
    elif typ == "Individuale":
        einzahlung = beitrag

    try:
        if intervall == "Mensile":
            filter_range = 1
        elif intervall == "Trimestrale":
            filter_range = 3
        elif intervall == "Semestrale":
            filter_range = 6
        elif intervall == "Annuale":
            filter_range = 12
    except NameError:
        pass


    st.subheader("Selezione dei parametri")

    if typ == "Base Collettiva":
        try:
            start_idx = df[(df['Quartal'] == quartal) & (df['Jahr'] == jahr)].index[0]
            df_filtered = df.iloc[start_idx:]
            df_filtered = df_filtered.groupby(['Quartal', 'Jahr']).tail(1)
            st.markdown(
                f"""
        Ha selezionato i seguenti parametri per la simulazione:
        * Linea di investimento: {line}
        * Reddito: {income}€
        * Contributo del lavoratore: {an_beitrag}%
        * Contributo del datore di lavoro: {ag_beitrag}%
        * Versamento trimestrale: {einzahlung}€
        * Primo trimestre di versamento: {quartal}
        * Primo anno di versamento: {jahr}
                """
            )
        except IndexError:
            st.markdown(
                """
        La simulazione non può essere avviata al momento da lei indicato, poiché i dati non sono disponibili.
        Verifichi di aver scelto un punto di inizio valido.
        * Per la linea Guaranty: da Q1 2019
        * Per la linea Safe: da Q4 2005
        * Per la linea Activity: da Q4 2005
        * Per la linea Dynamic: da Q1 2007
                """
            )
    elif typ == "Individuale":
        try:
            start_idx = df[(df['Monat'] == monat) & (df['Jahr'] == jahr)].index[0]
            df_filtered = df.iloc[start_idx::filter_range]
            st.markdown(
                f"""
        Ha selezionato i seguenti parametri per la simulazione:
        * Linea di investimento: {line}
        * Somma versata: {einzahlung}€
        * Intervallo del versamento: : {intervall}
        * Primo mese di versamento: {monat}
        * Primo anno di versamento: {jahr}
                """
            )
        except IndexError:
            st.markdown(
                """
        La simulazione non può essere avviata al momento da lei indicato, poiché i dati non sono disponibili.
        Verifichi di aver scelto un punto di inizio valido.
        * Per la linea Guaranty: da Q1 2019
        * Per la linea Safe: da Q4 2005
        * Per la linea Activity: da Q4 2005
        * Per la linea Dynamic: da Q1 2007
                """
            )


    portfolio_value = 0
    total_contributions = 0
    shares_owned = 0
    portfolio_values = []
    dates = []
    contribution = einzahlung

    for index, row in df_filtered.iterrows():
        total_contributions += contribution
        nav_per_share = row['NAV']
        
        # Buy shares with the new contributions
        shares_bought = contribution / nav_per_share
        shares_owned += shares_bought
        
        # Update portfolio value to include new shares
        portfolio_value = shares_owned * nav_per_share
        
        portfolio_values.append(portfolio_value)
        dates.append(row['Datum'])
    profit = portfolio_value - total_contributions
    profit_percent = (profit/total_contributions) * 100

    st.markdown("<div style='margin: 75px;'></div>", unsafe_allow_html=True)  # Adds 100px of space

    
    first_date = min(df_filtered["Datum"]).strftime("%d/%m/%Y")
    last_date = max(df_filtered["Datum"]).strftime("%d/%m/%Y")

    col1, col2 = st.columns(2)
    col1.metric("Contributi dal " + first_date + " al " + last_date, f"{round(total_contributions, 1):,}€")
    col2.metric("Valore portafoglio al " + last_date, f"{round(portfolio_value, 1):,}€")
        
    col3, col4 = st.columns(2)
    col3.metric("Profitto al " + last_date, f"{round(profit, 1):,}€")
    col4.metric("Performance dal " + first_date + " al " + last_date, f"{round(profit_percent, 1):,}%")

    style_metric_cards()





    st.markdown("<div style='margin: 50px;'></div>", unsafe_allow_html=True)  # Adds 100px of space



    plt.figure(figsize=(10, 5))
    plt.plot(dates, portfolio_values, marker='o', linestyle='-', markersize=4, color='blue')
    plt.title('Sviluppo della posizione totale nel corso del tempo')
    plt.xlabel('Periodo (mese/anno)', fontsize = 10)
    plt.ylabel('Valore del portafoglio in €', fontsize = 10)

    # Determine quarters and years for all dates
    months = [date.month for date in dates]
    years = [date.year for date in dates]

    # Function to check if observations are sequential months
    def are_sequential_months(months):
        for i in range(1, len(months)):
            # Check if the current month is either the next month of the previous or it's January following December
            if not ((months[i] == (months[i-1] % 12) + 1)):
                return False
        return True

    is_monthly = are_sequential_months(months)

    # Now, you can continue with setting up custom labels and positions based on 'is_monthly'
    custom_labels = []
    custom_positions = []

    if is_monthly:
        # If monthly, add every third month to labels and positions
        for i in range(0, len(dates), 3):
            month = dates[i].month
            year = dates[i].year
            custom_labels.append(f"{month}/{year}")
            custom_positions.append(dates[i])
    else:
        # If not monthly (e.g., quarterly, bi-annually), add all observations
        custom_labels = [f"{dates[i].month}/{dates[i].year}" for i in range(len(dates))]
        custom_positions = dates

    # Set custom ticks and labels
    plt.xticks(ticks=custom_positions, labels=custom_labels, rotation=90, fontsize = 7)
    # Set font size for y-axis tick labels
    plt.yticks(fontsize=8)

    vertical_offset = 10  # Adjust this value as needed for appropriate spacing

    # Label the first and last points with their values, adding vertical_offset for spacing
    plt.text(dates[0], portfolio_values[0] + vertical_offset, f"{portfolio_values[0]:.0f}€", color="black", ha="center", va="bottom", fontsize="small")
    plt.text(dates[-1], portfolio_values[-1] + vertical_offset, f"{portfolio_values[-1]:.0f}€", color="black", ha="center", va="bottom", fontsize="small")

    # Enable grid lines on the y-axis only, with custom color and linewidth
    plt.grid(axis='y', color='#c7c3c3', linestyle='-', linewidth=0.7)
    plt.tight_layout()
    # Display the plot in Streamlit
    st.pyplot(plt)

    st.markdown(
        """Sviluppato da **Alex Laimer**  """
    )
