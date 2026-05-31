# idempotentPayment

API desenvolvida com **FastAPI** para demonstrar a implementação de **idempotência em operações de pagamento**, utilizando **Redis** para controle de concorrência, armazenamento de respostas e prevenção de pagamentos duplicados.

---

## Objetivo

O objetivo da aplicação é garantir que uma mesma operação de pagamento seja processada apenas uma vez, mesmo que múltiplas requisições sejam enviadas simultaneamente ou que o cliente tente reenviar a mesma solicitação após um timeout ou falha de rede.

---

## Tecnologias Utilizadas

- Python 3.12+
- FastAPI
- Redis
- Docker
- Pydantic
- Uvicorn

---

## Conceitos Demonstrados

- Idempotency Key
- Request Hash (SHA256)
- Redis Cache
- Redis Distributed Lock (`SET NX`)
- Controle de Concorrência
- Race Conditions
- Retry Seguro
- Clean Architecture
- Repository Pattern

---

## Arquitetura

```text
idempotentPayment/
│
├── api/
│   └── payment_routes.py
│
├── app/
│   ├── model/
│   │   └── model_payment.py
│   │
│   ├── use_cases/
│   │   └── process_payment.py
│   │
│   └── utils/
│       └── hash_generator.py
│
├── domain/
│   ├── entities/
│   │   └── payment.py
│   │
│   └── repositories/
│       └── payment_repository.py
│
├── infra/
│   ├── redis/
│   │   └── redis_client.py
│   │
│   └── repositories/
│       └── memory_payment_repository.py
│
├── main.py
├── requirements.txt
├── stress_test.py
└── docker-compose.yml
```

---

## Como Funciona

Cada requisição de pagamento deve possuir um header chamado:

```http
Idempotency-Key
```

Exemplo:

```http
POST /payments
Idempotency-Key: abc123
```

Body:

```json
{
  "user_id": "1",
  "amount": 100
}
```

### Fluxo

1. Recebe a requisição.
2. Gera um hash SHA256 do payload.
3. Verifica se a chave de idempotência já existe no Redis.
4. Caso exista:
   - Com o mesmo payload: retorna a resposta salva.
   - Com payload diferente: retorna erro `409 Conflict`.
5. Caso não exista:
   - Cria um lock utilizando Redis (`SET NX`).
   - Processa o pagamento.
   - Armazena a resposta no Redis.
   - Retorna o resultado.

---

## Controle de Concorrência

Durante o processamento é criado um lock temporário:

```text
idempotency:<key> = PROCESSING
```

Isso impede que múltiplas requisições simultâneas processem o mesmo pagamento ao mesmo tempo.

Exemplo:

```text
20 requisições simultâneas
            │
            ▼
1 pagamento processado
19 requisições bloqueadas
```

---

## Subindo o Redis

### docker-compose.yml

```yaml
services:
  redis:
    image: redis:7
    container_name: redis
    ports:
      - "6379:6379"
```

Executar:

```bash
docker compose up -d
```

Verificar:

```bash
docker ps
```

---

## Instalação

### Clonar o projeto

```bash
git clone <repository-url>

cd idempotentPayment
```

### Criar ambiente virtual

```bash
python -m venv .venv
```

### Ativar ambiente virtual

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Executando a Aplicação

```bash
python main.py
```

Ou:

```bash
uvicorn main:app --reload
```

---

## 📄 Documentação Swagger

Após iniciar a aplicação:

```text
http://localhost:8000/docs
```

---

## Exemplo de Requisição

### Primeira chamada

```http
POST /payments

Idempotency-Key: abc123
```

```json
{
  "user_id": "1",
  "amount": 100
}
```

Resposta:

```json
{
  "status": "approved",
  "user_id": "1",
  "amount": 100,
  "source": "processor"
}
```

---

### Segunda chamada (mesma chave)

```http
POST /payments

Idempotency-Key: abc123
```

```json
{
  "user_id": "1",
  "amount": 100
}
```

Resposta:

```json
{
  "status": "approved",
  "user_id": "1",
  "amount": 100,
  "source": "redis"
}
```

O pagamento não é processado novamente. A resposta é retornada diretamente do Redis.

---

### Mesma chave com payload diferente

```http
POST /payments

Idempotency-Key: abc123
```

```json
{
  "user_id": "2",
  "amount": 100
}
```

Resposta:

```http
409 Conflict
```

```json
{
  "detail": "Idempotency key already used with different payload"
}
```

---

## Teste de Concorrência

O projeto possui um script para simular múltiplas requisições simultâneas utilizando `ThreadPoolExecutor`.

Executar:

```bash
python stress_test.py
```

### Primeira execução

```text
1 request -> approved (processor)

19 requests -> payment already being processed
```

### Segunda execução

```text
20 requests -> approved (redis)
```

Demonstrando que o pagamento foi processado apenas uma vez e as demais respostas foram servidas diretamente pelo cache.

---

## Aprendizados

Este projeto demonstra conceitos frequentemente utilizados em sistemas financeiros, gateways de pagamento e APIs distribuídas:

- Garantia de idempotência
- Locks distribuídos com Redis
- Controle de concorrência
- Processamento seguro de pagamentos
- Cache de respostas
- Retry resiliente
- Arquitetura limpa e desacoplada

---

## Autor

Desenvolvido por **Deryck Henrique Albuquerque**
