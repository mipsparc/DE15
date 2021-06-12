# ログローテーションをすることでログが肥大化するのを防ぐ

def rotate():
    import os

    LOG_DIR = './log/'

    log_files = sorted(os.listdir(LOG_DIR))

    #10個ログを残す
    for f in log_files[:-10]:
        os.remove(LOG_DIR + f)
