# Naming Conventions

## General Principles
- Names should describe what something is or does, not how it works.
- Use domain-specific terminology from the project glossary.
- Avoid abbreviations unless universally understood: `id`, `url`, `db`, `config` are fine. `usr`, `mgr`, `proc` are not.
- Be consistent. If the codebase uses `remove`, do not introduce `delete` for the same concept.
- Longer names for larger scopes. Single letters only for loop counters and lambdas.


## Python
- Variables and functions: `snake_case` (`get_user_by_id`, `is_active`, `order_count`).
- Classes: `PascalCase` (`UserService`, `OrderRepository`).
- Constants: `UPPER_SNAKE_CASE` (`MAX_RETRIES`, `DEFAULT_TIMEOUT`).
- Private members: single underscore prefix (`_internal_cache`, `_validate_input`).
- Dunder methods: double underscore (`__init__`, `__repr__`, `__eq__`).
- Modules and packages: `snake_case` (`user_service.py`, `data_access/`).
- Type variables: `PascalCase` with `T` suffix convention (`ItemT`, `ResponseT`).

