import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pandas import DataFrame as DF
import json


def getDepartament(URL):
    r = requests.get(URL) 
    departaments_list = []
    soup = BeautifulSoup(r.text, 'lxml') 
    for i in range(47):
        table = soup.find('span', {'id' : 'formPrincipal:tabela:{}:codigoDepartamento'.format(i)})
        table2 = soup.find('a', {'href' : '#'})
        departaments_list.append(table.text)
    return departaments_list


def getHTMLContent(URL, departament):
    driver = webdriver.Firefox()
    driver.get(URL)
    elem = driver.find_element_by_xpath("//*[text()='{}']".format(departament))
    elem.click()
    URL = driver.current_url
    html_source = driver.page_source
    soup = BeautifulSoup(html_source,'lxml')
    driver.quit()
    return (soup)

def getFieldList(html_content, departament, field):
    i = 0
    field_list = []
    while(i >= 0):
        for row in html_content.find_all('table', {'id' : 'formPrincipal:tabela'} ):
            if(row.find('span', {'id' : 'formPrincipal:tabela:{}:{}'.format(i, field)}) is None):
                i = -2
            else:
                field_string = row.find('span', {'id' : 'formPrincipal:tabela:{}:{}'.format(i, field)}).text
                field_list.append(field_string)
        i = i +1
    return(field_list)


URL = "https://zeppelin10.ufop.br/HorarioAulas/"
departaments_list = getDepartament(URL)
for departament in departaments_list:
    print(departament)
    html_content = getHTMLContent(URL, departament)
    columns_list = ['disciplina',
    'codigo',
    'modalidade',
    'turma',
    'horario',
    'vagas',
    'matriculados',
    'professores',
    'predio',
    'idioma',
    'reserva']
    columns_dict = {}
    departament_list = []
    for column_name in columns_list:
        field = getFieldList(html_content, departament, column_name)
        print(column_name)
        print(len(field))
        columns_dict[column_name] = field
    for i in range(len(field)):
        departament_list.append(departament)
    print('departamento')
    print(len(departament_list))
    columns_dict['departamento'] = departament_list
    columns_list.append('departamento')
    df = DF(columns_dict, columns = columns_list)
    path = "disciplinas/" +departament+".csv"
    print(path)
    df.to_csv(path, index = None, header = True)
    print(departament,"fininsh, go next")
    print("--------------------------------------------------")