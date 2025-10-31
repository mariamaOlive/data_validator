from io import StringIO
import pytest
from app.validator import Validator
from app.type_checker import TypeChecker


def test_validator_with_valid_data():
    
    csv = "id,name\n1,Ana\n2,Bob\n"
    vc = Validator()
    result = vc.validate_csv(StringIO(csv))
    assert result["is_valid"] is True
    
    
def test_type_summary_basic():
    
    tc = TypeChecker()
    
    csv = "name,age,active,joined\nJohn,30,true,2024-01-05\nJane,25,false,2023-12-31\n"
    
    result = tc.check_types(StringIO(csv))
    assert result["total_columns"] == 4
    assert result["column_types"] == {
        "name": "string",
        "age": "integer",
        "active": "boolean",
        "joined": "date",
    }
    
