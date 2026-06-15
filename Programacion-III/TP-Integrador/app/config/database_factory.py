''' class DatabaseFactory:

    @staticmethod
    def create_repository(tipo):

        if tipo == "sqlite":
            return SQLiteNotaRepository()

        if tipo == "oracle":
            return OracleNotaRepository(...)
            '''