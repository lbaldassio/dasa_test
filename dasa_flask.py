from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/annotate', methods=['POST'])
def annotate():
    try:
        # Tenta extrair os dados da requisição JSON
        data = request.get_json()

        # Imprimir o conteúdo recebido para debug
        print("Dados recebidos:", data)

        input_vcf = data.get('input_vcf')
        output_vcf = data.get('output_vcf')
        dbsnp = data.get('dbsnp')
        frequency = data.get('frequency')  # novo parâmetro
        depth = data.get('depth')  # novo parâmetro

        # Verifica se os parâmetros foram passados corretamente
        if not input_vcf or not output_vcf or not dbsnp:
            return jsonify({"error": "Parâmetros faltando."}), 400

        # Caminho do SnpSift
        snpsift_path = "/Users/leticia/Desktop/programas/snpEff/SnpSift.jar"

        # Monta o comando para SnpSift
        command = [
            "java", "-jar", snpsift_path,
            "annotate",
            "-dbsnp",
            "-db", dbsnp,  # Aqui o dbsnp é passado como vcf.gz
            input_vcf
        ]

        # Executa o comando e escreve a saída no arquivo
        with open(output_vcf, 'w') as output_file:
            subprocess.run(command, stdout=output_file, stderr=subprocess.PIPE, check=True)

        # Filtrar variantes por frequência e profundidade
        if frequency or depth:
            filtered_vcf = filter_variants(output_vcf, frequency, depth)
            return jsonify({"message": "Anotação e filtragem de variantes concluída", "output_file": filtered_vcf}), 200
        else:
            return jsonify({"message": "Anotação concluída", "output_file": output_vcf}), 200

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Erro ao executar SnpSift", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Erro desconhecido", "details": str(e)}), 500



def filter_variants(vcf_file, frequency=None, depth=None):
    filtered_file = vcf_file.replace(".vcf", "_filtered.vcf")  # Nome do arquivo filtrado

    with open(vcf_file, 'r') as infile, open(filtered_file, 'w') as outfile:
        for line in infile:
            if line.startswith("#"):  # Copia cabeçalhos
                outfile.write(line)
            else:
                # Exemplo: linha VCF típica
                fields = line.strip().split("\t")
                
                # Assumindo que a frequência e profundidade estão na coluna INFO (campo 8)
                info = fields[7]
                
                # Inicializa as variáveis de frequência e profundidade
                freq_values = []  # Lista para armazenar valores de frequência
                depth_value = None
                
                # Extrai informações do campo INFO
                info_fields = info.split(";")
                for field in info_fields:
                    if field.startswith("TOPMED="):  # Alterado de "AF=" para "TOPMED="
                        # Pega todos os valores de TOPMED
                        freq_string = field.split("=")[1]
                        # Se o valor for '.', consideramos como ausência
                        if freq_string != '.' and freq_string.strip() != '':
                            freq_values = [float(f) for f in freq_string.split(",") if f != '.']

                    if field.startswith("DP="):
                        depth_value = int(field.split("=")[1])  # Pega o valor de DP

                # Condições de filtragem
                freq_filter = True
                if frequency is not None:
                    # Usamos any apenas se houver valores válidos de frequência
                    freq_filter = any(f >= frequency for f in freq_values) if freq_values else False

                depth_filter = depth is None or (depth_value is not None and depth_value >= depth)

                if freq_filter and depth_filter:
                    outfile.write(line)

    return filtered_file


if __name__ == '__main__':
    app.run(debug=True)
