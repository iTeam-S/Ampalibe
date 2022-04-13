@ echo off

IF /I "%1" == "env" (
    python -c "import ampalibe.source;print(ampalibe.source.env_cmd)" > .env.bat
)

IF /I "%1" == "create" (
    md %2
    python -c "print('.env\n.env.bat\n__pycache__/\nngrok\nngrok.exe')" >> %2\.gitignore
    python -c "import ampalibe.source;print(ampalibe.source.env_cmd)" > %2\.env.bat
    python -c "import ampalibe.source;print(ampalibe.source.conf)" > %2\conf.py
    python -c "import ampalibe.source;print(ampalibe.source.core)" > %2\core.py
    md %2\assets\public
    md %2\assets\private
)
IF /I "%1" == "init" (
    python -c "print('.env\n.env.bat\n__pycache__/\nngrok\nngrok.exe')" >> .gitignore
    python -c "import ampalibe.source;print(ampalibe.source.env_cmd)" > .env.bat
    python -c "import ampalibe.source;print(ampalibe.source.conf)" > conf.py
    python -c "import ampalibe.source;print(ampalibe.source.core)" > core.py
    md assets\public
    md assets\private
)
IF /I "%1" == "run" (
    call .env.bat
    IF /I "%2" == "--dev" (
        watchmedo auto-restart --patterns="*.py;.env.bat" --recursive -- python -c "import core;core.ampalibe.init.run(core.Configuration())"
        exit
    )
    python -c "import core;core.ampalibe.init.run(core.Configuration())"
)
IF /I "%1" == "version" (
    python -c "import ampalibe;print(ampalibe.__version__)"
)