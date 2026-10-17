# 🎓 Projetos Acadêmicos

Atividades práticas desenvolvidas durante minha graduação em **Inteligência Artificial e Ciência da Computação**, documentadas com objetivo, passo a passo, conceitos aplicados e evidências de execução.

Mantenho este diretório para registrar, de forma reproduzível, o que aprendo em sala de aula e para acompanhar minha evolução ao longo do curso.

---

## 📚 Atividades

### MLOps

| Semana | Atividade | Tema central | Tecnologias |
|:---:|---|---|---|
| 08 | [Docker para ML](./mlops/mlops_semana08) | Empacotar um modelo e sua API de inferência em container | Python, FastAPI, Docker, Docker Compose |
| 09 | [FastAPI para serving](./mlops/mlops_semana09) | API de inferência com validação de contrato e testes automatizados | Python, FastAPI, Pydantic, Uvicorn |
| 10 | [BentoML + Triton](./mlops/mlops_semana10) | Serving com BentoML, benchmark contra FastAPI e adaptive batching | Python, BentoML, scikit-learn, FastAPI |
| 11 | [Monitoramento e Data Drift](./mlops/mlops_semana11) | Detectar drift com KS, PSI, qui-quadrado e Evidently, e registrar o histórico das execuções | Python, pandas, SciPy, Evidently, pytest |

### Big Data

| Semana | Atividade | Tema central | Tecnologias |
|:---:|---|---|---|
| 09 | [PySpark Avançado](./bigdata/bigdata_semana09) | Diagnosticar e otimizar um pipeline lento com `explain()` e Spark UI | Python, PySpark, Parquet, Spark UI |
| 10 | [Spark SQL e Otimização](./bigdata/bigdata_semana10) | Catalyst, leitura de planos, broadcast e cache | Python, PySpark, Spark SQL, Parquet |
| 11 | [dbt: Staging e Testes](./bigdata/bigdata_semana11) | ELT com dbt: camada de staging, testes de dados e DAG | Python, dbt, DuckDB, SQL |

> Novas atividades e disciplinas serão adicionadas aqui à medida que forem concluídas.

---

## 🧭 Como cada atividade está documentada

Cada pasta contém o projeto completo e um README com o mesmo padrão:

- **Objetivo** — o que a prática pedia e por que ela importa
- **O que foi construído** — visão geral do fluxo de ponta a ponta
- **Estrutura** — organização de pastas e arquivos
- **Como executar** — comandos na ordem de uso
- **API / Conceitos aplicados** — decisões técnicas e o raciocínio por trás delas
- **Problemas comuns** — sintomas frequentes e onde olhar

---

## 📌 Sobre o material

As atividades partem de kits e roteiros fornecidos pelas disciplinas. Cada pasta reúne o projeto como o executei, acompanhado de um README que explica o que ele faz e os conceitos envolvidos.

---

## 🛠️ Ambiente usado

- Windows + VS Code + PowerShell
- Python com ambientes virtuais (`.venv`) por atividade
- Docker Desktop (quando a atividade exige)
- Java 17+ e PySpark 4.2.0 (atividades de Big Data)
- dbt e DuckDB (Big Data, semana 11)

---

## 👤 Autor

**João Cláudio** — estudante de Tecnologia (IA e Ciência da Computação)

- GitHub: [@joaoclaudiotech](https://github.com/joaoclaudiotech)
- Prática complementar de Python: [projetos-python](https://github.com/joaoclaudiotech/projetos-python)
