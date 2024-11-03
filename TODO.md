# Optimization
- Desconstruir queries
    - Queries que puxem menos dados e relacionamentos para casos onde não é necessário
    - Disponibilizar mais opções de 'find' na classes de ports/queries (mais métodos / parâmetro de personalização de query / injeção do método de query vindo do driver.)
- Reduzir retornos para o mínimo necessário
- Expandir cache service para mais concrete application services and/or repositories

# Security
- Implementar middleware de autenticação e autorização
- Implementar hash de senhas
- Implementar controle de sessão

# Tests
- Implementar testes de integração
- Implementar testes de carga

# DataQuality
- Implementar o UnitOfWork nos repositórios para evitar alterações inconsistentes
- Alterar dataMappers (consequentemente implementações concretas dos repositories) para converter do Domain para classes do DB e não Dicts