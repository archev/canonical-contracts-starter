# Canonical Contracts Starter

Starter repository for a multi-service Protobuf platform with:
- shared technical metadata (`EventMetadata`)
- shared business identifiers (`BusinessContext`)
- service-owned typed events
- a canonical concept dictionary
- event policies
- a baseline CI validator

## Layout

```text
dictionary/common.yaml
policies/event_policies.yaml
proto/company/common/v1/{annotations,event_metadata,business_context}.proto
proto/company/services/payments/v1/payment_events.proto
proto/company/services/orders/v1/order_events.proto
scripts/validate_dictionary.py
requirements-dev.txt
Makefile
.github/workflows/contracts.yml
```

## Prerequisites

- Python 3.10+
- `protoc` (Protocol Buffers compiler)

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\Activate.ps1
pip install -r requirements-dev.txt
make validate-dictionary
make proto
```

The dictionary validator checks required attributes and duplicate canonical IDs.
The Protobuf build compiles schemas and emits a descriptor set.

**Scope note:** this starter does not yet implement descriptor-to-dictionary
field validation or event-policy enforcement. Add those before treating it as
production governance.

## Conventions

1. Keep shared messages focused on one responsibility.
2. Keep canonical concept IDs stable when a field moves between messages.
3. Never reuse removed Protobuf field numbers; reserve them.
4. Prefer additive changes and test compatibility against consumer schemas.
5. Wire compatibility does not guarantee semantic compatibility.
6. Validate populated values at runtime; schemas alone do not guarantee valid
   trace IDs, timestamps, or business identifiers.
