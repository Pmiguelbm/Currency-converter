from requests import get
from PySimpleGUI import PySimpleGUI as sg

class ConversorMoeda:
    def __init__(self, api_chave):
        self.url_base = "https://api.freecurrencyapi.com"
        self.api_chave = api_chave
        self.moedas = self.pegar_moedas()
        self.moeda_transformada = {}

    def pegar_moedas(self):
        pontofinal = f"/v1/currencies?apikey={self.api_chave}"
        url = self.url_base + pontofinal
        data = get(url).json()["data"]
        data = list(data.values())
        return data

    def mostrar_moedas(self):
        moedas = []
        for moeda in self.moedas:
            name = moeda.get("name", "")
            symbol = moeda.get("symbol", "")
            code = moeda.get("code", "")
            moedas.append(f"{code} | {name} | {symbol}")
        return moedas

    def transformar_moeda(self, moeda_inicial, moeda_final):
        pontofinal = f"/v1/latest?apikey={self.api_chave}"
        parametros = f"&currencies={moeda_final}&base_currency={moeda_inicial}"
        url = self.url_base + pontofinal + parametros
        data = get(url).json()["data"]
        data = list(data.values())
        if len(data) == 0:
            return "Moeda Inválida"
        self.moeda_transformada[moeda_final] = data[0]
        return data[0]

    def multi_moeda(self, quantidade, moeda_inicial, moeda_final):
        taxa = self.moeda_transformada.get(moeda_final)
        if taxa is None:
            taxa = self.transformar_moeda(moeda_inicial, moeda_final)
            if taxa == "Moeda Inválida":
                return taxa

        resultado = quantidade * taxa
        return f"\n{quantidade} {moeda_inicial} = {resultado} {moeda_final}"


api_chave = '15Ks6VqRSayLieinS68hvjyMJDgImea9A6FiCr3R'
conversor = ConversorMoeda(api_chave)

sg.theme('LightGrey1')

layout = [
    [sg.Text('Moeda Base'), sg.Input(key='base3')],
    [sg.Text('Moeda para conversão'), sg.Input(key='conv2')],
    [sg.Text('Quantidade'), sg.Input(key='quant1')],
    [sg.Button('Converter')],
    [sg.Button('Mostrar moedas')]
]

# Janela
janela = sg.Window('Conversor de Moedas', layout)

# Ler os eventos
while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
    if eventos == 'Mostrar moedas':
        moedas = conversor.mostrar_moedas()
        sg.Popup("Todas as Moedas", '\n'.join(moedas))
    if eventos == 'Converter':
        qt = float(valores['quant1'])
        m1 = valores['base3'].upper()
        m2 = valores['conv2'].upper()
        resultado = conversor.multi_moeda(qt, m1, m2)
        sg.Popup("Conversão", resultado)