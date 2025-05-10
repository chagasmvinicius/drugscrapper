{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.chromium
    pkgs.chromedriver
    pkgs.xorg.libX11
    pkgs.xorg.libxcb
    pkgs.xorg.libXcomposite
    pkgs.xorg.libXcursor
    pkgs.xorg.libXdamage
    pkgs.xorg.libXext
    pkgs.xorg.libXi
    pkgs.xorg.libXrender
    pkgs.xorg.libXtst
    pkgs.xorg.libXrandr
    pkgs.xorg.libXScrnSaver
    pkgs.xorg.libxshmfence
    pkgs.fontconfig
    pkgs.glib
    pkgs.gtk3
    pkgs.nss
    pkgs.gconf
    pkgs.libnotify
  ];
}