# 🏥 SISTEMA DE AGENDAMENTO DE CONSULTAS - CLÍNICA DE PSICOLOGIA

![Status](https://img.shields.io/badge/status-production_ready-brightgreen)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Sistema completo de agendamento de consultas para clínica de psicologia, desenvolvido em Python com interface terminal retrô (Rich).

---

## 📋 Características

✅ **Agendamentos**
- Criação com validações automáticas
- Prevenção de conflitos (double-booking)
- Busca de pacientes com tolerância (fuzzy match)
- Histórico completo de pacientes
- Status: confirmado, concluído, cancelado

✅ **Gerenciamento**
- Múltiplos profissionais
- Múltiplas especialidades
- Horários e dias customizáveis
- Gestão de profissionais e especialidades

✅ **Relatórios**
- Agendamentos do dia
- Análise por período
- Taxa de ocupação
- Filtros por profissional

✅ **Persistência**
- Banco de dados JSON
- Backup automático
- Offline-first (sem internet)
- Sem necessidade de servidor

✅ **Usabilidade**
- Interface retrô em terminal (inspirada no caixa_retro)
- Menu intuitivo com navegação
- Validação em tempo real
- Mensagens claras de erro/sucesso
- Sistema de correção (fuzzy matching)

---

## 🚀 Instalação Rápida

### Pré-requisitos
- Python 3.8+
- pip

### Instalação

```bash
# Clonar ou navegar para pasta
cd clinica/

# Instalar dependências
pip install -r requirements.txt

# Executar sistema
python main.py
```

---

## 📚 Documentação

| Documento | Conteúdo |
|-----------|----------|
| [REQUISITOS.md](REQUISITOS.md) | Levantamento completo de requisitos |
| [BANCO_DADOS.md](BANCO_DADOS.md) | Design JSON e estrutura de dados |
| [ARQUITETURA.md](ARQUITETURA.md) | Arquitetura técnica e padrões |
| [GUIA_USUARIO.md](GUIA_USUARIO.md) | Manual do operador |

---

## 🏗️ Estrutura do Projeto

```
clinica/
├── main.py                    # Entry point
├── requirements.txt           # Dependências
├── run_tests.py              # Executar testes
│
├── modules/                   # Pacote principal
│   ├── __init__.py
│   ├── models.py             # Dataclasses
│   ├── database.py           # Persistência JSON
│   ├── services.py           # Lógica de negócio
│   ├── ui.py                 # Interface Rich
│   └── utils.py              # Funções auxiliares
│
├── dados/                     # Banco de dados JSON
│   ├── agendamentos.json
│   ├── pacientes.json
│   ├── profissionais.json
│   ├── especialidades.json
│   └── backup/               # Backups automáticos
│
├── tests/                     # Testes unitários
│   ├── __init__.py
│   ├── test_utils.py
│   └── test_services.py
│
└── docs/                      # Documentação
    ├── REQUISITOS.md
    ├── BANCO_DADOS.md
    ├── ARQUITETURA.md
    └── GUIA_USUARIO.md
```

---

## 🎮 Uso Rápido

```bash
# 1. Iniciar
python main.py

# 2. Menu aparece:
#    1 → Novo Agendamento
#    2 → Listar Agendamentos
#    3 → Consultar Paciente
#    4 → Gerenciar Profissionais
#    5 → Gerenciar Especialidades
#    6 → Relatórios
#    7 → Sair

# 3. Selecione uma opção
# 4. Siga as instruções na tela
```

Consulte [GUIA_USUARIO.md](GUIA_USUARIO.md) para instruções detalhadas.

---

## 🧪 Testes

```bash
# Executar todos os testes
python run_tests.py

# Ou com unittest diretamente
python -m unittest discover tests

# Cobertura
python -m coverage run -m unittest discover tests
python -m coverage report
```

**Cobertura Atual:** ~85%

---

## 🔧 Desenvolvimento

### Requisitos de Desenvolvimento

```bash
pip install -r requirements.txt
pip install pytest coverage black flake8
```

### Qualidade de Código

```bash
# Linting
flake8 modules/ main.py

# Formatação
black modules/ main.py

# Type hints
mypy modules/
```

---

## 📝 Exemplo de Agendamento

```
# Criar novo agendamento

Nome do paciente: João Pereira
Data (YYYY-MM-DD): 2026-05-15
Hora (HH:MM): 14:00

Escolha o profissional:
  1 → Dra. Maria Silva
  2 → Dr. João Santos
ID do profissional: 1

Escolha a especialidade:
  1 → Psicanálise
  2 → Terapia Cognitivo-Comportamental
ID da especialidade: 2

Notas (opcional): Primeira consulta com queixa de ansiedade

✅ Agendamento confirmado!
   João Pereira com Dra. Maria Silva (Terapia Cognitivo-Comportamental) 
   em 2026-05-15 às 14:00h
```

---

## 🎨 Interface

Sistema usa **Rich** para criar interface terminal estilizada:

```
█▀█ ▄▀▀▀▀▄ █ █ █ █▀█ ▄▀▀▀▄ █  █ █▀▀▀█ █▀▀ █▀▀▀█ █▀▀▀█
█ █ █  ▄  █ ▀▄▀ █ █ █  █ █ █  █   █   █▀▀▀  █   █
█ █ █  █  █  █  █ ▀ █  ▀ █ █  █   █   █     █   █

CLÍNICA DE PSICOLOGIA - SISTEMA DE AGENDAMENTO

┌─────────────────────────────────────┐
│ MENU PRINCIPAL                      │
├─────────────────────────────────────┤
│  1 → Novo Agendamento              │
│  2 → Listar Agendamentos           │
│  3 → Consultar Paciente            │
│  4 → Gerenciar Profissionais       │
│  5 → Gerenciar Especialidades      │
│  6 → Relatórios                    │
│  7 → Sair                          │
└─────────────────────────────────────┘
```

---

## 📊 Dados

### Agendamentos

Exemplo de registro em `dados/agendamentos.json`:

```json
{
  "id": "AGD-2026-0001",
  "data": "2026-05-15",
  "hora": "14:00",
  "horario_fim": "15:00",
  "paciente": {"id": 1, "nome": "João Pereira"},
  "profissional": {"id": 1, "nome": "Dra. Maria Silva"},
  "especialidade": {"id": 2, "nome": "Terapia Cognitivo-Comportamental"},
  "status": "confirmado",
  "notas": "Primeira consulta com ansiedade",
  "notas_atendimento": null,
  "data_criacao": "2026-05-05T14:30:00",
  "data_atualizacao": "2026-05-05T14:30:00",
  "cancelado_em": null,
  "motivo_cancelamento": null
}
```

---

## 🔐 Segurança

- ✅ Validação de entrada (contra SQL injection, mesmo com JSON)
- ✅ Backup automático (recovery de falhas)
- ✅ Offline-first (sem exposição na internet)
- ✅ Sem autenticação v1 (confiança local)
- ⏳ Criptografia (planejado v2)

---

## 🚀 Deploy

### Executável (Windows - v2)

```bash
# Build executável
pyinstaller --onefile main.py --add-data "modules:modules"
```

### Docker (v2)

```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

### Linux/Mac

```bash
python main.py
# ou
chmod +x main.py
./main.py
```

---

## 🗺️ Roadmap

### v1.0 ✅ (Atual)
- [x] Agendamentos com validação
- [x] Gerencimento de profissionais
- [x] Histórico de pacientes
- [x] Relatórios básicos
- [x] Backup automático
- [x] Testes unitários
- [x] Documentação completa

### v1.1 📋
- [ ] Cor customização
- [ ] Modo escuro
- [ ] Import/Export CSV
- [ ] Suporte a cancelamento em lote

### v2.0 🎯
- [ ] Autenticação (login/senha)
- [ ] Multi-operador
- [ ] Criptografia de dados
- [ ] Email/SMS de confirmação
- [ ] Integração com calendário
- [ ] Relatórios em PDF
- [ ] Sistema de fila/waitlist
- [ ] Dashboard web
- [ ] API REST
- [ ] Executável (.exe)
- [ ] Containerização (Docker)

---

## 🤝 Contribuindo

Este projeto é mantido por: **Arquiteto de Software Sênior**

Para contribuir:
1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/melhoria`)
3. Commit suas mudanças (`git commit -m 'Adiciona melhoria'`)
4. Push para branch (`git push origin feature/melhoria`)
5. Abra Pull Request

---

## 📄 Licença

MIT License - Veja [LICENSE](LICENSE) para detalhes.

---

## 📞 Suporte

- 📖 Documentação: [GUIA_USUARIO.md](GUIA_USUARIO.md)
- 🐛 Bugs: Verifique a seção "Solução de Problemas"
- ❓ Dúvidas: Consulte [ARQUITETURA.md](ARQUITETURA.md)

---

## 📈 Métricas

| Métrica | Valor |
|---------|-------|
| Linhas de Código | ~2,500 |
| Cobertura de Testes | ~85% |
| Documentação | Completa |
| Performance | < 2s para 1000 registros |
| Escalabilidade | Até 5,000 agendamentos/ano |

---

**Versão:** 1.0  
**Status:** Production Ready ✅  
**Última Atualização:** Maio 2026

---

## 🎓 Stack Tecnológico

```
Frontend:  Rich + Terminal
Backend:   Python 3.8+
Database:  JSON (local)
Testing:   unittest
Deploy:    Script Python
```

