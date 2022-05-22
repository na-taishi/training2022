import re
import pathlib
import zipfile
import tarfile
import itertools

import settings


class PasswordCreate:
    '''パスワード作成'''
    def generate_characters(self):
        '''文字の生成処理'''
        #Unicode数値作成
        unicode_nums = list(range(48,58))
        #Unicodeアルファベット小文字作成
        unicode_low_al = list(range(97,123))
        #Unicodeアルファベット大文字作成
        unicode_up_al = list(range(65,90))
        #文字作成
        chrar_nums = unicode_nums + unicode_low_al + unicode_up_al
        chars = []
        for num in chrar_nums:
            char = chr(num)
            chars.append(char)
        return chars

    def __init__(self):
        # パスワードの桁数を「settings.py」から取得
        self.digits = settings.PASSWORD_LENGTH
        # パスワードを作成する文字を生成する
        self.chars = self.generate_characters()

    def generate_password(self,row):
        '''パスワードを作成'''
        pw = ''.join(map(str,row))
        return pw


class Decompression:
    '''zip,tar,tar.gz解凍'''
    target_dir =  pathlib.Path(settings.TARGET_DIR)
    output_dir =  pathlib.Path(settings.OUTPUT_DIR)
    file_extensions = ["zip","tar","tar.gz"]

    def get_file_path_objects(self):
        '''対象拡張子ファイル取得'''
        file_path_objects = {}
        for extension in Decompression.file_extensions:
            file_paths = [
                file for file in Decompression.target_dir.glob("*")
                if str(file).endswith("." + extension)
            ]
            file_path_objects[extension] = file_paths
        return file_path_objects

    def __init__(self):
        # インスタンス生成時に対象拡張子を持つファイルを辞書形式で取得する
        self.file_path_objects = self.get_file_path_objects()
        # パスワード付きファイルのみに使用するため初期値はNone
        self.true_pw = None

    def get_output_path(self,file_name):
        '''出力先取得'''
        dir = str(Decompression.output_dir)
        path_object = pathlib.Path(dir,file_name)
        return str(path_object)

    def decompress_zip(self,path_object,pw):
        '''zipファイル解凍'''
        flg = False
        file_path = str(path_object)
        file_name = path_object.stem
        output_path = self.get_output_path(file_name)
        with zipfile.ZipFile(file_path,"r") as zip_file:
            try:
                if pw is None:
                    zip_file.extractall(path=output_path)
                else:
                    zip_file.extractall(path=output_path,pwd=pw.encode())
                flg = True
            except RuntimeError as e:
                # 無効なパスワードの場合にここでキャッチする
                pass
            except FileNotFoundError as e:
                print(e)
            except Exception as e:
                pass
        return flg

    def decompress_tar(self,path_object):
        '''tarファイル解凍'''
        flg = False
        file_path = str(path_object)
        file_name = path_object.stem
        output_path = self.get_output_path(file_name)
        with tarfile.open(file_path, 'r') as tar:
            try:
                tar.extractall(path=output_path)
                flg = True
            except RuntimeError as e:
                pass
            except FileNotFoundError as e:
                print(e)
            except Exception as e:
                print(e)
        return flg

    def decompress_tar_gz(self,path_object):
        '''tar.gzファイル解凍'''
        flg = False
        file_path = str(path_object)
        file_name = path_object.stem
        output_path = self.get_output_path(file_name)
        with tarfile.open(file_path, 'r:gz') as tar:
            try:
                tar.extractall(path=output_path)
                flg = True
            except RuntimeError as e:
                pass
            except FileNotFoundError as e:
                print(e)
            except Exception as e:
                print(e)
        return flg

    def repeat_decompression(self,func,path_object):
        '''解凍繰り返し'''
        pw_obj = PasswordCreate()
        digits = pw_obj.digits
        chars = pw_obj.chars
        flg = func(path_object,None)
        if flg == True:
            return flg
        for row in itertools.product(chars, repeat=digits):
            pw = pw_obj.generate_password(row)
            flg = func(path_object,pw)
            if flg == True:
                self.true_pw = pw
                break
        return flg

    @staticmethod
    def execute():
        '''解凍対象ファイル取得して、解凍する'''
        decompression = Decompression()
        decompression.file_path_objects
        for extension in decompression.file_extensions:
            for file_path_object in decompression.file_path_objects[extension]:
                # パスワードを総当たりでの解凍時は「repeat_decompression」関数を使用する
                if extension == "zip":
                    flg = decompression.repeat_decompression(decompression.decompress_zip,file_path_object)
                elif extension == "tar":
                    flg = decompression.decompress_tar(file_path_object)
                elif extension == "tar.gz":
                    flg = decompression.decompress_tar_gz(file_path_object)
                if flg == True:
                    print(file_path_object.name + "を解凍しました。")
                    if not decompression.true_pw is None:
                        print(file_path_object.name + "パスワード:" + decompression.true_pw)
                        decompression.true_pw = None
                else:
                    print(file_path_object.name + "の解凍に失敗しました。")


def main():
    Decompression().execute()


if __name__ == "__main__":
    main()
