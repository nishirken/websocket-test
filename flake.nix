{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        packageName = "websocket-test";
      in {
        defaultPackage = self.packages.${system}.${packageName};

        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            nodejs_20
            python311
            uv
          ];
          shellHook = ''
            export TEST_BROWSER_PATH="${pkgs.chromium}/bin/chromium"
            export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib"
            export PLAYWRIGHT_NODEJS_PATH="${pkgs.nodejs}/bin/node"
          '';
        };
      });
}

