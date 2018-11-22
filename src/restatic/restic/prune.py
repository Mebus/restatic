import platform
from .restic_thread import ResticThread


class ResticPruneThread(ResticThread):

    def log_event(self, msg):
        self.app.backup_log_event.emit(msg)

    def started_event(self):
        self.app.backup_started_event.emit()
        self.app.backup_log_event.emit('Pruning old snapshots..')

    def finished_event(self, result):
        self.app.backup_finished_event.emit(result)
        self.result.emit(result)
        self.app.backup_log_event.emit('Pruning done.')

    @classmethod
    def prepare(cls, profile):
        ret = super().prepare(profile)
        if not ret['ok']:
            return ret
        else:
            ret['ok'] = False  # Set back to false, so we can do our own checks here.

        cmd = ['restic', '-r', f'{profile.repo.url}', 'prune', '--json']

        ret['ok'] = True
        ret['cmd'] = cmd

        return ret
