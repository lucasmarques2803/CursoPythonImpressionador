import xmltodict
import os
import pandas as pd

def ler_xml_DANFE(nota: str):
    """Lê notas fiscais padrão DANFE em arquivos .xml

    Args:
        nota (str): caminho do arquivo da nota fiscal.

    Returns:
        dict[str, Any]: dicionário com as informações principais da nota fiscal
    """
    # abrir e ler o arquivo
    with open(nota, 'rb') as arquivo:
        documento = xmltodict.parse(arquivo)

    # valor_total, produtos/serviços (valores), cnpj_vendeu, nome_vendeu, cpf/cnpj_comprou, nome_comprou
    dic_notafiscal = documento['nfeProc']['NFe']['infNFe']
    valor_total = dic_notafiscal['total']['ICMSTot']['vNF']
    cnpj_vendeu = dic_notafiscal['emit']['CNPJ']
    nome_vendeu = dic_notafiscal['emit']['xNome']
    cpf_comprou = dic_notafiscal['dest']['CPF']
    nome_comprou = dic_notafiscal['dest']['xNome']
    produtos = dic_notafiscal['det']

    lista_produtos = []
    for produto in produtos:
        valor_produto = produto['prod']['vProd']
        nome_produto = produto['prod']['xProd']
        lista_produtos.append((nome_produto, valor_produto))

    resposta = {
        'valor_total': [valor_total], 
        'cnpj_vendeu': [cnpj_vendeu],
        'nome_vendeu': [nome_vendeu],
        'cpf_comprou': [cpf_comprou],
        'nome_comprou': [nome_comprou],
        'lista_produtos': [lista_produtos],
        }
    
    return resposta

def ler_xml_servico(nota: str):
    """Lê notas fiscais de serviço em arquivos .xml

    Args:
        nota (str): caminho do arquivo da nota fiscal.

    Returns:
        dict[str, Any]: dicionário com as informações principais da nota fiscal
    """

    # abrir e ler o arquivo
    with open(nota, 'rb') as arquivo:
        documento = xmltodict.parse(arquivo)

    # valor_total, produtos/serviços (valores), cnpj_vendeu, nome_vendeu, cpf/cnpj_comprou, nome_comprou
    dic_notafiscal = documento['ConsultarNfseResposta']['ListaNfse']['CompNfse']['Nfse']['InfNfse']
    valor_total = dic_notafiscal['Servico']['Valores']['ValorServicos']
    cnpj_vendeu = dic_notafiscal['PrestadorServico']['IdentificacaoPrestador']['Cnpj']
    nome_vendeu = dic_notafiscal['PrestadorServico']['RazaoSocial']
    cpf_comprou = dic_notafiscal['TomadorServico']['IdentificacaoTomador']['CpfCnpj']['Cnpj']
    nome_comprou = dic_notafiscal['TomadorServico']['RazaoSocial']
    produtos = dic_notafiscal['Servico']['Discriminacao']

    resposta = {
        'valor_total': valor_total, 
        'cnpj_vendeu': cnpj_vendeu,
        'nome_vendeu': nome_vendeu,
        'cpf_comprou': cpf_comprou,
        'nome_comprou': nome_comprou,
        'lista_produtos': produtos,
        }
    
    return resposta

# Printando todos os arquivos
lista_arquivos = os.listdir('NFs finais')
for arquivo in lista_arquivos:
    if '.xml' in arquivo:
        if 'DANFE' in arquivo:
            print(ler_xml_DANFE(f'NFs finais/{arquivo}'))
        else:
            print(ler_xml_servico(f'Nfs finais/{arquivo}'))