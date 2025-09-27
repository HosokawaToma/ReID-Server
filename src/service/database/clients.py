from migration.models.clients import Clients
from service.database.session import ServiceDatabaseSession


class ServiceDatabaseClients:
    @staticmethod
    def get_client_by_id(client_id: str):
        with ServiceDatabaseSession.get_session() as session:
            return session.query(Clients).filter(Clients.id == client_id).first()
