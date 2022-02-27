#! /usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
import xlrd
import platform
import os
from sys import exit
from typing import Any

"""
Cette "constante" de dictionnaire permet de modifier facilement les information de la base de données
tel que l'utilisateur ou le mot de passe ou le nom de la base à utiliser, ainsi que l'host           
"""
DATABASE = {
    'host' : 'localhost',
    'user' : 'zebrra',
    'passwd' : 'cba9bc67810',
    'db' : 'data_for_figure', 
}
# Même principe pour le fichier xls
XLS = {
    'filename' : '../../DataForFigure2.1WHR2021_1.xls'
}

SUDO_PASSWORD = 'cba9bc67810'

def connect_to_database() -> object:
    """Connexion à une base MySQL avec une gestion d'erreur."""
    try:
        database = pymysql.connect(**DATABASE) # **DATABASE permet de transformer les key, value du dict en kwargs.
        return database
    except Exception as e:
        print(f"Erreur lors de la connection à la base de données :\nCode d'erreur : {e.args[0]}\nErreur : {e.args[1]}")
        if e.args[0] == 2003:
            if platform.system().lower() == 'linux':
                print("Tentative de connexion à la base de données en cours....\n")
                command = 'service mysql start'
                os.system(f"echo {SUDO_PASSWORD}|sudo -S {command}")
                return connect_to_database()
        exit(1)


def open_xls_sheet() -> object:
    """Ouverture d'un fichier xls avec une gestion d'erreur."""
    try:
        excel_sheet = xlrd.open_workbook(**XLS)
        return excel_sheet
    except Exception as e:
        print(f"Erreur lors de l'ouverture du fichier xls :\nErreur : {e}")
        exit(1)

def transfert_data() -> Any:
    database = connect_to_database()
    cursor = database.cursor()

    excel_sheet = open_xls_sheet()
    sheet_name = excel_sheet.sheet_names()

    for sh in range(0, len(sheet_name)):
        sheet = excel_sheet.sheet_by_index(sh)

        for r in range(1, sheet.nrows):
            insert_query = """INSERT INTO filtred_data (
                country_name,
                regional_indicator,
                ladder_score,
                standard_error_of_ladder_score,
                upperwhisker,
                lowerwhisker,
                logged_gdp_per_capita,
                social_support,
                healthy_life_expectancy,
                freedom_to_make_life_choices,
                generosity,
                perceptions_of_corruption,
                ladder_score_in_dystopia,
                explained_by_log_gdp_per_capita,
                explained_by_social_support,
                explained_by_healthy_life_expectancy,
                explained_by_freedom_to_make_life_choices,
                explained_by_generosity,
                explained_by_perceptions_of_corruption,
                dystopia_plus_residual
            ) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"""\
                %(sheet.cell(r, 0).value,
                sheet.cell(r, 1).value,
                sheet.cell(r, 2).value,
                sheet.cell(r, 3).value,
                sheet.cell(r, 4).value,
                sheet.cell(r, 5).value,
                sheet.cell(r, 6).value,
                sheet.cell(r, 7).value,
                sheet.cell(r, 8).value,
                sheet.cell(r, 9).value,
                sheet.cell(r, 10).value,
                sheet.cell(r, 11).value,
                sheet.cell(r, 12).value,
                sheet.cell(r, 13).value,
                sheet.cell(r, 14).value,
                sheet.cell(r, 15).value,
                sheet.cell(r, 16).value,
                sheet.cell(r, 17).value,
                sheet.cell(r, 18).value,
                sheet.cell(r, 19).value
                )   
            cursor.execute(insert_query)
            database.commit()
    cursor.close()
    database.close()

if __name__ == '__main__':
    transfert_data()