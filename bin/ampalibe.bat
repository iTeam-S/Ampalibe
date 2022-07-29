@ echo off

IF /I "%1" == "env" (
    python -c "import ampalibe.source;print(ampalibe.source.env_cmd)" > .env.bat
)

IF /I "%1" == "lang" (
    python -c "import ampalibe.source;print(ampalibe.source.langs)" > langs.json
)

IF /I "%1" == "create" (
    md %2
    python -c "print('.env\n.env.bat\n__pycache__/\nngrok\nngrok.exe')" >> %2\.gitignore
    python -m ampalibe create %2
    md %2\assets\public
    md %2\assets\private
)
IF /I "%1" == "init" (
    python -c "print('.env\n.env.bat\n__pycache__/\nngrok\nngrok.exe')" >> .gitignore
    python -m ampalibe init
    md assets\public
    md assets\private
)
IF /I "%1" == "run" (

    IF NOT exist "core.py" (
        echo ERROR !! core.py not found  1>&2
        echo Please, go to your dir project.
        exit
    )

    IF NOT exist "conf.py" (
        echo ERROR !! conf.py not found  1>&2
        exit
    )

    call .env.bat
    IF /I "%2" == "--dev" (
        watchmedo auto-restart --patterns="*.py;.env.bat" --recursive -- python -c "import core;core.ampalibe.init.run()"
        exit
    )
    python -c "import core;core.ampalibe.init.run()"
)

IF /I "%1" == "version" (
    python -m ampalibe version
)