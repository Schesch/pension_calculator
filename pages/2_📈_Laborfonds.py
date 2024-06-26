import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



st.set_page_config(page_title="Pension Calculator", page_icon=":chart_with_upwards_trend:", layout="wide")







sprache = st.selectbox(
   "Language",
   ("Deutsch", "Italiano"),
   index=0,
   placeholder="",
)

# Load the appropriate translation
if sprache == 'Deutsch':
    st.title("Zusatzrentenfonds Rechner - Laborfonds")
    st.markdown("Dieser Rechner ermöglich es Ihnen die Entwicklung Ihrer Beiträge im Zusatzrentenfonds zu visualisieren.")
    st.markdown("Sie können zwischen den angebotenen Investitionslinien auswählen und den Beitragsbeginn für die Berechnung bestimmen.")
    st.markdown(
        """ 
                * Investitionslinie **Garantierte Linie**: Geringes Risiko
                * Investitionslinie **Vorsichtig-Ethische Linie**: Mittleres Risiko
                * Investitionslinie **Ausgewogene Linie**: Mittleres Risiko
                * Investitionslinie **Dynamische Linie**: Hohes Risiko
                """
    )
    url_ra = "https://www.laborfonds.it/de/"
    st.markdown("Weitere Informationen finden Sie hier: [Laborfonds](%s)" % url_ra)


    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  


    st.subheader("Berechnen Sie die Portfolio Entwicklung")
    st.markdown("In dieser Berechnung werden die öffentlich zugänglichen Daten des jeweiligen Pensionsfonds verwendet. Alle Pensionsfonds sind verpflichtet den Wert aller Investitionslinien zu veröffentlichen. Dabei wird der sogennante Net Asset Value verwendet, bei welchem jegliche Verwaltungskosten (bis auf Mitgliedsgebühr) bereits abgezogen sind.")


    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  # Adds 100px of space

    st.subheader("1. Schritt: Wählen Sie die Investitionslinie aus")
    line = st.selectbox(
    "Wählen Sie eine Investitionslinie von Laborfonds aus",
    ("Garantierte Linie", "Vorsichtig-Ethische Linie", "Ausgewogene Linie", "Dynamische Linie"),
    index=2,
    placeholder="Ihre Linie",
    )

    if line == "Ausgewogene Linie":
        fund_name = "LB_BIL"
    elif line == "Garantierte Linie":
        fund_name = "LB_GAR"
    elif line == "Dynamische Linie":
        fund_name = "LB_DIN"
    elif line == "Vorsichtig-Ethische Linie":
        fund_name = "LB_PRU"



    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  # Adds 100px of space

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



    st.subheader("2. Schritt: Bestimmen Sie Ihren Beitrag")
    # Create three columns
    col1, col2, col3 = st.columns(3)
    # Place each widget in its respective column
    with col1:
        income = st.number_input('Jahreseinkommen Brutto beim Beitritt (€)', format='%.0f', placeholder= "Geben Sie Ihr Einkommen an", value = float(30000), step = float(1000))
    with col2:
        an_beitrag = st.number_input('Arbeitnehmer Beitrag (%)', value = float(1.0), step = float(0.1), min_value=float(0.0), max_value=float(10.0), format='%.2f')
    with col3:
        ag_beitrag = st.number_input('Arbeitgeber Beitrag (%)', value = float(1.0), step = float(0.1), min_value=float(0.0), max_value=float(10.0), format='%.2f')

    st.markdown("Das Bruttoeinkommen wird in der Berechnung mit einem jährlichen Inflationsfaktor von 2% erhöht.")
    url_kv = "https://www.laborfonds.it/de/kollektivvertraege"
    st.markdown("Informationen zu den Kollektivverträgen finden Sie hier: [Laborfonds Kollektivverträge](%s)" % url_kv)

    st.subheader("Abfertigung")
    st.markdown("Die Abfertigung entspricht 6.91% vom Bruttogehalt und kann zusätzlich eingezahlt werden")
    tfr = st.number_input(
    "Bestimmen Sie den Anteil Ihrer Abfertigung der eingezahlt werden soll (%)",
    value = float(100),
    step = float(10),
    min_value = float(0),
    max_value = float(100),
    format='%.0f'
    )
    st.markdown("Bei Erstanstellung nach dem 28.04.1993 sind üblicherweise 100% der Abfertigung als Einzahlung vorgesehen. Dies kann jedoch in den jeweiligen angewandten Kollektivverträgen unterschiedlich gestaltet sein. Diese Information müssen Sie aus Ihrem jeweiligen Kollektivvertrag entnehmen.")


    # Determine the start year based on the fund_name
    start_year = int(2000) if fund_name == "LB_BIL" else int(2010)



    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  # Adds 100px of space




    st.subheader("3. Schritt: Bestimmen Sie den Startpunkt der Einzahlung")
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
        jahr = st.slider('Startpunkt Einzahlungen Jahr', start_year, int(2023), int(2010), format='%.0f', step=int(1))

    st.markdown("Die Einzahlungen beginnen im ersten Monat des jeweiligen Quartals.")


    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  # Adds 100px of space




    excel_path = 'https://raw.githubusercontent.com/Schesch/pension_calculator/main/data/Laborfond.xlsx'

    # Read Excel file
    df = pd.read_excel(excel_path, sheet_name=fund_name)

    tfr_beitrag = round((income) * 0.0691 * (tfr/100) / 4,1)
    einzahlung = round((income * ((an_beitrag/100) + (ag_beitrag/100))) / 4 + tfr_beitrag,1)
    einkommen = f"{round(income, 1):,}"


    try:
        start_idx = df[(df['Quartal'] == quartal) & (df['Jahr'] == jahr)].index[0]
        df_filtered = df.iloc[start_idx:]
        st.subheader("Auswahl Ihrer Parameter")
        st.markdown(
            f"""
    Sie haben folgende Parameter für die Berechnung ausgewählt:
    * **Investitionslinie**: {line}
    * Bruttoeinkommen im ersten Jahr: {einkommen}€
    * Arbeitnehmer Beitrag: {an_beitrag}%
    * Arbeitgeber Beitrag: {ag_beitrag}%
    * Abfertigung Beitrag pro Quartal zu Beginn: {tfr_beitrag}€
    * **Gesamte Einzahlung** pro Quartal zu Beginn: {einzahlung}€
    * Startpunkt Quartal: {quartal}
    * Startpunkt Jahr: {jahr}
            """
        )
    except IndexError:
        st.subheader("Die Berechnung kann nicht durchgeführt werden")
        st.markdown(
            """
    Die Berechnung kann nicht zu Ihrem angegeben Zeiptunkt nicht gestartet werden, da die Daten nicht verfügbar sind.
    Überprüfen Sie, ob Sie einen gültigen Startpunkt gewählt haben.
    * Für die Garantierte Linie: ab Q1 2008
    * Für die Ausgewogene Linie: ab Q3 2000
    * Für die Dynamische Linie: ab Q2 2008
    * Für die Vorsichtig-Ethische Linie: ab Q2 2008
            """
        )


    portfolio_value = 0
    total_contributions = 0
    shares_owned = 0
    portfolio_values = []
    dates = []
    inflation_rate = 0.02

    try:
        # Iterate through each row to calculate contributions and portfolio value
        for index, row in df_filtered.iterrows():
            # Check if a new year has started and update income accordingly
            if index > 0 and row['Quartal'] == "Q1":
                income *= (1 + inflation_rate)

            # Calculate TFR contribution based on the current income
            tfr_beitrag = round((income) * 0.0691 * (tfr / 100) / 4, 1)
            # Calculate total quarterly contribution based on the current income
            einzahlung = round((income * ((an_beitrag / 100) + (ag_beitrag / 100))) / 4 + tfr_beitrag, 1)

            # Contribution for this quarter
            contribution = einzahlung
            total_contributions += contribution
            nav_per_share = row['NAV']

            # Buy shares with the new contributions
            shares_bought = contribution / nav_per_share
            shares_owned += shares_bought

            # Update portfolio value to include new shares
            portfolio_value = shares_owned * nav_per_share

            # Record the portfolio value and corresponding date
            portfolio_values.append(portfolio_value)
            dates.append(row['Datum'])
        profit = portfolio_value - total_contributions
        profit_percent = (profit/total_contributions) * 100

        st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  # Adds 100px of space

        first_date = min(df_filtered["Datum"]).strftime("%d/%m/%Y")
        last_date = max(df_filtered["Datum"]).strftime("%d/%m/%Y")


        col1, col2 = st.columns(2)
        col1.metric("Beiträge vom " + first_date + " bis zum " + last_date, f"{round(total_contributions, 1):,}€")
        col2.metric("Portfolio Wert am " + last_date, f"{round(portfolio_value, 1):,}€")

        col3, col4 = st.columns(2)
        col3.metric("Gewinn am " + last_date, f"{round(profit, 1):,}€")
        col4.metric("Performance vom " + first_date + " bis zum " + last_date, f"{round(profit_percent, 1):,}%")

        style_metric_cards()





        st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  # Adds 100px of space



        plt.figure(figsize=(10, 5))
        plt.plot(dates, portfolio_values, marker='o', linestyle='-', markersize=3, color='blue')
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

        vertical_offset = 50  # Adjust this value as needed for appropriate spacing

        # Label the first and last points with their values, adding vertical_offset for spacing
        plt.text(dates[0], portfolio_values[0] + vertical_offset, f"{portfolio_values[0]:.0f}€", color="black", ha="center", va="bottom", fontsize="small")
        plt.text(dates[-1], portfolio_values[-1] + vertical_offset, f"{portfolio_values[-1]:.0f}€", color="black", ha="center", va="bottom", fontsize="small")

        # Enable grid lines on the y-axis only, with custom color and linewidth
        plt.grid(axis='y', color='#c7c3c3', linestyle='-', linewidth=0.7)
        plt.tight_layout()
        # Display the plot in Streamlit
        st.pyplot(plt)
    except NameError:
        st.markdown("")

    st.markdown(
        """Entwickelt von **Alex Laimer**"""
    )

