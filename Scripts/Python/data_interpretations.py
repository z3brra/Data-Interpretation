#! /usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Any
import numpy as np
import pymysql
import os
import platform
from sys import exit


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


DATABASE = {
    'host' : 'localhost',
    'user' : 'my_user',
    'passwd' : 'my_password',
    'db' : 'my_database', 
}
SUDO_PASSWORD = 'my_password'

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


def loop_on_query(column_name: str) -> list:
    database = connect_to_database()
    cursor = database.cursor()

    cursor.execute(f"SELECT {column_name} FROM filtred_data;")
    result = cursor.fetchall()

    sql_rows = [result[i][0] for i in range(cursor.rowcount)]
    
    cursor.close()
    database.close()
    return sql_rows[::-1]


def loop_on_error_value() -> list:
    database = connect_to_database()
    cursor = database.cursor()

    cursor.execute(f"SELECT upperwhisker FROM filtred_data;")
    result_upperwhisker = cursor.fetchall()

    cursor.execute("SELECT lowerwhisker FROM filtred_data;")
    result_lowerwhisker = cursor.fetchall()

    sql_rows = []
    for i in range(cursor.rowcount):
        tempo = [result_upperwhisker[i][0], result_lowerwhisker[i][0]]
        sql_rows.append(tempo)

    cursor.close()
    database.close()
    return sql_rows[::-1]


def plot_format(df: pd.core.frame.DataFrame, country_sum: list, error_value: list) -> Any:
    x = [i for i in range(9)]

    df.plot(width=0.5, kind='barh', stacked=True, zorder=2, figsize=(15, 10)).grid(axis='y', visible=None)

    #calacul la différence de la barre d'erreur par rapport à la longueur de la barre 
    #et transforme l'array dans une forme (2, N)
    err_vals = np.abs(np.asarray(error_value).T - country_sum[None])[::-1, :]

    plt.errorbar(country_sum, np.arange(df.shape[0]), xerr=err_vals, capsize=2, color="k", ls="none", label="95% confidence interval")
    plt.subplots_adjust(bottom=0.2, left=0.2)
    plt.axvline(x=2.43, label="Dystopia (hapiness=2.43)", c='black', zorder=0)

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
            fancybox=True, shadow=True, ncol=3)

    plt.xticks(x)
    return plt



def manager() -> None:
    country_id = loop_on_query("country_id")
    country_name = loop_on_query("country_name")

    data = {
        "Dystopia + residual": loop_on_query("dystopia_plus_residual"),
        "Explained by : Log GDP per Capita": loop_on_query("explained_by_log_gdp_per_capita"),
        "Explained by : Social Support": loop_on_query("explained_by_social_support"),
        "Explained by : Healthy life expectancy": loop_on_query("explained_by_healthy_life_expectancy"),
        "Explained by : Freedom to make life choices": loop_on_query("explained_by_freedom_to_make_life_choices"),
        "Explained by : Generosity": loop_on_query("explained_by_generosity"),
        "Explained by : Perceptions of corruption": loop_on_query("explained_by_perceptions_of_corruption"),
    }
    error_value = loop_on_error_value()
    df = pd.DataFrame(data, index=country_name)

    country_sum = df.sum(axis=1).values

    country_name = [f"{country_id[i]}.{country_name[i]} ({round(country_sum[i], 3)})" for i,v in enumerate(country_name)]

    df = pd.DataFrame(data, index=country_name)

    plot_format(df[-53:], country_sum[-53:], error_value[-53:])
    plot_format(df[43:96], country_sum[43:96], error_value[43:96])
    plot_format(df[:-106], country_sum[:-106], error_value[:-106])
    plt.show()

if __name__ == '__main__':
    manager()
