from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from ..models import Grayscale


class LoggedInTestCase(TestCase):
    """各テストクラスで共通の事前準備処理をオーバーライドした独自TestCaseクラス"""

    def setUp(self):
        """テストメソッド実行前の事前設定"""

        # テストユーザーのパスワード
        self.password = 'r2k3h07c'

        # 各インスタンスメソッドで使うテスト用ユーザーを生成し
        # インスタンス変数に格納しておく
        self.test_user = get_user_model().objects.create_user(
            username='ngn_hoshino',
            email='ngn2149610@stu.o-hara.ac.jp',
            password=self.password)

        # テスト用ユーザーでログインする
        self.client.login(email=self.test_user.email, password=self.password)


class TestGrayscaleCreateView(LoggedInTestCase):
    """GrayscaleCreateView用のテストクラス"""

    def test_create_grayscale_success(self):
        """日記作成処理が成功することを検証する"""

        # Postパラメータ
        params = {'title': 'テストタイトル',
                  'content': '本文',
                  'photo1': '',
                  'photo2': '',
                  'photo3': ''}

        # 新規日記作成処理(Post)を実行
        response = self.client.post(reverse_lazy('grayscale:grayscale_create'), params)

        # 日記一覧ページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('grayscale:grayscale_list'))

        # 日記データがデータベースに登録されたかを検証
        self.assertEqual(Grayscale.objects.filter(title='テストタイトル').count(), 1)

    def test_create_grayscale_failure(self):
        """新規日記作成処理が失敗することを検証する"""

        # 新規日記作成処理(Post)を実行
        response = self.client.post(reverse_lazy('grayscale:grayscale_create'))

        # 必須フォームフィールドが未入力によりエラーになることを検証
        self.assertFormError(response, 'form', 'title', 'このフィールドは必須です。')


class TestGrayscaleUpdateView(LoggedInTestCase):
    """GrayscaleUpdateView用のテストクラス"""

    def test_update_grayscale_success(self):
        """日記編集処理が成功することを検証する"""

        # テスト用日記データの作成
        grayscale = Grayscale.objects.create(user=self.test_user, title='タイトル編集前')

        # Postパラメータ
        params = {'title': 'タイトル編集後'}

        # 日記編集処理(Post)を実行
        response = self.client.post(reverse_lazy('grayscale:grayscale_update', kwargs={'pk': grayscale.pk}), params)

        # 日記詳細ページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('grayscale:grayscale_detail', kwargs={'pk': grayscale.pk}))

        # 日記データが編集されたかを検証
        self.assertEqual(Grayscale.objects.get(pk=grayscale.pk).title, 'タイトル編集後')

    def test_update_grayscale_failure(self):
        """日記編集処理が失敗することを検証する"""

        # 日記編集処理(Post)を実行
        response = self.client.post(reverse_lazy('grayscale:grayscale_update', kwargs={'pk': 999}))

        # 存在しない日記データを編集しようとしてエラーになることを検証
        self.assertEqual(response.status_code, 404)


class TestGrayscaleDeleteView(LoggedInTestCase):
    """GrayscaleDeleteView用のテストクラス"""

    def test_delete_grayscale_success(self):
        """日記削除処理が成功することを検証する"""

        # テスト用日記データの作成
        grayscale = Grayscale.objects.create(user=self.test_user, title='タイトル')

        # 日記削除処理(Post)を実行
        response = self.client.post(reverse_lazy('grayscale:grayscale_delete', kwargs={'pk': grayscale.pk}))

        # 日記一覧ページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('grayscale:grayscale_list'))

        # 日記データが削除されたかを検証
        self.assertEqual(Grayscale.objects.filter(pk=grayscale.pk).count(), 0)

    def test_delete_grayscale_failure(self):
        """日記削除処理が失敗することを検証する"""

        # 日記削除処理(Post)を実行
        response = self.client.post(reverse_lazy('grayscale:grayscale_delete', kwargs={'pk': 999}))

        # 存在しない日記データを削除しようとしてエラーになることを検証
        self.assertEqual(response.status_code, 404)
