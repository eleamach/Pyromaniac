class DataBaseRequest:

    @staticmethod
    def get_all_data(db, table):
        return db.query(table).all()

    @staticmethod
    def get_data_by_something(db, table, where):
        return db.query(table).where(where).first()

    @staticmethod
    def get_all_data_by_something(db, table, where):
        return db.query(table).where(where).all()

    @staticmethod
    def post_data(db, data):
        db.add(data)
        db.commit()
        db.refresh(data)
        return data

    @staticmethod
    def delete_data(db, table, where):
        db.query(table).filter(where).delete()
        db.commit()
        return True

    @staticmethod
    def update_data(db, db_data, data):
        for var, value in vars(data).items():
            if value is not None:
                setattr(db_data, var, value)
        db.commit()
        db.refresh(db_data)
        return db_data
