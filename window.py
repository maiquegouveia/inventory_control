import datetime
from tkinter import *

######## funcionalidades do sistema #############
import pyodbc

database = f"codigo\janela\Estoque.db"
connection_info = ("Driver=SQLite3 ODBC Driver;Server=localhost;Database={}".format(database))
connection = pyodbc.connect(connection_info)
cursor = connection.cursor()

def validar_data(data):
    try:
        dataObj = datetime.datetime.strptime(data, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
def adicionar_insumo():
    if len(nome_insumo.get()) < 2 or len(qtde_insumo.get()) < 1 or len(data_insumo.get()) < 1 or len(lote_insumo.get()) < 1:
        caixa_texto.delete("1.0", END)
        caixa_texto.insert("1.0", "Preencha todos os campos para adicionar um produto!")
        return
    else:
        if not validar_data(data_insumo.get()):
            caixa_texto.delete("1.0", END)
            caixa_texto.insert("1.0", "Preencha uma data válida para adicionar um produto!")
            return
        
    cursor.execute(f'''
    INSERT INTO Estoque (Produto, Quantidade, DataValidade, Lote)
    VALUES
    ("{nome_insumo.get()}", "{qtde_insumo.get()}", "{data_insumo.get()}", "{lote_insumo.get()}")
    ''')
    cursor.commit()
    caixa_texto.delete("1.0", END)
    caixa_texto.insert("1.0", f"{nome_insumo.get()} adicionado com sucesso!")
    
def deletar_insumo():
    if len(nome_insumo.get()) < 2 or len(lote_insumo.get()) < 1:
        caixa_texto.delete("1.0", END)
        caixa_texto.insert("1.0", "Preencha o nome e o lote do produto!")
        return
    else:
        cursor.execute(f'''
        SELECT * FROM Estoque
        WHERE Produto="{nome_insumo.get()}"
        AND Lote={lote_insumo.get()}
        ''')
        if not cursor.fetchone():
            caixa_texto.delete("1.0", END)
            caixa_texto.insert("1.0", "Produto não encontrado no estoque!")
            return

    cursor.execute(f'''
    DELETE FROM Estoque
    WHERE Produto="{nome_insumo.get()}"
    ''')
    cursor.commit()
    caixa_texto.delete("1.0", END)
    caixa_texto.insert("1.0", f"{nome_insumo.get()} deletado do estoque.")

def consumir_insumo():
    if len(nome_insumo.get()) < 2 or len(lote_insumo.get()) < 1 or len(qtde_insumo.get()) < 1:
        caixa_texto.delete("1.0", END)
        caixa_texto.insert("1.0", "Preencha os campos de nome, lote e quantidade!")
        return
    else:
        cursor.execute(f'''
        SELECT * FROM Estoque
        WHERE Produto="{nome_insumo.get()}"
        AND Lote={lote_insumo.get()}
        ''')
        if not cursor.fetchone():
            caixa_texto.delete("1.0", END)
            caixa_texto.insert("1.0", "Produto não encontrado no estoque!")
            return
        
    cursor.execute(f'''
    UPDATE Estoque
    SET Quantidade=Quantidade-{qtde_insumo.get()}
    WHERE Produto="{nome_insumo.get()}"
    AND Lote={lote_insumo.get()}
    ''')
    cursor.commit()
    # Deletar tudo da caixa de texto
    caixa_texto.delete("1.0", END)
    # Escrever na caixa de texo
    caixa_texto.insert("1.0", f"{nome_insumo.get()} foi consumido em {qtde_insumo.get()} unidades.")


def visualizar_insumo():
    if len(nome_insumo.get()) < 2 or len(lote_insumo.get()) < 1:
        caixa_texto.delete("1.0", END)
        caixa_texto.insert("1.0", "Preencha o nome e o lote do produto para visualizar!")
        return
    else:
        cursor.execute(f'''
        SELECT * FROM Estoque
        WHERE Produto="{nome_insumo.get()}"
        AND Lote={lote_insumo.get()}
        ''')
        if not cursor.fetchone():
            caixa_texto.delete("1.0", END)
            caixa_texto.insert("1.0", "Produto não encontrado no estoque!")
            return
        
    cursor.execute(f'''
    SELECT * FROM Estoque
    WHERE Produto="{nome_insumo.get()}"
    AND Lote={lote_insumo.get()}
    ''')
    produto = cursor.fetchone()
    caixa_texto.delete("1.0", END)
    caixa_texto.insert("1.0", f"O produto {produto[1]} do lote {produto[4]} tem {produto[2]} unidades em estoque com validade até {produto[3]}.")
    
    
######### criação da Janela ##################
    
window = Tk()

window.geometry("711x646")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 646,
    width = 711,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"codigo/janela/background.png")
background = canvas.create_image(
    355.5, 323.0,
    image=background_img)

img0 = PhotoImage(file = f"codigo/janela/img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = visualizar_insumo,
    relief = "flat")

b0.place(
    x = 479, y = 195,
    width = 178,
    height = 38)

img1 = PhotoImage(file = f"codigo/janela/img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = deletar_insumo,
    relief = "flat")

b1.place(
    x = 247, y = 197,
    width = 178,
    height = 36)

img2 = PhotoImage(file = f"codigo/janela/img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = consumir_insumo,
    relief = "flat")

b2.place(
    x = 479, y = 123,
    width = 178,
    height = 35)

img3 = PhotoImage(file = f"codigo/janela/img3.png")
b3 = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = adicionar_insumo,
    relief = "flat")

b3.place(
    x = 247, y = 125,
    width = 178,
    height = 34)

entry0_img = PhotoImage(file = f"codigo/janela/img_textBox0.png")
entry0_bg = canvas.create_image(
    455.0, 560.0,
    image = entry0_img)

caixa_texto = Text(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

caixa_texto.place(
    x = 250, y = 502,
    width = 410,
    height = 114)

entry1_img = PhotoImage(file = f"codigo/janela/img_textBox1.png")
entry1_bg = canvas.create_image(
    517.0, 294.5,
    image = entry1_img)

nome_insumo = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

nome_insumo.place(
    x = 377, y = 278,
    width = 280,
    height = 31)

entry2_img = PhotoImage(file = f"codigo/janela/img_textBox2.png")
entry2_bg = canvas.create_image(
    517.0, 340.5,
    image = entry2_img)

data_insumo = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

data_insumo.place(
    x = 377, y = 324,
    width = 280,
    height = 31)

entry3_img = PhotoImage(file = f"codigo/janela/img_textBox3.png")
entry3_bg = canvas.create_image(
    517.0, 388.5,
    image = entry3_img)

lote_insumo = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

lote_insumo.place(
    x = 377, y = 372,
    width = 280,
    height = 31)

entry4_img = PhotoImage(file = f"codigo/janela/img_textBox4.png")
entry4_bg = canvas.create_image(
    517.0, 436.5,
    image = entry4_img)

qtde_insumo = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

qtde_insumo.place(
    x = 377, y = 420,
    width = 280,
    height = 31)

window.resizable(False, False)
window.mainloop()
cursor.close()
connection.close()