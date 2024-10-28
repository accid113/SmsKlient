import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import tkinter as tk
import vonage
from tkinter import messagebox


# Funkcja do sprawdzenia, czy adres e-mail jest poprawny
def czy_poprawny_email(adres):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, adres) is not None


# Funkcja do sprawdzenia, czy numer telefonu ma 9 cyfr
def czy_poprawny_numer(numer):
    return numer.isdigit() and len(numer) == 9


# Funkcja do sprawdzenia, czy wartość jest liczbą zmiennoprzecinkową
def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# Funkcja do wysłania e-maila potwierdzającego
def wyslij_potwierdzenie_email(adres_potwierdzenia, address, keyword, tracking_link):
    if not czy_poprawny_email(adres_potwierdzenia):
        messagebox.showerror(title='ERROR!!!', message=f"Adres e-mail potwierdzenia {adres_potwierdzenia} jest nieprawidłowy.")
        sys.exit()

    smtp_server = ''
    smtp_port = 587
    smtp_user = ''
    smtp_password = ''

    msg = MIMEMultipart()
    msg['From'] = 'DotDesign <noreply@dotd.pl>'
    msg['To'] = adres_potwierdzenia
    msg['Subject'] = f'Potwierdzenie wysłania wiadomości na adres: {address}'

    msg.attach(MIMEText(f'''
        <p>Wiadomość została wysłana pomyślnie na adres: {address}<br>
           Wysłałeś maila o treści: {keyword}<br>
           Link do śledzenia: {tracking_link}
        </p>
       ''', 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, adres_potwierdzenia, msg.as_string())
        messagebox.showinfo(title='Sukces!', message=f'Wysłano potwierdzenie do: {adres_potwierdzenia}')
    except Exception as e:
        messagebox.showerror(title='ERROR!!!', message=f'Błąd podczas wysyłania potwierdzenia do {adres_potwierdzenia}: {str(e)}')


# Funkcja do wysłania wiadomości e-mail
def send_email(keyword, address, tracking_link, kwota_pobrania=None):
    if not czy_poprawny_email(address):
        messagebox.showerror(title='ERROR!!!', message=f"Skup się, to nie takie trudne :D, Adres e-mail {address} jest nieprawidłowy.")
        sys.exit()

    smtp_server = ''
    smtp_port = 587
    smtp_user = ''
    smtp_password = ''

    if keyword == 'drzwipobranie':
        if not is_float(kwota_pobrania):
            messagebox.showerror(title='ERROR!!!', message="Skup się, to nie takie trudne :D, Nie wpisałeś kwoty pobrania")
            sys.exit()
        body = f'''Szanowni Państwo,<br><br>
                Miło nam poinformować, że przewoźnik otrzymał zlecenie realizacji dostawy Państwa zamówienia.<br>
                Link do strony ze śledzeniem przesyłki: <a href="{tracking_link}">{tracking_link}</a><br><br>
                Dostawa odbędzie się za pobraniem, płatnym u kuriera, w dniu doręczenia. Kwota pobrania: {kwota_pobrania} zł<br>
                Prosimy o przygotowanie wyliczonej gotówki do zapłaty.<br><br>
                Proszę dokładnie obejrzeć karton z każdej strony celem wykrycia ewentualnych uszkodzeń przesyłki!<br>
                Następnie, należy sprawdzić zawartość przesyłki w obecności kuriera, a w razie wykrycia uszkodzeń - spisać protokół szkody!<br>
                Bez spisanego protokołu szkody reklamacje z powodu uszkodzenia nie będą uwzględniane!<br>
                Protokół szkody powinien być dostępny u kuriera, a jeśli kurier go nie posiada, protokół szkody znaleźć będzie można w kopercie z listem przewozowym znajdującej się na przesyłce!<br><br>
                W przypadku jakichkolwiek pytań lub wątpliwości zapraszamy do kontaktu:<br><br>
                Numer telefonu: 532 888 999<br>
                Adres e-mail: biuro@dotd.pl<br><br>
                Pozdrawiamy, DotDesign.<br><br>
                (wiadomość wygenerowana automatycznie, adres e-mail z którego wysłana została powyższa wiadomość nie jest obsługiwany)'''
        subject = '[DOTDESIGN] Informacje na temat wysyłki'
    elif keyword == 'drzwi':
        body = f'''Szanowni Państwo,<br><br>
                Miło nam poinformować, że przewoźnik otrzymał zlecenie realizacji dostawy Państwa zamówienia.<br>
                Link do strony ze śledzeniem przesyłki: <a href="{tracking_link}">{tracking_link}</a><br><br>
                Proszę dokładnie obejrzeć karton z każdej strony celem wykrycia ewentualnych uszkodzeń przesyłki!<br>
                Następnie, należy sprawdzić zawartość przesyłki w obecności kuriera, a w razie wykrycia uszkodzeń - spisać protokół szkody!<br>
                Bez spisanego protokołu szkody reklamacje z powodu uszkodzenia nie będą uwzględniane!<br>
                Protokół szkody powinien być dostępny u kuriera, a jeśli kurier go nie posiada, protokół szkody znaleźć będzie można w kopercie z listem przewozowym znajdującej się na przesyłce!<br><br>
                W przypadku jakichkolwiek pytań lub wątpliwości zapraszamy do kontaktu:<br><br>
                Numer telefonu: 532 888 999<br>
                Adres e-mail: biuro@dotd.pl<br><br>
                Pozdrawiamy, DotDesign.<br><br>
                (wiadomość wygenerowana automatycznie, adres e-mail z którego wysłana została powyższa wiadomość nie jest obsługiwany)'''
        subject = '[DOTDESIGN] Informacje na temat wysyłki'
    elif keyword == 'wniesieniepobranie':
        if not is_float(kwota_pobrania):
            messagebox.showerror(title='ERROR!!!', message="Skup się, to nie takie trudne :D, Nie wpisałeś kwoty pobrania")
            sys.exit()
        body = f'''Szanowni Państwo,<br><br>
                Miło nam poinformować, że przewoźnik otrzymał zlecenie realizacji dostawy Państwa zamówienia.<br>
                Link do strony ze śledzeniem przesyłki: <a href="{tracking_link}">{tracking_link}</a><br><br>
                Uprzejmie przypominamy, że do standardu dostawy wykupiona została dodatkowa usługa wniesienia i rozpakowania przesyłki przez kurierów.<br><br>
                Dostawa odbędzie się za pobraniem, płatnym u kuriera, w dniu doręczenia. Kwota pobrania: {kwota_pobrania} zł<br><br>
                Proszę dokładnie obejrzeć karton z każdej strony celem wykrycia ewentualnych uszkodzeń przesyłki!<br>
                Następnie, należy sprawdzić zawartość przesyłki w obecności kuriera, a w razie wykrycia uszkodzeń - spisać protokół szkody!<br>
                Bez spisanego protokołu szkody reklamacje z powodu uszkodzenia nie będą uwzględniane!<br>
                Protokół szkody powinien być dostępny u kuriera, a jeśli kurier go nie posiada, protokół szkody znaleźć będzie można w kopercie z listem przewozowym znajdującej się na przesyłce!<br><br>
                W przypadku jakichkolwiek pytań lub wątpliwości zapraszamy do kontaktu:<br><br>
                Numer telefonu: 532 888 999<br>
                Adres e-mail: biuro@dotd.pl<br><br>
                Pozdrawiamy, DotDesign.<br><br>
                (wiadomość wygenerowana automatycznie, adres e-mail z którego wysłana została powyższa wiadomość nie jest obsługiwany)'''
        subject = '[DOTDESIGN] Informacje na temat wysyłki'
    elif keyword == 'wniesienie':
        body = f'''Szanowni Państwo,<br><br>
                Miło nam poinformować, że przewoźnik otrzymał zlecenie realizacji dostawy Państwa zamówienia.<br>
                Link do strony ze śledzeniem przesyłki: <a href="{tracking_link}">{tracking_link}</a><br><br>
                Uprzejmie przypominamy, że do standardu dostawy wykupiona została dodatkowa usługa wniesienia i rozpakowania przesyłki przez kurierów.<br><br>
                Proszę dokładnie obejrzeć karton z każdej strony celem wykrycia ewentualnych uszkodzeń przesyłki!<br>
                Następnie, należy sprawdzić zawartość przesyłki w obecności kuriera, a w razie wykrycia uszkodzeń - spisać protokół szkody!<br>
                Bez spisanego protokołu szkody reklamacje z powodu uszkodzenia nie będą uwzględniane!<br>
                Protokół szkody powinien być dostępny u kuriera, a jeśli kurier go nie posiada, protokół szkody znaleźć będzie można w kopercie z listem przewozowym znajdującej się na przesyłce!<br><br>
                W przypadku jakichkolwiek pytań lub wątpliwości zapraszamy do kontaktu:<br><br>
                Numer telefonu: 532 888 999<br>
                Adres e-mail: biuro@dotd.pl<br><br>
                Pozdrawiamy, DotDesign.<br><br>
                (wiadomość wygenerowana automatycznie, adres e-mail z którego wysłana została powyższa wiadomość nie jest obsługiwany)'''
        subject = '[DOTDESIGN] Informacje na temat wysyłki'
    elif keyword == 'poczta':
        body = f'''Szanowni Państwo,<br><br>
                Miło nam poinformować, że przewoźnik otrzymał zlecenie realizacji dostawy Państwa zamówienia.<br>
                Link do strony ze śledzeniem przesyłki: <a href="{tracking_link}">{tracking_link}</a><br><br>
                Uprzejmie informujemy, że do zlecenia wykupiona została usługa sprawdzenia zawartości przesyłki przy kurierze.<br>
                Proszę dokładnie obejrzeć karton z każdej strony celem wykrycia ewentualnych uszkodzeń przesyłki!<br>
                Następnie, należy sprawdzić zawartość przesyłki w obecności kuriera, a w razie wykrycia uszkodzeń - spisać protokół szkody!<br>
                Bez spisanego protokołu szkody reklamacje z powodu uszkodzenia nie będą uwzględniane!<br>
                Protokół szkody powinien być dostępny u kuriera, a jeśli kurier go nie posiada, protokół szkody znaleźć będzie można w kopercie z listem przewozowym znajdującej się na przesyłce!<br><br>
                W przypadku jakichkolwiek pytań lub wątpliwości zapraszamy do kontaktu:<br><br>
                Numer telefonu: 532 888 999<br>
                Adres e-mail: biuro@dotd.pl<br><br>
                Pozdrawiamy, DotDesign.<br><br>
                (wiadomość wygenerowana automatycznie, adres e-mail z którego wysłana została powyższa wiadomość nie jest obsługiwany)'''
        subject = '[DOTDESIGN] Informacje na temat wysyłki'
    elif keyword == 'pocztapobranie':
        if not is_float(kwota_pobrania):
            messagebox.showerror(title='ERROR!!!', message="Skup się, to nie takie trudne :D, Nie wpisałeś kwoty pobrania")
            sys.exit()
        body = f'''Szanowni Państwo,<br><br>
                Miło nam poinformować, że przewoźnik otrzymał zlecenie realizacji dostawy Państwa zamówienia.<br>
                Link do strony ze śledzeniem przesyłki: <a href="{tracking_link}">{tracking_link}</a><br><br>
                Dostawa odbędzie się za pobraniem, płatnym u kuriera, w dniu doręczenia. Kwota pobrania: {kwota_pobrania} zł<br>
                Prosimy o przygotowanie wyliczonej gotówki do zapłaty.<br><br>
                Uprzejmie informujemy, że do zlecenia wykupiona została usługa sprawdzenia zawartości przesyłki przy kurierze.<br>
                Proszę dokładnie obejrzeć karton z każdej strony celem wykrycia ewentualnych uszkodzeń przesyłki!<br>
                Następnie, należy sprawdzić zawartość przesyłki w obecności kuriera, a w razie wykrycia uszkodzeń - spisać protokół szkody!<br>
                Bez spisanego protokołu szkody reklamacje z powodu uszkodzenia nie będą uwzględniane!<br>
                Protokół szkody powinien być dostępny u kuriera, a jeśli kurier go nie posiada, protokół szkody znaleźć będzie można w kopercie z listem przewozowym znajdującej się na przesyłce!<br><br>
                W przypadku jakichkolwiek pytań lub wątpliwości zapraszamy do kontaktu:<br><br>
                Numer telefonu: 532 888 999<br>
                Adres e-mail: biuro@dotd.pl<br><br>
                Pozdrawiamy, DotDesign.<br><br>
                (wiadomość wygenerowana automatycznie, adres e-mail z którego wysłana została powyższa wiadomość nie jest obsługiwany)'''
        subject = '[DOTDESIGN] Informacje na temat wysyłki'
    else:
        messagebox.showerror(title='ERROR!!!', message="Skup się, to nie takie trudne :D, błąd w słowie rodzaju dostawy")
        sys.exit()
    msg = MIMEMultipart()
    msg['From'] = 'DotDesign <noreply@dotd.pl>'
    msg['To'] = address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, address, msg.as_string())
        messagebox.showinfo(title='Sukces!', message=f'Wysłano do: {address}')
    except Exception as e:
        messagebox.showerror(title='ERROR!!!', message=f'Błąd podczas wysyłania e-maila do {address}: {str(e)}')


