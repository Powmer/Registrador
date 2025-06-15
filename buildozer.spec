[app]

# (str) Título do seu app
title = JPPocket

# (str) Nome do pacote (tudo minúsculo, sem espaços)
package.name = jppocket

# (str) Nome do domínio reverso para seu app (pode ser qualquer coisa, só é identificador)
package.domain = org.jppocket

# (str) Nome do arquivo principal python do seu app
# Se seu arquivo principal for main.py, coloque main.py; se for jppocket.py, ajuste
source.main = main.py

# (list) Extensões dos arquivos a incluir no pacote (imagens, kv, planilhas etc)
source.include_exts = py,png,jpg,kv,xlsx

# (list) Diretórios ou arquivos extras a incluir (se tiver)
# source.include_patterns = assets/*,images/*.png

# (str) Lista de dependências Python que seu app usa
requirements = python3,kivy,openpyxl,pandas

# (str) Permissões Android necessárias para leitura e escrita em armazenamento
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (int) Versão do SDK mínimo (você pode deixar o padrão 21)
android.minapi = 21

# (int) Versão do SDK alvo
android.sdk = 33

# (str) Versão do NDK
android.ndk = 25b

# (str) Arquivo de ícone do app (coloque o seu ícone aqui, se quiser)
# icon.filename = %(source.dir)s/icon.png

# (str) Orientação da tela (portrait, landscape ou sensor)
orientation = portrait

# (bool) Se seu app usa a interface de tela cheia (sem status bar)
fullscreen = 0

# (str) Pacotes Java extra (geralmente vazio)
# android.add_jars =

# (list) Permite permissões extras
# android.permissions = INTERNET

# (bool) Ativa o log do python no Android (útil para debug)
log_level = 2

# (bool) Usa a flag debug para facilitar debug no dispositivo
# android.debug = 1

