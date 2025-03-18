class Lc0 < Formula
  desc "Open source neural network based chess engine"
  homepage "https://lczero.org/"
  url "https://github.com/LeelaChessZero/lc0.git",
      tag:      "v0.31.2",
      revision: "8ba8aa426460bbeda452754ff7d6a9bb60bb0e54"
  license "GPL-3.0-or-later"

  depends_on "cmake" => :build
  depends_on "meson" => :build
  depends_on "ninja" => :build
  depends_on "pkg-config" => :build
  depends_on "eigen"

  uses_from_macos "python" => :build # required to compile .pb files
  uses_from_macos "zlib"

  on_linux do
    depends_on "openblas"
  end

  fails_with gcc: "5" # for C++17

  # We use "753723" network with 15 blocks x 192 filters (from release notes)
  # Downloaded from https://training.lczero.org/networks/?show_all=0
  resource "network" do
    url "https://training.lczero.org/get_network?sha=3e3444370b9fe413244fdc79671a490e19b93d3cca1669710ffeac890493d198", using: :nounzip
    sha256 "ca9a751e614cc753cb38aee247972558cf4dc9d82c5d9e13f2f1f464e350ec23"
  end

  def install
    args = ["-Dgtest=false", "-Dbindir=libexec"]

    if OS.mac?
      # Disable metal backend for older macOS
      # Ref https://github.com/LeelaChessZero/lc0/issues/1814
      args << "-Dmetal=disabled" if MacOS.version <= :big_sur
    else
      args << "-Dopenblas_include=#{Formula["openblas"].opt_include}"
      args << "-Dopenblas_libdirs=#{Formula["openblas"].opt_lib}"
    end

    system "meson", "setup", "build", *args, *std_meson_args
    system "meson", "compile", "-C", "build", "--verbose"
    system "meson", "install", "-C", "build"

    bin.write_exec_script libexec/"lc0"
    resource("network").stage { libexec.install Dir["*"].first => "42850.pb.gz" }
  end

  test do
    assert_match "Creating backend [blas]",
      shell_output("#{bin}/lc0 benchmark --backend=blas --nodes=1 --num-positions=1 2>&1")
    assert_match "Creating backend [eigen]",
      shell_output("#{bin}/lc0 benchmark --backend=eigen --nodes=1 --num-positions=1 2>&1")
  end
end
