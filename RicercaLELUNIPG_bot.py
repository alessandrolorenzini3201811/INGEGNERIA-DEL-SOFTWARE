from telegram import *
from telegram.ext import Updater, CommandHandler,ConversationHandler, MessageHandler ,Filters
import datetime
import logging
import requests
from bs4 import BeautifulSoup
TOKEN='1924200564:AAGjge1g3EH5szTfLXZ9jYk2HJZ2fBEhNUk'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger("testlore")

ports = []
INPUT_TEXT = 0
a=1
updater = Updater(TOKEN, use_context=True)

dispatcher = updater.dispatcher



def lezioni(update,context):
    text =update.message.text
    if text == '/TORNA_MENU':
        update.message.reply_text('SEI NEL MENU')
        istruzioni(update,context)
        return ConversationHandler.END
    else:
        payload = {'query': text, 'submit': 'Cerca+link'}
        r = requests.post("https://www.unistudium.unipg.it/cercacorso.php/post?p=0", data=payload)
        text=update['message']['text']
        html_text = r.text
        #print(r.text)
        soup = BeautifulSoup(html_text, 'html.parser')
        rows = soup.find_all('tr')[1:]
        for row in rows:
            columns = row.find_all('td')
            datas = []
            for column in columns:
                if 'link al meeting' in column.get_text().casefold():
                    datas.append(column.a.get('href'))
                else:
                    datas.append(column.get_text())
            teaching_name, teachers, degree_course, teams_link = datas
            update.message.reply_text(f'NOME: {teaching_name}\nPROFESSORE: {teachers}\nCORSO DI LAUREA: {degree_course}\nLINK: {teams_link}')

def esami(update,context):
    text =update.message.text
    if text == '/TORNA_MENU':
        update.message.reply_text('SEI NEL MENU')
        istruzioni(update,context)
        return ConversationHandler.END
    else:
        payload = {'query': text, 'submit': 'Cerca+link'}
        r = requests.post("https://www.unistudium.unipg.it/cercacorso.php?p=1", data=payload)
        text=update['message']['text']
        html_text = r.text
        soup = BeautifulSoup(html_text, 'html.parser')
        rows = soup.find_all('tr')[1:]
        for row in rows:
            columns = row.find_all('td')
            datasi = []
            for column in columns:
                if 'link aula virtuale' in column.get_text().casefold():
                    datasi.append(column.a.get('href'))
                else:
                    datasi.append(column.get_text())
            teaching_name , teachers, degree_course, data ,teams_link = datasi
            update.message.reply_text(f'NOME: {teaching_name}\nPROFESSORE: {teachers}\nCORSO DI LAUREA: {degree_course}\nDATA E ORA:{data}\nLINK: {teams_link}')




def lauree(update,context):
    text =update.message.text
    if text == '/TORNA_MENU':
        update.message.reply_text('SEI NEL MENU\n')
        istruzioni(update,context)
        return ConversationHandler.END
    else:
        payload = {'query': text, 'submit': 'Cerca+link'}
        r = requests.post("https://www.unistudium.unipg.it/cercacorso.php?p=245", data=payload)
        text=update['message']['text']
        html_text = r.text
        print(r.text)
        soup = BeautifulSoup(html_text, 'html.parser')
        rows = soup.find_all('tr')[1:]
        for row in rows:
                columns = row.find_all('td')
                datas = []
                for column in columns:
                    if 'link al meeting' in column.get_text().casefold():
                        datas.append(column.a.get('href'))
                    else:
                        datas.append(column.get_text())
                teaching_name, teachers, degree_course, teams_link = datas
                update.message.reply_text(f'NOME: {teaching_name}\nPROFESSORE: {teachers}\nCORSO DI LAUREA: {degree_course}\nLINK: {teams_link}')
        #print(teams_link)
        rowsa = soup.find_all('br')[1:]
        for righe in rowsa :
            colonne =righe.find_all('br')
            for colenni in colonne:
                if '0 risultati'in colenni.get_text().casefold():
                    update.message.reply_text('0 RISULTATI')
                    return



def istruzioni(update,context):
    update.message.reply_text('ISTRUZIONI \n DIGITARE "/CERCA_LEZIONI" PER ACCEDERE ALLA RICERCA DELLE LEZIONI \n DIGITARE "/CERCA_ESAMI" PER ACCEDERE ALLA RICERCA DEGLI ESAMI \n DIGITARE "/CERCA_LAUREE" PER ACCEDERE ALLA RICERCA DELLE LAUREE \n DIGIRA "/TORNA_MENU" PER TORNARE NEL MENU" DI RICERCA  ')

def prelezioni(update,context):
    update.message.reply_text('SEI NELLA SEZIONI LEZIONI -->digita il nome del professore o della materia')
    return INPUT_TEXT

def preesami(update,context):
    update.message.reply_text('SEI NELLA SEZIONI ESAMI -->digita il nome del professore o della materia')
    return INPUT_TEXT

def prelauree(update,context):
    update.message.reply_text('SEI NELLA SEZIONI LAUREE -->Digitare nome del Corso di Studi e/o nome del Dipartimento')
    return INPUT_TEXT

def main():
    dispatcher.add_handler(CommandHandler('istruzioni',istruzioni))
    dispatcher.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('CERCA_LEZIONI',prelezioni)
            ],
            states={
                INPUT_TEXT:[MessageHandler(Filters.text,lezioni)]
            },
            fallbacks=[]
            )
            )
    dispatcher.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('CERCA_ESAMI',preesami)
            ],
            states={
                INPUT_TEXT:[MessageHandler(Filters.text,esami)]
            },
            fallbacks=[]
            ))
    dispatcher.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('CERCA_LAUREE',prelauree)
            ],
            states={
                INPUT_TEXT:[MessageHandler(Filters.text,lauree)]
            },
            fallbacks=[]
            ))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
