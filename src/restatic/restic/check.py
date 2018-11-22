from .restic_thread import ResticThread


class ResticCheckThread(ResticThread):

    errormsg = ""

    def log_event(self, msg):
        self.app.backup_log_event.emit(msg)

    def started_event(self):
        self.app.backup_started_event.emit()
        self.app.backup_log_event.emit("Starting consistency check..")

    def process_line(self, line):
        self.errormsg += line

    def finished_event(self, result):
        self.app.backup_finished_event.emit(result)
        self.result.emit(result)

        if result["returncode"] == 0:
            self.app.backup_log_event.emit("Check finished. No errors were reported.")
        else:
            self.app.backup_log_event.emit(
                "Check finished. An error was reported:\n\n" + self.errormsg
            )

    @classmethod
    def prepare(cls, profile):
        ret = super().prepare(profile)
        if not ret["ok"]:
            return ret
        else:
            ret["ok"] = False  # Set back to false, so we can do our own checks here.

        cmd = ["restic", "-r", f"{profile.repo.url}", "--json", "check"]

        ret["ok"] = True
        ret["cmd"] = cmd

        return ret
