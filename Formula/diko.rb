class Diko < Formula
  include Language::Python::Virtualenv

  desc "CLI tool for downloading and verifying Linux distribution ISO images"
  homepage "https://github.com/aleksandr/diko"
  url "https://github.com/aleksandr/diko/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "placeholder"
  license "Apache-2.0"

  depends_on "python@3.11"
  depends_on "openjdk"

  resource "click" do
    url "https://files.pythonhosted.org/packages/76/0a/b8c5f311e32aabe55a5792758175d054238e21a20a44018335b2a0c72c4e/click-8.1.7.tar.gz"
    sha256 "ca9853ad459e787e2192211578cc907e7594e294c7ccc3c6a8dcb64e52f6f508"
  end

  def install
    # Compile Java downloader
    system "javac", "diko/java/Downloader.java"
    
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/diko", "--version"
  end
end