# Funkcja do wysłania wiadomości SMS
def send_sms(number, message):
    if not czy_poprawny_numer(number):
        messagebox.showerror(title='ERROR!!!', message=f"Numer telefonu {number} jest nieprawidłowy.")
        sys.exit()

    client = vonage.Client(key="", secret="")
    sms = vonage.Sms(client)
    responseData = sms.send_message(
        {
            "from": "DotDesign",
            "to": f"48{number}",
            "text": message,
        }
    )

    if responseData["messages"][0]["status"] == "0":
        messagebox.showinfo(title='Sukces!', message="Wiadomość SMS została wysłana pomyślnie.")
    else:
        messagebox.showerror(title='ERROR!!!', message=f"Błąd: {responseData['messages'][0]['error-text']}")


# Funkcja obsługująca przycisk wysyłania wiadomości e-mail i SMS
def on_send_all():
    keyword = keyword_entry.get()
    address = email_entry.get()
    number = phone_entry.get()
    tracking_link = tracking_link_entry.get()
    kwota_pobrania = kwota_entry.get() if keyword in ('drzwipobranie', 'wniesieniepobranie', 'pocztapobranie') else None
    adres_potwierdzenia = 'mn@dotd.pl'  # Stały adres e-mail do potwierdzeniamn
    numer_potwierdzenia = '532888999'  # Stały numer telefonu do potwierdzenia

    send_email(keyword, address, tracking_link, kwota_pobrania)
    wyslij_potwierdzenie_email(adres_potwierdzenia, address, keyword, tracking_link)
    send_sms(number, f'Witamy,\n'
                    f'Link do sledzenia przesylki: {tracking_link}\n'
                    f'Wiecej inf. w wiad. mailowej.\n'
                    f'Pozdrawiamy'),

    send_sms(numer_potwierdzenia,
             f'Potwierdzenie wyslania wiadomosci na nr: {number}')


