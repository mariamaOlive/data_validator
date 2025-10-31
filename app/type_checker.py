import csv
from datetime import datetime
from typing import TextIO, Dict, List

class TypeChecker:

    TRUTHY = {"true", "1", "yes", "y"}
    FALSY  = {"false", "0", "no", "n"}

    def _infer_scalar(self, values: List[str]) -> str:
        # remove empties
        vals = [v.strip() for v in values if str(v).strip() != ""]
        if not vals:
            return "string"

        low = [v.lower() for v in vals]
        if all(v in self.TRUTHY | self.FALSY for v in low):
            return "boolean"

        try:
            for v in vals: int(v)
            return "integer"
        except Exception:
            pass

        try:
            for v in vals: float(v)
            return "number"
        except Exception:
            pass

        try:
            for v in vals: datetime.strptime(v, "%Y-%m-%d")
            return "date"
        except Exception:
            pass

        return "string"

    def check_types(self, file_like: TextIO, sample_rows: int = 200) -> Dict:
        file_like.seek(0)
        r = csv.reader(file_like, delimiter=",", quotechar='"')
        header = next(r, None) or []
        if not header:
            return {"total_columns": 0, "column_types": {}}

        # collect up to N sample rows
        samples: List[List[str]] = []
        for i, row in enumerate(r, start=1):
            if i <= sample_rows:
                samples.append(row)

        # infer per column
        col_types = {}
        for i, name in enumerate(header):
            vals = [(row[i] if i < len(row) else "") for row in samples]
            col_types[name] = self._infer_scalar(vals)

        return {"total_columns": len(header), "column_types": col_types}