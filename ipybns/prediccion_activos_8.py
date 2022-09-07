
import math as mt 
from numpy import random
import pandas as pd
import numpy as np
from statistics import mode 

lista_mapp = pd.read_csv('listas_top10_mapping.csv')
summary = pd.read_csv('act_summary29.csv',index_col=0)
gt_predict=  pd.read_csv('compounds30_ni_29.csv',index_col=0)
#filtro del sumary 
compounds_pred = gt_predict[gt_predict['cell_id'].isin(lista_mapp['cell_id'].tolist())]
#compounds_pred_sim = compounds_pred.drop_duplicates(subset=['compound_id','cell_id','active'], keep="first")

compuestos_val = compounds_pred.compound_id.unique()
lista_respuesta = []
lista_extendida = []



for comp in compuestos_val:
    #ahora necesitamos extrar las celulas que tienen interacciones con este compuesto
    cell_interact_compound = compounds_pred[compounds_pred['compound_id'].isin([comp])]
    #print(cell_interact_compound)
    lista_cell_interact_compound = cell_interact_compound['cell_id'].to_list()
    
    #Iteracion en el caso de que ese compuesto interactue con mas de una celula

    for index, cell_interact in cell_interact_compound.iterrows():
        #print(cell_interact['active'])
            
        df_cell_interact_top10 = lista_mapp[lista_mapp['cell_id'].isin([cell_interact['cell_id']])]
        #print(df_cell_interact_top10)
            
        lista_actividades=[]
        lista_cell =[]
        active_prediccion = 0
        cell_top10 =eval(df_cell_interact_top10['cell_top10'].tolist()[0])
        #print(cell_top10)
        for cell in cell_top10:
            cell_exist = summary[summary['cell_id'].isin([cell])]
            cell_exist1=cell_exist[cell_exist['compound_id'].isin([comp])]

            #En el caso de que alguna cell del top interactue con el compuesto
            if len(cell_exist1)>0:
                lista_actividades.append(cell_exist1['active'].values[0])
            else:
                lista_cell.append(cell)
        if len(lista_actividades)>1:
            #Generamos predicciones tanto para el  par compund- cell como para compound top10 
            #El valor de active sera el que tenga mayor repeticion en lista_actividades
            pred_a= lista_actividades.count(1)
            pred_i= lista_actividades.count(-1)
            if pred_a != pred_i :
                active_prediccion = mode(lista_actividades)
        #lista_respuesta.append([comp,cell_interact['cell_id'],cell,active_prediccion])
                lista_respuesta.append([comp,cell_interact['cell_id'],active_prediccion])
                #print([comp,cell_interact['cell_id'],cell_interact['cell_id'],active_prediccion])
                for cell in lista_cell:
                    #añade a la lista las recomendaciones que no existen
                    lista_extendida.append([comp,cell_interact['cell_id'],cell,active_prediccion])
                        #print([comp,cell_interact['cell_id'],cell,active_prediccion]



df_recomendacion = pd.DataFrame(lista_respuesta, columns =['compuesto','cell','active'])
df_recomendacion.to_csv('recomendaciones_top10.csv',index=0)

df_recomendacion_ext = pd.DataFrame(lista_extendida, columns =['compuesto','cell_interact','cell','active'])
df_recomendacion_ext.to_csv('recomendaciones_top10_ext.csv',index=0)