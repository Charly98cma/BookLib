from typing import Any

class BaseService:
    
    @staticmethod
    def update_orm_object(dest: Any, src: Any) -> None:
        for field, value in src.items():
            setattr(dest, field, value)