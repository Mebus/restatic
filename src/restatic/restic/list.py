from dateutil import parser
from .restic_thread import ResticThread
from restatic.models import ArchiveModel, RepoModel


class ResticListThread(ResticThread):
    def log_event(self, msg):
        self.app.backup_log_event.emit(msg)

    def started_event(self):
        self.app.backup_started_event.emit()
        self.app.backup_log_event.emit("Refreshing snapshots..")

    def finished_event(self, result):
        self.app.backup_finished_event.emit(result)
        self.result.emit(result)
        self.app.backup_log_event.emit("Refreshing snapshots done.")

    @classmethod
    def prepare(cls, profile):
        ret = super().prepare(profile)

        cls.profile = profile

        if not ret["ok"]:
            return ret
        else:
            ret["ok"] = False  # Set back to false, so we can do our own checks here.

        cmd = ["restic", "-r", profile.repo.url, "--json", "snapshots"]

        ret["ok"] = True
        ret["cmd"] = cmd

        return ret

    def process_result(self, result):
        if result["returncode"] == 0:
            repo, created = RepoModel.get_or_create(url=self.profile.repo.id)

            remote_snapshots = result["data"]

            # Delete snapshots that don't exist on the remote side
            for snapshot in ArchiveModel.select().where(
                ArchiveModel.repo == self.profile.repo.id
            ):
                if not list(
                    filter(lambda s: s["id"] == snapshot.snapshot_id, remote_snapshots)
                ):
                    snapshot.delete_instance()

            if result["data"]:

                # Add remote snapshots we don't have locally.
                for snapshot in result["data"]:

                    new_snapshot, _ = ArchiveModel.get_or_create(
                        snapshot_id=snapshot["id"],
                        defaults={
                            "repo": self.profile.repo.id,
                            "name": snapshot["id"],
                            "time": parser.parse(snapshot["time"]),
                            "hostname": snapshot["hostname"],
                        },
                    )
                    new_snapshot.save()
