import tkinter as tk
from tkinter import messagebox, scrolledtext
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Função para adicionar mensagens ao log (apenas sucesso ou erro)
# A função recebe uma mensagem e a exibe no campo de log da interface.
def add_log(message):
    """
    Adiciona uma mensagem ao log na interface gráfica.
    
    Parâmetros:
    - message (str): A mensagem a ser exibida no log.
    """
    log_text.config(state="normal")  # Habilita a edição para adicionar texto
    log_text.insert(tk.END, message + "\n")  # Adiciona a mensagem ao final
    log_text.config(state="disabled")  # Desativa a edição após adicionar texto
    log_text.see(tk.END)  # Mantém o scroll no final do log

# Inicializa o WebDriver globalmente
driver = None

# Função para iniciar o driver do Selenium (Chrome WebDriver)
# Inicializa o navegador e abre o WhatsApp Web. Exibe uma caixa de mensagem para o usuário escanear o QR code.
def iniciar_driver():
    """
    Inicializa o WebDriver e abre o WhatsApp Web.
    Solicita ao usuário que escaneie o QR code para autenticação.
    """
    global driver
    if driver is None:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("https://web.whatsapp.com")
        messagebox.showinfo("QR Code", "Escaneie o QR code no WhatsApp Web e clique em OK para continuar.")

# Função para enviar mensagens via WhatsApp Web
# A função localiza o campo de pesquisa do WhatsApp, seleciona o contato e envia a mensagem.
def enviar_mensagem_whatsapp(nome_contato, mensagem):
    """
    Envia uma mensagem para um contato específico no WhatsApp Web.
    
    Parâmetros:
    - nome_contato (str): O nome do contato ou grupo para o qual a mensagem será enviada.
    - mensagem (str): O conteúdo da mensagem a ser enviada.
    """
    try:
        # Localiza a caixa de pesquisa e envia o nome do contato
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.clear()
        search_box.send_keys(nome_contato)
        time.sleep(2)
        search_box.send_keys(Keys.ENTER)

        # Localiza a caixa de mensagem e envia a mensagem
        message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        message_box.send_keys(mensagem)
        message_box.send_keys(Keys.ENTER)

        # Adiciona log de sucesso
        add_log(f"✅ Mensagem enviada para: {nome_contato}")
        time.sleep(2)
    except Exception as e:
        # Caso ocorra um erro, adiciona log de erro
        add_log(f"❌ Erro ao enviar para {nome_contato}: {e}")

# Função para enviar mensagens imediatamente
# Esta função obtém os contatos e a mensagem inseridos na interface gráfica e os envia.
def enviar_mensagens():
    """
    Envia mensagens para uma lista de contatos, conforme os valores inseridos na interface gráfica.
    """
    global driver
    # Obtém os contatos da entrada de texto, separados por vírgula
    contatos = entry_contatos.get().split(",")
    contatos = [contato.strip() for contato in contatos]  # Remove espaços extras
    # Obtém a mensagem inserida no campo de texto
    mensagem = entry_mensagem.get("1.0", tk.END).strip()

    # Verifica se os campos estão preenchidos
    if not contatos or not mensagem:
        messagebox.showwarning("Atenção", "Preencha os contatos e a mensagem antes de enviar.")
        return

    # Se o driver não estiver iniciado, inicializa
    if driver is None:
        iniciar_driver()
    
    # Envia a mensagem para cada contato
    for contato in contatos:
        enviar_mensagem_whatsapp(contato, mensagem)

# Criando a Interface Tkinter
root = tk.Tk()
root.title("WhatsApp Sender 🚀")  # Título da janela
root.geometry("500x500")  # Definição do tamanho da janela
root.configure(bg="#E3F2FD")  # Cor de fundo da janela

# Frame principal da interface
frame = tk.Frame(root, bg="white", bd=2, relief="flat")
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Título da aplicação
title_label = tk.Label(frame, text="📩 Envio Automático de WhatsApp", bg="white", font=("Arial", 14, "bold"), fg="#0078D7")
title_label.pack(pady=10)

# Label e campo de entrada para os contatos
tk.Label(frame, text="📞 Contatos (separados por vírgula):", bg="white", font=("Arial", 11, "bold")).pack(pady=5)
entry_contatos = tk.Entry(frame, width=50, font=("Arial", 12), bd=1, relief="solid", justify="center")
entry_contatos.pack(pady=5, ipady=5)

# Label e campo de entrada para a mensagem
tk.Label(frame, text="✉️ Mensagem:", bg="white", font=("Arial", 11, "bold")).pack(pady=5)
entry_mensagem = tk.Text(frame, height=5, width=50, font=("Arial", 12), bd=1, relief="solid")
entry_mensagem.pack(pady=5)

# Botão para enviar as mensagens
btn_enviar = tk.Button(frame, text="📤 Enviar Mensagem", command=enviar_mensagens, font=("Arial", 12, "bold"), bg="#0078D7", fg="white", padx=10, pady=5, relief="flat", cursor="hand2")
btn_enviar.pack(pady=5)

# Label para o campo de log
tk.Label(frame, text="📜 Log:", bg="white", font=("Arial", 11, "bold")).pack(pady=5)

# Campo de log com rolagem para mostrar o histórico de envios
log_text = scrolledtext.ScrolledText(frame, height=8, width=60, font=("Courier", 10), bd=1, relief="solid", state="disabled")
log_text.pack(pady=5)

# Inicia o loop principal da interface gráfica
root.mainloop()
