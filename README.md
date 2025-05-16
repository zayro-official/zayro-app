ZAYRO プロジェクト開発ドキュメント
1. プロジェクト概要
プロジェクト名: ZAYRO（ザイロ）
目的: レストラン向けレビュー管理システム
特徴: 複数プラットフォーム（Google、Yelp、TripAdvisorなど）のレビューを一元管理
差別化ポイント: 多言語対応、AIを活用した自動返信、顧客管理連携
2. 要件定義
機能要件

ダッシュボード機能

統計情報表示（平均評価、レビュー総数、未返信数、返信時間）
プラットフォーム別レビュー管理
レビューリスト表示


レビュー管理機能

レビュー詳細表示
レビュー返信機能
テンプレート選択機能


データ同期機能

各プラットフォーム（Google/Yelp/TripAdvisor）からのレビュー自動取得
レビュー更新の定期チェック


レポート・分析機能（将来実装）

時系列評価推移グラフ
プラットフォーム比較
キーワード分析



非機能要件

レスポンシブデザイン
多言語対応（日本語・英語）
データセキュリティ
定期バックアップ

3. 基本設計
システムアーキテクチャ

フロントエンド: HTML/CSS/JavaScript（GitHubページでホスティング）
バックエンド: Python FastAPI
データストレージ: 現在はメモリ内データ（将来的にデータベース実装予定）
外部API連携: Google/Yelp/TripAdvisor APIとの連携

データフロー

外部APIからレビューデータを取得
バックエンドでデータを処理・保存
フロントエンドからAPIリクエストでデータ取得
ユーザーがレビューに返信するとAPIを通じてデータ更新

4. 詳細設計
API設計

GET /: ルートエンドポイント
GET /reviews: 全レビュー取得（オプションでプラットフォームによるフィルタリング）
GET /reviews/{review_id}: 特定のレビュー取得
PUT /reviews/{review_id}/respond: レビューへの返信

UI設計

ダッシュボード画面: 統計情報、プラットフォームタブ、レビューリスト
レビュー詳細・返信画面: レビュー内容、顧客情報、返信エディタ、テンプレート選択

5. 技術スタック
フロントエンド

HTML/CSS/JavaScript: 基本構成
Bootstrap: UIフレームワーク
Chart.js: グラフ表示（将来実装）

バックエンド

Python 3.13: プログラミング言語
FastAPI: APIフレームワーク
Uvicorn: ASGIサーバー
Pydantic: データバリデーション

データベース（将来実装）

SQLite（開発環境）
PostgreSQL（本番環境、予定）

外部API

Google My Business API
Yelp Fusion API
TripAdvisor Content API

6. 開発環境
ローカル開発環境

OS: macOS
エディタ: テキストエディタ（VSCode推奨）
ブラウザ: Google Chrome
バージョン管理: Git/GitHub

デプロイ環境

フロントエンド: GitHub Pages
バックエンド: 未定（AWS/Heroku候補）

7. 現在の進捗状況
完了した作業

フロントエンドのプロトタイプ作成

ダッシュボード画面の基本レイアウト
レビュー詳細・返信画面の基本レイアウト
GitHub Pagesへのデプロイ


バックエンドの基本実装

FastAPIの基本セットアップ
仮データによるレビューAPIの実装（CRUD操作）
ローカル環境での動作確認



現在の動作状況

APIサーバー: http://127.0.0.1:8000/で動作中
API機能: レビュー一覧取得、特定レビュー取得、レビュー返信が機能中
サンプルデータ: 2件のダミーレビューデータが実装済み

8. 次のステップ（優先順位順）

フロントエンドとバックエンドの連携

API連携用のJavaScriptクライアント実装
ダッシュボードページのAPI連携
レビュー詳細・返信ページのAPI連携
CORS設定の追加


実際のAPIデータ取得機能の実装

Google/Yelp APIからのデータ取得
データの統合と保存


データの永続化

データベース設計と実装（SQLite/PostgreSQL）
データモデルのORM実装


グラフ機能の実装

Chart.jsによる評価推移の可視化
プラットフォーム比較グラフの実装



9. 実装コード（現状）
バックエンド（simple_main.py）
API設計

GET /: ルートエンドポイント
GET /reviews: 全レビュー取得（オプションでプラットフォームによるフィルタリング）
GET /reviews/{review_id}: 特定のレビュー取得
PUT /reviews/{review_id}/respond: レビューへの返信

UI設計

ダッシュボード画面: 統計情報、プラットフォームタブ、レビューリスト
レビュー詳細・返信画面: レビュー内容、顧客情報、返信エディタ、テンプレート選択

5. 技術スタック
フロントエンド

HTML/CSS/JavaScript: 基本構成
Bootstrap: UIフレームワーク
Chart.js: グラフ表示（将来実装）

バックエンド

Python 3.13: プログラミング言語
FastAPI: APIフレームワーク
Uvicorn: ASGIサーバー
Pydantic: データバリデーション

データベース（将来実装）

SQLite（開発環境）
PostgreSQL（本番環境、予定）

外部API

Google My Business API
Yelp Fusion API
TripAdvisor Content API

6. 開発環境
ローカル開発環境

OS: macOS
エディタ: テキストエディタ（VSCode推奨）
ブラウザ: Google Chrome
バージョン管理: Git/GitHub

デプロイ環境

フロントエンド: GitHub Pages
バックエンド: 未定（AWS/Heroku候補）

7. 現在の進捗状況
完了した作業

フロントエンドのプロトタイプ作成

ダッシュボード画面の基本レイアウト
レビュー詳細・返信画面の基本レイアウト
GitHub Pagesへのデプロイ


バックエンドの基本実装

FastAPIの基本セットアップ
仮データによるレビューAPIの実装（CRUD操作）
ローカル環境での動作確認



現在の動作状況

APIサーバー: http://127.0.0.1:8000/で動作中
API機能: レビュー一覧取得、特定レビュー取得、レビュー返信が機能中
サンプルデータ: 2件のダミーレビューデータが実装済み

8. 次のステップ（優先順位順）

フロントエンドとバックエンドの連携

API連携用のJavaScriptクライアント実装
ダッシュボードページのAPI連携
レビュー詳細・返信ページのAPI連携
CORS設定の追加


実際のAPIデータ取得機能の実装

Google/Yelp APIからのデータ取得
データの統合と保存


データの永続化

データベース設計と実装（SQLite/PostgreSQL）
データモデルのORM実装


グラフ機能の実装

Chart.jsによる評価推移の可視化
プラットフォーム比較グラフの実装



9. 実装コード（現状）
バックエンド（simple_main.py）
10. 課題と解決策
現在の課題

CORSエラー: フロントエンドとバックエンドの連携時に発生する可能性

解決策: FastAPIにCORSミドルウェアを追加


データの永続化: 現在はメモリ内データ

解決策: SQLiteまたはPostgreSQLの導入


実際のAPI連携: 各プラットフォームのAPIキー管理と適切な例外処理

解決策: 環境変数でAPIキーを管理、例外処理の導入



11. 連絡先とリソース

GitHub リポジトリ: zayro-official/zayro-app
GitHub Pages: https://zayro-official.github.io/zayro-app/
APIドキュメント: http://127.0.0.1:8000/docs (ローカル環境のみ)
