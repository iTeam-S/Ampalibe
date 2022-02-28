@ echo off

IF /I "%1" == "create" (
    md %2
    python -c "import ampalibe;print(ampalibe.source.env_cmd)" > %2\.env.bat
    python -c "import ampalibe;print(ampalibe.source.conf)" > %2\conf.py
    python -c "import ampalibe;print(ampalibe.source.core)" > %2\core.py
    md %2\assets\public
    md %2\assets\private
)
IF /I "%1" == "init" (
    python -c "import ampalibe;print(ampalibe.source.env_cmd)" > .env.bat
    python -c "import ampalibe;print(ampalibe.source.conf)" > conf.py
    python -c "import ampalibe;print(ampalibe.source.core)" > core.py
    md assets\public
    md assets\private
)
IF /I "%1" == "run" (
    call .env.bat
    python -c "import core;core.ampalibe.init.run(core.Configuration())"
)