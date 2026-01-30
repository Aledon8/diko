class Diko < Formula
  include Language::Python::Virtualenv

  desc "CLI tool for downloading and verifying Linux distribution ISO images"
  homepage "https://github.com/Aledon8/diko.git"
  url "https://github.com/Aledon8/diko/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "5779d3c32f8fcf60e6f24eb4d70fe755634c71bb16f6a9105cad61ce55f3c25d"
  license "Apache-2.0"

  depends_on "openjdk"
  depends_on "python@3.12"

  resource "click" do
    url "https://files.pythonhosted.org/packages/76/0a/b8c5f311e32aabe55a5792758175d054238e21a20a44018335b2a0c72c4e/click-8.1.7.tar.gz"
    sha256 "ca9853ad459e787e2192211578cc907e7594e294c7ccc3c6a8dcb64e52f6f508"
  end

  def install
    # Compile Java downloader
    system "javac", "diko/java/Downloader.java"
    
    virtualenv_install_with_resources
    
    # Replace the default symlink with a wrapper that sets JAVA_HOME
    # This ensures diko can find the Java runtime provided by the openjdk dependency
    rm_f bin/"diko"
    (bin/"diko").write_env_script libexec/"bin/diko", Language::Java.overridable_java_home_env
  end

  test do
    system bin/"diko", "--version"
    assert_match "Available distributions", shell_output("#{bin}/diko list")
  end
end
