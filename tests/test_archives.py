from restatic.models import BackupProfileModel, ArchiveModel
import restatic.restic


def test_prune_intervals(app, qtbot):
    prune_intervals = ['hour', 'day', 'week', 'month', 'year']
    main = app.main_window
    tab = main.archiveTab
    profile = BackupProfileModel.get(id=1)

    for i in prune_intervals:
        getattr(tab, f'prune_{i}').setValue(9)
        tab.save_prune_setting(None)
        profile = profile.refresh()
        assert getattr(profile, f'prune_{i}') == 9


def test_repo_list(app_with_repo, qtbot, mocker, restic_json_output):
    main = app_with_repo.main_window
    tab = main.archiveTab
    main.tabWidget.setCurrentIndex(3)
    tab.list_action()
    assert not tab.checkButton.isEnabled()

    stdout, stderr = restic_json_output('list')
    popen_result = mocker.MagicMock(stdout=stdout, stderr=stderr, returncode=0)
    mocker.patch.object(restatic.restic.restic_thread, 'Popen', return_value=popen_result)

    qtbot.waitUntil(lambda: main.createProgressText.text() == 'Refreshing snapshots done.')
    assert ArchiveModel.select().count() == 6
    assert main.createProgressText.text() == 'Refreshing snapshots done.'
    assert tab.checkButton.isEnabled()
