I am getting a persistent `ImportError: libstdc++.so.6: cannot open shared object file` when trying to run my Python scripts. This is because the `google-cloud-firestore` library requires C++ system libraries that are missing from the current Nix environment.

I need you to completely rewrite my `.idx/dev.nix` file to fix this permanently.

Please overwrite `.idx/dev.nix` with the following configuration exactly. This configuration enables Python, adds the C++ library (`stdenv.cc.cc.lib`), and most importantly, sets the `LD_LIBRARY_PATH` so Python can find it.

```nix
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-24.05";

  # Use [https://search.nixos.org/packages](https://search.nixos.org/packages) to find packages
  packages = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.virtualenv
    pkgs.stdenv.cc.cc.lib  # Required for google-cloud-firestore / grpc
  ];

  # Sets environment variables in the workspace
  env = {
    # This is critical: it tells Python where to find the C++ libraries
    LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
  };

  idx = {
    extensions = [
      "google.gemini-cli-vscode-ide-companion"
      "ms-python.python"
    ];
    workspace = {
      onCreate = {
        # Create the virtual environment automatically
        create-venv = "python3 -m venv .venv && source .venv/bin/activate && pip install -r research-archive-bot/requirements.txt";
      };
      onStart = {
        # Always activate venv on startup
        activate-venv = "source .venv/bin/activate";
      };
    };
  };
}