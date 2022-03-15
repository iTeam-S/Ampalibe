@ECHO OFF
for /F %%a in ('echo prompt $E ^| cmd') do @set "ESC=%%a"

python1 -c "" > NUL 2>NUL
IF %ERRORLEVEL% EQU 0 (
    @SET "python=python"
) ELSE (
    ECHO "Wait, what? no python in path !! Let's test python3"

    python3 -c "" > NUL 2>NUL
    IF %ERRORLEVEL% EQU 0 (
        @SET "python=python3"
    ) ELSE (
        ECHO "Oh, Give up !! No python/python3 in path :("
        EXIT 1
    )
)

IF /I "%1" == "create" (
    IF EXIST "%2\" (
        ECHO "~ ERROR :( ~ A folder %2 already exists"
    ) ELSE (
        MD "%2"
            ECHO "~ :::  | Creating %2..."
        %python% -c "import ampalibe.source;print(ampalibe.source.env_cmd)" > %2\.env.bat
            ECHO "~ :::  | Env file created"
        %python% -c "import ampalibe.source;print(ampalibe.source.conf)" > %2\conf.py
            ECHO "~ :::  | Config file created"
        %python% -c "import ampalibe.source;print(ampalibe.source.core)" > %2\core.py
            ECHO "~ :::  | Core file created"

        MD %2\assets\public
        MD %2\assets\private
            ECHO "~ ::: | Project Ampalibe created. Youpii 😎"
            ECHO "~ TIPS | Fill in .env file."
            ECHO "~ TIPS | cd  && ampalibe run for lauching project."
    )
)

IF /I "%1" == "init" (
            ECHO "~ :::  | Initialize projet..."
        %python% -c "import ampalibe.source;print(ampalibe.source.env_cmd)" > .\.env.bat
            ECHO "~ :::  | Env file created"
        %python% -c "import ampalibe.source;print(ampalibe.source.conf)" > .\conf.py
            ECHO "~ :::  | Config file created"
        %python% -c "import ampalibe.source;print(ampalibe.source.core)" > .\core.py
            ECHO "~ :::  | Core file created"

        MD ".\assets\public"
        MD ".\assets\private"
            ECHO "~ ::: | Project Ampalibe created. Youpii 😎"
            ECHO "~ TIPS | Fill in .env file."
            ECHO "~ TIPS | cd  && ampalibe run for lauching project."
    )
)

IF /I "%1" == "run" (
       call .env.bat

       IF EXIST "core.py" (
            %python% -c "import core;core.ampalibe.init.run(core.Configuration())";
            ECHO "~ ::: | Env Loaded"
            ECHO "~ ::: | Ampalibe running..."
       ) ELSE (
           ECHO "~ ERROR | core.py not found"
       )
    )
)   
