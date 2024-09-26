# aws-cloudtrail-clean

**Como fazer funcionar localmente?**

Após baixar o programa abra seu VSCode ou terminal e execute o arquivo "app.py" com o comando "python app.py", em seguida acesse o "http" fornecido no terminal.

Se você tem conhecimento em AWS vai conseguir fazer esse processo numa boa, caso não, entre em [contato comigo]( https://www.linkedin.com/in/dhione-souza/ ) que posso te ajudar.

**1°** Acesso o painel da AWS e crie um usuário IAM:

**Sugestão de Nome:** aws-cloudtrail-clean

**Permissão:** AWSCloudTrail_ReadOnlyAccess

**2°** Crie uma AccessKey para o usuário recém criado, neste exemplo, para o usuário, **"aws-cloudtrail-clean"**.

**3°** Use a access key e Secret Key para preencher o campo de AWSCredentials

**4°** Insira a região de maior fluxo do trail, por exemplo, "us-east-1".

**OBS:** fique a vontade em ler o código antes de inserir sua credencial, este programa foi criado com o intuito de facilitar a vida daqueles que precisam de informações relevantes e rápidas do cloudtrail da AWS, nenhuma informação é coletada ou transferida para a internet ou servidor remoto.
O aplicativo é executado localmente, garantindo ainda mais a privacidade dos dados durante as consultas.
Os dados coletados são resgatados do cloudtrail default da AWS, isso significa que os logs são dos últimos 3 meses apenas.