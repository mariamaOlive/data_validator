from csv import reader


class Validator:
    
    def validate_csv(self, csv, dialect: dict | None = None) -> bool:
        errors = 0
        rows = 0

        # Configure a basic dialect override
        delimiter = (dialect or {}).get("delimiter", ",")
        quotechar = (dialect or {}).get("quotechar", '"')

        try:
            r = reader(csv, delimiter=delimiter, quotechar=quotechar)
            header = next(r, None)  # allow empty CSV -> considered valid (0 rows)
            if header is not None:
                for _ in r:
                    rows += 1
        except Exception:
            errors += 1
            
        return {
        "is_valid": errors == 0,
        "summary": {"rows_read": rows, "errors": errors},
        "errors": [],
        "warnings": [],
        }