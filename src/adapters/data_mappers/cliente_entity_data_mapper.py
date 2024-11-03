from typing import Optional
from src.adapters.data_mappers.usuario_data_mapper import UsuarioEntityDataMapper
from src.adapters.driven.infra.models.persona import Persona
from src.adapters.driven.infra.models.user import User
from src.core.domain.entities.cliente_entity import PartialClienteEntity
from src.core.domain.value_objects.address_value_object import AddressValueObject
from src.core.domain.value_objects.persona_value_object import PersonaValueObject


class ClientEntityDataMapper:
    @classmethod
    def from_db_to_domain(cls, client: Persona, user: Optional[User] = None):
        return PartialClienteEntity(
            id=client.id,
            person=PersonaValueObject(
                name=client.name,
                document=client.document,
                email=client.email,
                address=(
                    AddressValueObject(
                        zip_code=client.address.zip_code,
                        street=client.address.street,
                        number=client.address.number,
                        city=client.address.city,
                        state=client.address.state,
                        country=client.address.country,
                        additional_information=client.address.additional_information,
                    )
                    if client.address
                    else None
                ),
                birth_date=client.birth_date,
                phone=client.phone,
            ),
            created_at=client.created_at,
            updated_at=client.updated_at,
            deleted_at=client.deleted_at,
            user=UsuarioEntityDataMapper.from_db_to_domain(user) if user else None,
        )

    @classmethod
    def from_domain_to_db(cls, client: PartialClienteEntity):
        return {
            "id": client.id,
            "name": client.person.name,
            "document": client.person.document,
            "email": client.person.email,
            "address": (
                {
                    "zip_code": client.person.address.zip_code,
                    "street": client.person.address.street,
                    "number": client.person.address.number,
                    "city": client.person.address.city,
                    "state": client.person.address.state,
                    "country": client.person.address.country,
                    "additional_information": client.person.address.additional_information,
                }
                if client.person.address
                else None
            ),
            "birth_date": client.person.birth_date,
            "phone": client.person.phone,
        }
