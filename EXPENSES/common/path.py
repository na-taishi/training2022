import os


def make_path(*args):
    '''パス作成
    実行ファイルから、パスを作成。
    Args:
        args(string):ディレクトリ、ファイル名
    Returns:
        path(string):作成パス
    '''
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(current_dir,*args)
    return path