# -*- coding: utf-8 -*-
"""dataset_prepocesado.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/brainhack-school2023/hcgalvan_project/blob/main/src/dataset_prepocesado.ipynb

## Recorrer una carpeta y leer todos los archivos
"""

# importamos las librerias necesarias
import os
import pandas as pd

##############################################################################################################
# recorremos los archivos de la carpeta y los guardamos en una lista. Lo transpones y lo guardas en un dataframe.
# Luego concatenas todos los dataframes en uno solo y lo guardas en un csv.
# El csv resultante es el dataset que se usara para preprocesado posterior.
# carpeta ../data/datasets/Frontal_Aslant_Tract_L
##############################################################################################################
folder_paths = ['../data/datasets/Frontal_Aslant_Tract_L']

def read_txt_to_df(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    df = pd.DataFrame([data.split('\n')])
    return df

def transpose_df(df):
    return df.transpose()

df_list = []
for folder_path in folder_paths:
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            df = read_txt_to_df(file_path)
            
            df = transpose_df(df)
            df['N'] = file_name+"\t"+df.index.astype(str)
            df_list.append(df)

result = pd.concat(df_list)
result1 = result.apply(lambda x: pd.Series(x.dropna().values))
result1.to_csv('../data/dataset_fatl.csv', index=False)

##############################################################################################################
# recorremos los archivos de la carpeta y los guardamos en una lista. Lo transpones y lo guardas en un dataframe.
# Luego concatenas todos los dataframes en uno solo y lo guardas en un csv.
# El csv resultante es el dataset que se usara para preprocesado posterior.
# carpeta ../data/datasets/Frontal_Aslant_Tract_R
##############################################################################################################
folder_paths = ['../data/datasets/Frontal_Aslant_Tract_r']

def read_txt_to_df(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    df = pd.DataFrame([data.split('\n')])
    return df

def transpose_df(df):
    return df.transpose()

df_list = []
for folder_path in folder_paths:
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            df = read_txt_to_df(file_path)
            
            df = transpose_df(df)
            df['N'] = file_name+"\t"+df.index.astype(str)
            df_list.append(df)

result = pd.concat(df_list)
result1 = result.apply(lambda x: pd.Series(x.dropna().values))
result1.to_csv('../data/dataset_fatr.csv', index=False)

"""## Limpiar datos y ordenar en columnas"""

# levantamos los dataset y le agregamos la columna data y Label. Limpiamos los nombres de las columnas.
datasetfatl= pd.read_csv("../data/dataset_fatl.csv", delimiter=',', header=None, skiprows=1, names=['data','Label'])
datasetfatr= pd.read_csv("../data/dataset_fatr.csv", delimiter=',', header=None, skiprows=1, names=['data','Label'])

# verificacion de los dataset
datasetfatl

# dividimos la columna data en dos columnas, una con el codigo y otra con los valores.
datasetfatl[['Codigo','values']]= datasetfatl.data.str.split(pat='\t',expand=True)
datasetfatr[['Codigo','values']]= datasetfatr.data.str.split(pat='\t',expand=True)

# verificacion de los dataset
datasetfatl

# limpia valores nulos en la misma tabla
datasetfatl.dropna(inplace=True)
datasetfatr.dropna(inplace=True)

# verificacion de los dataset
datasetfatl.shape

# dividimos la columna Label en dos columnas, una con "Et" y otra con "id".
datasetfatl[['Et','id']]= datasetfatl.Label.str.split(pat='\t',expand=True)
datasetfatr[['Et','id']]= datasetfatr.Label.str.split(pat='\t',expand=True)

# verificacion de los dataset
datasetfatl.head()

# quitamos la columna Label y data de los dataset
datasetfatl.drop(columns = ['data', 'Label'], inplace=True) 
datasetfatr.drop(columns = ['data', 'Label'], inplace=True)

# verificacion de los dataset
datasetfatl.head()

# reindexamos las columnas "Et" de los dataset
datasetfatl.reindex(columns=['Et'])
datasetfatr.reindex(columns=['Et'])

# agregamos la columna "Ncodigo" a los dataset que es "codigo" con el prefijo "fatl_"
# la sigla "fatl" es por Frontal_Aslant_Tract_Left
datasetfatl['Ncodigo'] = 'fatl_'+datasetfatl['Codigo']

# agregamos la columna "Ncodigo" a los dataset que es "codigo" con el prefijo "fatl_"
# la sigla fatr es por Frontal Aslant Tract Right
datasetfatr['Ncodigo'] = 'fatr_'+datasetfatr['Codigo']

# concatenamos los dataset
subject = pd.concat([datasetfatl, datasetfatr])

# quitamos la columna "Codigo" de subject
subject.drop(columns = ['Codigo'], inplace=True)

# verificacion de subject
subject.head()

#utilizamos regex para dividir la columna Et a partir de encontrar _dwi que es elimnado
# y los dos grupos de datos se agrupan en las columnas cod y scrup

subject[['cod','scrup']]= subject['Et'].str.split(r'[\_]dwi', expand=True)

# verificacion de subject
subject.head()

# quitamos la columna Et y scrup de subject
subject.drop(columns = ['Et','scrup'], inplace=True)

# reindexamos la columna cod de subject
subject.reindex(columns=['cod'])

# verificacion de subject
subject.head()

# pivotamos la tabla subject para que los valores de la columna Ncodigo se conviertan en columnas
df = subject.pivot(index=['cod'], columns='Ncodigo', values='values').reset_index()

# verificacion de las columnas de df
df.columns

# renombramos las columnas de df para que no tengan espacios en blanco y se puedan utilizar en python
df.rename(columns={'fatr_area of end region 1(mm^2)' : 'fatr_area_of_end_region_1', 
                    'fatr_area of end region 2(mm^2)': 'fatr_area_of_end_region_2',
                    'fatr_branch volume(mm^3)' : 'fatr_branch_volume',
                    'fatr_fatr_curl' : 'fatr_curl',
                    'fatr_diameter(mm)' : 'fatr_diameter',
                    'fatr_dti_fa': 'fatr_dti_fa',
                    'fatr_elongation' : 'fatr_elongation',
                    'fatr_irregularity' : 'fatr_irregularity',
                    'fatr_irregularity of end region 1' : 'fatr_irregularity_of_end_region_1',
                    'fatr_irregularity of end region 2' : 'fatr_irregularity_of_end_region_2',
                    'fatr_iso' : 'fatr_iso',
                    'fatr_md' : 'fatr_md',
                    'fatr_mean length(mm)'  : 'fatr_mean_length',
                    'fatr_nrdi02L' : 'fatr_nrdi02L',
                    'fatr_nrdi04L' : 'fatr_nrdi04L',
                    'fatr_nrdi06L' : 'fatr_nrdi06L',
                    'fatr_number of tracts' : 'fatr_number_of_tracts',
                    'fatr_qa' : 'fatr_qa',
                    'fatr_radius of end region 1(mm)' : 'fatr_radius_of_end_region_1',
                    'fatr_radius of end region 2(mm)' : 'fatr_radius_of_end_region_2',
                    'fatr_rd' : 'fatr_rd',
                    'fatr_rdi' : 'fatr_rdi',
                    'fatr_span(mm)' : 'fatr_span',
                    'fatr_total area of end regions(mm^2)' : 'fatr_total_area_of_end_regions',
                    'fatr_total radius of end regions(mm)' : 'fatr_total_radius_of_end_regions', 
                    'fatr_total surface area(mm^2)' : 'fatr_total_surface_area',
                    'fatr_trunk volume(mm^3)' : 'fatr_trunk_volume',
                    'fatr_volume(mm^3)' : 'fatr_volume', 
                    'fatr_households': 'fatr_households',
                    'fatr_houses': 'fatr_houses',
                    'fatl_area of end region 1(mm^2)' : 'fatl_area_of_end_region_1', 
                    'fatl_area of end region 2(mm^2)': 'fatl_area_of_end_region_2',
                    'fatl_branch volume(mm^3)' : 'fatl_branch_volume',
                    'fatl_curl' : 'fatl_curl',
                    'fatl_diameter(mm)' : 'fatl_diameter',
                    'fatl_dti_fa': 'fatl_dti_fa',
                    'fatl_elongation' : 'fatl_elongation',
                    'fatl_irregularity' : 'fatl_irregularity',
                    'fatl_irregularity of end region 1' : 'fatl_irregularity_of_end_region_1',
                    'fatl_irregularity of end region 2' : 'fatl_irregularity_of_end_region_2',
                    'fatl_iso' : 'fatl_iso',
                    'fatl_md' : 'fatl_md',
                    'fatl_mean length(mm)'  : 'fatl_mean_length',
                    'fatl_nrdi02L' : 'fatl_nrdi02L',
                    'fatl_nrdi04L' : 'fatl_nrdi04L',
                    'fatl_nrdi06L' : 'fatl_nrdi06L',
                    'fatl_number of tracts' : 'fatl_number_of_tracts',
                    'fatl_qa' : 'fatl_qa',
                    'fatl_radius of end region 1(mm)' : 'fatl_radius_of_end_region_1',
                    'fatl_radius of end region 2(mm)' : 'fatl_radius_of_end_region_2',
                    'fatl_rd' : 'fatl_rd',
                    'fatl_rdi' : 'fatl_rdi',
                    'fatl_span(mm)' : 'fatl_span',
                    'fatl_total area of end regions(mm^2)' : 'fatl_total_area_of_end_regions',
                    'fatl_total radius of end regions(mm)' : 'fatl_total_radius_of_end_regions', 
                    'fatl_total surface area(mm^2)' : 'fatl_total_surface_area',
                    'fatl_trunk volume(mm^3)' : 'fatl_trunk_volume',
                    'fatl_volume(mm^3)' : 'fatl_volume', 
                    'fatl_households': 'fatl_households',
                    'fatl_houses': 'fatl_houses'}, inplace=True)

# verificacion df
df.head()

# verificacion de las columnas de df
df.shape

df.to_csv('../data/dataset_final.csv', index=False)