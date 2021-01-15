#### Autor

Código criado e desenvolvido por Gustavo Eugênio para a disciplina Segurança e Auditoria de Sistemas ministrada pela professora Yeda Venturini no periodo letivo ENPE no 2o semestre de 2020.

#### Informações

Os códigos foram desenvolvido em python3, em teoria, todas os módulos utlizados são nativos para o Ubuntu 20, caso não estejam disponíveis por padrão, podem ser instaladas com o comando:
"pip3 install sys base64 datetime pkg_resources cryptography"

# Gerando a assinatura

obs: pode ser necessário alterar a permissão de execução do programa. utilize o comando "chmod +x nome_do_arquivo" pra tal.

executar o arquivo python3 no seguinte formato:

./sign "nome do arquivo" caminho_do_arquivo caminho_do_certificado senha

note que:
 - "nome do arquivo" é o nome desejado do documento após a decodificação
 - caminho_do_arquivo é o caminho, sendo absolutou ou relativo, do arquivo a ser codificado
 - caminho_do_certificado é o caminho, sendo absolutou ou relativo, do certificado p12
 - senha é a senha do certificado p12

## Funcionamento

O código implementado utilizada biblioteca 'cryptography' para fazer a leitura e interpretação do arquivo de certificado p12 e a biblioteca 'base64' para codificação/decodificação.

### Passos do algoritmo

  1) Importa bibliotecas e define constantes.
  2) Checa pelo número de correto de argumentos e extrai argumentos inseridos juntos ao comando de execução.
  3) Procura pelo arquivo no caminho absoluto ou relativo fornecido e salva seu conteudo.
  4) Checa pela possível existência de um cabeçalho, indicando que o arquivo já foi assinado.
  5) Procura pelo certificado p12, no caminho absoluto ou relativo fornecido, testa a senha e em caso de sucesso salva o conteudo do certificado.
  6) Extrai o Common Name do certificado para gravar posteriormente no cabeçalho.
  7) Formata String para uso como base para no cabeçalho.
  8) Codifica o arquivo e assinatura em base64 para posteriormente salvar no cabeçalho.
  9) Preenche o cabeçalho e sobrescreve um novo arquivo de texto com o nome informado.

# Verificando a assinatura

obs: pode ser necessário alterar a permissão de execução do programa. utilize o comando "chmod +x nome_do_arquivo" pra tal.

executar o arquivo python3 no seguinte formato:

./validate caminho_do_arquivo caminho_do_certificado

note que:
 - caminho_do_arquivo é o caminho, sendo absolutou ou relativo, do arquivo de texto a ser decodificado
 - caminho_do_certificado é o caminho, sendo absolutou ou relativo, do certificado crt utilizado para verificar a assinatura

## Funcionamento

O código implementado utilizada biblioteca 'cryptography' para fazer a leitura e interpretação do arquivo de certificado DER, a biblioteca 'base64' para codificação/decodificação e a biblioteca 'datetime' para geração e comparação de timestamps.

### Passos do algoritmo

  1) Importa bibliotecas e define constantes.
  2) Checa pelo número de correto de argumentos e extrai argumentos inseridos juntos ao comando de execução.
  3) Procura pelo arquivo no caminho absoluto ou relativo fornecido e salva seu conteudo.
  4) Checa pela existência de um cabeçalho, indicando se o arquivo foi assinado.
  5) Procura pelo certificado crt utilizado para verificação, no caminho absoluto ou relativo fornecido, e salva seu conteudo.
  6) Decodifica o arquivo e assinatura em base64.
  7) Gera uma timestamp atual.
  8) Valida a assinatura e o prazo do certificado.
  9) Salva o arquivo decodificado com o nome retirado do cabeçalho na pasta output.
