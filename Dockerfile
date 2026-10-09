# Imagem do pipeline api-feriados (DW Guaraves). Roda sob demanda: docker compose run --rm api-feriados
FROM python:3.13-slim
ENV TZ=America/Sao_Paulo LANG=C.UTF-8 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
RUN apt-get update && apt-get install -y --no-install-recommends tzdata \
 && rm -rf /var/lib/apt/lists/* \
 && groupadd --gid 1001 dataway && useradd --uid 1001 --gid 1001 --create-home dataway
WORKDIR /app
COPY Requirements.txt /tmp/requirements.raw
# Alguns requirements.txt foram gerados por "pip freeze >" no PowerShell (UTF-16): normaliza antes.
RUN python -c "import pathlib;b=pathlib.Path('/tmp/requirements.raw').read_bytes();t=b.decode('utf-16') if b[:2] in (b'\xff\xfe',b'\xfe\xff') or b'\x00' in b else b.decode('utf-8-sig');pathlib.Path('/tmp/requirements.txt').write_text(t.replace('\r',''))" \
 && pip install --no-cache-dir -r /tmp/requirements.txt
COPY --chown=dataway:dataway . .
USER dataway
CMD ["python", "main.py"]
