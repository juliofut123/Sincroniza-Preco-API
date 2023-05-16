import requests
from configparser import ConfigParser
import xml.etree.ElementTree as ET
import urllib.parse

#Diretorio arquivo de dados e XML
dirDados = "C:\\Bancamais\\Fastcommerce\\DadosLoja"

#Administração do arquivo .cfg
config_object = ConfigParser()
config_object.read(f"{dirDados}\\StoreData.cfg")
STOREINFO = config_object["STOREINFO"]
StoreName = STOREINFO["StoreName"]
StoreID = STOREINFO["StoreID"]
Username = STOREINFO["Username"]
password = STOREINFO["password"]

#Armazena na variavel file1 o conteúdo do arquivo estoqueB+.txt
with open("C:\\Bancamais\\Fastcommerce\\ProgramasExtras\\Sincronizações\\Sincroniza-Preço\\syncPreco.txt") as t1:
    file1 = t1.readlines()
    t1.close()

#Cria um dicionário que armazena como keys as ids e como value as quantidades do arquivo Input1B+.txt
dict1 = {}
for line in file1:
    dict1[line[0:7].strip()] = line[7:].strip()

#Formatação do arquivo XML
root = ET.Element("Records")

for key, value in dict1.items():
    record = ET.SubElement(root, "Record")
    comando = ET.SubElement(record, "Field", {"Name": "Comando", "Value": "A"})
    id_produto = ET.SubElement(record, "Field", {"Name": "IDProduto", "Value": key})
    estoque = ET.SubElement(record, "Field", {"Name": "Preco", "Value": value})
    change_flag_prod_api = ET.SubElement(record, "Field", {"Name": "ChangeFlagProdAPI", "Value": "0"})

xml_doc = ET.tostring(root, encoding="utf-8")

#Codificar XML para a URL
xmlrecord = urllib.parse.quote(xml_doc)

#Request
url = "https://www.rumo.com.br/sistema/adm/APILogon.asp"
payload= (f"""StoreName={StoreName}&StoreID={StoreID}&Username={Username}&
          method=ProductManagement&password={password}&XMLRecords={xmlrecord}""")
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

response = requests.request("POST", url, headers=headers, data=payload)

resposta = response.text


if (response.text.find("<ErrCod>0")) == -1:
    with open("C:\\Bancamais\\Fastcommerce\\ProgramasExtras\\Sincronizações\\Sincroniza-Preço\\Erro.txt", "w+") as e:
        e.write("Houve um erro ao checar os IDs.")
        e.write("\n")
        e.write(response.text)
        e.close()
