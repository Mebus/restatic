from collections import namedtuple
from .restic_thread import ResticThread
from restatic.models import RepoModel

FakeRepo = namedtuple("Repo", ["url", "id"])
FakeProfile = namedtuple("FakeProfile", ["repo", "name", "ssh_key"])


class ResticInfoThread(ResticThread):
    def started_event(self):
        self.updated.emit("Validating existing repo...")

    @classmethod
    def prepare(cls, params):
        """
        Used to validate existing repository when added.
        """

        cls.params = params

        # Build fake profile because we don't have it in the DB yet.
        profile = FakeProfile(
            FakeRepo(params["repo_url"], 999), "New Repo", params["ssh_key"]
        )

        ret = super().prepare(profile)
        if not ret["ok"]:
            return ret
        else:
            ret["ok"] = False  # Set back to false, so we can do our own checks here.

        cmd = ["restic", "-r", profile.repo.url, "--json", "stats"]

        if params["password"] == "":
            ret[
                "password"
            ] = (
                "999999"
            )  # Dummy password if the user didn't supply one. To avoid prompt.
        else:
            ret["password"] = params["password"]
        ret["ok"] = True
        ret["cmd"] = cmd

        return ret

    @classmethod
    def prepare_existing(cls, profile):
        ret = super().prepare(profile)
        cls.profile = profile

        if not ret["ok"]:
            return ret
        else:
            ret["ok"] = False  # Set back to false, so we can do our own checks here.

        cmd = ["restic", "-r", profile.repo.url, "--json", "stats"]

        ret["ok"] = True
        ret["cmd"] = cmd

        return ret

    def process_result(self, result):
        new_repo, _ = RepoModel.get_or_create(url=self.params["repo_url"])

        if "total_size" in result["data"]:
            stats = result["data"]
            new_repo.total_size = stats["total_size"]
            new_repo.total_file_count = stats["total_file_count"]
            # new_repo.unique_size = stats["unique_size"]
            # new_repo.total_unique_chunks = stats["total_unique_chunks"]

        new_repo.save()

        self.app.backup_log_event.emit("Refresh info finished.")