elif sprache == "Italiano":
    st.title("Calcolatore del fondo pensione complementare - Laborfonds")
    st.markdown("Questa calcolatrice le permette di visualizzare lo sviluppo dei suoi contributi nel fondo pensione complementare.")
    st.markdown("Può scegliere tra le linee di investimento, offerte dal Laborfonds, e determinare l'inizio dei contributi per la calcolazione.")
    st.markdown(
        """ 
                * Linea di Investimento **Linea Garantita**: Rischio basso
                * Linea di Investimento **Linea Prudente Etica**: Rischio medio
                * Linea di Investimento **Linea Bilanciata**: Rischio medio
                * Linea di Investimento **Linea Dinamica**: Rischio alto
                """
    )
    url_ra = "https://www.laborfonds.it/de/"
    st.markdown("Per ulteriori informazioni, consultare qui: [Laborfonds](%s)" % url_ra)


    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  


    st.subheader("Calcolo per lo sviluppo del portafoglio")


    st.markdown("In questo calcolo vengono utilizzati i dati pubblicamente accessibili del rispettivo fondo pensione. Tutti i fondi pensione sono obbligati a pubblicare il valore di tutte le linee di investimento. Si utilizza il cosiddetto Valore Patrimoniale Netto, dal quale sono già detratti tutti i costi di gestione (esclusa la quota associativa).")


    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  # Adds 100px of space

    st.subheader("1° Passo: Scegliere la linea di investimento")
    line = st.selectbox(
    "Selezionare una linea di investimento di Laborfonds",
    ("Linea Garantita", "Linea Prudente Etica", "Linea Bilanciata", "Linea Dinamica"),
    index=2,
    placeholder="La sua Linea",
    )

    if line == "Linea Bilanciata":
        fund_name = "LB_BIL"
    elif line == "Linea Garantita":
        fund_name = "LB_GAR"
    elif line == "Linea Dinamica":
        fund_name = "LB_DIN"
    elif line == "Linea Prudente Etica":
        fund_name = "LB_PRU"



    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  # Adds 100px of space

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



    st.subheader("2° Passo: Determinare il suo contributo")
    # Create three columns
    col1, col2, col3 = st.columns(3)
    # Place each widget in its respective column
    with col1:
        income = st.number_input('Reddito annuo lordo iniziale', format='%.0f', placeholder= "Geben Sie Ihr Einkommen an", value = float(30000), step = float(1000))
    with col2:
        an_beitrag = st.number_input('Contributo del lavoratore', value = float(1.0), step = float(0.1), min_value=float(0.0), max_value=float(10.0), format='%.2f')
    with col3:
        ag_beitrag = st.number_input('Contributo del datore di lavoro', value = float(1.0), step = float(0.1), min_value=float(0.0), max_value=float(10.0), format='%.2f')

    st.markdown("Il reddito lordo viene aumentato nel calcolo con un fattore di inflazione annuale del 2%.")
    url_kv = "https://www.laborfonds.it/de/kollektivvertraege"
    st.markdown("Per informazioni sui contratti collettivi, clicca qui: [Contratti Collettivi Laborfonds](%s)" % url_kv)

    st.subheader("TFR")
    st.markdown("Il TFR corrisponde al 6.91% dello stipendio lordo e viene versato aggiuntivamente.")
    tfr = st.number_input(
    "Determina la quota del TFR che vuole versare (%).",
    value = float(100),
    step = float(10),
    min_value=float(0),
    max_value=float(100),
    format='%.0f'
    )

    st.markdown("In caso la prima occupazione è avvenuta dopo il 28.04.1993, generalmente è previsto il versamento del 100% del trattamento di fine rapporto. Tuttavia, questo può variare nei diversi contratti collettivi applicati. Questa informazione deve essere ricavata dal proprio contratto collettivo specifico.")


    # Determine the start year based on the fund_name
    start_year = int(2000) if fund_name == "LB_BIL" else int(2008)



    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  # Adds 100px of space




    st.subheader("3° Passo: Determinare il punto di inizio del versamento")
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
        jahr = st.slider('Anno di inizio dei versamenti', start_year, int(2023), int(2010), format='%.0f', step=int(1))



    st.markdown("Le contribuzioni iniziano nel primo mese del rispettivo trimestre.")  # Adds 100px of space




    excel_path = 'https://raw.githubusercontent.com/Schesch/pension_calculator/main/data/Laborfond.xlsx'

    # Read Excel file
    df = pd.read_excel(excel_path, sheet_name=fund_name)

    tfr_beitrag = round((income) * 0.0691 * (tfr/100) / 4,1)
    einzahlung = round((income * ((an_beitrag/100) + (ag_beitrag/100))) / 4 + tfr_beitrag,1)
    einkommen = f"{round(income, 1):,}"


    try:
        start_idx = df[(df['Quartal'] == quartal) & (df['Jahr'] == jahr)].index[0]
        df_filtered = df.iloc[start_idx:]
        st.subheader("Selezione dei parametri")
        st.markdown(
            f"""
    Ha selezionato i seguenti parametri per la calcolazione:
    * **Linea di investimento**: {line}
    * Reddito al primo anno: {einkommen}€
    * Contributo del lavoratore: {an_beitrag}%
    * Contributo del datore di lavoro: {ag_beitrag}%
    * Versamento del TFR trimestrale iniziale: {tfr_beitrag}€
    * **Versamento totale** trimestrale iniziale: {einzahlung}€
    * Primo trimestre di versamento: {quartal}
    * Primo anno di versamento: {jahr}
            """
        )
    except IndexError:
        st.subheader("Il calcolo non può essere eseguito")
        st.markdown(
            """
    La calcolazione non può essere avviata al momento da lei indicato, poiché i dati non sono disponibili.
    Verifichi di aver scelto un punto di inizio valido.
    * Per la Linea Garantita: da Q1 2008
    * Per la Linea Bilanciata: da Q3 2000
    * Per la Linea Prudente Etica: da Q2 2008
    * Per la Linea Dinamica: da Q2 2008
            """
        )


    portfolio_value = 0
    total_contributions = 0
    shares_owned = 0
    portfolio_values = []
    dates = []
    inflation_rate = 0.02

    try:
        # Iterate through each row to calculate contributions and portfolio value
        for index, row in df_filtered.iterrows():
            # Check if a new year has started and update income accordingly
            if index > 0 and row['Quartal'] == "Q1":
                income *= (1 + inflation_rate)

            # Calculate TFR contribution based on the current income
            tfr_beitrag = round((income) * 0.0691 * (tfr / 100) / 4, 1)
            # Calculate total quarterly contribution based on the current income
            einzahlung = round((income * ((an_beitrag / 100) + (ag_beitrag / 100))) / 4 + tfr_beitrag, 1)

            # Contribution for this quarter
            contribution = einzahlung
            total_contributions += contribution
            nav_per_share = row['NAV']

            # Buy shares with the new contributions
            shares_bought = contribution / nav_per_share
            shares_owned += shares_bought

            # Update portfolio value to include new shares
            portfolio_value = shares_owned * nav_per_share

            # Record the portfolio value and corresponding date
            portfolio_values.append(portfolio_value)
            dates.append(row['Datum'])
        profit = portfolio_value - total_contributions
        profit_percent = (profit/total_contributions) * 100

        st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  # Adds 100px of space

        first_date = min(df_filtered["Datum"]).strftime("%d/%m/%Y")
        last_date = max(df_filtered["Datum"]).strftime("%d/%m/%Y")


        col1, col2 = st.columns(2)
        col1.metric("Contributi dal " + first_date + " al " + last_date, f"{round(total_contributions, 1):,}€")
        col2.metric("Valore del portafoglio al " + last_date, f"{round(portfolio_value, 1):,}€")

        col3, col4 = st.columns(2)
        col3.metric("Reddito al " + last_date, f"{round(profit, 1):,}€")
        col4.metric("Performance dal " + first_date + " al " + last_date, f"{round(profit_percent, 1):,}%")

        style_metric_cards()





        st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)  # Adds 100px of space



        plt.figure(figsize=(10, 5))
        plt.plot(dates, portfolio_values, marker='o', linestyle='-', markersize=3, color='blue')
        plt.title('Sviluppo della posizione totale nel corso del tempo')
        plt.xlabel('Periodo (Mese/Anno)', fontsize = 10)
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

        vertical_offset = 50  # Adjust this value as needed for appropriate spacing

        # Label the first and last points with their values, adding vertical_offset for spacing
        plt.text(dates[0], portfolio_values[0] + vertical_offset, f"{portfolio_values[0]:.0f}€", color="black", ha="center", va="bottom", fontsize="small")
        plt.text(dates[-1], portfolio_values[-1] + vertical_offset, f"{portfolio_values[-1]:.0f}€", color="black", ha="center", va="bottom", fontsize="small")

        # Enable grid lines on the y-axis only, with custom color and linewidth
        plt.grid(axis='y', color='#c7c3c3', linestyle='-', linewidth=0.7)
        plt.tight_layout()
        # Display the plot in Streamlit
        st.pyplot(plt)
    except NameError:
        st.markdown("")

    st.markdown(
        """Sviluppato da **Alex Laimer**  """
    )