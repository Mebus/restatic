import sys
import os
import peewee

from restatic.models import init_db
from restatic.application import RestaticApp
from restatic.config import SETTINGS_DIR
from restatic.updater import get_updater


def main():

    # Init database
    dbpath = os.path.join(SETTINGS_DIR, "settings.db")
    print("Using database " + dbpath)
    sqlite_db = peewee.SqliteDatabase(dbpath)
    init_db(sqlite_db)

    app = RestaticApp(sys.argv, single_app=True)
    app.updater = get_updater()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
