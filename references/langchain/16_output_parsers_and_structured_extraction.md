# 16 - Output Parsers and Structured Extraction

## Why Parsers Matter

Model output is often free-form text. Parsers make downstream code safer and deterministic.

## Common Parsers

- `StrOutputParser`: plain string output
- `JsonOutputParser`: parse JSON outputs
- schema-bound extraction with `with_structured_output(PydanticModel)`

## Recommended Order of Reliability

1. function/tool calling + structured output schema
2. strict JSON response with parser
3. regex/text parsing (last resort)

## Pydantic Structured Output

```python
class Ticket(BaseModel):
    priority: Literal["low", "medium", "high"]
    summary: str

structured = model.with_structured_output(Ticket)
result = structured.invoke("Classify this issue: ...")
```

## Parser Failure Handling

- return explicit parse errors
- retry with repair prompt
- keep original raw model text for debugging
- test parser behavior with adversarial outputs
