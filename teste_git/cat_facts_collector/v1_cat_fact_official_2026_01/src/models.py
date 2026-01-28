"""
Modelos de dados para validação usando Pydantic.

Define a estrutura esperada dos dados da API Cat Facts.
"""

from datetime import datetime, timezone
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, validator


class User(BaseModel):
    """Modelo para informações do usuário."""
    
    id: Optional[str] = Field(None, alias="_id")
    name: Optional[Dict[str, str]] = None
    photo: Optional[str] = None
    
    class Config:
        populate_by_name = True


class CatFact(BaseModel):
    """Modelo para um fato sobre gatos."""
    
    id: Optional[str] = Field(None, alias="_id")
    fact: Optional[str] = None
    text: Optional[str] = None
    type: Optional[str] = None
    user: Optional[User] = None
    user_id: Optional[str] = None
    upvotes: Optional[int] = 0
    user_upvoted: Optional[bool] = None
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    deleted: Optional[bool] = False
    source: Optional[str] = None
    used: Optional[bool] = None
    sent_count: Optional[int] = Field(None, alias="sentCount")  # Campo da API oficial
    __v: Optional[int] = None  # Versão do MongoDB
    length: Optional[int] = None
    
    # Campo adicionado pela aplicação
    extracted_at: Optional[datetime] = None  # Timestamp de quando o dado foi extraído
    
    class Config:
        populate_by_name = True
    
    @validator('created_at', 'updated_at', pre=True)
    def parse_datetime(cls, value):
        """Converte string para datetime se necessário."""
        if value is None:
            return None
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                return None
        return value
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o modelo para dicionário flat (sem objetos aninhados).
        
        Returns:
            Dicionário com os dados do fato
        """
        user_name = None
        if self.user and self.user.name:
            first = self.user.name.get("first", "")
            last = self.user.name.get("last", "")
            user_name = f"{first} {last}".strip()
        
        # Usa 'fact' ou 'text' como texto do fato
        fact_text = self.fact or self.text
        
        # Gera um ID se não houver
        fact_id = self.id or str(hash(fact_text))[:16] if fact_text else "unknown"
        
        return {
            "id": fact_id,
            "text": fact_text,
            "type": self.type,
            "user_id": self.user_id or (self.user.id if self.user else None),
            "user_name": user_name,
            "upvotes": self.upvotes,
            "user_upvoted": self.user_upvoted,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted": self.deleted,
            "source": self.source,
            "used": self.used,
            "sent_count": self.sent_count,
            "length": self.length or (len(fact_text) if fact_text else None),
            "extracted_at": self.extracted_at.isoformat() if self.extracted_at else datetime.now(timezone.utc).isoformat(),
        }
