from src.adapters.driven.infra.models.user import User
from src.core.domain.entities.usuario_entity import UsuarioEntity


class UsuarioEntityDataMapper:
    @classmethod
    def from_db_to_domain(cls, user: User):
        return (
            UsuarioEntity(
                username=user.username,
                password=user.password,
                created_at=user.created_at,
                updated_at=user.updated_at,
                deleted_at=user.deleted_at,
            ),
        )

    @classmethod
    def from_domain_to_db(cls, user: UsuarioEntity):
        return {
            "id": user.id,
            "username": user.username,
            "password": user.password,
        }
