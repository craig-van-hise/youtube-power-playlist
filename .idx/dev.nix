{ pkgs, ... }: {
  # Use the stable channel
  channel = "stable-24.05";

  # Install Python and the C++ Library
  packages = [
    pkgs.python3
    pkgs.stdenv.cc.cc.lib
  ];

  # Force Python to find the C++ library
  env = {
    LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
  };

  # VS Code configuration
  idx = {
    extensions = [
      "ms-python.python"
    ];
    workspace = {
      onCreate = {
        # Create venv, activate it, and install requirements automatically
        install-deps = "python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt";
      };
    };
  };
}