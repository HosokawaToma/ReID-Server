# 初期セットアップ

## Docker のインストール

```
# 必要なパッケージをインストール
sudo apt update
sudo apt install ca-certificates curl gnupg lsb-release
# Docker の公式 GPG キーを取得
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
# Docker リポジトリの登録
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
# Docker のインストール
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
# 現在のユーザを Docker グループに追加
sudo usermod -aG docker $USER
```

## NVIDIA Container Toolkit のインストール

```
# 1. GPGキーとリポジトリのセットアップ
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# 2. パッケージリストの更新
sudo apt-get update

# 3. NVIDIA Container Toolkit のインストール
sudo apt-get install -y nvidia-container-toolkit

# 4. Docker の設定変更と再起動
# (nvidia-container-runtime を Docker のデフォルトランタイムとして設定します)
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

## .env ファイルの作成

## SSL/TLS証明書の発行

## nginx.conf.template ファイルの作成

## 起動
