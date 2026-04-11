{
  description = "Pure Python development environment (stable)";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-23.05"; 
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in {
        devShells.default = pkgs.mkShell {
          name = "python-dev-shell";

          buildInputs = [
            pkgs.python311
            pkgs.python311Packages.pip
            pkgs.python311Packages.virtualenv
            pkgs.python311Packages.setuptools
            pkgs.python311Packages.wheel
            pkgs.poetry
            pkgs.git
            pkgs.curl
            pkgs.fzf
            pkgs.ripgrep
            pkgs.lsd
            pkgs.gcc
            pkgs.gnumake
            pkgs.docker
          ];

          shellHook = ''
            echo "🐍 Welcome to the Pure Python Dev Shell"
            echo "Python version: $(python3 --version)"
          '';
        };
      }
    );
}

