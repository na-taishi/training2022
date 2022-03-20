from config import status_code

MESSAGE = {
    status_code.SUCCESS:"成功しました!",
    status_code.ERROR_DB:"DB更新に失敗しました。。",
    status_code.ERROR_ALREADY_TABLE:"テーブルがすでに存在します。",
    status_code.ERROR_ALREADY_TABLE:"レコードがすでに存在します。",
    status_code.ERROR_NO_TABLE:"テーブルが存在しません。",
    status_code.ERROR_NO_RECORD:"レコードが存在しません。",
    status_code.RECORD_NOT_FOUND:"レコードが見つかりませんでした。",
    status_code.ERROR_INPUT_VALUE:"正しい値を入力して下さい。"
}

POPUP = {
    status_code.ERROR_DB:"DBエラー。",
    status_code.ERROR_ALREADY_TABLE:"DBテーブルエラー",
    status_code.ERROR_ALREADY_TABLE:"DBレコードエラー",
    status_code.ERROR_NO_TABLE:"DBテーブルエラー",
    status_code.ERROR_NO_RECORD:"DBレコードエラー",
    status_code.RECORD_NOT_FOUND:"レコードなし",
    status_code.ERROR_INPUT_VALUE:"入力エラー"
}