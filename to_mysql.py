import os
import csv
import codecs
import pymysql


connection = pymysql.connect(
    host=HOST,
	user=USER,
	password=PASSWORD,
	db=DATABASE
	)

cursor = connection.cursor()

directory_str = "../data/"
for sub_dirs, dirs, files in os.walk(directory_str):
    for current_file in files:
        if current_file.endswith("csv"):
            file_path = directory_str + current_file
            table_name = current_file[:-4]

            if table_name =='Master':
                header = ['Year int', 'Team_Rank int','Team varchar(32)','Conf varchar(10)','Win_Loss varchar(10)','Eff_Margin float','Off_Eff float','Rank_Off_Eff int','Def_Eff float','Rank_Def_Eff int','Tempo float','Rank_Tempo int','Luck float','Rank_Luck int','SOS float','Rank_SOS int','Avg_Opp_Off_Eff float','Rank_Opp_Off_Eff int','Avg_Opp_Def_Eff float','Rank_Opp_Def_Eff int','Non_Conf_SOS float','Rank_NonConf_SOS int']
            elif table_name == 'Results':
                header = ['Year int', 'Day int', 'WinningID int', 'Winning_Score int', 'LosingID int', 'Losing_Score int', 'Winner_Location varchar(32)', 'Overtime int']
            elif table_name == 'Seeds':
                header = ['Year int', 'Seed varchar(6)', 'TeamID int']
            elif table_name == 'Slots':
                header = ['Year int', 'Slot varchar(6)', 'Strong_Seed varchar(6)', 'Weak_Seed varchar(6)']
            elif table_name == 'Teams':
                header = ['Team_ID int', 'Table_Name varchar(32)', 'FirstD1Season int', 'LastD1Season int']
            elif table_name == 'TeamSpellings':
                header = ['TeamSpelling varchar(32)', 'TeamID int']

            cursor.execute("SHOW TABLES LIKE '{}'".format(table_name))
            result = cursor.fetchone()
            print(result)
            if result == None:
                cursor.execute("CREATE TABLE {} ({})".format(table_name, ', '.join(header)))
                connection.commit()
            else:
                cursor.execute("DROP TABLE {}".format(table_name))
                cursor.execute("CREATE TABLE {} ({})".format(table_name, ', '.join(header)))
                connection.commit()

            with codecs.open(file_path, 'r',  encoding='utf-8', errors='ignore') as raw_file:
                open_csv = csv.reader(raw_file)
                columns = next(open_csv)

                for data in open_csv:
                    formatted_row=[]
                    for item in data:
                        if type(item) == str:
                            formatted_row.append('"' + item + '"')
                        else:
                            formatted_row.append(item)
                    query = 'insert into {} values ({})'.format(table_name, ', '.join(formatted_row))
                    cursor.execute(query)
                    print(query)
                connection.commit()
        else:
            continue