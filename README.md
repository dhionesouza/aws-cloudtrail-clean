# aws-cloudtrail-clean

Como fazer funcionar localmente?

Após baixar o programa abra seu VSCode ou terminal e execute o arquivo "app.py" com o comando "python app.py", e em seguida acesse no navegador o "http" fornecido pelo terminal.

Se você tem conhecimento em AWS vai conseguir fazer esse processo numa boa, caso não, entre em contato que posso te ajudar, ( https://www.linkedin.com/in/dhione-souza/ ).

1° Acesso o painel da AWS e crie um usuário IAM:
    Sugestão de Nome: aws-cloudtrail-clean
    Permissão: AWSCloudTrail_ReadOnlyAccess

2° Crie uma Access Key para o usuário recen criado, neste exemplo, para o usuário, "aws-cloudtrail-clean":
    Use a access key e Secret Key para preencher o campo de AWS Credentials no site que estará em execução.

3° Inseira a região de maior fluxo do trail, por exemplo, "us-east-1".

OBS: fique a vontade em ler o código antes de inserir sua credencial, este programa foi criado com o intuíto de facilitar a vida daqueles que precisam de informações relevantes e rápidas do cloudtrail da AWS, nenhuma informação é coletada ou transferida para a internet ou servidor remoto.
O aplicativo é executado localmente, garantindo ainda mais a privacidade dos dados durante as consultas.

OBS²: Os dados coletados são resgatados do cloudtrail default da AWS, isso significa que os logs são dos ultimos 3 meses apenas.