# Tworzenie głównego okna GUI
root = tk.Tk()
root.title("Wysyłanie e-maili i SMS")

# Tworzenie i układanie widżetów GUI
tk.Label(root, text="Słowo kluczowe").grid(row=0, column=0)
keyword_entry = tk.Entry(root)
keyword_entry.grid(row=0, column=1)

tk.Label(root, text="Adres e-mail").grid(row=1, column=0)
email_entry = tk.Entry(root)
email_entry.grid(row=1, column=1)

tk.Label(root, text="Numer telefonu").grid(row=2, column=0)
phone_entry = tk.Entry(root)
phone_entry.grid(row=2, column=1)

tk.Label(root, text="Link do śledzenia").grid(row=3, column=0)
tracking_link_entry = tk.Entry(root)
tracking_link_entry.grid(row=3, column=1)

tk.Label(root, text="Kwota pobrania (opcjonalnie)").grid(row=4, column=0)
kwota_entry = tk.Entry(root)
kwota_entry.grid(row=4, column=1)

tk.Label(root, text="drzwi").grid(row=0, column=4)
tk.Label(root, text="drzwipobranie").grid(row=1, column=4)
tk.Label(root, text="poczta").grid(row=2, column=4)
tk.Label(root, text="pocztapobranie").grid(row=3, column=4)
tk.Label(root, text="wniesienie").grid(row=4, column=4)
tk.Label(root, text="wniesieniepobranie").grid(row=5, column=4)
tk.Label(root, text="             ").grid(row=6, column=3)
tk.Button(root, text="Wyślij wszystko", command=on_send_all).grid(row=5, column=0, columnspan=2)

# Uruchomienie głównej pętli GUI
root.mainloop()
