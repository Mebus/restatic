import psutil
from .restic_thread import ResticThread


class ResticUmountThread(ResticThread):
    def started_event(self):
        self.updated.emit("Unmounting archive...")

    @classmethod
    def prepare(cls, profile):
        ret = super().prepare(profile)
        if not ret["ok"]:
            return ret
        else:
            ret["ok"] = False  # Set back to false, so we can do our own checks here.

        ret["active_mount_points"] = []
        partitions = psutil.disk_partitions(all=True)
        for p in partitions:
            if p.device == "resticfs":
                ret["active_mount_points"].append(p.mountpoint)

        if len(ret["active_mount_points"]) == 0:
            ret["message"] = "No active Restic mounts found."
            return ret

        cmd = ["restic", "umount", "--log-json"]

        ret["ok"] = True
        ret["cmd"] = cmd

        return ret
