Para que o arquivo dasa_flask.py funcione é necessário rodar o flask com o seguinte comando: 

"flask --app dasa_flask.py run"

Em outra janela, depois de ativar o flask, é necessário rodar o seguinte comando:

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
