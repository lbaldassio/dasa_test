1. Vá até o diretório do seu projeto no terminal

2. Construa a imagem Docker usando o seguinte comando:
"docker-compose build"

3. Inicie a aplicação Flask
"docker-compose up"

4. Com o Flask ativado e rodando vá para outra janela da sua linha de comando.

5. Faça uma requisição curls para testar a API
"curl -X POST http://127.0.0.1:5000/annotate \
    -H "Content-Type: application/json" \
    -d '{
        "input_vcf": "/Users/leticia/Desktop/DASA/NIST.vcf",
        "output_vcf": "/Users/leticia/Desktop/DASA/NIST_annotated.vcf",
        "dbsnp": "/Users/leticia/Desktop/programas/snpEff/common_all_20180423.vcf.gz",
        "frequency": 0.1,
        "depth": 20
    }'
"

Colocando em cada uma das variantes o caminho até os respectivos arquivos.     
