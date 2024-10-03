# Use uma imagem base do Python
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos necessários para o contêiner
COPY requirements.txt requirements.txt
COPY dasa_flask.py dasa_flask.py

### Instala as dependências ###
RUN pip install --no-cache-dir -r requirements.txt
RUN wget https://snpeff.blob.core.windows.net/versions/snpEff_latest_core.zip
RUN unzip snpEff_latest_core.zip

# databeses
RUN wget wget https://ftp.ncbi.nlm.nih.gov/snp/organisms/human_9606_b151_GRCh37p13/VCF/common_all_20180423.vcf.gz
RUN wget https://ftp.ncbi.nlm.nih.gov/snp/organisms/human_9606_b151_GRCh37p13/VCF/common_all_20180423.vcf.gz

# Expõe a porta que o Flask irá rodar
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "dasa_flask.py"]
