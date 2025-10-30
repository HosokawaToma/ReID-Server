# 参照して使用することを想定していないため即終了する
exit 1

# マイグレーションファイルの作成
alembic revision --autogenerate -m ""

# マイグレーションの実行
alembic upgrade head
