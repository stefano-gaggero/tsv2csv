Maggio 2018

Conversione file da Nanodrop TSV a CSV

In ingresso file TSV del nanodrop (IN_FILE_PATH) con lunghezze d'onda comprese nell'intervallo [FREQ_FROM, FREQ_TO]
Esegue un fit con una gaussiana nell'intervallo [FREQ_MIN, FREQ_MAX] per stabilire se è presente un picco di assorbimento
Dal fit viene calcolato sigma^2 
Se sigma^2<SIGMASQUARE_TRESHOLD si considera presente il picco di assorbimento
Visualizza grafici (dati + fit) e stampa i nomi dei campioni su cui è presente il picco
Crea in uscita un file CSV (OUT_FILE_PATH) in cui i campioni sono in colonne diverse
La prima riga del CSV contiene i valori di sigma^2
La seconda riga contiene un flag (0,1) che indica la presenza o meno del picco di assorbimento.
