{ pkgs }: {
  deps = [
    pkgs.npm
  ];

  nativeBuildInputs = [
    pkgs.nodejs
  ];

  meta = with pkgs.lib; {
    description = "Supabase";
    license = licenses.mit;
  };

  # Install the supabase-js package using npm
  preBuild = ''
    npm install supabase/supabase-js
  '';
}